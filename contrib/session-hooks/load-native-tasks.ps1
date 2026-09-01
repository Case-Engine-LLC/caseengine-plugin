# SessionStart hook: load Connor's NATIVE Case Engine task queue.
# Fires on startup|resume|clear|compact, registered BEFORE load-brain-context.ps1
# so the work queue leads the session and the brain reads as background context.
#
# Source of truth: public.campaign_task on Supabase, pulled through
# caseengine-cli/sbsql.py (Management API — no MCP auth, works headless).
# This mirrors src/lib/work/adapters/delivery.ts in case-engine-webapp:
# same OPEN statuses, same archived_at filter, same deliverer/verifier match.
# Identity bridge is crm_team.team_members.id ('connor-gallic'), per
# src/lib/work/identity.ts.
#
# Deliberately NOT the other six work adapters (internal/clickup/marker/
# request/approval/change_request): 'native tasks' means campaign_task, and a
# personal pull returns delivery rows only anyway.
#
# On success -> cache + emit. On failure/empty -> emit last cached block with a
# staleness marker folded INSIDE additionalContext (a prefix line outside the
# JSON breaks the harness parse — same bug the brain hook was repaired for).
# Always exit 0 so a slow Supabase never blocks a session.

$ErrorActionPreference = 'SilentlyContinue'
$cache  = Join-Path $env:USERPROFILE '.claude\native-tasks.cache.json'
$python = 'C:\Users\cgall\AppData\Local\Programs\Python\Python311\python.exe'
$sbsql  = 'E:\Dev2\caseengine-cli\sbsql.py'
$person = 'connor-gallic'

# Harness timeout is 40s (settings.json); stay well under so the fallback runs.
$CapSeconds = 25
$MaxItems   = 30

$sql = @"
select t.id, t.name, t.status, t.due_date, t.priority, c.name as client,
       (t.due_date is not null and t.due_date < current_date) as overdue
from campaign_task t
left join campaign_plan p on p.id = t.plan_id
left join clients c on c.id = p.client_id
where t.archived_at is null
  and t.status in ('todo','in_progress','needs_approval','blocked')
  and (t.deliverer_person_id = '$person' or t.verifier_person_id = '$person')
order by (t.due_date is null), t.due_date asc
limit 400;
"@

$rows = $null
try {
  $job = Start-Job -ArgumentList $python, $sbsql, $sql -ScriptBlock {
    param($py, $script, $q)
    & $py $script --sql $q 2>$null
  }
  if (Wait-Job $job -Timeout $CapSeconds) {
    $raw = (Receive-Job $job) -join "`n"
    if ($raw -and $raw.TrimStart().StartsWith('[')) { $rows = $raw | ConvertFrom-Json }
  }
  Remove-Job $job -Force
} catch { $rows = $null }

function Format-Row($r) {
  $due = if ($r.due_date) { $r.due_date } else { 'no due date' }
  $flag = if ($r.overdue) { ' OVERDUE' } else { '' }
  $pri = if ($r.priority) { " [$($r.priority)]" } else { '' }
  $client = if ($r.client) { $r.client } else { 'unassigned client' }
  "- **$($r.name)** — $client · $($r.status) · due $due$flag$pri · ``$($r.id)``"
}

if ($null -ne $rows) {
  $all = @($rows)
  $lines = New-Object System.Collections.Generic.List[string]
  $lines.Add('# Connor''s open Case Engine tasks (NATIVE — the work queue)')
  $lines.Add('')
  $lines.Add('This is the authoritative task list for this session: `public.campaign_task`, open statuses, where Connor is deliverer or verifier. Task questions ("what am I working on", "what''s overdue", sweeps, triage) are answered from HERE, not from the brain context that follows.')
  $lines.Add('')

  if ($all.Count -eq 0) {
    $lines.Add('**No open native tasks.** That is a real answer, not a failed pull.')
  } else {
    $byStatus = $all | Group-Object status | Sort-Object Count -Descending |
      ForEach-Object { "$($_.Name) $($_.Count)" }
    $overdue = @($all | Where-Object { $_.overdue })
    $lines.Add("**$($all.Count) open** — $($byStatus -join ' · ') · **$($overdue.Count) overdue**")
    $lines.Add('')

    $shown = @($all | Select-Object -First $MaxItems)
    $lines.Add("## Next $($shown.Count) by due date")
    foreach ($r in $shown) { $lines.Add((Format-Row $r)) }

    if ($all.Count -gt $shown.Count) {
      $lines.Add('')
      $lines.Add("_$($all.Count - $shown.Count) further open tasks not listed. Re-run the pull for the full queue:_")
      $lines.Add('`python E:\Dev2\caseengine-cli\sbsql.py --sql "..."` (see this hook at ~/.claude/hooks/load-native-tasks.ps1), or `work_list_items` once caseengine-tasks MCP is authorized.')
    }
  }

  $payload = @{
    hookSpecificOutput = @{
      hookEventName    = 'SessionStart'
      additionalContext = ($lines -join "`n")
    }
  }
  $json = $payload | ConvertTo-Json -Depth 20 -Compress
  try { Set-Content -Path $cache -Value $json -Encoding utf8 -NoNewline } catch {}
  Write-Output $json
} elseif (Test-Path $cache) {
  $cached = Get-Content -Path $cache -Raw
  $stamp = (Get-Item $cache).LastWriteTime.ToString('yyyy-MM-dd HH:mm')
  $marker = "> **STALE TASK QUEUE.** Live Supabase pull failed; this is a cached snapshot from $stamp. " +
            "Statuses and due dates may have moved. Re-pull before acting on any item below.`n`n"
  $emitted = $false
  try {
    $obj = $cached | ConvertFrom-Json
    if ($obj.hookSpecificOutput -and $obj.hookSpecificOutput.additionalContext) {
      $obj.hookSpecificOutput.additionalContext = $marker + $obj.hookSpecificOutput.additionalContext
      Write-Output ($obj | ConvertTo-Json -Depth 20 -Compress)
      $emitted = $true
    }
  } catch { $emitted = $false }
  if (-not $emitted) { Write-Output $cached }
}
exit 0
