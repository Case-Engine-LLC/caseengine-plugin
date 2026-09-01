# Session re-grounding (read this first)

Claude Code's SessionStart hooks are unreliable after `/clear` and compaction (known bugs: anthropics/claude-code #34072 closed not-planned, #15174, #26794). This CLAUDE.md, however, reliably reloads on `/clear` — so this instruction is the dependable path.

Two separate blocks load at session start, and they are **not interchangeable**:

## 1. Tasks — the native queue (priority)

`# Connor's open Case Engine tasks (NATIVE — the work queue)` is the authoritative task list: `public.campaign_task` on Supabase, open statuses, where Connor is deliverer or verifier. Every task question — "what am I working on", "what's overdue", a sweep, triage, "pull my tasks" — is answered from here.

**If that block is missing above**, re-pull it before answering anything task-shaped:

- Run `pwsh -NoProfile -File C:\Users\cgall\.claude\hooks\load-native-tasks.ps1` (it prints the block as hook JSON), or
- Read `C:\Users\cgall\.claude\native-tasks.cache.json` for the last good pull — treat it as stale and re-verify before acting.

Never substitute the brain for this. The brain has no campaign tasks in it.

## 2. Brain — background context only

`# Connor's Brain Context` (identity, brands, social, wiki pointers, standing rules) is background, not work. It tells you who Connor is and what his standing rules are; it never tells you what is on his plate.

**If that block is missing above**, read `C:\Users\cgall\.claude\brain-context.cache.json` (refreshed every fresh launch; holds the last good brain context) before doing substantive work.

Loading order is enforced in `~/.claude/settings.json`: `load-native-tasks.ps1` runs before `load-brain-context.ps1`, so the queue leads and the brain follows.
