# Introduction

The first 45 to 60 seconds of the episode. Read by `steps/04-segment-1.md`. Everything here governs four sentences and one beat - it is the most-edited, most-clipped, highest-leverage passage in the document, which is why it gets its own file.

The introduction is not a script to read. It is a shape. The host says these things, in this order, in their own words. The one exception is line 1, which is verbatim every time.

## GUARDRAILS — read this, then the examples, then write

**Calibrate on `examples/intro-outro-examples.md` before writing.** Every pair in it is real. The examples carry more than these rules do; these exist so you know what is non-negotiable.

**Hard, never violated:**
- The topic is NAMED in line 2. Never teased.
- Line 2 never re-names the attorney. No "here with **{{ATTORNEY}}**" - line 1 already welcomed them, and a third name in forty seconds is the tell of a template (Gabe, 2026-08-26).
- The verb stays. "today we're talking about X", never "Today, X".
- Line 4 is one sentence and carries the episode topic. No invented beats.
- Line 2 and line 4 do not say the same thing twice.
- No dramatized scene. No `{{CITY}}` in S1. No CTA, ever.
- Contractions. Numbers spelled. Nothing claimed that the firm has not told us.
- Read it aloud. If a person wouldn't say it, it fails no matter how well it reads.
- No word repeats across adjacent lines. No stacked "and"s. Never restate what an earlier line already established.

**Soft, judgment:**
- Stakes clause is optional and the first thing to cut.
- Credential is germane to THIS episode; tenure is the fallback. Vague years are fine. Tenure is BANNED when any recent episode's credential already used years - go vaguer: a nod to expertise and experience that sets up the topic (Gabe, 2026-08-26).
- Don't repeat the last few episodes' wording *or sentence shape*.

## EXECUTION — the order that produces it every time

1. Read `examples/intro-outro-examples.md`.
2. Read the previous 2-3 episodes' intro and outro for this client. You are avoiding their wording and their shapes.
3. Line 1: paste the static open. Episode 1 takes "Welcome to".
4. Line 2: host ID first and alone - never "here with **{{ATTORNEY}}**" (Gabe, 2026-08-26) - then verb, then topic named plainly. Two sentences beat one run-on chain. Hook when it carries the episode's genuine insight; skip it when the plain name lands. Stakes clause only if it earns its place.
5. Line 3: pick the credential frame that is germane to this episode AND sourceable. If only tenure is available, use it and say the years loosely if unknown.
6. Line 4: pick the situation, then the ask verb from the topic shape, then the topic phrase. Check it against line 2 for echo.
7. Outro: `outro.md`, three lines, no CTA.
8. **Read all seven lines aloud, in order.** This is the gate. Anything you would not say to a person gets rewritten now, not at populate.
9. **The natural pass.** Read once more and fix the three things that survive every other rule:
   - **Repeated words across adjacent lines.** "the other side's adjuster ... dealing with the insurance adjuster" - the ask can point back at what line 2 set up: "if someone just got that call."
   - **Stacked "and"s.** "I'm Kara, and today we're talking about X, and what they're really after" - break it: "I'm Kara. Today we're talking about X, and what they're really after."
   - **Restating what an earlier line established.** If line 2 has already put the listener in the situation, line 4's setup can be two words.

## Angle variants (Gabe, 2026-08-26)

Generation SHOULD produce one primary plus 3-4 alternate angles for each spoken line (lines 2, 3 and 4). The alternates are not paraphrases. Each one is a different angle on the same job, and every alternate clears the same guardrails and gates as the primary, because the producer may swap any of them in verbatim from the tool.

- Line 2: alternates use different openers from the opener bank ("today we're going to discuss X" / "today the topic is X" / "the theme today is X" / "we're going to dive into X" / "today we're talking about X"), one opener per alternate, never repeating the primary's.
- Line 3: alternates use different EEAT axes - Experience (tenure or volume), Expertise (depth in this case type), Authoritativeness (the topic sits at the practice core), Trust (battle-tested against the adjusters on the other side). One axis per alternate, never the primary's axis twice.
- Line 4: alternates use different verb frames (walk us through / break down / explain / lay out / tell us / set us straight on) around the same topic phrase anchor.

The primary ships in the payload's main field; the alternates ride beside it (segment_1.alternates) and surface in the tool's caret menu, where the producer picks the angle. A pick promotes the alternate to primary and keeps the displaced line in the list, so no angle is ever lost.

## THE SPEC — detail behind the guardrails

Four sentences. About 40 seconds. If it can be done in three, do it in three.

**1. The open.** Verbatim, every time.
> Welcome back to **{{PODCAST_NAME}}** with **{{ATTORNEY_NAME}}**.

Episode 1 only: "Welcome to" instead of "Welcome back to."

**Embedded-name shows (Gabe, 2026-08-26):** when the podcast name embeds the attorney's name (e.g. "Car Accident Attorney w. Robert May"), line 1 is "Welcome back to the **{{PODCAST_NAME}}** Podcast." (Episode 1: "Welcome to the **{{PODCAST_NAME}}** Podcast.") - never "with **{{ATTORNEY_NAME}}**", which doubles the name. A "w." in the podcast name is spoken, and rendered in the welcome, as "with". All four constants live in `references/statics.json`.

**2. Who's asking, and what today is.** Host ID first and alone: "I'm **{{INTERVIEWER}}**." NEVER "here with **{{ATTORNEY}}**" - line 1 already welcomed them, and re-naming them here makes the intro say the name three times (Gabe, 2026-08-26). Then a **verb**, then the topic named plainly. Prefer two sentences over one run-on chain. A hook clause after the topic is encouraged when it carries the episode's genuine insight - "...and why the most serious injury from a California crash is often the one nobody can see" - and skipped when the plain name lands. A stakes clause is optional and is the first thing to cut.

**KEEP THE VERB.** "today we're talking about" / "today we're getting into" / "today we're looking at". Dropping it to save words produces a headline, not a sentence — "Today, the insurance adjuster" is a newspaper subhead and no person says it out loud. Short is good; verbless is not short, it's broken.
> I'm Kara, and today we're talking about the insurance adjuster, and what they're really doing when they call you a day after a crash.
> I'm Kara, and today we're getting into what an injury is actually worth.

Never the episode title verbatim. Geo here is **{{STATE}}**, never **{{CITY}}**. This line does not carry the SEO weight — line 4 does.

**3. Why listen to him.** One sentence, spoken to him, one credential, germane to THIS episode. Vary it across episodes; tenure every time is the weakest option, and tenure is BANNED when any recent episode's credential already used years - reach for a vaguer nod to expertise and experience that sets up the topic instead (Gabe, 2026-08-26). If the exact years aren't known, say it loosely — "for a number of years," "for more than a decade." Never invent a fact about the practice.
> Brett, you've sat across from these adjusters for twelve years.
> Brett, uninsured claims are a core part of your practice.

**The beat.** The attorney says hello. Unscripted, a sentence or two, marked as a direction. Cuttable in post.

**4. The ask.** One sentence: a situation, then an imperative ask **carrying the episode topic**. This is the retrieval anchor and the clip title, so the topic phrase survives into it. No invented beats. No question mark needed — an instruction asks for narration, and narration is what fills the segment.
> If someone just got a call from the other side's adjuster, walk us through dealing with the insurance adjuster.
> If someone gets an offer and has no idea if it's fair, break down what a car accident case is worth and what goes into that number.

Match the verb to the topic: process → *walk us through*; number → *break down*; rule → *explain*; comparison → *lay out*; judgment → *tell us*; misconception → *set us straight on*.

**Line 2 and line 4 must not say the same thing twice.** They are forty seconds apart and both name the topic, so they collide easily — line 2 "what happens when the driver who hit you has no insurance" against line 4 "explain what happens when the other driver has no insurance" is one sentence said twice. Line 4 owns the full topic phrase; line 2 gets the short human version. If they overlap, cut line 2 down.

**Rules that apply to all of it.** Contractions. Numbers spelled. No dramatized scene — no "suddenly," no "out of nowhere." Read it aloud; if a person wouldn't say it, it fails no matter how well it reads. Don't repeat the wording *or the sentence shape* of the last few episodes.

---

*Everything below is background: the anatomy tables, the pattern and frame libraries, and the 2026-08-14 call this was built from. Read it when you need to understand why a rule exists or want more examples. Don't read it to write an intro.*

## Three parts, four sentences

Gabe, 08-14 (10:06): "The introduction needs to be like three sentences, or three parts. Branding and identification of the podcast and where we're at. Then setup of what the topic is. And then the prompt about the topic. And then just shut them up."

Cyle, same call (4:23), reacting to a long one: "By the time they get to the end of that, it's like - what did you just say? It needs to be three sentences, that's it."

The three parts are **branding**, **topic setup**, and **the prompt**. The prompt runs to two sentences because it carries a credential and an ask, which is why the table below has four rows and not three. Four sentences is the ceiling, not a target. If it can be done in three, do it in three.

**The north star is "sounds normal."** Gabe, comparing an AI draft to Cyle's improvised version (26:48): "Yours sounds normal. [The AI one] sounds a little AI. I don't know how else to say it." Cyle: "It sounds weird. That's a good way to put it. Mine is normal." If a line would be strange to say out loud to a person, it fails, regardless of how well it reads.

**Why brevity, specifically.** Cyle (1:00:48): "The way we have it is good, because it just gets right into it, and it doesn't give the viewer that much time to be like, nah, this. They'll watch it right away." Every extra sentence is another chance for someone to leave.

## The four lines

| Line | Job | Contains | Target |
|---|---|---|---|
| 1 | Name the show and whose show it is | `{{PODCAST_NAME}}`, `{{ATTORNEY_NAME}}` | Under 12 words. STATIC |
| 2 | Who is asking, what the subject is, where | `{{INTERVIEWER}}`, the topic, `{{STATE}}` | 25-30 words. Generated |
| 3 | Establish the attorney, pivot to addressing them | `{{ATTORNEY}}`, one credential, `{{YEARS_PRACTICING}}` | One sentence, under 25 words. Generated |
| - | **The beat** - attorney says hello | - | A sentence or two. Not scripted |
| 4 | Hand over the floor | situation, ask, story invitation | Three short sentences, 25-35 words. Generated |

Four sentences, roughly 95 words, about 40 seconds of host. The beat puts a second voice in at around 25 seconds, which is the point of it.

## Line 1 - the open

Two forms, and which one fires is decided by the episode number, not by taste.

**Every episode after the first:**

```
Welcome back to **{{PODCAST_NAME}}** with **{{ATTORNEY_NAME}}**.
```

**Episode 1, the launch:**

```
Welcome to **{{PODCAST_NAME}}** with **{{ATTORNEY_NAME}}**.
```

"Welcome back" on a first episode is the tell that a show was assembled rather than started - there is no back to welcome anyone to yet. Episode 1 is also the only episode that gets to introduce the show itself, so line 2 carries a launch setup: what this show is going to do all season, for whom, in **{{STATE}}**. It says that once, in the first episode, and never again.

**The embedded-name variant (Gabe, 2026-08-26).** When the podcast name embeds the attorney's name - "Car Accident Attorney w. Robert May" - the standard close would double it: "...with Robert May with Robert May." Those shows take "Welcome back to the **{{PODCAST_NAME}}** Podcast." (Episode 1: "Welcome to the **{{PODCAST_NAME}}** Podcast."). A "w." in the podcast name is spoken, and rendered in the welcome, as "with". All four constants live in `references/statics.json`.

Both forms are verbatim otherwise. The line is a sonic marker, not information. Adding a tagline, an episode number, or a welcome-to-the-show breaks it.

## Line 2 - the setup

The middle of Gabe's three parts: "then setup of what the topic is." It is the only line that has to do four things at once, which is why it is the hardest one to write and the one that goes wrong most often.

### The anatomy

Four slots, in this order. The whole line is 25-30 words.

| Slot | What it does | Rules |
|---|---|---|
| **Host ID** | "I'm **{{INTERVIEWER}}**" | Three words. Never a title, never a role description, never "your host." Never the attorney's name - line 1 already said it (Gabe, 2026-08-26). |
| **The turn** | The pivot into the subject | Vary the verb - "today we're getting into," "today is about," "today we're taking." Never "in this episode we'll cover," which turns the line into a table of contents. |
| **The subject** | Names the thing in plain language | This is where the ten patterns live. Never the practice area as a category, never the episode title verbatim. If the only name is a legal one, say it once and alias it immediately: "premises liability, or so-called slip and fall." |
| **The stakes** | Why a stranger should keep listening | OPTIONAL. One clause, second person, practice-area neutral, different every episode. **Drop it when the subject already carries the hook** - a short line 2 beats a padded one. |

**The geo rides inside the subject slot**, once, and in S1 it is **{{STATE}}** - never `{{CITY}}`. "Something a lot of people in **{{STATE}}** end up dealing with." The long-form answer is state-governed, so one recording serves every city the firm covers; the city blocks in S2 are where `{{CITY}}` lives. Nearly every firm is one state; a multi-state firm is flagged at generation time and `{{STATE}}` resolves to the spoken phrase instead.

### Line 2 is short. Line 4 carries the topic.

**Line 2 does not have to carry the SEO weight** - line 4's ask carries the topic phrase intact, and that is enforced. So line 2 can be short and human. Trying to make one sentence both name the topic for retrieval AND land a hook is what bloated this section to ten patterns; it is the wrong sentence for the job.

Name the thing, plainly and briefly. Add a hook in apposition when it carries the episode's genuine insight; skip it when the plain name lands (Gabe, 2026-08-26). Then stop. **The stakes clause is optional and usually the first thing to cut.**

### Vary the SHAPE, not just the words

**Different words in the same sentence shape is not variation.** A ten-episode set generated 2026-08-21 used ten different stakes clauses and six different ask verbs, and still opened every single episode with `I'm {host}, and today [verb] [subject], and [trailing clause]` followed by `If someone [situation], [verb] [topic]`. Read one at a time they look varied. Read as a library they are the same two sentences twelve times.

**A near-verbatim uniqueness check does not catch this** - none of those ten were near-verbatim. Uniqueness is necessary and not sufficient. The test is: lay this episode's line 2 and line 4 next to the last three episodes' and ask whether they have the same skeleton.

**The opener is EXEMPT (Gabe directive 2026-08-21).** Line 1 is static, and the host-ID slot that opens line 2 is static or near-static by design - a sonic marker, not information. It does not need to vary and must not be relocated inside the sentence to manufacture variation. Acceptable near-static forms:

> I'm **{{INTERVIEWER}}**.
> I'm **{{INTERVIEWER}}**, ...

The "here with **{{ATTORNEY}}**" and "sitting down with **{{ATTORNEY}}**" forms are RETIRED (Gabe, 2026-08-26): line 1 already welcomed the attorney, and re-naming them here makes the intro say the name three times. Host ID is first and alone, and two sentences beat one run-on chain.

Pick one and let it sit. **Variation comes from the turn, the subject and the stakes - never from moving the host ID.**

**Line 2 shapes** - the part that DOES vary. Do not end every episode on a trailing "and ..." clause:
- Trailing stakes: "...today we're getting into {subject}, and what most people get wrong about it."
- No trailing clause at all: "...today is about {subject}." Let the subject carry it. Shortest is often best.
- Stakes folded into the subject: "...today we're taking on the {subject} nobody explains until it is too late."
- Two beats: "...today, {subject}. {stakes}."

**Line 4 shapes** - do not open every episode with "If someone":
- Conditional: "If someone was just in a wreck, walk us through {topic}."
- Declarative setup: "Somebody's three weeks out and still hurting. Walk us through {topic}."
- Hypothetical: "Say the other driver has no insurance. Explain {topic}."
- Straight ask, no setup: "Walk us through {topic}." Use when the topic is self-evident and the setup would pad it.

Rotate the shape across consecutive episodes the same way the verb rotates. Neither has a counter and neither has a quota - the check is reading the last three episodes and not matching them.

### The stakes clause: neutral, and never the same twice

**It must survive every topic the client will ever record.** "And what you actually need to know if it happens to you" works for a crash and is nonsense on an episode about hiring a lawyer or filing deadlines - neither of those happens *to* anyone. This is the same failure Gabe retired from outro line 3 in 2026-08-14, where "if you were hurt" was replaced by "in {{STATE}} and need a lawyer" because the practice-area branch was managed instead of removed. Line 2 carried the same bug until 2026-08-21.

Neutral constructions that survive any topic: "and what that actually means for you." / "and what most people get wrong about it." / "and what you'd want to know before you're in it." / "and why it matters more than people think."

**It must be different every episode.** Not by rotating a bank - by writing it. A run once produced ten consecutive episodes ending on the identical clause, which is exactly the drift the outro banks were built to prevent, arriving through a different door. The examples above are calibration, not a menu: sampling a fixed list produces the same flatness as repeating one line.

**The test is the read-aloud, not a counter.** If it sounds like a person and it is not what the last episode said, it passes. There is deliberately no quota and no rotation index here - every mechanical rule of that shape tried on this pipeline produced worse output by forcing it.

**Vary the turn verb too.** "today we're getting into" opening every episode is the same defect one slot to the left. Rotate: today we're getting into / today we're taking on / today is about / today we're looking at.

### Three rules that matter more than the pattern choice

**It ends at the stakes clause.** Cyle, editing live on the 08-14 call: "Everything after 'if it happens to you' - delete." No second thought, no qualifier, no bridge into line 3. The full stop is what makes line 3 land as a turn toward the attorney.

**The stakes clause is a fact, not a threat.** "What you actually need to know if it happens to you" is a fact. "Before you lose everything" is a fear pitch, and it is the failure this line drifts toward every time somebody tries to make it stronger.

**One sentence, or two short ones.** If it needs a semicolon, it is too long to say.

### Patterns

Four moves. Combine at most two. Anything longer than one sentence, or two short ones, is too long to say.

- **Name it plainly.** The default and usually the best. "today we're talking about the insurance adjuster" / "today we're getting into what an injury is actually worth"
- **Name it, then the hook.** Encouraged when the hook carries the episode's genuine insight - "...and why the most serious injury from a California crash is often the one nobody can see" - and skipped when the plain name lands (Gabe, 2026-08-26). "today we're talking about the insurance adjuster, and what they're really doing when they call you a day after a crash"
- **Prevalence.** "Something a lot of people in **{{STATE}}** end up dealing with." Use a number ONLY when research supplies a real one - say the source briefly, round it, never guess. `{{N}}` never ships unresolved.
- **Nobody plans for this.** For topics with a decision window. "Today's topic is one nobody plans for."

**The local moment (a named road, a named place) is OFF in S1.** The long form speaks at state level so one recording serves every city; `{{CITY}}` lives in the S2 blocks. Never stack local detail here.

**Do not write it as a search.** "The thing people search for at two in the morning" is internal framing, not a spoken line.


## Line 3 - the credential

> **{{ATTORNEY}}**, you've been representing car accident victims in **{{STATE}}** for **{{YEARS_PRACTICING}}** years.

One credential, stated as a fact, spoken directly to them. This is the line that answers "why should we listen to you" so line 4 never has to ask.

### The eight frames

Each frame is a different kind of proof. Use ONE. Two credentials in one sentence is a bio, and a bio is the thing an attorney's website already does badly.

**Tenure is the DEFAULT, not the answer (Gabe directive 2026-08-21).** "You've been doing this for {{YEARS_PRACTICING}} years" every episode is the weakest possible use of this line - the spec's own note on L3-A says it "says nothing surprising." A run once opened ten consecutive episodes on tenure. **`{{YEARS_PRACTICING}}` is optional here, not required.** **Hardened 2026-08-26 (Gabe): tenure is BANNED outright when any recent episode's credential already used years. When the fallback is needed twice, the second one goes loose - a vaguer nod to expertise and experience that sets up the topic, not another years figure.**

- **Pick the frame that is germane to THIS episode.** Trial record on an episode about whether the insurer will actually pay. Specific case type on an injury-type episode. The local system on venue or the responding agency. The bench behind them on medical treatment. Tenure only when nothing more specific is true.
- **The credential must not repeat, near-verbatim, any prior episode for this client.** Same uniqueness rule as line 2 and the outro - checked against the prior episodes' text, not a rotation index.
- **Reinforce experience, expertise, or something germane to the topic.** That is the job. The years number is one way to do it and usually the dullest.
- **L3-G and L3-H are CONDITIONAL** on the firm actually having told us. Never synthesize a reason or a result.
- **Use only the frame you can SOURCE.** Most frames assert a fact about the firm: L3-B needs a real case volume, L3-C needs to know they actually try cases, L3-F needs a confirmed medical network, L3-D needs the practice mix. If the firm has not told us, the frame is unavailable - a vivid invented credential is worse than a dull true one, and this is the same sourcing discipline the rest of the pipeline runs on.
- **The safe pair is L3-A (tenure) and L3-D (specific case type)** - tenure derives from the bar admission date and case type from the topic plan's practice mix, so both are sourceable for any client on day one. When only those two are available, alternate them and accept the repetition. Flag the gap rather than filling it.
- **The four questions that unlock the rest**, worth asking every firm once at intake: roughly how many of these a month, do you try cases or settle them, is there a medical or expert network, and is there a recent result you are willing to have named on air. Answers belong in the client record, not in a one-off doc.

**L3-A - Tenure.** The default. Safe, works for anyone, says nothing surprising.

> **{{ATTORNEY}}**, you've been representing {topic} clients here for **{{YEARS_PRACTICING}}** years.

**L3-B - Volume.** Stronger than tenure when the number is real, because time served is not the same as reps. Two shapes, and the second is better:

> **{{ATTORNEY}}**, you've handled over {N} of these, most of them right here.

> **{{ATTORNEY}}**, your firm takes on {X} to {Y} of these a month, every month, right here.

**A rate beats a total.** "Over 500 cases" is a lifetime number - it could all have happened a decade ago, and every firm's total only goes up. "Thirty to forty a month" answers the two things the attribute research says people actually want to know, how many of THIS kind and how recently, in one clause. It also ages well: a total gets stale the day it is spoken, a rate stays true as long as the practice does.

Use a range for a rate and a rounded floor for a total. "Thirty to forty a month" is honest about variation; "37.5 a month" is a spreadsheet talking. And keep the range tight - "ten to fifty" is not a range, it is an admission that nobody counted.

**L3-C - Trial record.** The single strongest frame available. Trial willingness is the top-ranked attribute across every answer-engine pull, and it is usually the first thing the AI answer says to look for.

> **{{ATTORNEY}}**, you actually try these cases when they don't settle, which is rarer around here than most people realize.

**L3-D - Specific case type.** Answers the attribute that matters more than practice area: how many of THIS kind, how recently.

> **{{ATTORNEY}}**, {specific case type} is what your firm handles day in and day out.

**Three shapes that work.** All three concede breadth and then name the depth, which is both more credible and more likely to be true:

> **{{ATTORNEY}}**, your firm handles a lot of different {practice area} work, but {specific case type} is where you specialize.

> **{{ATTORNEY}}**, a core part of your practice is {specific case type}.

> **{{ATTORNEY}}**, you take a range of cases, but {specific case type} is where the emphasis has always been.

The concession is what makes the claim land. "We only do X" invites the listener to wonder what happens when their case is not exactly X. "We do a lot of things, and this is the one we go deep on" answers the question they were actually asking, which is whether this firm has seen their situation before.

**State the focus, never deny the rest.** "You don't just do injury work," "your practice is X and that's it," "you don't take anything else" - all wrong, for two reasons. It is a claim about what the firm does NOT do, which nobody verified and which is usually false; most firms that concentrate in one area still take adjacent work. And negation is a defensive shape: it answers an accusation nobody made. Depth is a positive fact and it should sound like one. "This is what your firm does day in and day out" says more than "that is it," and it is true.

**L3-E - The local system.** Courts, judges, the defense firms, the adjusters. Concrete local knowledge, not "we serve the area."

> **{{ATTORNEY}}**, you've been in front of these judges and across the table from these adjusters for **{{YEARS_PRACTICING}}** years.

**L3-F - The bench behind them.** The team, the experts, the medical network. Cyle flagged medical network as the attribute an answer engine surfaced first for a real client.

> **{{ATTORNEY}}**, your firm has the doctors and the specialists people need lined up before most of them have figured out who to call.

**L3-G - Why they do it.** CONDITIONAL, and only when the firm has actually told us. Warmest of the set and the easiest to fake, which is why it needs a real answer behind it.

> **{{ATTORNEY}}**, you started doing this work for a specific reason, and it still shows up in how your firm takes cases.

**L3-H - The recent result.** CONDITIONAL, and the most powerful frame in the set when it is available, because it is proof rather than description. Requires a real, recent, same-case-type outcome.

> **{{ATTORNEY}}**, your firm settled a case a lot like this one here last year for over {amount}.

Four conditions, all required:

- **Verified.** The amount, the date, and the case type come from the firm, not from a news story we half-remember and not from another episode's ROS.
- **Recent.** Inside about two years. "Back in 2019" is history; a result from last year is evidence the firm is still doing this.
- **Same case type as the episode.** A truck verdict does not credential a slip-and-fall episode. Mismatched results are the version of this that sounds like bragging.
- **Compliance-cleared by the firm.** Advertising a specific past result is regulated by the state bar, and most states expect a disclaimer that past results do not guarantee a future outcome. This template is marketing collateral for a law firm, so the firm's compliance position governs - if they have not cleared it, the frame is off.

**Awards are the weak version of this.** Reviews and awards rank BELOW verifiable bar standing in every attribute pull, and the pay-to-play directories are transparent enough that naming one can cost more credibility than it earns. If an award goes in, it needs real selection criteria behind it, and it never replaces a result or a number - at most it rides along in the same sentence. A case outcome is proof; a badge is a purchase.

### What each frame needs from the client profile

Every frame is a rendering of a field that already exists on the client record. This is the binding, and it is what makes the line generatable rather than written by hand:

| Frame | What it needs | Derivable from |
|---|---|---|
| L3-A Tenure | Years in practice | Years-of-experience field, or computed from the founding date |
| L3-B Volume | Cases per month, or lifetime count of this case type | Caseload / volume field; case-type breakdown |
| L3-C Trial record | Tries cases vs settles; trial count | Positioning / differentiators; trial-firm flag |
| L3-D Case type | The specific case types they actually take | Practice focus |
| L3-E Local system | Counties and courts they appear in | Service area / office locations |
| L3-F The bench | Team size, in-house specialists, medical network | Team, referral dynamics |
| L3-G Why they do it | The founding story | Positioning; Episode 1 Founder Story transcript |
| L3-H Recent result | Amount, date, case type, compliance clearance | Case results / notable outcomes; firm confirmation |

**Tenure is computed, not asked.** If the profile carries a founding date or an admission year rather than a years count, derive it at generation time so the number is right every year instead of frozen at whatever it was when someone typed it. A hardcoded "23 years" is wrong twelve months later, and these episodes rank for years.

**The exact column names are not confirmed yet.** The bindings above are stated as intent, not read off the live schema. As of 2026-08-17 the `caseengine` MCP at `contentgenapi.caseengine.com/mcp` rejects its configured token with HTTP 401, so the `client_profiles` table could not be read. Confirm each mapping against the live table before the first real run, and correct this table rather than working around it.

**This binding has to survive the move to the tool.** When this runs on tool.caseengine.com for the whole team, the profile lookup is a server-side query against Supabase, not an MCP call from somebody's laptop. The frames and the fields they need stay identical; only the transport changes. Write the mapping so it reads as "this frame needs this field," never as "call this tool."

### Verifying the credential before it ships

Every frame except A asserts something specific about a real firm, and the template is what an attorney reads on their own show. Resolve the fact, in this order, and never from memory:

1. **The CE database first.** Client profile data in Supabase, through the `mcp__caseengine__*` client tools - years in practice, practice areas, case types, office locations, team. This is canonical and it is the only source that is current by construction.
2. **The firm's own website second.** The attorney bio page, for anything the profile does not carry. Record the URL and the date it was read; bios go stale and nobody updates them when a number changes.
3. **Ask, third.** If neither resolves it, ask the producer outright - batched into one question with anything else that is missing, not one interruption per line.

**Every credential lands on a number or a range.** "Over 500 of these." "Fifteen to twenty years." "More than 40 trials." Never `countless`, `numerous`, `many`, `a lot of`, `hundreds upon hundreds`, or `years of experience` with no figure attached - those are what an unverified claim sounds like, and they read exactly as weak as they are. A vague credential is worse than a smaller true one: "over 200" beats "countless" every time, because one is checkable and the other is filler.

Round the same way as any other number - "over" rounds DOWN, and the figure ends in zeros. If the profile says 640 cases, "over 600" is right and "over 700" is a lie made by rounding.

**If it is still unresolved at generation time, switch frames.** L3-A tenure needs one number that the profile always has. Do not ship an unverified count with a hedge in front of it - get the number, or use the frame whose number you already have.

Record every asserted fact in `metadata.json` as claim, source, and date checked. A future run refreshing this episode inherits the provenance instead of re-guessing, and the same discipline applies to a firm claim as to a market statistic: **never carry a credential forward from a previous episode's ROS.** That is how one wrong number becomes twelve.

### Where the name goes

Cyle's improvised version put the name at the END of the clause: "...as an attorney for 23 years, John." That is how people actually talk. Front-loading it - "John, you've been..." - is how a script reads. Both are allowed; alternate them so neither becomes the tic.

### Rules

- **One frame per episode.** Never stack.
- **Rotate across the library.** Do not run the same frame on consecutive episodes of the same show. A-B-C-A-E reads like a person; A-A-A-A reads like a template.
- **Match the frame to the episode goal.** Differentiation takes C or D. Authority takes A or B. Conversion takes E or F. Narrative takes G.
- **Every credential is a claim about a real firm.** Years, case counts, trial record, and network all come from the client profile or intake, never from inference. "Hundreds of these" is a factual assertion; if nobody has confirmed it, use tenure.
- **Facts, not adjectives.** No "renowned," "top-rated," "award-winning," "premier." Reviews and awards rank BELOW verifiable bar standing in every attribute pull, so the adjectives are both weaker and less true.
- **Under 25 words, one sentence.**
- **Line 3 is where the city is allowed.** Line 2 speaks at the state level because the listener could be anywhere in it. Line 3 is about where the firm practices, so naming the base city is accurate rather than promotional: "you've been serving **{{CITY}}** and across **{{STATE}}** for **{{YEARS_PRACTICING}}** years." That is Cyle's original construction, and it is how the cities we already know still land in the long form.

**One city, maximum.** A firm with six offices names its base and lets `{{STATE}}` cover the rest. Two or more cities in a spoken sentence is a keyword list, and it is the exact impression the geo rule exists to prevent. If the firm has no single base, drop the city and say "here."

**Do not repeat the state.** It was in line 2. Say "here," or name the city, not `{{STATE}}` twice in three sentences.
- **It seeds the attribute block.** Whatever frame line 3 uses is the attribute the attorney will hit hardest in the answer, so pick the one this episode most needs established.

## The beat

After line 3, the attorney says hello. A sentence or two, unscripted, marked in the document as a direction rather than dialogue. It exists so the second voice arrives at 25 seconds instead of 40.

It is also the one part of S1 that is fair game to cut in post. S1 is otherwise edited light - ums out, pacing intact - so hosts need telling that a flat hello can go.

## Line 4 - the ask

> If someone was just in a wreck, walk us through the first steps after a crash, and the mistakes that sink a claim.

**One sentence. A conditional situation, then an imperative ask that carries the episode topic.** Then the host stops talking.

**This shape replaced the three-sentence form on 2026-08-21** (Gabe). The line has moved three times: a single compound question, then three sentences (situation / ask / story invitation), now one conditional sentence. Recording it once rather than as three change-log entries because it is one decision - the ask should sound like a person handing over the floor, carry the topic phrase, and stop.

### The two halves

| Half | Job | Shape |
|---|---|---|
| The setup | Put a person in a situation, conditionally | `If someone {situation},` - under 12 words, plain, no drama |
| The ask | Name what you want covered | Imperative, carries the episode topic in natural speech |

**The ask carries the episode topic.** This is the rule that matters most and the one most likely to drift. The ask is the retrieval anchor and it becomes the clip title, so the topic phrase has to survive into it more or less intact. Episode "How to File a Car Accident Claim in California" -> "walk us through how to file a car accident claim in California." Episode "What Your Car Accident Case Is Worth" -> "break down what a car accident case is worth and what goes into that number."

- **Never invent a beat that is not in the topic** to pad the ask out. A run once produced "how a car accident claim gets built" for an episode about first steps and mistakes - a third item that existed nowhere in the episode. That is the failure this rule exists to stop.
- **Never read the episode title verbatim either.** Line 2 already bans that and the same reason applies here: it has to sound spoken. Render the topic, do not recite it.
- **Natural first, then optimized, and short.** If the optimized phrasing will not come out of a mouth, the phrasing loses. If it comes out fine but runs long, cut it. One sentence is the ceiling.

**The ask is an instruction, not a question.** "Walk us through what they need to do" outperforms "what do they need to do" because it asks for a narration rather than an answer, and narration is what fills 15 to 30 minutes.

**But the verb is a judgment call, not a formula.** Match the verb to the shape of the topic:

| Topic shape | Verb that fits | Example |
|---|---|---|
| A process or sequence | Walk us through | "walk us through what they need to do." |
| A number or a range | Break down | "break down what a case is worth and what goes into that number." |
| A rule or a system | Explain | "explain how that actually works here." |
| A comparison | Lay out | "lay out the difference between the two." |
| A judgment call | Tell us | "tell us how you decide which way to go." |
| A misconception | Set us straight on | "set us straight on what people get wrong." |

A library where every episode's ask opens identically is the same drift the outro banks exist to prevent. Rotate the verb.

**No story invitation.** The line previously closed with "And if you have a real world example, please walk us through it." **Cut 2026-08-21 (Gabe).** If an episode needs a case example, the interviewer asks for one live as a follow-up beat; it does not live in the opening ask. Watch for answers running short as a result - if that shows up in recordings, the fix is interviewer coaching, not restoring the sentence.

### The six frames

The setup half rotates. Pick one frame per episode; the ask half is always the topic.

**L4-A - The aftermath.** Default. The listener is in it right now.

> If someone was just in a wreck, {ask}.

**L4-B - The decision.** The listener has not called anyone yet.

> If someone is trying to decide whether they even need a lawyer, {ask}.

**L4-C - The first week.** Narrow window, concrete actions.

> If someone is a few days out and still figuring it out, {ask}.

**L4-D - The mistake.** Pairs naturally with an attorney comfortable saying hard things.

> If someone has already done the thing everybody does wrong, {ask}.

**L4-E - The other side.** Positions the attorney against the adversary rather than the listener.

> If someone just got a call from the other side's adjuster, {ask}.

**L4-F - The spread.** For topics where outcomes vary wildly - value, sentencing, custody.

> If someone gets an offer and has no idea if it is fair, {ask}.


## Where this came from - the 2026-08-14 call

Gabe and Cyle, [Impromptu Zoom, 49 min](https://fathom.video/share/m6xLu2NKh6TBH3u3wQ41BPprdr5CS2ax). The whole format was decided here. These are the load-bearing quotes; they are kept verbatim because paraphrasing them is how the format drifts.

**The prompt shape, said out loud (16:13).** Cyle, improvising what the intro should sound like:

> "You've been serving the so-and-so and so-and-so cities as an attorney for 23 years, John. What do people actually need to know if they've gotten in a car accident? And what have you done in the past with past clients that have gotten a serious wreck in so-and-so cities? Tell us a little bit about that - the facts and what they need to know right this second. And then give us maybe an example or two of some cases you guys have worked on that they can relate to, and help them understand what kind of journey they're about to go through."

Gabe's reaction, immediately: "We should just clip that." That improvised paragraph IS lines 3 and 4. Note what it does that a written version would not: the attorney's name lands at the END of the credential clause, not the start. "...as an attorney for 23 years, John" is how a person talks. "John, you've been an attorney for 23 years" is how a script reads.

**Two intents, and only two (14:07).** Cyle on what the listener is actually doing:

> "They want to know if they should essentially hire them. Or they're trying to get a few facts, or they're trying to look for an attorney. It's one of the two. And if they're looking for facts, then they're trying to probably hire an attorney right after."

Line 2 must land on one of those two intents. Facts, or the hire decision. A line 2 that serves neither is decoration.

**The decision framing, verbatim (14:07).** Cyle: "What you should know, and what you need to do before you hire an attorney, for a car accident in California, or in so-and-so. You could even do the city. I like talking about the city." That is pattern F, and it is where the preference for naming the city in line 2 comes from.

**The most-asked question (14:07).** Cyle: "It's just a better prompt slash topic. And then you could be like, the most asked question is this." That is pattern G.

**Stop reading it verbatim (17:30).** Gabe, on the current failure:

> "We need to level up our interviewers a little bit as well, because they're just reading verbatim. The goal is to let them understand the premise of what we're after and let them freestyle a little bit. Put their personality in, make it sound more natural. But most of them aren't doing that."

This is why the introduction is a shape, not a script. The host reads line 1 as written and says the rest in their own words. If a recording sounds read, the fix is training, not tighter wording.

**Too wordy is a real failure (27:55).** Cyle on a generated episode topic: "Duty of Care and Proving Notice - I think this is a little wordy." He is reacting to five words. The tolerance here is much tighter than written English suggests, because every one of these lines is spoken.

**What the intro is FOR (41:14).** Gabe, summarizing:

> "A stronger intro, better lead-in and setup to establish authority, trust, expertise - and then a topic selection that's broad enough to just let them hit on it."

Authority in line 3, breadth in line 4. That sentence is the job description for both.

**Direct, not wordy (41:44).** Cyle: "Super direct to the point. The questions aren't too wordy, they're just enough. And then boom, the attorney hits it."

## The second call, same day - [78 min](https://fathom.video/share/jnP_jzjzsfyv5ubTr1mChQsCm4xr5nK4)

The working session where the intro got rebuilt line by line against the live prototype doc.

**The ask is three things (6:01).** Cyle, spelling out what the prompt has to get:

> "For somebody watching, if they were in a car accident in the Fresno or Central Valley area - what are the things that they need to know right now? And tell us a little bit about why they should listen to you. And we'll follow that up with a real example. It's three things. It's tell us what to do, tell us why we should listen to you, and tell us an example or two. And then they just shut up."

Two of those are asked in line 4. The third - why we should listen to you - is what line 3 already established, which is why line 4 does not ask for credentials again. Three things get covered; only two get asked.

**The stakes clause ends line 2 (24:48).** Cyle, editing the draft live: "Everything after 'if it happens to you' - delete." Line 2 stops at the stakes clause. No extra qualifier, no second thought, no bridge sentence into line 3.

**Cut the qualifier (56:59).** Reading his own version aloud, Cyle stopped mid-sentence on "who was just in a serious wreck": "I would maybe take out 'serious'." A qualifier narrows who the episode is for. The listener decides whether theirs was serious.

**Two in the morning, rejected (20:41).** Cyle, on the AI's line: "Two in the morning - I don't know if anybody, nobody's searching it two in the morning." This is why pattern C is conditional and why it names a moment rather than a search.

**Interviewer, not host (10:30).** Cyle: "It should say co-host, not host. They're not the host. The attorney is the host. We have different co-hosts all the time." Gabe: "It should be interviewer and attorney. That way it's very clear." That is the origin of both the speaker tags and the `{{INTERVIEWER}}` token.

**Not "today we're talking about practice area" (11:08).** Cyle's objection to the stock line is the reason line 2 has a pattern set at all, and the reason the cover and line 2 use `{{TOPIC}}` rather than `{{PRACTICE_AREA}}`.

**Alias the jargon in line 2 (56:59).** Cyle's read-aloud version: "premises liability, or so-called slip and fall, in the Central Valley of California." When the practice area only has a legal name, say it once and immediately give the plain-language alias. Never the legal name alone.

**Filler is the AI tell (9:15).** Gabe on the attribute block: "'Strongest signal, four out of four sources' - I just need to remove that. That's just filler." Cyle: "AI just goes heavy on the filler." Applies to the whole document, but it starts here: an intro sentence that explains why the intro is structured that way is filler.

## Do not

- **Do not re-greet.** Line 1 is the greeting. Line 2 opening with "welcome" or "hey everyone" greets twice.
- **Do not say "special topic."** It promises significance instead of demonstrating it, and it sounds like a host stalling.
- **Do not read the episode title.** The title is written for search. Line 2 is written for a mouth.
- **Do not name the practice area as a category.** "Premises liability" is what a lawyer calls it. "Getting hurt somewhere that should have been safe" is what happened.
- **Do not stack credentials.** One fact beats three. No awards, no "renowned," no "top-rated."
- **Do not frame the attorney as a guest.** It is their show. See `references/editorial-rules.md`.
- **Do not enumerate in line 4.** Three questions is an interrogation, which is the format v2 exists to replace.
- **Do not inflate stakes.** "Before you lose everything" is a fear pitch. "If it happens to you" is a fact.

## Gates

- **IN-1** Exactly four lines plus the beat direction, in order.
- **IN-2** Line 1 renders byte-identical to the constant in `references/statics.json`.
- **IN-3** Line 2 matches one of the approved patterns and carries `{{STATE}}`.
- **IN-4** Any number in line 2 traces to a source recorded in metadata. No source means pattern A.
- **IN-5** Line 3 carries exactly one credential frame.
- **IN-6** Line 4 is THREE short sentences in order: situation, ask, conditional story invitation. At most two asks. It does NOT have to end in a question mark - the story invitation is an invitation, not a question, and ending on one is correct. A single compound question FAILS.
- **IN-7** Zero guest framing, zero legal jargon, zero em dashes.
- **IN-8** Word count 80-110. Read it aloud before accepting it.
