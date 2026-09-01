# SessionStart hook: load brain/session context, resiliently.
# Fires on startup|resume|clear|compact so context survives /clear and compaction.
# On SSH success -> cache + emit. On failure/empty -> emit last cached context.
# Always exit 0 so a flaky agent box never blocks a session.
#
# 2026-07-27 repair. Two silent failure paths were found in the session logs:
#   1. ssh could hang past the harness hook timeout, killing the whole pwsh
#      process — so the cached-snapshot fallback below never ran in the exact
#      case it was written for (8 hook_cancelled events, clustered 07-21+).
#      Fixed by capping ssh in a job well under the harness timeout.
#   2. the fallback emitted a human-readable prefix line before the JSON, which
#      broke the harness JSON parse. Hook reported exitCode 0 and delivered
#      nothing. Fixed by folding the staleness note INTO additionalContext.

#
# 2026-09-01. Demoted from "the session's work list" to background context.
# load-native-tasks.ps1 now runs first and carries the actual task queue
# (campaign_task); this block is personal/strategic background only. The
# framing line below is prepended INSIDE additionalContext on both the fresh
# and the cached path, for the same reason the staleness note is.

$ErrorActionPreference = 'SilentlyContinue'
$cache = Join-Path $env:USERPROFILE '.claude\brain-context.cache.json'

# Prepended to every emission so this block is never mistaken for the task queue.
$ContextMarker = "> **BACKGROUND CONTEXT — not the task queue.** This is Connor's personal brain " +
                 "(identity, brands, social, wiki pointers, standing rules). Case Engine work items " +
                 "come from the native task block above (``public.campaign_task``); never answer " +
                 "``what am I working on`` / ``what's overdue`` / a task sweep from what follows.`n`n"

# Hard cap the remote call. Harness timeout is 60s (settings.json); stay well under
# it so the fallback path below always gets a chance to run.
$SshCapSeconds = 20

$out = ''
try {
  $job = Start-Job -ScriptBlock {
    & ssh -o BatchMode=yes -o ConnectTimeout=6 -o StrictHostKeyChecking=accept-new `
      connor@agent '/home/connor/brain/bin/brain_session_context.py --json' 2>$null
  }
  if (Wait-Job $job -Timeout $SshCapSeconds) {
    $out = (Receive-Job $job) -join "`n"
  }
  Remove-Job $job -Force
} catch { $out = '' }

if ($out -and $out.Trim().Length -gt 2) {
  # Cache the fresh context RAW (unmarked), then emit it with the framing note.
  try { Set-Content -Path $cache -Value $out -Encoding utf8 -NoNewline } catch {}
  $emitted = $false
  try {
    $obj = $out | ConvertFrom-Json
    if ($obj.hookSpecificOutput -and $obj.hookSpecificOutput.additionalContext) {
      $obj.hookSpecificOutput.additionalContext = $ContextMarker + $obj.hookSpecificOutput.additionalContext
      Write-Output ($obj | ConvertTo-Json -Depth 20 -Compress)
      $emitted = $true
    }
  } catch { $emitted = $false }
  # Unparseable shape — emit verbatim rather than nothing.
  if (-not $emitted) { Write-Output $out }
} elseif (Test-Path $cache) {
  # SSH failed/empty: fall back to last known-good context so the session isn't blind.
  # Must stay valid JSON — the staleness marker goes INSIDE additionalContext.
  $cached = Get-Content -Path $cache -Raw
  $stamp = (Get-Item $cache).LastWriteTime.ToString('yyyy-MM-dd HH:mm')
  $marker = "> **STALE CONTEXT WARNING.** Live brain fetch failed; this is a cached " +
            "snapshot from $stamp. Treat every fact below as a lead to verify, not " +
            "as current state. Check the live host before asserting anything from it.`n`n"
  $emitted = $false
  try {
    $obj = $cached | ConvertFrom-Json
    if ($obj.hookSpecificOutput -and $obj.hookSpecificOutput.additionalContext) {
      $obj.hookSpecificOutput.additionalContext = $marker + $ContextMarker + $obj.hookSpecificOutput.additionalContext
      Write-Output ($obj | ConvertTo-Json -Depth 20 -Compress)
      $emitted = $true
    }
  } catch { $emitted = $false }
  if (-not $emitted) {
    # Cache unparseable — emit the raw cached JSON rather than nothing.
    Write-Output $cached
  }
}
exit 0
