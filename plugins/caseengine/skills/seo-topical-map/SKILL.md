---
name: seo-topical-map
description: Design topical map architecture with quality nodes and trending nodes for optimal PageRank flow and internal linking strategy. Use when planning site architecture, creating content silos, or optimizing internal linking. Implements node classification, link equity distribution, and content hierarchy principles for SEO.
---

# SEO Topical Map Architecture

Structure website content into quality nodes and trending nodes with strategic internal linking for maximum PageRank flow and topical relevance.

## Node Types

### Quality Nodes
Core pages that receive the most internal links, PageRank, and relevance signals.

**Characteristics:**
- Highest-quality, most comprehensive content
- Target primary commercial keywords
- Receive links from all other page types
- Evergreen content (rarely needs updates)

**Examples:**
- Homepage
- Main service pages (Car Accident Attorney, Personal Injury Lawyer)
- Location hub pages (Houston, Los Angeles)

### Trending Nodes
Freshness-focused pages that capture time-sensitive queries and flow PageRank to quality nodes.

**Characteristics:**
- Updated frequently (news, statistics)
- Target trending/temporal queries ("[city] accident today")
- Link TO quality nodes (not the reverse)
- Attract links naturally due to newsworthy content

**Examples:**
- Statistics pages
- News/recent events pages
- Trend analysis pages

## Architecture Pattern

```
                    ┌─────────────┐
                    │  Homepage   │ ← Quality Node (Primary)
                    │  (Root)     │
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
    ┌────▼────┐      ┌─────▼─────┐     ┌────▼────┐
    │ Service │      │ Location  │     │ Service │
    │ Page 1  │      │ Hub Page  │     │ Page 2  │  ← Quality Nodes
    └────┬────┘      └─────┬─────┘     └────┬────┘
         │                 │                 │
         │     ┌───────────┼───────────┐     │
         │     │           │           │     │
    ┌────▼─────▼───┐ ┌─────▼─────┐ ┌───▼─────▼───┐
    │  Location +  │ │ Trending  │ │  Location + │
    │  Service     │ │ Stats Page│ │  Service    │  ← Sub-pages
    └──────────────┘ └───────────┘ └─────────────┘
                           ↑
                    Trending Node
                    (links UP only)
```

## Internal Linking Rules

### Quality Node → Quality Node
Bidirectional linking allowed. Use primary anchor text variations.

```
Homepage ←→ Service Page ←→ Location Page
```

### Trending Node → Quality Node
**One-way linking only.** Trending pages link TO quality pages.

```
Statistics Page → Homepage (via H1)
Statistics Page → Service Pages (via accident type sections)
```

**Never link FROM quality nodes TO trending nodes** (wastes PageRank).

### Supporting Pages → Quality Nodes
Blog posts, glossary pages, FAQ pages all link to quality nodes.

## Anchor Text Strategy

### Primary Anchors (Header, H1s, First Links)
Most valuable exact-match terms:
- "Houston Car Accident Attorney"
- "Personal Injury Lawyer Houston"

### Secondary Anchors (Footer, Body Links)
Synonyms and variations:
- "Auto Accident Lawyer Houston"
- "Vehicle Collision Attorney"
- "Houston Injury Claim Lawyer"

### Internal Link Placement Priority

| Location | Link Value | Use For |
|----------|------------|---------|
| H1 heading | Highest | Primary quality node |
| First paragraph | Very high | Primary quality node |
| Section headings | High | Related quality nodes |
| Body content | Medium | Supporting context |
| Footer | Lower | Synonym variations |

## PageRank Flow Optimization

### Principles

1. **Minimize boilerplate links**: Fewer nav links = more equity per link
2. **Dynamic navigation**: Remove current-section links from nav
3. **Concentrate on quality nodes**: Most links should point to quality nodes
4. **Trending nodes as feeders**: News/stats pages collect external links, pass equity up

### Calculation Example

Site with 10 links in nav vs. 5 links in dynamic nav:

```
Static nav:  Each link gets 1/10 = 10% of page's link equity
Dynamic nav: Each link gets 1/5 = 20% of page's link equity
```

**50% more link equity per quality node with dynamic navigation.**

## Content Silo Structure

### Vertical Silo (By Practice Area)

```
/car-accident/
├── /car-accident/houston/
├── /car-accident/los-angeles/
├── /car-accident/types/rear-end/
├── /car-accident/types/intersection/
└── /car-accident/compensation/
```

All pages link up to `/car-accident/` (quality node).

### Horizontal Silo (By Location)

```
/houston/
├── /houston/car-accident/
├── /houston/truck-accident/
├── /houston/motorcycle-accident/
└── /houston/statistics/  ← Trending node
```

All pages link up to `/houston/` (quality node).

### Hybrid Approach (Recommended)

```
Homepage (Primary Quality Node)
├── /car-accident-attorney/  (Quality Node - Practice Area)
│   └── /houston-car-accident-attorney/  (Quality Node - Location + Practice)
├── /truck-accident-attorney/  (Quality Node)
│   └── /houston-truck-accident-attorney/  (Quality Node)
├── /houston/  (Quality Node - Location Hub)
│   └── /houston-car-accident-statistics/  (Trending Node)
└── /blog/  (Supporting Content)
    └── Individual posts → Link to quality nodes
```

## Trending Node Implementation

### Statistics Pages

**URL**: `/houston-car-accident-statistics/`

**Links from this page:**
- H1 → Homepage
- Accident type headers → Service pages
- State comparison → State statistics page

**Updated**: Whenever new data available (feeds, reports)

**Content**:
- Aggregate statistics (demographics, time, location)
- Recent incidents (modal-based, no URL bloat)
- Comparisons and trends

### News/Events Pages

**URL**: `/houston-car-accident-news/`

**Alternative**: Combine with statistics on single page for lower-volume markets.

**Links**: Same as statistics page.

**Updated**: Daily/weekly based on news feeds.

## Link Equity Audit Checklist

### Quality Nodes Should Have:
- [ ] Links from all child pages
- [ ] Links from trending nodes in same topic
- [ ] Links from blog posts mentioning the topic
- [ ] Internal links in first paragraph of related pages
- [ ] Anchor text variations (not all exact match)

### Trending Nodes Should Have:
- [ ] Links TO quality nodes (not from them)
- [ ] H1 linking to primary quality node
- [ ] Section headings linking to related quality nodes
- [ ] No outbound links to external sites (keep equity internal)
- [ ] Fresh content signals (recent dates, updated data)

### Avoid:
- [ ] Orphan pages (no internal links pointing to them)
- [ ] Quality nodes linking to trending nodes
- [ ] Too many nav links (>7-10 dilutes equity)
- [ ] Same anchor text on all links (over-optimization)
- [ ] Reciprocal linking between trending nodes

## Implementation Priority

1. **Identify quality nodes**: Homepage, main service pages, location hubs
2. **Audit internal links**: Ensure all pages link to quality nodes
3. **Create trending nodes**: Statistics/news pages that link up
4. **Implement dynamic nav**: Reduce boilerplate, increase link value
5. **Synonymize footer anchors**: Different from header anchors
6. **Add supporting content**: Blog posts that link to quality nodes
