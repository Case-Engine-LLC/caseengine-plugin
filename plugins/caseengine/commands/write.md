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

- **Check for duplicates against what is actually on their site.** The inventory
  is the first pass — search titles and slugs for the topic. But the inventory
  can lag, so for anything that looks close, confirm against the live sitemap:

  ```bash
  python3 "${CLAUDE_PLUGIN_ROOT}/hooks/checks.py" --url <client-homepage> --check sitemap
  ```

  That pulls every URL the site publishes. A topic already live is a rewrite or a
  refresh, not a new post — say which, and get it confirmed before writing.
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

## 4. Check it before you send it

Section 6 of the Content Writing Training Guide is a pre-submission checklist,
and it names five common rejection reasons. Most of them are mechanical, and a
writer re-reading their own draft is the worst instrument for catching them.

Save the draft and run:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/hooks/content_check.py" \
  --file draft.md --city "<target city>" --firm "<firm name>" \
  --against <folder of this client's other drafts>
```

It runs three rulesets that were never checked automatically:

- **The training guide's checklist** — H1 pattern, heading hierarchy with no
  skipped levels, numerals over spelled-out numbers, settlement ranges starting
  low and ending in "+", win rates inside the 70–92% band, city density,
  italicised CTAs, placeholders, consistent firm naming.
- **Maja's legal-content-review skill** — the Algorithmic Authorship rules and
  the banned-phrase blocklist. It gives you the replacement, not just the
  objection: *"maximum compensation" → full compensation*, *"legal experts" →
  legal professionals*. Plus em-dashes, bold used mid-paragraph, subordinate
  clauses opening a sentence instead of closing it, connectives rationed to
  three per document, and the rule that the first sentence after a heading must
  reuse words from that heading.
- **Uniqueness** — word-shingle overlap against the client's other drafts, the
  same method the pipeline's own checker uses, with the same 60% floor. Reused
  sentence skeletons across a client's city and practice-area pages are the
  single biggest controllable cause of a low originality score, and this catches
  them before anything reaches a paid scanner.

Fix what it flags, then run it again. A clean run is what "ready to send" means.

It does not judge whether the writing is good, whether the argument holds, or
whether the client will like it. That is the editor's call and always was.

## 5. Submit

Where the draft goes depends on which path this client is on.

**Generation pipeline** (there is a `content_pieces` row): use
`content_generation_get_piece` to read state, then `content_transition_piece` to
move it — `needs_review` → `approved` → `ready_to_ship`.

Note that **`published` is deliberately not reachable** through this tool. There
is no verified WordPress push behind it, and the codebase refuses to let a status
say "published" when nothing was pushed. Do not work around that.

**Everything else**: the draft is a Google Doc and the workbook row is the
record. The generation pipeline already writes .docx into the client's Drive
folder, so the Doc is usually where the piece lives before anyone reads it.

Send it properly. A handoff someone can act on without asking you a question
contains: what it is and who it is for, the link, the target URL and title, what
the pre-submission check returned, and the one thing you want from the reader —
review, approval, or scheduling. Put the draft where the client's work already
lives, update the workbook row, and say which of those you did.

Then close your writing task — and be honest that writing it is not publishing
it. The scheduling task belongs to a developer, and the piece is not live until
someone confirms it is.

## 6. Known gap, worth saying out loud

There is no tool that takes a human-written draft and attaches it to a piece.
`content_start_generation` creates AI-generated content from a brief; it is not
a submit path for something you wrote. Until that exists, the draft lives in a
Doc and the plugin can help you write it and move its state, but it cannot carry
the words themselves. Do not pretend otherwise in a handoff.
