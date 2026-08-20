---
name: seo-trending-pages
description: Design and build trending/news statistics pages that capture freshness signals without URL bloat. Use when creating pages for time-sensitive queries like "[city] car accident today", "[topic] news", or "[location] statistics". Implements modal-based news display, hash URLs, RSS feed syndication, and evergreen page architecture that flows PageRank to quality nodes while ranking for trending queries.
---

# SEO Trending Pages

Create pages that capture trending/time-sensitive queries without bloating the site with thousands of outdated news URLs.

## Core Concept: Trending Nodes

**Quality Nodes** = Core pages with highest relevance, most internal links, and PageRank (service pages, homepage)

**Trending Nodes** = Freshness-focused pages that rank for time-sensitive queries and flow PageRank to quality nodes

Problem: Publishing 2,000+ individual news articles bloats the site and triggers negative effects during helpful content updates (especially without news publisher status or news sitemap).

Solution: Single evergreen page with dynamically updated news content displayed in modals with hash URLs.

## Page Architecture

### URL Structure
```
/houston-car-accident-statistics-today/
```

Title: `[City] Car Accident Today and Statistics`

### Content Sections

1. **H1**: Links to homepage with primary anchor text (e.g., "Houston Car Accident Statistics")
2. **Statistics Grid**: Demographics, accident types, time periods, sub-districts, city comparisons
3. **Latest News Grid**: Modal-based news items (no new URLs created)
4. **Accident Type Links**: Motorcycle, truck, etc. linking to relevant service pages

### Modal Implementation

Instead of creating new URLs for each news item, display news in modals with hash URLs:

```
/houston-car-accident-statistics/#accident-2024-01-15-fm1960
```

Modal content includes:
- Date of accident
- Number of vehicles involved
- Location
- One-sentence statement
- Optional: Location image (not accident scene)

**Key**: Hash URLs don't create crawlable pages but allow sharing/bookmarking.

## Technical Implementation

### News Data Extraction

Feed sources: Local news RSS feeds (Click2Houston, local TV stations)

Filter keywords: "accident", "truck", "motorcycle", "collision", vehicle brands (BMW, SUV, etc.)

Extract per incident:
1. Date
2. Number of vehicles
3. Location
4. Summary statement
5. Image (optional - prefer location over accident scene)

### N8N/Automation Workflow

```
RSS Feed → Filter (accident keywords) → AI Extraction → WordPress API
```

AI prompt for extraction:
```
Extract from this news text:
- date_of_accident
- number_of_vehicles
- location_of_accident
- one_statement_summary

Output as JSON.
```

### Rendering Optimization

**Problem**: 10,000+ news items bloats page, slows rendering.

**Solutions**:

1. **Number limit (not time)**: Keep 100 most recent items
   - Avoids empty page if no accidents for months
   - Prevents excessive page size

2. **Progressive disclosure**: Show 5 initially, hide rest
   - Use HTML `<template>` tag for deferred rendering
   - Content in source code (crawlable) but not rendered until clicked
   - No impact on initial page load speed

3. **Backend archive**: Store all historical data
   - Accessible via search/filter (hash URLs)
   - AI chatbot can query archive

### CSS for Hidden Content

```css
/* Content crawlable but not rendered until interaction */
.news-hidden {
  content-visibility: auto;
}
```

Or use `<template>` tag for complete render deferral.

## Internal Linking Strategy

### From Trending Page

| Element | Links To | Anchor Text |
|---------|----------|-------------|
| H1 | Homepage | Primary keyword (Car Accident Attorney Houston) |
| Accident type headers | Service pages | Truck Accident, Motorcycle Accident, etc. |
| Statistics comparisons | State/regional stats page | Texas Car Accident Statistics |

### To Trending Page

| From | Link Location |
|------|---------------|
| Homepage | Statistics section |
| Service pages | Relevant statistics callout |
| Blog posts | Data citations |

**PageRank flow**: Trending page ranks → gains authority → flows to homepage and service pages via links.

## Scaling Considerations

### When to Split Pages

| Search Volume | Page Structure |
|---------------|----------------|
| Low | Combined: `[City] Car Accident Today Statistics` |
| High (state-level) | Separate: `Texas Car Accident Statistics` + `Texas Car Accident News Today` |

### Title Attribute Ordering

For conditional freshness:
- If accident today: "today" more prominent
- Normal days: "statistics" more prominent

Future: Dynamic title adjustment based on feed activity.

## Example Implementation

### Page: `/houston-car-accident-statistics/`

```html
<h1><a href="/">Houston Car Accident Attorney</a> - Statistics and News</h1>

<section class="statistics">
  <h2>Houston Car Accident Statistics</h2>
  <!-- Statistics by demographics, type, time, location -->
  <p>Link to <a href="/texas-car-accident-statistics/">Texas statistics</a></p>
</section>

<section class="news-grid">
  <h2>Latest Houston Car Accidents</h2>

  <!-- Visible items -->
  <article data-modal="accident-2024-01-15">
    <span class="date">Jan 15, 2024</span>
    <span class="location">FM 1960</span>
    <span class="vehicles">2 vehicles</span>
  </article>

  <!-- Hidden items in template -->
  <template id="news-archive">
    <!-- Older items -->
  </template>

  <button onclick="showMore()">View More</button>
</section>

<section class="accident-types">
  <h2>Statistics by Accident Type</h2>
  <a href="/houston-truck-accident-lawyer/">Truck Accidents</a>
  <a href="/houston-motorcycle-accident-lawyer/">Motorcycle Accidents</a>
</section>
```

### Modal Structure

```html
<dialog id="accident-2024-01-15">
  <h3>FM 1960 Collision - January 15, 2024</h3>
  <p><strong>Vehicles:</strong> 2 (motorcycle, truck)</p>
  <p><strong>Location:</strong> FM 1960 Westbound</p>
  <p>Two individuals were killed in a motorcycle and truck collision near the FM 1960 corridor.</p>
  <img src="/images/locations/fm1960.jpg" alt="FM 1960 Houston">
</dialog>
```

## Engagement Features

Optional enhancements for user signals:

1. **Login/Register**: Allow users to submit questions or reviews
2. **AI Chatbot**: Query historical accident data by location/date
3. **Newsletter signup**: Alert subscribers to new incidents
4. **Search/filter**: Find specific incidents by street, date, vehicle type

These features differentiate from content-only sites and increase return visits.
