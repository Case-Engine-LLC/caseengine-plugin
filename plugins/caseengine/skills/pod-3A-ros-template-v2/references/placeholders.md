# Placeholders

The approved token taxonomy for the v2 ROS Template. Read by `steps/04-segment-1.md`, `steps/05-segment-2.md`, and `steps/03-cover-page.md`; enforced by the placeholder gate in `steps/08-qa.md`.

Everything specific to a firm is a token so one template serves every firm recording that episode at that scope. `pod-3B-client-ros-v2` resolves them at populate time, which is why this table and its populate mirror (`pod-3B-client-ros-v2/references/placeholders.md`) must agree exactly - a token the populate skill does not know ships into a recording as literal markup. THIS file is canonical; the mirror follows it.

## The taxonomy

| Placeholder | Resolves to |
|---|---|
| `{{TOPIC}}` | The episode's subject, as a phrase. Cover line. **New 2026-08-17.** |
| `{{CITY}}` | The city. Anchors every S2 block; a multi-location episode gives each additional location its own full question set and names that city in PLAIN TEXT, so there is no second city token and `{{CITY_2}}` must never be invented (decided 2026-08-18). in S1 it appears only in the credential line, naming where the firm practices. Restored 2026-08-18 in place of `{{LOCATION}}`, which was ambiguous once `{{STATE}}` took the S1 geo. |
| `{{STATE}}` | **SEGMENT 1 geo.** State full name (`CA` -> `California`). Multi-state firms say so at generation time and it resolves to the spoken phrase (`Maryland and DC`). |
| `{{PODCAST_NAME}}` | Client's podcast name |
| `{{ATTORNEY_NAME}}` | Full attorney name. Line 1 of the intro only - the branded open. |
| `{{ATTORNEY}}` | How the host addresses them on air - first name. Everywhere the attorney is spoken to. |
| `{{INTERVIEWER}}` | CE host on the recording |
| `{{FIRM_NAME}}` | Full firm name |
| `{{PHONE_NUMBER}}` | Firm phone `(XXX) XXX-XXXX` |
| `{{WEBSITE}}` | **BUSINESS** website, including `https://`. Used in the conversion CTA - a case inquiry must land on the FIRM. |
| `{{PODCAST_DOMAIN}}` | Where episodes live. Used in the subscribe line. **Never** interchangeable with `{{WEBSITE}}` (Gabe directive 2026-08-21). |
| `{{YEARS_PRACTICING}}` | Integer years in practice, in this market |

Twelve tokens (`{{PODCAST_DOMAIN}}` added 2026-08-21; this caption said eleven until 2026-08-25). Every one appears bold wherever it renders, and stays bold after populate.

## The two geo levels

**S1 speaks at the state level. S2 carries the geo explicitly, question by question.** Every S2 question names either `{{CITY}}` or `{{STATE}}` - whichever the question is actually about. A hiring question is a city question; a filing-deadline question is a state question. That is where the geo signal lives, so it is stated rather than implied.

**S1 speaks at the state level. S2 speaks at the city level.** The substance of the long-form answer is state-governed - deadlines, comparative fault, damage caps, bar admission are all state rules - so one S1 recording serves every city a firm covers. City ranking signals live in S2, which is where the per-city blocks are.

- S1's setup line uses `{{STATE}}`. The listener could be anywhere in the state, so that is the honest scope for "what you need to know."
- S1's credential line may name the city, because that sentence is about where the FIRM practices, not where the listener is: "you've been serving **{{CITY}}** and across **{{STATE}}** for **{{YEARS_PRACTICING}}** years." This is Cyle's original construction from the 08-14 call, and it is the reason the cities we already know still reach S1.
- One city, maximum, in S1. A firm with six offices names its base and lets `{{STATE}}` carry the rest; listing them is a keyword list read aloud.
- S2 uses `{{CITY}}` per block, paired with its plain-text region.
- Almost every firm is one state, so `{{STATE}}` is just the state name. If a firm covers more than one, say so at generation time and `{{STATE}}` resolves to the spoken phrase instead (`Maryland and DC`). No extra field, no intake change - it is a question asked on the run that needs it.

## Rules

- **Nothing outside this table.** A grep for `{{...}}` returns only these twelve. An invented token never gets resolved.
- **The region is plain text, never a token.** It is fixed by the template's location scope, so it renders literally ("the Inland Empire", "Chatham County and coastal Georgia"). `{{REGION}}` does not exist. Guard this one: it was invented twice and removed twice.
- **No hard-coded firm, attorney, city, or state names in the body.** The region is the sole intentional exception.

## Open

- `{{RECORDING_DATE}}` is RETIRED as of 2026-08-18. It rendered on the cover and nowhere else. A ROS Template is generic and tokenized so one template serves every firm that records that episode at that scope, and different firms record on different dates, so a recording date was never a template-level fact. It also dated the cover of an asset that is meant to stay evergreen. The recording date still belongs on the Client ROS, where `pod-3B-client-ros-v2` collects it per firm (TBD non-blocking; renders only as a small cover line). Do not reintroduce it here.
- `{{EPISODE_NUMBER}}` is retired from the rendered document as of 2026-08-17 - it was only ever on the old cover. It stays valid for filenames (`E{N}: {Episode Title} // ROS Template v2`). Decide whether it re-enters the body anywhere.
- RESOLVED 2026-08-18: `pod-3B-client-ros-v2` v1.0.0 populates all twelve tokens (the legacy `pod-3B-client-ros` stays on its own 12-token legacy taxonomy and never touches v2 templates). The former top ship blocker is closed.

## Naming note

`{{ATTORNEY_NAME}}` and `{{ATTORNEY}}` are not interchangeable and the names alone do not say which is which. `{{ATTORNEY_NAME}}` is the full name and appears once, in the branded open. `{{ATTORNEY}}` is direct address - first name - and is what the host actually says to them. The populate skill must map both.
