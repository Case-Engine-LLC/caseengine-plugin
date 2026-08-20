---
description: Everything on file for a client — websites, hosting, tracking, team, brand, socials.
argument-hint: "<client name or slug> [what you need]"
---

Pull a client's full record so you can actually do work on them, rather than
guessing or asking someone.

## 1. Get the profile

`client_get_profile` with `$ARGUMENTS` — it accepts a UUID or a slug, and
returns the client row plus branding, integrations, SEO config, services, team
assignments, websites, custom fields, links, GBP locations and social accounts.

If the name is ambiguous, list the candidates and ask. Do not pick one.

## 2. Lead with where the site actually lives

This is what people open this for. Use `client_list_websites` when the profile
dump is more than you need.

Report per website: domain, environment, whether it is marked primary, the
Cloudways server and app ids, and the WP admin URL.

**A client legitimately has several rows** — production, staging, a legacy
migration — and they are frequently mislabelled. The domain is usually
Cloudflare-proxied, so a DNS lookup will not tell you the true origin. If more
than one row could plausibly be live, say so rather than asserting one is.
Confirm before acting on it.

## 3. Then what was asked for

If `$ARGUMENTS` named something specific — tracking, GBP, who's on the account,
the brand palette — answer that directly from the profile and keep the rest
short.

With nothing specific asked, give a tight orientation: what the client is, which
sites exist, which integrations are wired, who is assigned, and anything that
looks missing or stale.

## Handling gaps

Say plainly when a field is empty. "No GA4 property recorded" is useful; quietly
omitting it is not, because the next person assumes it was checked.

Never paste credentials or tokens into the conversation. Reference where a
credential lives — a 1Password vault, an integration record — and stop there.
