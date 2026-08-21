---
description: A client's podcast episodes and the run of show for each.
argument-hint: "<client name or slug> [status]"
---

Show where every episode is in production, and what the slate is waiting on.

## 1. Pull the episodes

`client_list_podcast_episodes` with the client from `$ARGUMENTS`. Pass `status`
to narrow to `published` or `drafting`.

Each episode comes back with a **run of show** — the production ladder in order,
which stages are done, and which one is next:

1. Audio/video published
2. Transcript received
3. Transcript cleaned
4. Transcript approved
5. Transcript published
6. Show notes created
7. Blog repurpose created
8. Social assets planned

## 2. Lead with what is stuck

The response includes `waiting_on`: how many episodes are sitting at each stage.
That is the answer to "where is the slate", and it should be the first thing you
report — not a list of every episode.

Then the episodes themselves, by number, each showing progress and next stage.

## 3. Keep produced and accepted separate

`fully_produced` means all eight stages are done. `client_verified` means the
client actually signed off. They are different numbers and the gap between them
matters — an episode can be complete and still not accepted.

Do not merge them into a single "done" count.

## 4. If asked whether an episode is live

Check it rather than trusting `status`. The episode URL, the audio URL, and
whether the show resolves in the directories it is supposed to be in. Record
what you found with `hooks/record.py`, or run `/caseengine:prove` if there is a
task to close.

## Worth knowing

Transcripts are the usual bottleneck, and the data shows it: across the whole
inventory, far more episodes have audio published than have a transcript
published. If someone asks why podcast delivery feels stalled, look there first.
