---
label: GOOD
skill: entity-research
scope: Topic
run_date: 2026-04-20
topic: Car Accidents (Topic-level, location-agnostic)
location: (topic-level - location-agnostic by design)
source: Production demo - /Users/gjordan/Desktop/research-workflow-demo--sutliff-stout/02--entity-research.md (Sutliff & Stout, 2026-04-20)
why_this_label: |
  Hits every Koray rule at the right weight for a Topic-level foundation map and matches the
  canonical Entity Map shape produced by `scripts/build-entity-map-docx.py`.
  Target counts all land on spec: 45 entities (target 40-50), 11 clusters (target 8-15), 6 bridges
  (target 4-6). Tier distribution is healthy: 12 / 20 / 13 across Tier 1 / 2 / 3.
  Vector strength formula is shown in-line with the 0.45 / 0.35 / 0.20 prominence-relatedness-
  popularity weighting; every row carries its individual P/R/Pop sub-scores so downstream
  consumers can re-weight if needed.
  Entity types cover breadth (12+ types: legal concepts, statutes, gov agencies, insurance
  concepts, medical, evidence, damages, case types, liable parties, causes, practices,
  credentials) rather than depth in one bucket - exactly the "breadth not depth" Best
  Practices rule.
  Localization is handled CORRECTLY at Topic scope: generic entity names (Police Department,
  Insurance Company, Civil Court) are kept AS-IS because Topic-level is location-agnostic by
  design. Localization Summary is advisory; locally-strong entities ENTER at Location /
  Extension scope via the localization-coverage evaluation step, not via a hard validation
  gate at this level.
  Bridge entities are genuine 3+ cluster connectors (Comparative Fault / SoL / Policy Limits /
  Police Report / Medical Records / Breach of Duty) not re-labeled Tier 1s.
  Data source flagged `llm_only` in frontmatter AND Executive Summary; downstream
  treats prominence as reliable, popularity as directional.
known_flaws: |
  - Liable Parties cluster is thin at Topic scope - specific parties (driver, employer,
    manufacturer, government) live inside Vicarious Liability + Product Liability rather
    than as standalone entities. Expected to expand at Location scope.
  - Professional Credentials cluster only has Board Certification (PI) at Topic scope.
    Expected to expand at Location scope (AAJ membership, big-verdict recognitions,
    trial-experience tallies, Texas Trial Lawyers Association).
  - Score sources are LLM-only estimates, not content-gap mined. Prominence attribute is
    reliable; popularity attribute is directional. Flagged for downstream readers.
drive_doc: null
---

# Entity Research - Car Accidents (Topic Only)

## Executive Summary

This map captures the entity universe for Car Accidents at Topic Only scope. Foundation map - jurisdiction-agnostic; every Location and Extension build inherits from this.

### Counts

- 45 entities (target: 40-50)
- 11 clusters (target: 8-15)
- 6 bridge entities (target: 4-6)

### Tier distribution

- Tier 1 (core, vector strength >= 0.80): 12 entities
- Tier 2 (major, 0.60-0.79): 20 entities
- Tier 3 (supporting, 0.40-0.59): 13 entities

### Localization

- Coverage: 0% jurisdictional-named (expected at Topic Only)
- Supplement: not triggered, not applicable at this scope

Vector strength formula:
```
vector_strength = (prominence * 0.45) + (relatedness * 0.35) + (popularity * 0.20)
```

Data source: `llm_only` - no content-gap scoring data available; vector strengths estimated from domain knowledge per Koray's three attributes. Prominence is reliable, popularity is directional. Flagged for downstream readers.

### Learnings & Insights

- **Domain leaning:** top 3 entity types are Legal Concept (10), Insurance (7), Damages (6) - 51% of all entities. The domain is most heavily Legal Concept.
- **Largest cluster:** Legal Framework (10 entities) - the gravitational center of this practice area.
- **Central bridge:** Comparative Fault (51% Rule) spans 3 clusters (Legal Framework + Damages + Insurance). State-specific threshold determines whether you recover anything at 51%+ fault. Critical pivot in every negotiation.
- **Balanced distribution** (T1 27% / T2 44% / T3 29%) - healthy spread across core, major, and supporting tiers. No single tier dominates; downstream content can pull from across the hierarchy.
- **Score consensus:** Tier 1 mean vector strength 0.86, Tier 2 0.69, Tier 3 0.51. Tier 1 consensus is solid - core entities are well-clear of the 0.80 threshold.
- **Bridge composition:** mixed tiers (5 T1 of 6 total) - cross-cluster connections come predominantly from the core tier, with Breach of Duty (Tier 2) earning bridge status by structural role rather than vector strength.

### What does this mean?

- The practice area is balanced across multiple subject types - no single category dominates. Top three are legal concept, insurance, damages. Content can range broadly without feeling off-topic.
- The biggest theme in this domain is **Legal Framework** - more entities than any other cluster (10). Audiences expect a real conversation about this; if your content skips it, you're missing the gravitational center.
- **Comparative Fault (51% Rule)** is the connective tissue across the whole practice area. It ties together Legal Framework, Damages and Insurance. If your content explains it well, you're educating AND linking related topics in one move.
- **The landscape is balanced.** Core, major, and supporting ideas all carry weight. Content can range across the full hierarchy without feeling top-heavy or scattered.
- **The connectors are the most prominent ideas.** Five of the six bridges are Tier 1 entities, so coverage of the bridge entities does double duty - explains the central concepts AND ties related topics together. Highest-leverage content lives here.

---

## Vector Space Visualization

Entities plotted radially - cluster determines angle, vector strength determines distance from center. Bridges highlighted with gold border.

Vector-space chart embedded in the paired DOCX (see `good--entity-map-car-accidents-topic-only.docx`). Generated by `scripts/entity-vector-space.py`.

---

## Tier 1 - Core Entities

Central to the practice area; appears in nearly every episode at every scope. Bold rows are bridges (connect 3+ clusters).

| Entity | Type | Vec Str | Prom | Rel | Pop | Cluster | Bridge |
|---|---|---|---|---|---|---|---|
| **Negligence** | Legal Concept | 0.930 | 0.98 | 0.95 | 0.80 | Legal Framework | - |
| **Liability** | Legal Concept | 0.920 | 0.98 | 0.95 | 0.78 | Legal Framework | - |
| **Comparative Fault (51% Rule)** | Legal Concept | 0.880 | 0.95 | 0.92 | 0.68 | Legal Framework | * |
| **Statute of Limitations** | Legal Concept | 0.870 | 0.92 | 0.88 | 0.78 | Legal Framework | * |
| **Insurance Policy Limits** | Insurance | 0.860 | 0.95 | 0.90 | 0.65 | Insurance Concepts | * |
| **Police Report** | Evidence | 0.860 | 0.92 | 0.88 | 0.75 | Evidence Types | * |
| **Medical Records** | Evidence | 0.850 | 0.90 | 0.90 | 0.70 | Evidence Types | * |
| **Damages (Economic + Non-Economic)** | Damages | 0.850 | 0.92 | 0.88 | 0.72 | Damages Categories | - |
| **Duty of Care** | Legal Concept | 0.830 | 0.90 | 0.92 | 0.62 | Legal Framework | - |
| **Contingency Fee** | Practice | 0.820 | 0.90 | 0.85 | 0.70 | Attorney Process | - |
| **Insurance Claims Process** | Insurance | 0.820 | 0.88 | 0.88 | 0.70 | Insurance Concepts | - |
| **Causation (Proximate Cause)** | Legal Concept | 0.810 | 0.90 | 0.90 | 0.55 | Legal Framework | - |

---

## Tier 2 - Major Entities

Important; appears in most episodes. Topic has room for depth here. Bold rows are bridges.

| Entity | Type | Vec Str | Prom | Rel | Pop | Cluster | Bridge |
|---|---|---|---|---|---|---|---|
| Underinsured Motorist (UIM) | Insurance | 0.780 | 0.85 | 0.85 | 0.55 | Insurance Concepts | - |
| Uninsured Motorist (UM) | Insurance | 0.780 | 0.85 | 0.85 | 0.55 | Insurance Concepts | - |
| Personal Injury Protection (PIP) | Insurance | 0.770 | 0.82 | 0.85 | 0.58 | Insurance Concepts | - |
| Subrogation | Insurance | 0.750 | 0.80 | 0.85 | 0.55 | Insurance Concepts | - |
| **Breach of Duty** | Legal Concept | 0.740 | 0.85 | 0.82 | 0.48 | Legal Framework | * |
| Whiplash / Soft Tissue Injury | Medical | 0.740 | 0.78 | 0.85 | 0.58 | Medical & Injury | - |
| Traumatic Brain Injury (TBI) | Medical | 0.720 | 0.75 | 0.82 | 0.62 | Medical & Injury | - |
| Pain and Suffering | Damages | 0.720 | 0.80 | 0.80 | 0.50 | Damages Categories | - |
| Settlement Negotiation | Practice | 0.710 | 0.78 | 0.82 | 0.50 | Attorney Process | - |
| Demand Letter | Practice | 0.700 | 0.80 | 0.78 | 0.50 | Attorney Process | - |
| Distracted Driving | Cause | 0.700 | 0.75 | 0.82 | 0.55 | Accident Causes | - |
| DUI / Impaired Driving | Cause | 0.690 | 0.72 | 0.80 | 0.58 | Accident Causes | - |
| Hit and Run | Case Type | 0.690 | 0.75 | 0.80 | 0.50 | Case / Claim Types | - |
| Dash Cam / Black Box (EDR) | Evidence | 0.680 | 0.72 | 0.80 | 0.52 | Evidence Types | - |
| Wrongful Death | Case Type | 0.680 | 0.72 | 0.78 | 0.55 | Case / Claim Types | - |
| Witness Statement | Evidence | 0.670 | 0.75 | 0.78 | 0.48 | Evidence Types | - |
| Economic Damages | Damages | 0.660 | 0.72 | 0.78 | 0.48 | Damages Categories | - |
| Non-Economic Damages | Damages | 0.660 | 0.72 | 0.78 | 0.48 | Damages Categories | - |
| State Department of Insurance | Gov Agency | 0.640 | 0.72 | 0.72 | 0.48 | Government & Regulatory | - |
| State Department of Motor Vehicles | Gov Agency | 0.620 | 0.70 | 0.72 | 0.42 | Government & Regulatory | - |

---

## Tier 3 - Supporting Entities

Niche / specialized; appears where relevant. Depth signal for topical authority.

| Entity | Type | Vec Str | Prom | Rel | Pop | Cluster | Bridge |
|---|---|---|---|---|---|---|---|
| Punitive Damages | Damages | 0.580 | 0.65 | 0.68 | 0.38 | Damages Categories | - |
| Vicarious Liability | Legal Concept | 0.570 | 0.65 | 0.68 | 0.35 | Legal Framework | - |
| Product Liability (Defective Vehicle) | Legal Concept | 0.560 | 0.62 | 0.68 | 0.38 | Legal Framework | - |
| NHTSA (Natl Hwy Traffic Safety Admin) | Gov Agency | 0.550 | 0.62 | 0.62 | 0.42 | Government & Regulatory | - |
| Maximum Medical Improvement (MMI) | Medical | 0.540 | 0.60 | 0.65 | 0.38 | Medical & Injury | - |
| Ambulance Chasing (Bar Rule) | Practice | 0.520 | 0.60 | 0.58 | 0.38 | Attorney Process | - |
| Board Certification (Personal Injury) | Credential | 0.500 | 0.58 | 0.55 | 0.38 | Professional Credentials | - |
| Mediation / Alternative Dispute Resolution | Practice | 0.500 | 0.55 | 0.60 | 0.35 | Attorney Process | - |
| Jury Trial | Practice | 0.480 | 0.55 | 0.58 | 0.32 | Attorney Process | - |
| Burden of Proof (Preponderance) | Legal Concept | 0.470 | 0.55 | 0.55 | 0.32 | Legal Framework | - |
| Loss of Consortium | Damages | 0.440 | 0.52 | 0.52 | 0.28 | Damages Categories | - |
| Minimum Auto Insurance Limits | Insurance | 0.430 | 0.48 | 0.52 | 0.32 | Insurance Concepts | - |
| Accident Reconstruction Expert | Practice | 0.420 | 0.50 | 0.48 | 0.28 | Evidence Types | - |

---

## Cluster Architecture

11 contextual layers slice this practice area. Each cluster represents one way the domain is sliced; together they form the topical map.

### Legal Framework

Core legal concepts that define every car-accident claim. Every cluster touches this.

- **Negligence** (Tier 1)
- **Liability** (Tier 1)
- **Duty of Care** (Tier 1)
- **Causation (Proximate Cause)** (Tier 1)
- **Comparative Fault (51% Rule)** (Tier 1, bridge)
- **Statute of Limitations** (Tier 1, bridge)
- **Breach of Duty** (Tier 2, bridge)
- **Vicarious Liability** (Tier 3)
- **Product Liability (Defective Vehicle)** (Tier 3)
- **Burden of Proof (Preponderance)** (Tier 3)

### Insurance Concepts

How carriers structure coverage and how that shapes recovery.

- **Insurance Policy Limits** (Tier 1, bridge)
- **Insurance Claims Process** (Tier 1)
- **Underinsured Motorist (UIM)** (Tier 2)
- **Uninsured Motorist (UM)** (Tier 2)
- **Personal Injury Protection (PIP)** (Tier 2)
- **Subrogation** (Tier 2)
- **Minimum Auto Insurance Limits** (Tier 3)

### Government & Regulatory

Entities that enforce, record, or regulate. At Location scope these get localized (e.g., TDI, TxDOT, TxDMV).

- **State Department of Insurance** (Tier 2)
- **State Department of Motor Vehicles** (Tier 2)
- **NHTSA (Natl Hwy Traffic Safety Admin)** (Tier 3)

### Evidence Types

Documents and artifacts that prove fault and damages.

- **Police Report** (Tier 1, bridge)
- **Medical Records** (Tier 1, bridge)
- **Dash Cam / Black Box (EDR)** (Tier 2)
- **Witness Statement** (Tier 2)
- **Accident Reconstruction Expert** (Tier 3)

### Medical & Injury

Injury categories and treatment milestones the claim tracks.

- **Whiplash / Soft Tissue Injury** (Tier 2)
- **Traumatic Brain Injury (TBI)** (Tier 2)
- **Maximum Medical Improvement (MMI)** (Tier 3)

### Damages Categories

What claimants can recover.

- **Damages (Economic + Non-Economic)** (Tier 1)
- **Pain and Suffering** (Tier 2)
- **Economic Damages** (Tier 2)
- **Non-Economic Damages** (Tier 2)
- **Punitive Damages** (Tier 3)
- **Loss of Consortium** (Tier 3)

### Case / Claim Types

Classifications that determine strategy.

- **Hit and Run** (Tier 2)
- **Wrongful Death** (Tier 2)

### Liable Parties

Who can be held responsible beyond the other driver. (Implicit at Topic scope - other driver, employer, manufacturer, government - captured as concepts within Vicarious Liability + Product Liability. Expands at Location scope.)

### Accident Causes

Behavioral and mechanical causes that drive liability analysis.

- **Distracted Driving** (Tier 2)
- **DUI / Impaired Driving** (Tier 2)

### Attorney Process

How attorneys navigate the engagement.

- **Contingency Fee** (Tier 1)
- **Settlement Negotiation** (Tier 2)
- **Demand Letter** (Tier 2)
- **Ambulance Chasing (Bar Rule)** (Tier 3)
- **Mediation / Alternative Dispute Resolution** (Tier 3)
- **Jury Trial** (Tier 3)

### Professional Credentials

Trust signals that differentiate firms. Thin at Topic scope; expands significantly when localized (AAJ membership, big-verdict recognitions, trial-experience tallies, Texas Trial Lawyers Association).

- **Board Certification (Personal Injury)** (Tier 3)

---

## Bridge Entities

Bridges connect multiple clusters and carry the highest authority value because they are where the topical graph reconverges.

| Bridge | Tier | Connects | Connections |
|---|---|---|---|
| **Comparative Fault (51% Rule)** | T1 | Legal Framework + Damages Categories + Insurance Concepts | 3 |
| **Statute of Limitations** | T1 | Legal Framework + Case / Claim Types + Insurance Concepts | 3 |
| **Insurance Policy Limits** | T1 | Insurance Concepts + Damages Categories + Liable Parties | 3 |
| **Police Report** | T1 | Evidence Types + Government & Regulatory + Accident Causes | 3 |
| **Medical Records** | T1 | Evidence Types + Medical & Injury + Damages Categories | 3 |
| **Breach of Duty** | T2 | Legal Framework + Liable Parties + Evidence Types | 3 |

Bridge selection logic:

1. **Comparative Fault (51% Rule)** - State-specific threshold determines whether you recover anything at 51%+ fault. Critical pivot in every negotiation.
2. **Statute of Limitations** - Time-bar. Missed deadline = claim dead regardless of merits.
3. **Insurance Policy Limits** - Ceiling on recovery from a single policy. Drives UM/UIM strategy and multi-defendant analysis.
4. **Police Report** - Single document anchoring fault determination, agency recording, and cause narrative.
5. **Medical Records** - Bridge between injury reality and dollar value.
6. **Breach of Duty** - The "did they violate?" question connecting legal primitive, party identification, and proof. Tier 2 entity earning bridge status by structural role, not vector strength.

---

## Localization Summary

This map is at Topic Only scope - jurisdiction-agnostic by design. No location-specific entities are forced. When this map is inherited by a Location or Extension build, locally-strong entities (named police departments, local hospitals, state-specific statutes/forms) enter via the localization-coverage evaluation step.

Coverage at this scope: 0% jurisdictional-named (expected). Supplement: not triggered.

For downstream Location runs, generic tokens such as `Police Department`, `State Department of Motor Vehicles`, `State Department of Insurance`, `Civil Court`, `Hospital (unqualified)`, and `Highway Patrol (unqualified)` will be candidates for substitution with their jurisdictional named instances (e.g., `Houston Police Department (HPD)`, `Texas Department of Motor Vehicles (TxDMV)`, `Texas Department of Insurance (TDI)`). At Location scope the localization-coverage evaluation determines which generic entities get substituted, which locally-strong entities get added, and which Topic-level entities get dropped because they do not apply in the jurisdiction (e.g., PIP shifts from default to optional add-on in Texas because Texas is not a no-fault state).

---

## Inheritance Notes

This Topic Only map is the foundation that every Location and Extension cascade reads first. When building below this scope:

- Carry forward Tier 1 + Tier 2 entities that are jurisdiction-neutral (Negligence, Liability, Duty of Care, Comparative Fault, Contingency Fee, etc.) without re-scoring them
- Add entities unique to the jurisdiction at Location scope (e.g., Texas Civil Practice and Remedies Code § 33.001 codifying the 51% rule, CR-3 Crash Report Form, Memorial Hermann Trauma Center for Houston, Harris County Civil Courts, Texas Tort Claims Act, Texas Minimum Auto Insurance Limits 30/60/25)
- Substitute generic tokens for jurisdictional named instances (`Police Department` -> `Houston Police Department (HPD)`; `State Department of Insurance` -> `Texas Department of Insurance (TDI)`)
- Remove entities that do not apply in the jurisdiction (e.g., PIP mandatory status removed for Texas; No-Fault Claims procedures removed)
- At Extension scope (e.g., TX - Houston - Katy), inherit the Location map and substitute city-level instances where relevant; acronym convention is `Full Name (ACRONYM)`
- Per-scope entity form: Topic uses generic tokens with comma separator and 1-2 entities per row; Location uses full jurisdictional stack with semicolon separator and 3-5 entities per row

The single-question stress test for any entity in this map: if I swapped the scope from Topic to Location (TX - Houston), would this entity still appear as-is or would it need to be substituted, added, or removed? Negligence, Liability, Duty of Care, Comparative Fault (51% Rule), and Contingency Fee hold unchanged - they are legal primitives and genuinely location-agnostic, which is exactly what a Topic-scope map should carry. State Department of Insurance, State Department of Motor Vehicles, and Police Report all need substitution. PIP needs to shift from Tier 2 to "optional add-on" at Texas Location scope. That break pattern is the signature of a genuine Topic-level foundation map.
