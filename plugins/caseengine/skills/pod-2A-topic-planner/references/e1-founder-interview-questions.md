# E1 - "The Founder Interview" Founder-Interview Question Set

Canonical, hard-coded question set for Episode 1 (the biographic anchor) of every Case Engine client podcast. EP1 is always titled **"The Founder Interview"** and themed **"Founder Story"**. Its questions are identical for every client - they are NOT n-gram-derived and NOT scored. The `pod-2A-topic-planner` Episode Breakdown roll-up populates E1's table directly from this file; the n-gram build step skips E1 entirely.

**Tokens** are filled per client at render time:

- `{{LOCATION}}` - the client's city / anchor (e.g., "Houston, TX")
- `{{BUSINESS}}` - the firm name (e.g., "Sutliff & Stout")
- `{{NICHE}}` - the firm's practice specialty / focus area

The 21 questions are read in order. The **render** is a flat two-column `Question | Rationale` table - all 21 questions top to bottom, unnumbered, with no Segment column (the S1-S5 + Outro grouping below is kept here for maintainer clarity only and is NOT a rendered column). The `Rationale` column carries the hard-coded interview-purpose note for each question - a few words on what the question accomplishes in the founder interview, not a research signal.

## S1: Personal & Professional Foundation

| Question | Rationale |
|---|---|
| What inspired you to become a lawyer? | Builds relatability -- the human behind the firm |
| What's your educational background and key credentials? | Establishes credentials and authority |
| Where are you originally from, and what brought you to {{LOCATION}}? How does that shape how you practice today? | Roots the founder in the local market |
| You specialize in personal injury law. Within that, are there specific types of cases you focus on most? And why those areas? | Defines the firm's niche and depth |
| What's one thing you wish more people understood about what personal injury attorneys actually do? | Positions the founder as an educator |

## S2: Practice Philosophy & Approach

| Question | Rationale |
|---|---|
| What's the mission behind {{BUSINESS}}? What are the core services your firm provides, and what types of clients do you find yourself working with most often? | Surfaces the firm's mission and ideal client |
| Walk me through your case strategy. When you take on a personal injury case, how do you develop your approach? | Demonstrates a deliberate case strategy |
| What's your philosophy on negotiation versus litigation? How do you decide whether to settle or take a case to trial? | Signals trial readiness |
| How do you define success in your practice? Is it just about case outcomes, or is there more to it? | Reframes success around the client |
| What's something about your approach to personal injury law that might surprise people? | Differentiates from generalist firms |

## S3: Experience & Achievements

| Question | Rationale |
|---|---|
| Take us through your career. How did you get from law school to where you are today? | Lays out the experience arc |
| What are some of the cases or achievements you're most proud of? | Concrete proof of results |
| How do you give back to the legal community beyond your case work? | Shows community leadership and character |
| Have there been any awards, recognitions, or honors that have been meaningful to you? | Third-party validation of reputation |

## S4: Vision, Innovation & Values

| Question | Rationale |
|---|---|
| Let's talk about {{NICHE}}. What's your take on it, and where do you see it heading? | Establishes thought leadership on the practice area |
| How do you see technology and AI changing the way law is practiced? | Shows a modern, forward-thinking firm |
| How important is it for people to actually understand the legal process, and what role do you play in that education? | Ties the founder's values to the show's mission |
| What are the guiding principles that shape your career, and who inspires you? | Reveals guiding principles and character |

## S5: Client Access & Next Steps

| Question | Rationale |
|---|---|
| If someone listening wants to find you online, where should they go? | Drives listeners to the firm online |
| For someone who's been in an accident and thinks they might need help, what's the best way to reach you? | Direct conversion CTA for injured listeners |

## Outro

| Question | Rationale |
|---|---|
| What motivates you to keep doing this work and fighting for your clients? | Emotional close on passion and commitment |
</content>
</invoke>
