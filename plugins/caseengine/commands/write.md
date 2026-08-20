---
description: Pick up a writing assignment, get the context to do it well, draft it, and submit it.
argument-hint: "<client or task> [topic]"
---

The writer's loop, start to finish, without leaving Claude or hunting through
five tabs for context.

## 1. What am I picking up

If `$ARGUMENTS` names a task or client, start there. Otherwise pull the caller's
queue with `work_list_items` and find the writing work — `Write & edit blogs
posts`, `Blog topic revisions`, `Create Content Briefs`, `Compare blog topics
against strategy doc`.

Writers usually hold the same task across several clients at once. Show which
clients are waiting before diving into one.

## 2. Get the context before writing a word

This is the part that costs a writer the most time, and all of it is one call
each.

**`client_get_profile`** — practice areas, target locations, brand voice, the
services they actually offer. Writing a personal-injury piece for a firm that
does not take those cases is the expensive kind of mistake.

**`client_list_blogs`** — every post the client already has, 5,104 rows across
the roster. Two things to do with it:

- **Check for duplicates.** Search the titles and slugs for the topic you are
  about to write. If something close already exists, say so and ask whether this
  is a rewrite, a refresh, or a genuine gap.
- **Match the register.** Read two or three published pieces for the same client
  before drafting. Their voice is in there.

**The assignment itself** — topic, target URL and title usually come from the SEO
workbook's `new_content` tab rather than the task. If the task does not carry
them, say so and ask rather than inventing a slug.

## 3. Draft

Write it properly. House rules that come up repeatedly in review comments:

- Match the heading hierarchy to the brief — an H2 followed by an H4 is a
  correction waiting to happen, and it recurs constantly in Marker tickets.
- Every CTA needs a real destination. Unlinked buttons are the single most
  common client complaint in the corpus.
- Statutes and deadlines get cited precisely, with the code reference.
- No placeholder text. Not even temporarily.

## 4. Submit

Where the draft goes depends on which path this client is on.

**Generation pipeline** (there is a `content_pieces` row): use
`content_generation_get_piece` to read state, then `content_transition_piece` to
move it — `needs_review` → `approved` → `ready_to_ship`.

Note that **`published` is deliberately not reachable** through this tool. There
is no verified WordPress push behind it, and the codebase refuses to let a status
say "published" when nothing was pushed. Do not work around that.

**Everything else**: the draft is a Google Doc and the workbook row is the
record. Put the draft where the client's work already lives, update the workbook
row, and say plainly in your handoff which of those you did.

Then close your writing task — and be honest that writing it is not publishing
it. The scheduling task belongs to a developer, and the piece is not live until
someone confirms it is.

## Known gap, worth saying out loud

There is no tool that takes a human-written draft and attaches it to a piece.
`content_start_generation` creates AI-generated content from a brief; it is not
a submit path for something you wrote. Until that exists, the draft lives in a
Doc and the plugin can help you write it and move its state, but it cannot carry
the words themselves. Do not pretend otherwise in a handoff.
