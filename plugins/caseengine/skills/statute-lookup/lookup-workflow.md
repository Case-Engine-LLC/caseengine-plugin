# Statute Lookup Workflow

This document describes the detailed process for looking up statutes using the hybrid database + web search approach.

## Step 1: Identify the Request

Parse the user's request to determine:
- **State**: Which state's laws are being requested
- **Practice Area**: General, auto, bicycle, pedestrian, truck, motorcycle, dog_bite, rideshare, wrongfulDeath, insurance
- **Specific Topic**: Statute of limitations, comparative negligence, damage caps, etc.

## Step 2: Check Local Database

1. Locate the statute JSON file: `statute-data/{state}-statutes.json`
2. Navigate to the appropriate practice area category
3. Search for statutes matching the topic

**Database Entry Fields:**
- `citation`: Official legal citation (e.g., "C.R.S. § 13-21-111")
- `officialTitle`: Full statute name
- `summary`: 2-3 sentence overview
- `applicability`: Detailed explanation of how it applies to legal cases
- `relatedStatutes`: Cross-references to related laws
- `sourceUrl`: Link to official statute text
- `lastRevised`: Year of most recent amendment

## Step 3: Evaluate Freshness

Check the `lastRevised` and `lastResearched` dates:
- If `lastRevised` is within current year: Data is likely current
- If `lastResearched` is > 1 year old: Consider web verification
- For dollar amounts (caps, minimums): Always verify - these change frequently

**Known Recent Changes (2024-2025):**
- California insurance minimums: 15/30/5 → 30/60/15 (Jan 1, 2025)
- Colorado non-economic caps: $729,790 → $1,500,000 (Jan 1, 2025)
- Colorado wrongful death caps: → $2,125,000 (Jan 1, 2025)
- Florida comparative negligence: Modified to 50% bar (March 2023)

## Step 4: Web Search (If Needed)

When to search:
- Statute not in database
- Data appears stale (>1 year)
- User specifically asks for "current" or "updated" law
- Dollar amounts that change with inflation

Search strategy:
1. Search: `[State] [statute topic] statute [current year]`
2. Prefer official sources: state legislature websites, Justia, FindLaw
3. Verify against multiple sources for critical information

## Step 5: Format Response

**Standard Response Format:**

```markdown
## [Statute Topic]

**Citation:** [Full citation]
**Official Title:** [Statute name]

**Summary:**
[2-3 sentence overview]

**Applicability:**
[How this applies to the case type]

**Related Statutes:**
- [Related statute 1]
- [Related statute 2]

**Source:** [URL]
**Last Revised:** [Year]
```

## Step 6: Flag Uncertainties

If there's any uncertainty:
- Note when database was last updated
- Recommend verification for critical deadlines (SOL, notice requirements)
- Flag if dollar amounts may have changed due to inflation adjustments

## Database File Locations

**Personal Installation:**
```
~/.claude/statute-data/
├── california-statutes.json
├── colorado-statutes.json
├── florida-statutes.json
├── georgia-statutes.json
├── maryland-statutes.json
├── texas-statutes.json
└── virginia-statutes.json
```

**Project Installation:**
```
.claude/statute-data/
└── [same files]
```

## Adding New States

1. Copy `state-template.json` to `{state}-statutes.json`
2. Fill in state name and code
3. Research and add statutes by practice area
4. Update `lastResearched` date

See `state-template.json` for the required structure.
