---
name: statute-reviewer
description: Review legal content for accurate statute citations, dollar amounts, and legal references. Auto-activates when reviewing legal documents or verifying citation accuracy.
---

# Statute Reviewer Skill

Use this skill to review legal marketing content and verify that statute citations, dollar amounts, time periods, and legal references are accurate and current.

## Quick Validation Checklist

### Citation Format

| Check | Pass | Fail |
|-------|------|------|
| Uses proper state citation format | Cal. Veh. Code § 23152 | California Vehicle Code 23152 |
| Section symbol (§) used correctly | § 768.81 | Section 768.81 |
| State abbreviation matches style guide | Fla. Stat. | FL Stat |

### Dollar Amounts - CRITICAL

| State | Item | Current (2025) | Common Error |
|-------|------|----------------|--------------|
| California | Minimum insurance | 30/60/15 | 15/30/5 (pre-2025) |
| Colorado | Non-economic cap | $1,500,000 | $729,790 (pre-2025) |
| Colorado | Wrongful death cap | $2,125,000 | Not specified |
| Florida | No cap on PI | Unlimited | Any specific number |

### Time Periods - SOL

| State | Motor Vehicle | General PI | Wrongful Death | Gov't Notice |
|-------|---------------|------------|----------------|--------------|
| California | 2 years | 2 years | 2 years | 6 months |
| Colorado | 3 years | 2 years | 2 years | 182 days |
| Florida | 4 years | 4 years | 2 years | 3 years (state) |
| Georgia | 2 years | 2 years | 2 years | 1 year |
| Texas | 2 years | 2 years | 2 years | 6 months |
| Virginia | 2 years | 2 years | 2 years | 1 year |

## Supporting Documents

- [review-checklist.md](review-checklist.md) - Detailed verification steps
- [common-errors.md](common-errors.md) - Known pitfalls and recent changes

## Review Workflow

1. **Scan for citations** - Find all statute references in the document
2. **Verify format** - Check each citation uses proper state format
3. **Cross-reference database** - Confirm statute exists and is cited correctly
4. **Check dollar amounts** - Verify caps, minimums, thresholds are current
5. **Check time periods** - Verify SOL and notice periods are accurate
6. **Flag uncertainties** - Note anything that needs verification

## Red Flags to Catch

### Outdated Information
- California insurance minimums of 15/30/5 (changed Jan 1, 2025)
- Colorado non-economic caps below $1.5M (changed Jan 1, 2025)
- Florida pure comparative negligence references (changed March 2023)

### Common Mistakes
- Mixing up motor vehicle SOL with general PI SOL (different in some states)
- Using state-specific caps for states without caps
- Citing federal regulations as state law
- Wrong comparative negligence threshold (49% vs 50% vs 51%)

### Comparative Negligence Variations

| State | Type | Bar Threshold |
|-------|------|---------------|
| California | Pure | None - can recover at any % fault |
| Colorado | Modified | 50% bar - no recovery if 50%+ at fault |
| Florida | Modified | 50% bar (changed 2023 from pure) |
| Georgia | Modified | 50% bar |
| Texas | Modified | 51% bar |
| Virginia | Contributory | Any fault bars recovery |
| Maryland | Contributory | Any fault bars recovery |

## Usage

**Review a document:**
> "Review this content for statute accuracy: [paste content]"

**Check specific citation:**
> "Is 'Fla. Stat. § 768.81' the correct citation for Florida's comparative negligence law?"

**Verify dollar amount:**
> "Is $729,790 still the correct non-economic damage cap in Colorado?"
