"""v3 - rebuilt from the 08-14 Gabe/Cyle call.
Single prompt, authority lead-in, three-move answer, attributes over jargon,
Segment 2 as 60-second search-phrase questions."""
from topics2 import TOPICS

# The seven attributes AI Mode surfaced as what searchers actually want (call 45:11).
# Plain language, no jargon. This replaces the statute-heavy "runway" from v2.
ATTRIBUTES = [
 ("Trial willingness", "Have you taken these to trial, or do you only settle? If you are a trial firm, say so early and say it plainly."),
 ("Specific case-type experience", "Not the practice area, the case type. How many of THIS kind, not how many injury cases. How recently."),
 ("Fee and expenses in detail", "Percentage, whether it rises if you file suit, who pays records, filing fees, investigators, experts and court reporters, and what happens if you lose."),
 ("Local court familiarity", "The county court, the judges, how the local defense firms operate. Specifics, not \"we serve the area\"."),
 ("Evidence preservation speed", "What you secure in the first days and how fast, before it is deleted or overwritten."),
 ("Expert network", "Name the roles you bring in - reconstructionists, safety engineers, code inspectors, medical specialists, economists."),
 ("Who actually handles the case", "Am I hiring you, or an intake operation that refers this out? Who do I talk to day to day and how often."),
 ("Honest assessment", "Name what would make the case difficult. Saying the hard part builds more trust than a promise."),
 ("Verifiable standing", "Bar license and disciplinary history. This ranks above reviews and awards."),
 ("Deadlines", "Say the number of years and what happens if it passes."),
]

V3 = {
"Inland Empire (CA)": {
 "theme": "car accidents",
 "cities": "Riverside and San Bernardino",
 "victims": "car accident victims",
 "situation": "was just in a serious wreck",
 "topic_phrase": "**{{PRACTICE_AREA}}** in **{{LOCATION}}**, and what you actually need to know if it happens to you",
 "cold_open": "If you got hurt in a wreck out here, you probably have two questions and no straight answers. Is this worth anything, and who do I actually trust with it.",
 "lead_in": [
  "Today we are talking about car accidents across the Inland Empire, and what you actually need to know if it happens to you.",
  "**{{ATTORNEY_NAME}}** of **{{FIRM_NAME}}**. They have been doing this here for **{{YEARS_PRACTICING}}** years, and they have handled a lot of these cases for people in **{{LOCATION}}** and the surrounding cities.",
 ],
 "prompt": "You have been serving **{{LOCATION}}** and the surrounding cities as an attorney for **{{YEARS_PRACTICING}}** years. What do people actually need to know if they have been in a car accident out here? And what have you done in the past for clients who were in a serious wreck? Tell us the facts, what they need to do right this second, and then give us an example or two of cases your firm has worked on so people can understand the kind of journey they are about to go through.",
 "need_to_know": [
  "What to do in the first hours, in plain terms",
  "Get checked out even if you feel fine, and why the gap between the crash and the doctor hurts you later",
  "What not to say to the other side's adjuster, and why the first offer is not the real offer",
  "Being partly at fault does not end your case in California",
  "The one deadline that ends everything if you miss it",
 ],
 "examples": "One or two real matters. No names. What came in the door, what the other side said it was worth, what actually happened. The city is the detail that makes it land.",
},
"Truck Accidents (GA)": {
 "theme": "truck accidents",
 "cities": "Savannah and the surrounding areas",
 "victims": "truck accident victims",
 "situation": "was just hit by an eighteen-wheeler",
 "topic_phrase": "**{{PRACTICE_AREA}}** in **{{LOCATION}}**, and what happens when a commercial truck hits you",
 "cold_open": "Getting hit by an eighteen-wheeler is not a bigger version of a car wreck. It is a completely different situation, and the trucking company knows that before you do.",
 "lead_in": [
  "Today we are talking about what happens when a commercial truck hits you in the Savannah area, and why almost nothing about it works the way people expect.",
  "I am here with **{{ATTORNEY_NAME}}** from **{{FIRM_NAME}}**, who has been handling these cases here for **{{YEARS_PRACTICING}}** years.",
 ],
 "prompt": "You have been serving **{{LOCATION}}** and the surrounding cities as an attorney for **{{YEARS_PRACTICING}}** years. What do people actually need to know if they have been hit by a commercial truck out here? And what have you done in the past for clients who were in a serious truck wreck? Give us the facts, what they need to do right this second, and then walk us through an example or two of cases your firm has handled so people understand the journey they are about to go through.",
 "need_to_know": [
  "The trucking company has people working on this within hours. You do not.",
  "The evidence that proves your case gets erased on a schedule unless somebody stops it",
  "It is almost never just the driver who is responsible",
  "Trucking companies follow federal rules that regular drivers do not, and breaking one helps your case",
  "Why these cases are worth more and also harder, and what that means for who you hire",
 ],
 "examples": "One or two real matters. What the company did in the first week, what the evidence showed, how it ended. Name the road or the corridor if it helps people picture it.",
},
"Birth Injury (MD)": {
 "theme": "birth injuries",
 "cities": "Baltimore and the surrounding counties",
 "victims": "families after a birth injury",
 "situation": "just got a diagnosis and cannot get anyone to tell them why",
 "topic_phrase": "**{{PRACTICE_AREA}}** in **{{LOCATION}}**, and what a family can actually do when nobody will tell them why",
 "cold_open": "There is a question parents in this situation ask months after the diagnosis, usually late at night. Could this have been prevented. It has an honest answer, but nobody at the hospital is going to give it to you.",
 "lead_in": [
  "Today we are talking about birth injuries, cerebral palsy, and what a family can actually do when they are told a diagnosis but never told why.",
  "I am joined by **{{ATTORNEY_NAME}}** from **{{FIRM_NAME}}**, who has represented families here for **{{YEARS_PRACTICING}}** years.",
  "Fair warning that this one is heavier than most of our episodes, and we are going to take it slowly.",
 ],
 "prompt": "You have been serving families in **{{LOCATION}}** and the surrounding areas for **{{YEARS_PRACTICING}}** years. What does a parent actually need to know when their child has been diagnosed and nobody will tell them why it happened? And what have you done in the past for families in this situation? Give us the facts, what they need to do right now, and then tell us about a case or two your firm has handled so families understand what the road ahead actually looks like.",
 "need_to_know": [
  "A diagnosis tells you what is happening, not why it happened",
  "Not every one of these is somebody's fault, and that is part of an honest answer",
  "The records that hold the answer, and that the hospital has to give you",
  "Why a case can take years to surface and still be on time under Maryland's rule for children",
  "What a lifetime of care actually costs, because most families badly underestimate it",
 ],
 "examples": "One or two real matters, handled gently. What the family was told at the time, what the record showed later, what changed for them. No names, no identifying detail.",
},
"Medical Malpractice (FL)": {
 "theme": "hospital and medical negligence",
 "cities": "Boca Raton and Palm Beach County",
 "victims": "patients and families harmed in a hospital",
 "situation": "thinks a hospital hurt someone they love",
 "topic_phrase": "**{{PRACTICE_AREA}}** in **{{LOCATION}}**, and what happens when a hospital hurts someone in your family",
 "cold_open": "When a hospital hurts someone, almost every family walks in wanting to sue the doctor. And very often the doctor does not even work for the hospital you were standing in.",
 "lead_in": [
  "Today we are talking about what actually happens when a hospital harms someone in your family, and why the obvious answer about who is responsible is usually the wrong one.",
  "**{{ATTORNEY_NAME}}** of **{{FIRM_NAME}}**, who has been taking on hospitals here for **{{YEARS_PRACTICING}}** years.",
 ],
 "prompt": "You have been serving **{{LOCATION}}** and the surrounding areas as an attorney for **{{YEARS_PRACTICING}}** years. What do people actually need to know if they think a hospital or a doctor hurt someone in their family? And what have you done in the past for clients in that situation? Give us the facts, what they need to do right this second, and then share an example or two of cases your firm has handled so people understand what they are getting into.",
 "need_to_know": [
  "A bad outcome is not automatically a case, and the difference is the whole conversation",
  "The ER doctor who treated you probably does not work for the hospital, and why that matters",
  "Get the complete records, including the nursing notes, and do it early",
  "Do not sign anything the hospital sends you",
  "Florida makes you do a lot of work before you are even allowed to file, so the clock matters more than people think",
 ],
 "examples": "One or two real matters. What the family was told happened, what the chart actually showed, who ended up responsible. No names.",
},
"Brain Injury (TX)": {
 "theme": "brain injuries",
 "cities": "Fort Worth and Tarrant County",
 "victims": "brain injury victims",
 "situation": "hit their head in a wreck and has not felt right since",
 "topic_phrase": "**{{PRACTICE_AREA}}** in **{{LOCATION}}**, and why they are so hard to prove",
 "cold_open": "A broken bone proves itself. You hold up the X-ray and the argument is over. A brain injury has to be proven again and again to people who are looking for a reason not to believe you.",
 "lead_in": [
  "Today we are talking about brain injuries after an accident, and why these are some of the hardest cases to prove even when the harm is obvious to everyone who loves you.",
  "I am here with **{{ATTORNEY_NAME}}** from **{{FIRM_NAME}}**, who has handled these cases here for **{{YEARS_PRACTICING}}** years.",
 ],
 "prompt": "You have been serving **{{LOCATION}}** and Tarrant County as an attorney for **{{YEARS_PRACTICING}}** years. What do people actually need to know if they hit their head in a wreck and have not felt right since? And what have you done in the past for clients with a serious brain injury? Give us the facts, what they need to do right now, and then walk us through an example or two of cases your firm has handled so people understand the journey ahead.",
 "need_to_know": [
  "The person hurt is usually the last one to notice. The family sees it first.",
  "A normal scan at the hospital does not mean nothing is wrong",
  "The testing that actually documents it, and why doing it early matters so much",
  "Every gap in treatment gets used against you",
  "Do not settle before anyone knows how far you are going to recover, because there is no going back",
 ],
 "examples": "One or two real matters. What the client and the family noticed, what the testing showed, what it took to make the other side believe it.",
},
"Slip and Fall (CA)": {
 "theme": "slip and fall and premises cases",
 "cities": "San Diego",
 "victims": "people hurt on someone else's property",
 "situation": "was just badly hurt in a fall",
 "topic_phrase": "**{{PRACTICE_AREA}}** in **{{LOCATION}}**, and what actually happens when you fall on someone else's property",
 "cold_open": "Slip and fall has a reputation, and most of that reputation is wrong. Falling on someone's property is not the case. Proving they should have fixed it is the case.",
 "lead_in": [
  "Today we are talking about what actually happens when you fall on someone else's property in San Diego, including the cases that go nowhere and why.",
  "**{{ATTORNEY_NAME}}** of **{{FIRM_NAME}}**, who has handled these cases here for **{{YEARS_PRACTICING}}** years.",
 ],
 "prompt": "You have been serving **{{LOCATION}}** as an attorney for **{{YEARS_PRACTICING}}** years. What do people actually need to know if they have fallen and gotten hurt on someone else's property out here? And what have you done in the past for clients who were seriously injured in a fall? Give us the facts, what they need to do right this second, and then give us an example or two of cases your firm has worked on so people understand what the process actually looks like.",
 "need_to_know": [
  "Falling is not the case. Proving they knew, or should have, is the case.",
  "Report it before you leave and get a copy of whatever they write down",
  "The video that proves it gets recorded over fast, often within days",
  "They will say you should have been watching. In California that reduces your case, it does not end it.",
  "Photograph the condition that day, because it gets fixed the next day",
 ],
 "examples": "One or two real matters. What the store said at first, what the footage or the logs actually showed, how it ended. Include one you turned down and why.",
},
}

# ---- Segment 2: 60-second search-phrase questions ----
# Shape from the call: 2-3 top-keyword questions that MUST carry the city,
# 4 attribute questions, and 3-4 element questions phrased the way people search.

PA = {"Inland Empire (CA)": ("car accident", "California"),
      "Truck Accidents (GA)": ("truck accident", "Georgia"),
      "Birth Injury (MD)": ("birth injury", "Maryland"),
      "Medical Malpractice (FL)": ("medical malpractice", "Florida"),
      "Brain Injury (TX)": ("brain injury", "Texas"),
      "Slip and Fall (CA)": ("slip and fall", "California")}

# topic-specific tails, 4 each, phrased as searches not jargon
TAILS = {
"Inland Empire (CA)": [
 ("What should you do in the first 24 hours after a car accident?", "Ordered steps. Nothing legal-sounding."),
 ("What happens if the other driver has no insurance?", "Your own coverage. Check every policy in the household."),
 ("What happens if you were partly at fault for the crash?", "You still recover, reduced by your share. Give a concrete number."),
 ("Why is the first settlement offer always low, and what should you do?", "Anchoring. Do not accept and do not give a recorded statement."),
],
"Truck Accidents (GA)": [
 ("What should you do in the first 48 hours after getting hit by a truck?", "The company is already working. Say what that means for them."),
 ("Who is responsible when a commercial truck causes a wreck?", "Almost never just the driver. Name the others in plain words."),
 ("What evidence disappears after a truck accident, and how fast?", "The black box and the logs. Days, not weeks."),
 ("Why are truck accident cases worth more than car accident cases?", "Bigger coverage, worse injuries, a company on the other side."),
],
"Birth Injury (MD)": [
 ("What should a parent do first if they think something went wrong at delivery?", "Request the records. Gently, concretely."),
 ("What records should a family ask the hospital for?", "The delivery record, the monitoring strips, the placental pathology report."),
 ("How do you know if a birth injury could have been prevented?", "Honest answer. Sometimes it could not. Say so."),
 ("How long does a family have to bring a birth injury claim in Maryland?", "The rule for children is different. Say the number."),
],
"Medical Malpractice (FL)": [
 ("What is the difference between a bad outcome and actual malpractice?", "The whole conversation lives here. Plain language."),
 ("Who is responsible when an ER doctor makes a mistake?", "Often not the hospital's employee. Explain why it still matters."),
 ("What records should you request after a hospital injury?", "Everything, including nursing notes and timestamps. Early."),
 ("Should you sign anything the hospital sends you?", "No. Say why in one sentence."),
],
"Brain Injury (TX)": [
 ("What are the signs of a brain injury after a car accident?", "The family notices first. List what they notice."),
 ("What if the scan at the hospital came back normal?", "Normal imaging does not mean nothing is wrong."),
 ("How do you prove a brain injury that does not show up on a scan?", "The testing that documents it, in plain words."),
 ("Why should you not settle a brain injury case early?", "Nobody knows how far you recover yet. No going back."),
],
"Slip and Fall (CA)": [
 ("What should you do immediately after falling in a store?", "Report it, get a copy, photograph it, get treated."),
 ("How do you prove a store knew about the hazard?", "How long it sat there. The sweep logs. Plain language."),
 ("How long does a store keep the video of your fall?", "Days. Say why that is the single most urgent thing."),
 ("What if they say you should have been watching where you were going?", "Reduces your case, does not end it. Give a number."),
],
}

def s2_for(tab, city):
    pa, state = PA[tab]
    core = [
     (f"What should you look for before hiring a {pa} lawyer in {city}?", "top-keyword", "Name the city in the first sentence. Answer as a checklist someone could use."),
     (f"What does a {pa} lawyer in {city} actually do for you?", "top-keyword", "Concrete actions, not concepts."),
     (f"What is a {pa} case in {city} actually worth?", "top-keyword", "Honest range and what moves it. Do not dodge."),
     (f"How much does it cost to hire a {pa} attorney?", "attribute: financial risk", "No fee unless you win. Who fronts costs. Say it plainly."),
     (f"Do you have attorneys who focus specifically on {pa} cases?", "attribute: case experience", "Yes, then prove the depth. Volume, years, a recent result if you can say it."),
     (f"Do you handle cases in {city} specifically?", "attribute: local presence", "Prove it with the courts, hospitals and roads you actually know."),
     ("How fast will someone actually talk to an attorney at your firm?", "attribute: accessibility", "Attorney or case manager. Give a real response time."),
     ("What do your clients say about working with your firm?", "attribute: reputation", "Reviews, results, where someone can verify it."),
     (f"How long do you have to file a {pa} claim in {state}?", "attribute: deadlines", "Say the number. Say what happens if you miss it."),
    ]
    return core + [(q, "search-phrase", n) for q, n in TAILS[tab]]


# ---- Geo pairing (Cyle, 08-14): pair the city with its region instead of
# repeating the city. Region is fixed by the template's location scope, so it is
# static text, NOT a new placeholder.
REGION = {
 "Inland Empire (CA)":      ("Riverside", "the Inland Empire"),
 "Truck Accidents (GA)":    ("Savannah", "Chatham County and coastal Georgia"),
 "Birth Injury (MD)":       ("Baltimore", "the Baltimore metro and central Maryland"),
 "Medical Malpractice (FL)":("Boca Raton", "Palm Beach County and South Florida"),
 "Brain Injury (TX)":       ("Fort Worth", "Tarrant County and North Texas"),
 "Slip and Fall (CA)":      ("San Diego", "San Diego County and Southern California"),
}

def geo_plan(tab, city):
    """Per-question geo treatment: city / region / both / neutral."""
    _, region = REGION[tab]
    return region

def s2_v4(tab, city="{{LOCATION}}"):
    """Segment 2 with city+region pairing instead of city repetition."""
    pa, _state = PA[tab]
    state = "{{STATE}}"
    region = "{{REGION}}"
    core = [
     (f"What should you look for before hiring a {pa} lawyer in {city}?",
      "top-keyword | CITY", "Say the city in the first sentence. This one is a ranking target - do not swap in the region."),
     (f"What does a {pa} lawyer in {city} actually do for you?",
      "top-keyword | CITY", "City in the first sentence. Concrete actions, not concepts."),
     (f"What is a {pa} case actually worth around here?",
      "top-keyword | CITY + REGION", f"Open with the pairing: \"in {city} and across {region}...\" Honest range and what moves it."),
     (f"How much does it cost to hire a {pa} attorney?",
      "attribute: cost + expenses | NEUTRAL", "Percentage, whether it rises at litigation, who pays experts and filing fees, what happens if you lose."),
     (f"Have you taken {pa} cases to trial, or do you settle them?",
      "attribute: trial willingness | REGION", f"Answer for {region}. This is the single strongest attribute in the AI answers - lead the block with conviction."),
     (f"Who will actually handle my case day to day?",
      "attribute: who handles it | NEUTRAL", "Name the role. Are you hiring this attorney or an intake operation that refers it out."),
     (f"Do you handle {pa} cases across {region}, or only in {city}?",
      "attribute: local presence | CITY + REGION", "The pairing question. Courts, hospitals and roads you actually know, in both."),
     (f"What experts do you bring into a {pa} case?",
      "attribute: expert network | NEUTRAL", "Reconstructionists, safety engineers, code inspectors, economists. Named roles."),
     (f"How long do you have to file a {pa} claim in {state}?",
      "attribute: deadlines | STATE", "Say the number. Say what happens if you miss it."),
     ("What would make my case difficult?",
      "attribute: honest assessment | NEUTRAL", "Name real weaknesses. AI answers flag guaranteed numbers as a red flag - this is the differentiator."),
    ]
    # Hard cap of 10 per location set. Core carries the 3 CITY ranking targets plus the
    # attribute coverage; one topic question rides along. The rest of TAILS stays in the
    # appendix pull pool for per-location customization.
    return (core + [(q, "search-phrase | NEUTRAL", n) for q, n in TAILS[tab]])[:10]


# ---- STATIC BOILERPLATE ----------------------------------------------------
# Identical on every episode, every client, every scope. Never regenerated.
# These belong in the skill's JSON template, not in per-run generation.
STATIC = {
 "after_prompt":   "Then stop talking. Do not narrow it or offer an example to start them. The silence is the format.",
 "answer_header":  "[Attorney Response - 15 to 30 minutes]",
 "answer_intro":   "Three moves, in this order. A shape, not a script.",
 "move_1":         "**Proof, about a minute.** How long you have been doing this here, how many of these cases, your results. For a new listener this is the only introduction they get.",
 "move_2":         "**What they need to know right now.** The facts and the actions, direct. This is what someone in trouble is listening for.",
 "attr_intro":     "What people are actually trying to find out before they call anyone. Hit these anywhere in your answer, in your own words, in any order.",
 "attr_note_internal": "Two findings worth knowing. Reviews and awards rank BELOW verifiable bar standing. Naming what makes a case difficult reads as a positive signal, while guaranteeing a number is treated as a red flag.",
 "attr_sources_internal": "Source consistency, from live Google AI Overview and ChatGPT pulls on 08-14 across two practice areas and two markets. Ordering above follows this ranking.",
 "shortform_mode": "Mode switch, and say it on mic. Each answer is a standalone 60 seconds that restates the question. Higher energy than Segment 1, and no callbacks to the interview. Retakes are expected - if one comes out flat, go again.",
 "prompt_template": "**{{ATTORNEY}}**, you've been representing [VICTIMS] in **{{LOCATION}}** for **{{YEARS_PRACTICING}}** years. For someone listening right now who [SITUATION], what do they need to know next, and can you walk us through a real case that shows what the road ahead actually looks like?",
 "welcome":        "Welcome back to **{{PODCAST_NAME}}** with **{{ATTORNEY_NAME}}**. I'm **{{INTERVIEWER}}**, and today we are talking about {topic_phrase}.",
 "handoff":        "Then turn it over and let them run.",
 "outro_note":     "Keep it short. Thank the guest, plug the firm once, sign off. Do not recap the episode.",
 "outro_thanks":   "**{{ATTORNEY}}**, thank you for your time. This was genuinely useful.",
 "outro_plug":     "If you were hurt and you want someone to actually look at your case, reach **{{FIRM_NAME}}** at **{{PHONE_NUMBER}}**, or online at **{{WEBSITE}}**.",
 "outro_signoff":  "That is it for this one. **{{PODCAST_NAME}}**, produced by Case Engine. We will see you next episode.",
 "shortform_sets": "Ten questions per set, one set per location. Multi-location firms record additional sets back to back and each set gets customized to its city.",
}


# Cross-source consistency behind the ATTRIBUTES ordering. INTERNAL ONLY -
# never rendered in the attorney-facing Attributes section.
ATTR_SOURCES = [
 ("Trial willingness", "4 of 4, usually the first sentence"),
 ("Specific case-type experience", "4 of 4"),
 ("Fee and expenses in detail", "4 of 4"),
 ("Local court familiarity", "4 of 4"),
 ("Evidence preservation speed", "4 of 4"),
 ("Expert network", "4 of 4"),
 ("Who actually handles the case", "3 of 4"),
 ("Honest assessment", "2 of 4, high signal"),
 ("Verifiable standing", "1 of 4, explicitly ranked above reviews"),
 ("Deadlines", "1 of 4, state-specific"),
]


# Alternate introductions, each built on a different thing Cyle said on the
# 08-14 call. Fully tokenized and topic-agnostic so any episode can swap one in.
ALT_INTROS = [
 ("v3 - Before you hire an attorney",
  "Welcome back to **{{PODCAST_NAME}}** with **{{ATTORNEY_NAME}}**. I'm **{{INTERVIEWER}}**. Today is what you should know, and what you need to do, before you hire an attorney for **{{PRACTICE_AREA}}** in **{{LOCATION}}**. Most people making this call have never made it before, and they are making it during the worst week of their year.")
]
