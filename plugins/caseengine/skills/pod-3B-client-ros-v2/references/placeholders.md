# Placeholders - populate mirror

**CANONICAL SOURCE: `pod-3A-ros-template-v2/references/placeholders.md`.** That file wins on any disagreement; this mirror exists so the populate skill is freestanding. Last synced 2026-08-25 against taxonomy "twelve tokens" - `{{PODCAST_DOMAIN}}` was added to the canonical file on 2026-08-21 and never propagated here, so this mirror shipped eleven for four days.

## The twelve tokens and where their values come from

Populate source is **Supabase first** (`client_profiles` + `client_field_values`, see `SKILL.md -> Supabase firm lookup`), then `podcast-overview.md`, then user ask. The `Supabase key` column is the canonical key - use it verbatim.

| Placeholder | Supabase key | Populate source | Conversion |
|---|---|---|---|
| `{{TOPIC}}` | - | Template payload / Topic Plan | spoken phrase, as the template carries it |
| `{{CITY}}` | - (episode-level) | Episode geo target / user | the EPISODE GEO TARGET city, never the show anchor. `pod_location_1` is the SHOW anchor and is the default only when the episode declares no geo |
| `{{STATE}}` | `client_profiles.primary_state` | Supabase / user | code -> full name (`CA` -> `California`); multi-state -> spoken phrase (`Maryland and DC`) |
| `{{PODCAST_NAME}}` | `pod_name` | Supabase | as branded. **Not** `aeo_podcast_name` - that key never existed |
| `{{ATTORNEY_NAME}}` | `aeo_attorney_name` | Supabase / user | full name |
| `{{ATTORNEY}}` | first token of `cont_marketing_poc_name` | derived - confirm | FIRST name - direct address |
| `{{INTERVIEWER}}` | `pod_ce_host` | Supabase, overridable per episode | CE host on the recording. **Not** `aeo_ce_host` (never existed) and **not** `pod_cohost` (the firm's own co-host). Roster: `hr_team_members` job_title 'Podcast Interviewer'. If the episode is recorded IN-HOUSE by the firm, this token must not resolve |
| `{{FIRM_NAME}}` | `biz_legal_name` (fallback `client_profiles.name`) | Supabase | full firm name - legal name preferred, carries the `, P.A.` suffix |
| `{{PHONE_NUMBER}}` | `biz_official_phone` (fallback `client_profiles.primary_contact_phone`) | Supabase | `(XXX) XXX-XXXX` |
| `{{WEBSITE}}` | `client_profiles.website` | Supabase | **BUSINESS** site, including `https://`. The conversion CTA - a case inquiry must land on the FIRM |
| `{{PODCAST_DOMAIN}}` | `pod_domain` | Supabase | where episodes live - the SUBSCRIBE line. **Never** interchangeable with `{{WEBSITE}}` (Gabe directive 2026-08-21) |
| `{{YEARS_PRACTICING}}` | derived from `biz_open_date` | Inferred - confirm | integer, years in THIS market |

## Not body tokens in v2

- `{{RECORDING_DATE}}` - retired from the v2 body 2026-08-18. Collected per firm by this skill; renders only as the small cover line (omitted while `TBD`) and lives in the payload + metadata.
- `{{EPISODE_NUMBER}}` - filenames only.
- `{{ATTORNEY_FIRST_NAME}}`, `{{HOST_NAME}}`, `{{PRACTICE_AREA}}` - LEGACY tokens. Finding one in a template means it is NOT a v2 template: stop and route to `/pod-3B-client-ros`.

## Rules

- Resolution is `.replace()` on exact tokens, NEVER `str.format()` (format collapses the doubled braces).
- `{{ATTORNEY_NAME}}` (full, once, branded open) and `{{ATTORNEY}}` (first name, direct address) are not interchangeable - map both.
- Populated values stay **bold** wherever the template had the token bold - which is everywhere.
- The region is plain text fixed by the template; `{{REGION}}` does not exist and must not be invented.
