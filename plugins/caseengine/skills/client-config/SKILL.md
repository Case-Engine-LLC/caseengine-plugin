---
name: client-config
description: Guide creation of client configuration JSON files for legal content generators. Auto-activates when working with client/*.json files or creating law firm configurations.
---

# Client Configuration Skill

Use this skill when creating or editing client configuration files for legal content generation systems.

## Required Fields

Every client config must include:

| Field | Type | Description |
|-------|------|-------------|
| `client_id` | string | Unique identifier (lowercase, underscores) |
| `law_firm` | string | Official firm name |
| `city` | string | Primary city or "City1 and City2" format |
| `state` | string | Full state name (e.g., "California") |
| `county` | string | County name (e.g., "Orange County") |
| `output_dir` | string | Output path (e.g., "output/client_name") |
| `attorneys` | array | At least one attorney object |

## Attorney Object

Each attorney requires:

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Full name with credentials suffix if applicable |
| `credentials` | string | Bar membership, education, achievements, awards |
| `specialties` | array | List of practice areas |

## Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `contact.email` | string | Firm contact email |
| `contact.phone` | string | Firm phone number |
| `offices` | array | Office locations with address details |

## Template

See [template.json](template.json) for a complete annotated template.

## Validation Rules

1. `client_id` must be lowercase with underscores only
2. `state` must be full name, not abbreviation
3. `county` should include "County" suffix
4. `attorneys` array must have at least one entry
5. `credentials` should include specific achievements (verdicts, settlements, awards)
6. `specialties` should list actual practice areas offered

## Example Usage

```bash
# Generate content for a client
python generate.py --client clients/new_client.json --brief briefs/to_make/City_Car_MV.csv
```
