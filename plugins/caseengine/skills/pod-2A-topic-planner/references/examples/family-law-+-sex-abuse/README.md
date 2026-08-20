# Family Law + Sex Abuse - Topic Plan Example

Canonical pod-2A-topic-planner exemplar for firms practicing Family Law primary with a high-margin CPS / Child Abuse Civil + Criminal Sex Abuse defense moat. Sanitized from a real production run.

## What this is

A production-mode topic plan output. Includes everything the skill produces end to end:

- **Header block** - Prepared for, practice focus, locations, counties, episode count, prepared by, date.
- **Show Identity** - 4-field approval block (Podcast Name, Tagline, Description, Target Audience) - hard requirement for production mode before any tables get generated.
- **Methodology** - client-facing 2-paragraph explainer of how topics were selected.
- **The 12-Episode Plan** - main 12 episodes, 6-column table (#, Topic, Theme, Keywords, Search Volume, Rationale), sequenced into 3 production waves.
- **Additional Topics** - 5-row bonus / swap-in table with explicit `Swaps for` column pointing back to a main episode.
- **INTERNAL block** - everything below the `# INTERNAL` header. Topics by Practice Area with `[MAIN-#] / [BONUS] / [RESERVE] / [CUT]` tags, plan-construction notes, Fathom Service Weighting block, Similarity Filter cuts, underweighted entities pulled back in, recording-wave production order, coverage check, Next Steps.
- **Provenance** - every Fathom recording, CE artifact (Brand Guide, Tone Profile, Sales Report, Contract, Client Download), research output (entity / keyword / virality), master catalog, public web source, and open data gap that fed the plan. Future versions of this plan **append** here, never replace.

## What it demonstrates

Structural decisions every production-mode topic plan must repeat:

1. **Show Identity is the gate.** All four fields (Podcast Name, Tagline, Description, Target Audience) sit above the tables and must be approved before generation continues. Description weaves the firm's wow-factor anchor (here: the attorney's own published case) into the value prop.
2. **12-Episode main table = client-facing, curated, ranked.** Episode 1 is always the biographic anchor. Episodes 2-N are sequenced for compound trust + search visibility + qualified case flow, not raw MSV.
3. **Additional Topics is a real artifact, not a leftover bin.** Each bonus has a `Swaps for` cell tying it to a specific main episode. Bonus topics are recordable; they are not the cuts.
4. **INTERNAL block separates curation from research.** Topics by Theme catalogs the full reserve (every recordable topic across every sub-domain, tagged `[RESERVE]`) plus every `[CUT]` with the reason. Next Maryland-family-law client filters from this catalog instead of running fresh research.
5. **Fathom Service Weighting is the dominant modifier.** Search demand alone does not determine the main 12. The attorney's stated revenue mix from onboarding (here: family law pays the lights, CPS is high-margin niche, criminal is priority #2) bends the ranking. This is captured in the `## Fathom Service Weighting` sub-block inside INTERNAL.
6. **Provenance is the audit trail.** Every Fathom recording, every Drive artifact, every research JSON gets cited with date, ID, and why-it-matters. v2+ runs append; they do not overwrite.

## Why these 12 episodes

The Fathom Service Weighting outcome:

- **Episodes 2-8 = Family Law backbone (7 of 12).** "Family law pays the lights" per the strategy meeting. Equitable distribution, child support, divorce timeline, protective orders, modification, military divorce - the bread and butter that drives volume case flow.
- **Episodes 9-10 = CPS / Child Abuse Civil (2 of 12).** Attorney's stated #1 priority. "The big thing I want to focus on is the crimes and the child abuse." Differentiator versus peers who refer this out.
- **Episodes 11-12 = Sex Abuse - Criminal Defense + Civil Plaintiff (2 of 12).** Attorney's stated #2 priority. Episode 11 is the criminal-defense side (state sex offense statutes + sex offender registry tiers + first-30-days playbook). Episode 12 is the civil-plaintiff side under the state's Child Victims Act statute-of-limitations reform, opening up institutional liability claims.
- **Episode 1 = biographic anchor.** Required for every new show. Frames the show through the attorney's published-case wow-factor + 30-year career arc.

Selection ran two passes: topic-only against the universal family-law entity map (52 entities, 12 clusters), then topic+geo re-rank against state statutes + county demographics + nearby military base + state-published case law. Merged into a single client-facing table.

## Placeholders + what to swap

| Placeholder | What it represents | Example replacement |
|---|---|---|
| `{FIRM_NAME}` | Full firm name as it appears on letterhead | `Smith & Jones Law Group, PC` |
| `{ATTORNEY_NAME}` | Lead attorney full name | `Jane Smith` |
| `{FIRST_NAME}` | Lead attorney first name (in narrative + rationale prose) | `Jane` |
| `{LAST_NAME}` | Lead attorney last name (standalone use) | `Smith` |
| `{ATTORNEY_LAST_NAME_UPPER}` | Last name uppercased (used in INTERNAL section headers) | `SMITH` |
| `{PRIMARY_CITY}` | Main office city + state | `Houston, TX` |
| `{SECONDARY_CITY}` | Secondary office city + state (omit if single-office) | `The Woodlands, TX` |
| `{PRIMARY_COUNTY}` | Main county served | `Harris` |
| `{SECONDARY_COUNTY}` | Secondary county served | `Montgomery` |
| `{DATE}` | Plan run date - format: `Month DD, YYYY` for prose, `YYYY-MM-DD` for JSON | `May 15, 2026` / `2026-05-15` |
| `{DOC_ID}` | Google Drive file ID (Doc, Sheet, or PDF) | `1abc...xyz` |
| `{FOLDER_ID}` | Google Drive folder ID | `1abc...xyz` |
| `{LOGO_ID}` | Google Drive image ID for the firm's logo (used in cover-page rendering) | `1abc...xyz` |
| `{FATHOM_RECORDING_ID}` | Fathom recording numeric ID | `145795311` |
| `{FIRM_WEBSITE_URL}` | Firm website root URL | `https://www.smithjoneslaw.com/` |
| `{ATTORNEY_BIO_URL}` | Attorney bio page URL | `https://www.smithjoneslaw.com/attorneys/jane-smith/` |
| `{FIRM_LINKEDIN_URL}` | Firm LinkedIn company page URL | `https://www.linkedin.com/company/smith-jones-law-group` |
| `{ATTORNEY_NTL_URL}` | National Trial Lawyers profile URL (omit if not a member) | `https://thenationaltriallawyers.org/members/jane-smith/` |
| `{firm-website-domain}` | Bare firm domain | `smithjoneslaw.com` |
| `{firm-slug}` | Firm slug (lowercase, hyphenated, used in keywords + local paths) | `smith-jones` |
| `{firm-name-lower}` | Full firm name lowercased (brand-keyword context) | `smith and jones law group` |
| `{attorney-name-lower}` | Attorney full name lowercased (brand-keyword context) | `jane smith` |
| `{primary-city-lower}` | Primary city lowercased (brand-keyword context) | `houston` |
| `{ATTORNEY_PUBLISHED_CASE - Mohink's was Braun v. Headley; swap for the published case the attorney is known for}` | Inline annotation in Episode 2 rationale. Replace with the actual published case the attorney is mandatory authority on. If the attorney has no published case, replace the entire Episode 2 topic - the relocation-case wow-factor angle does not exist without it. | `Smith v. Texas` or restructure Ep 2 |

### Maryland-specific content kept in (these are exemplar specifics, swap by jurisdiction)

- **Statute references** (`FL §8-205`, `Criminal Law §§ 3-303-3-308`, `§ 3-602`, `CJP § 5-117`) - swap for the equivalent statutes in the firm's jurisdiction. The structure of "criminal sex offense statutes + sex offender registry tiers + civil SOL reform statute" is the pattern; the cite numbers change.
- **Maryland Child Victims Act** (Episode 12) - this is one example of a state statute-of-limitations reform that opened civil-plaintiff sex abuse claims against institutions. Many states now have equivalent legislation (CA AB 218, NY CVA, NJ Statute of Limitations Reform Act, etc.). Swap for the jurisdiction's equivalent.
- **Case law entities kept generic to the practice area, not the attorney**: `Taylor v. Taylor` (foundational MD joint-custody), `Koshko v. Haining` (MD grandparent visitation cut), `Use and Possession` (MD 3-year marital-home statute), `Voluntary Impoverishment` (MD child-support imputation doctrine), `Best Interests Attorney` (MD Rule 9-205.1), `USERRA 10/10 rule` (federal military divisor of disposable retired pay - same in every state). Replace these with the jurisdiction's foundational practice-area entities; the slot structure stays the same.

## How to use this as a starting point

1. Read the `## Show Identity` block. Replace the placeholders with the new firm's identity. Confirm the 4 fields with the client before generating tables.
2. Walk down the main 12 table. For each episode, keep the **structure** (the slot - "Custody / Relocation", "Property Division", "Procedure: Timeline", "Domestic Violence: Protective Orders", "Post-Decree Modification", "Special Audience: Military", "CPS Investigation", "False-Allegation Custody Defense", "Sex Abuse Criminal Defense", "Sex Abuse Civil Plaintiff under CVA") and swap the **specifics** (statutes, case names, keywords, MSV, geo references).
3. Run the Fathom Service Weighting block against the new firm's actual onboarding recording. The 8/2/2 split (Family Law / CPS / Criminal Sex Abuse) is firm-specific - if the new firm weights criminal heavier or CPS lighter, the main-12 mix changes.
4. Pull the bonus table from the topic catalog. The five swap-in candidates here are themselves swap-in candidates for the next firm; the catalog has 38 ranked topics across 10 sub-domains.
5. Generate the INTERNAL `## Topics by Practice Area` block fresh from the entity map. The reserve list here is Maryland family law specific; replace with the new jurisdiction's reserve list.
6. Populate Provenance with the new firm's actual artifacts. **Do not** carry forward the example artifact IDs.

## File inventory

- `good--family-law-sex-abuse-topic-plan.md` - sanitized markdown source. Canonical. All future renders (DOCX, PDF, Google Doc) generate from this file via pandoc + the topic-plan branding spec.
- `good--family-law-sex-abuse-topic-plan.json` - sanitized JSON. Machine-readable mirror of the markdown - used by downstream skills (pod-2B-n-gram-table, pod-3A-ros-template) to pull episode metadata without re-parsing prose.
- `good--family-law-sex-abuse-topic-plan.docx` - **intentionally not included.** The original Mohink DOCX is a binary rendered artifact containing the attorney's PII inside the OOXML stream and cannot be safely sanitized without unpacking + XML-editing + re-zipping the package. Future runs regenerate a fresh DOCX from the sanitized markdown via the standard render pipeline; no per-firm hand-edits to the DOCX are ever required. If a DOCX example is needed for visual reference, render the sanitized `.md` once with pandoc + the topic-plan branding spec and save the output here as `good--family-law-sex-abuse-topic-plan.docx`.

## Edge-case flags

- **Single-office firms** - omit `{SECONDARY_CITY}` and `{SECONDARY_COUNTY}`; the description prose collapses to a single-county audience line. Episode 8 (Special Audience: Military) only applies if a military base / first-responder concentration sits within the firm's geo. If not, swap Ep 8 for one of the bonus topics.
- **No published case** - Episode 2's relocation-case wow-factor is built around the attorney's own published case. If the attorney has no published case, replace Episode 2 with the highest-MSV family law topic from the catalog and move the relocation discussion into the broader Family Law: Custody slot.
- **Practice mix without sex abuse** - Episodes 11 + 12 are the differentiator for firms that take CPS / Child Abuse Civil seriously. Generic family law firms that do not handle sex abuse criminal defense or CVA civil plaintiff work should swap both for alimony + prenups (currently in the bonus table) or higher-volume family law procedural topics.
- **State without CVA-style SOL reform** - Episode 12 disappears entirely; replace with another high-margin civil plaintiff angle (institutional liability, mass tort, or a different practice-area extension).
