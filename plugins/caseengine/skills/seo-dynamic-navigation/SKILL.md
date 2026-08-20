---
name: seo-dynamic-navigation
description: Design dynamic header and footer navigation with context-sensitive anchor text optimization and PageRank flow control. Use when building website navigation, creating header/footer templates, or optimizing internal linking architecture. Implements boilerplate link reduction, anchor text synonymization, and semantic HTML structure for SEO-optimized navigation.
---

# SEO Dynamic Navigation

Design header and footer navigation that maximizes PageRank flow to main content while providing context-sensitive anchor text optimization.

## Core Principles

1. **Reduce boilerplate links**: Fewer navigation links = more link equity to main content
2. **Dynamic anchor text**: Change link text based on current page context
3. **Anchor text differentiation**: Header uses primary terms, footer uses synonyms
4. **Functional elements**: Login, search, newsletter = site classification signals

## Header Design

### Structure

```
[Logo] [Type Search] [Login/Register] [VMAT Links]
```

Keep header to single line. Header + above-fold should share space; header ≤10% of viewport.

### Components

#### 1. Logo with Alt/Title
```html
<a href="/" title="Houston Car Accident Attorney">
  <img src="/logo.png" alt="Houston Car Accident Attorney" />
</a>
```
- Alt/title = most valuable anchor text for homepage
- Include location if homepage targets location

#### 2. Type Search (Not Query Search)
```html
<input type="text" id="typesearch" placeholder="Search services..." />
```
- Algolia or similar instant search
- No URL query parameters (no `/search?q=`)
- User types → suggestions appear → click goes to landing page
- Prevents URL bloat from search queries

#### 3. Login/Register
```html
<button onclick="openModal('login')">Login</button>
<button onclick="openModal('register')">Register</button>
```
Purpose:
- Differentiates from content-only sites
- Enables forum context (Q&A, reviews)
- Builds email list
- Increases engagement signals

**For legal sites**: Users can submit questions, add reviews, subscribe to alerts.

#### 4. VMAT Links (Valuable Most-valuable Anchor Text)
```html
<nav class="header-nav">
  <a href="/houston/" title="Houston Personal Injury">Houston</a>
  <a href="/los-angeles/" title="Los Angeles Personal Injury">Los Angeles</a>
</nav>
```

**Dynamic behavior**: Links change based on current page section.

| Current Page | Header Shows |
|--------------|--------------|
| Homepage | All location links |
| /houston/ section | Hide Houston, show others |
| /houston/truck-accident/ | Hide Houston links |

**Implementation**: PHP/server-side conditional, NOT JavaScript (must be in HTML source for crawlers).

## Footer Design

### Structure

```
┌─────────────────────────────────────────────────────┐
│ [Logo + Secondary Anchor]                           │
│ [Site-wide definition sentence]                     │
│ [Page-specific definition sentence]                 │
├─────────────────────────────────────────────────────┤
│ [Newsletter Signup]                                 │
├─────────────────────────────────────────────────────┤
│ [Social Icons]                                      │
├─────────────────────────────────────────────────────┤
│ [Link Groups with Hover Menus]                      │
│   Corporate | Services | Locations | Resources      │
├─────────────────────────────────────────────────────┤
│ [Awards/Certifications]                             │
├─────────────────────────────────────────────────────┤
│ [Company Definition + Copyright]                    │
└─────────────────────────────────────────────────────┘
```

### Components

#### 1. Logo with Secondary Anchor
```html
<a href="/" title="Houston Personal Injury Lawyer">
  <img src="/logo.png" alt="Houston Personal Injury Lawyer" />
</a>
```
- Use DIFFERENT anchor text than header
- Header: "Car Accident Attorney" → Footer: "Personal Injury Lawyer"

#### 2. Dynamic Definition Sentences

**Sentence 1 (Site-wide, always present):**
```html
<p>Sutliff Start is a personal injury and car accident attorney in Houston,
   serving clients across Texas.</p>
```

**Sentence 2 (Page-specific, changes per page):**

| Page Type | Footer Sentence |
|-----------|-----------------|
| Service page | "Truck accident attorney services in Houston including [list]. Also provided by Sutliff Start." |
| Blog/Info page | "Learn more about [topic] from our Houston legal team." |
| Location page | "Serving [neighborhood] and surrounding areas." |

#### 3. Newsletter Signup
```html
<form class="newsletter">
  <label>Subscribe to legal updates</label>
  <input type="email" placeholder="Email" />
  <button type="submit">Subscribe</button>
</form>
```
Adds functional classification signal (subscription action).

#### 4. Social Icons
```html
<nav class="social">
  <a href="https://facebook.com/firm" onclick="..." title="Sutliff Start Facebook">
    <img src="/icons/facebook.svg" alt="Sutliff Start Facebook" />
  </a>
</nav>
```
- Use onclick events (not nofollow)
- Alt/title: Brand name + platform name

#### 5. Link Groups with Synonymized Anchors

**Header uses primary terms:**
```html
<a href="/houston/">Car Accident Attorney Houston</a>
```

**Footer uses synonyms:**
```html
<a href="/houston/">Auto Accident Lawyer Houston</a>
<a href="/houston/">Vehicle Collision Attorney Houston</a>
```

| Header Term | Footer Synonym |
|-------------|----------------|
| Car Accident Attorney | Auto Accident Lawyer |
| Truck Accident | Commercial Vehicle Accident |
| Personal Injury | Injury Claim |

**Hover menu structure:**
```html
<div class="footer-menu">
  <button>Services</button>
  <nav class="hover-menu">
    <a href="/car-accident/">Auto Accident Lawyer</a>
    <a href="/truck-accident/">Commercial Vehicle Attorney</a>
  </nav>
</div>
```

#### 6. Awards/Certifications
```html
<div class="awards">
  <img src="/awards/superlawyers.svg" alt="Super Lawyers 2024" title="Super Lawyers 2024" />
  <img src="/awards/avvo.svg" alt="Avvo 10.0 Rating" title="Avvo 10.0 Rating" />
</div>
```
- 3-4 awards maximum
- Verbalize in alt/title attributes
- Optional: DMCA protection badge (auto-submits complaints)

#### 7. Company Definition + Copyright
```html
<p class="company-definition">
  Sutliff Start, founded in 2015, is owned and operated by [Attorney Name],
  a licensed attorney in the State of Texas. This content is proprietary
  and protected by copyright.
</p>
<p class="copyright">© 2024 Sutliff Start. All rights reserved.</p>
```

Purpose:
- Establishes entity ownership
- Protects content claims
- Adds relevance signals (founding date, ownership, location)

## Semantic HTML Structure

```html
<footer>
  <section class="footer-top">
    <a href="/" class="footer-logo">...</a>
    <p class="site-definition">...</p>
    <p class="page-definition">...</p>
  </section>

  <section class="footer-newsletter">
    <form>...</form>
  </section>

  <nav class="footer-social">
    <a href="...">...</a>
  </nav>

  <nav class="footer-links">
    <div class="link-group">
      <h2>Services</h2>
      <ul>
        <li><a href="...">...</a></li>
      </ul>
    </div>
  </nav>

  <section class="footer-awards">
    <img ... />
  </section>

  <section class="footer-legal">
    <p class="company-definition">...</p>
    <p class="copyright">...</p>
  </section>
</footer>
```

**Key elements:**
- `<footer>` wrapper
- `<nav>` for link groups
- `<section>` for content blocks
- `<h2>` for link group headings (can be inside nav)
- `<ul><li>` optional for link lists

## Implementation Checklist

### Header
- [ ] Single-line design (≤10% viewport)
- [ ] Logo with primary anchor text in alt/title
- [ ] Type search (no query URLs)
- [ ] Login/Register functionality
- [ ] Dynamic VMAT links (server-side conditionals)

### Footer
- [ ] Secondary anchor text on logo (different from header)
- [ ] Site-wide definition sentence
- [ ] Page-specific definition sentence (dynamic)
- [ ] Newsletter signup form
- [ ] Social icons with onclick + alt/title
- [ ] Link groups with synonymized anchors
- [ ] Awards/certifications (3-4 max)
- [ ] Company definition + copyright

### Technical
- [ ] Server-side rendering (PHP/SSR) for dynamic links
- [ ] Semantic HTML structure
- [ ] Alt and title attributes on all images/links
- [ ] Consistent anchor text differentiation (header ≠ footer)
