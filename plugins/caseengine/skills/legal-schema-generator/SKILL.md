---
name: legal-schema-generator
description: Generate schema.org structured data (JSON-LD) for legal websites. Use when creating or updating schema markup for law firm websites including homepage organization schema, location+service pages (practice area pages), and attorney biography/profile pages. Triggers include "schema", "structured data", "JSON-LD", "rich snippets", "law firm schema", "attorney schema", "legal service schema", or any request to add/update schema markup on legal website pages.
---

# Legal Schema Generator

Generate comprehensive schema.org structured data for law firm websites. Supports three page types:

| Page Type | Schema File | Primary Types |
|-----------|-------------|---------------|
| Homepage | [homepage-schema.json](references/homepage-schema.json) | Organization, LegalService, WebSite, WebPage, FAQPage, HowTo |
| Location/Service | [local-service-schema.json](references/local-service-schema.json) | LegalService, Attorney, Service, WebPage, FAQPage, HowTo, LegalCase |
| Attorney Bio | [attorney-schema.json](references/attorney-schema.json) | Person, ProfilePage, LegalService, Organization, VideoObject |

## Workflow

1. Identify page type (homepage, location/service, attorney bio)
2. Read the appropriate reference file for the template
3. Collect required values from user or client configuration
4. Generate customized JSON-LD with proper @id references
5. Validate all @id cross-references match

## Key Implementation Rules

### @id Cross-References
All `@id` values must be unique and consistently referenced:
```json
"@id": "https://example.com/#org"         // Organization
"@id": "https://example.com/#website"     // WebSite
"@id": "https://example.com/#webpage"     // WebPage
"@id": "https://example.com/page#service" // Service on specific page
"@id": "https://example.com/page#faq"     // FAQ on specific page
```

When referencing an entity defined elsewhere, use:
```json
"provider": { "@id": "https://example.com/#org" }
```

### Graph Structure
Always use `@graph` array to contain multiple entities:
```json
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "WebSite", ... },
    { "@type": "WebPage", ... },
    { "@type": "LegalService", ... }
  ]
}
```

### Required Fields by Page Type

**Homepage:**
- Organization: name, legalName, url, logo, address, telephone, email, foundingDate, aggregateRating, sameAs, knowsAbout, areaServed
- WebSite: url, name, publisher reference
- FAQPage: minimum 2 questions with acceptedAnswer

**Location/Service Pages:**
- Service: name, serviceType, provider, areaServed, offers
- LegalService: all organization fields + location-specific address/geo
- Breadcrumb: Home → Practice Area → Location
- FAQPage: location-specific questions

**Attorney Bio:**
- Person: name, givenName, familyName, jobTitle, description, image, hasCredential, alumniOf, knowsAbout, sameAs
- ProfilePage: about and mainEntity reference Person
- Reviews: at least 2 client reviews with ratings

## Values Collection Checklist

### Organization/Firm Info
- [ ] Legal name and display name
- [ ] Primary URL
- [ ] Logo URL (with dimensions)
- [ ] Office address(es)
- [ ] Phone number (E.164 format: +1-xxx-xxx-xxxx)
- [ ] Email address
- [ ] Founding date
- [ ] Social media URLs (LinkedIn, Facebook, Twitter/X, Avvo, BBB, Google Maps CID)
- [ ] Practice areas / knowsAbout
- [ ] Awards and memberships
- [ ] Aggregate rating (value, count)
- [ ] Opening hours

### Location/Service Specific
- [ ] Service name and type
- [ ] City/locality served
- [ ] Geo coordinates (latitude, longitude)
- [ ] Service radius in meters
- [ ] Location-specific phone if different
- [ ] 2-4 FAQs about the service/location

### Attorney Specific
- [ ] Full name (given + family)
- [ ] Job title
- [ ] Bio description
- [ ] Headshot image URL
- [ ] Law school (alumniOf)
- [ ] Bar admission (credential name, identifier, URL)
- [ ] Practice areas
- [ ] Personal social links
- [ ] 2+ client reviews with ratings
- [ ] Video intro URL (optional)
- [ ] Notable cases (optional)

## Output Format

Wrap in script tag for HTML insertion:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [...]
}
</script>
```

## Validation Checklist

- [ ] All @id values are unique within the document
- [ ] All @id references point to defined entities
- [ ] URLs are absolute and properly formatted
- [ ] Phone numbers use E.164 format
- [ ] Dates use ISO 8601 format (YYYY-MM-DD)
- [ ] Geo coordinates are valid (lat: -90 to 90, lng: -180 to 180)
- [ ] aggregateRating has ratingValue, ratingCount, bestRating, worstRating
- [ ] FAQPage mainEntity is array of Question objects
- [ ] BreadcrumbList positions start at 1 and increment
