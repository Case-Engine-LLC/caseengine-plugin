---
name: statute-lookup
description: Look up state statutes and legal citations for personal injury law. Auto-activates when researching laws, statutes, legal requirements, or asking about state regulations.
---

# Statute Lookup Skill

Use this skill to look up state statutes, legal citations, and regulations for personal injury law across multiple states. The skill uses a hybrid approach: checking a local database first, then web search for updates or missing information.

## Available States

| State | Code | Practice Areas Covered |
|-------|------|------------------------|
| California | CA | General, Auto, Bicycle, Pedestrian, Truck, Motorcycle, Dog Bite, Rideshare, Wrongful Death, Insurance |
| Colorado | CO | General, Auto, Bicycle, Pedestrian, Truck, Dog Bite, Insurance |
| Florida | FL | General, Auto, Bicycle, Pedestrian, Truck, Motorcycle, Dog Bite, Wrongful Death, Insurance |
| Georgia | GA | General, Auto, Bicycle, Pedestrian, Truck, Motorcycle, Dog Bite, Wrongful Death, Insurance |
| Maryland | MD | General, Auto, Bicycle, Pedestrian, Truck, Insurance |
| Texas | TX | General, Auto, Bicycle, Pedestrian, Truck, Motorcycle, Dog Bite, Wrongful Death, Insurance |
| Virginia | VA | General, Auto, Bicycle, Pedestrian, Truck, Motorcycle, Dog Bite, Wrongful Death, Insurance |

## Lookup Workflow

See [lookup-workflow.md](lookup-workflow.md) for detailed process.

**Quick Process:**
1. Check statute database JSON for the state/practice area
2. If found, return citation with summary and applicability
3. If not found or stale (>1 year), search web for current statute
4. Always include source URL for verification

## Citation Formats by State

| State | Format Example |
|-------|----------------|
| California | Cal. Veh. Code § 23152 |
| Colorado | C.R.S. § 13-21-111 |
| Florida | Fla. Stat. § 768.81 |
| Georgia | O.C.G.A. § 51-1-6 |
| Maryland | Md. Code, Cts. & Jud. Proc. § 3-2A-06 |
| Texas | Tex. Civ. Prac. & Rem. Code § 33.001 |
| Virginia | Va. Code § 8.01-243 |

## Common Statute Categories

### General (All States)
- Statute of limitations
- Comparative/contributory negligence
- Damage caps
- Punitive damages
- Government immunity

### Practice Area Specific
- **Auto**: DUI, reckless driving, minimum insurance
- **Truck**: Commercial vehicle regulations, hours of service
- **Bicycle**: Safe passing distance, cyclist rights
- **Pedestrian**: Crosswalk laws, jaywalking
- **Dog Bite**: Strict liability vs. one-bite rule
- **Wrongful Death**: Beneficiary hierarchy, damage types

## Usage Examples

**Direct lookup:**
> "What is California's statute of limitations for car accidents?"

**Comparative research:**
> "Compare dog bite liability laws between California (strict liability) and Virginia (one-bite rule)"

**Recent changes:**
> "What changed in Colorado's non-economic damage caps in 2025?"

## Database Location

Statute JSON files are stored in `~/.claude/statute-data/` or `statute-data/` in the skills package. Each file follows this structure:

```json
{
  "state": "California",
  "stateCode": "CA",
  "lastResearched": "2025-01-15",
  "statutes": {
    "general": [...],
    "auto": [...],
    "bicycle": [...]
  }
}
```
