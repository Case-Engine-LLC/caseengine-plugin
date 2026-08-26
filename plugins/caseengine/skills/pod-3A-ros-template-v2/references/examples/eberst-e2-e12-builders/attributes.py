#!/usr/bin/env python3
"""The ATTORNEY RESPONSE block, written per episode - labels and detail both.

The catalog in references/attributes/attributes-fallback.json is topic-invariant.
The TRANSFORM is not. attributes.md says the unit of this block is "what the attorney
covers when answering", and what an attorney covers on a fatal truck case is not what
they cover on a crosswalk case.

Rewritten 2026-08-18 after nine of the twelve bold lead-ins turned out to be identical
across every episode. The lead-in is the only bold text in the block, so identical
labels made eleven different documents scan as one document, even though the detail
sentences underneath already differed. Labels are now episode-specific too.

Each entry keeps its catalog trace in CATALOG_TRACE below for AT-3.

Gates per block: 12 bullets (AT-2), zero question marks (AT-1), credentials through
logistics (AT-4), a bar-standing bullet present (AT-7), a name-the-hard-part bullet
last (AT-7), no superlatives or marketing language (AT-6).
"""

def _b(*pairs):
    return [{"name": n, "detail": d} for n, d in pairs]

# label -> catalog row it derives from, for AT-3. `fee` is the documented exception.
CATALOG_TRACE = {
 "trial": "Trial willingness", "casetype": "Specific case-type experience",
 "standing": "Verifiable bar standing", "court": "Local court familiarity",
 "evidence": "Evidence preservation speed", "experts": "Expert network",
 "whohandles": "Who actually handles the case day to day", "deadlines": "Deadlines",
 "fee": "Fee and expenses in detail (documented exception)", "honest": "Honest assessment",
 "episode": "episode-specific, derived from the episode's own n-gram substance",
}

ATTRIBUTES = {
 3: _b(
  ("Cases you took to trial", "A case like this one you actually put in front of a jury, and what that jury did with an injury the insurer had written off as minor."),
  ("This injury, not injuries", "Not injury cases generally. This crash type and this injury, how many, and how recently."),
  ("Credentials anyone can check", "Your license and your disciplinary history. Anyone can look both up, and they say more than any star rating does."),
  ("What juries here award", "The county court, the judges, and what a local jury has actually done with an injury like this one."),
  ("Getting to a number", "How you move from a stack of bills to a figure, and which injuries move that figure the most."),
  ("Waiting for the medical picture", "Why you do not put a number on it until the treatment has shown what the person is left with."),
  ("Who you bring in", "The treating doctors, the life-care planners, and the experts who put a dollar figure on the work somebody can no longer do."),
  ("The first week", "What you lock down before the cars get repaired, because the vehicles and the road are what tell us how the crash happened."),
  ("The two clocks", "The two-week medical window and the filing deadline, said as numbers, and which one people miss most."),
  ("What this costs you", "The percentage, whether it rises if you file suit, who fronts the imaging and the experts, and what happens if you lose."),
  ("Who you actually talk to", "Whether the client is hiring you or an intake operation, and who calls them when the offer arrives."),
  ("The hard part", "Which of these injuries is genuinely difficult to prove, and say it out loud before the client has to ask.")),

 4: _b(
  ("Cases you have tried", "The ones you took to a jury instead of settling, and what changes once an adjuster expects that of you."),
  ("Reports you have broken", "Not injury cases generally. Crashes where the report was wrong or thin, how many, and how recently."),
  ("Bar standing", "Your license and disciplinary history. Anyone can look it up with the Bar, which is more than you can say for a review site."),
  ("How a report plays here", "The county court, the judges, and which local defense firms fight a report and which accept it."),
  ("Reading the report", "What you look for in a crash report that the person it happened to would read straight past."),
  ("Prying records loose", "How you actually obtain body camera footage and a supplement, and how long each one really takes."),
  ("The short loop", "What goes out in the first days, because the systems record over the old footage and nobody is holding it for you."),
  ("Your bench", "Reconstructionists, treating physicians, and the people who chase an agency until the file arrives."),
  ("Both deadlines", "The two-week medical window and the filing deadline, and then the fact that the video is usually gone long before either one."),
  ("Your fee, in full", "The percentage, whether it rises if you file suit, who pays for records and footage requests, and what happens if you lose."),
  ("Who answers the phone", "Whether the client is hiring you or an intake operation, and who chases the agency for the records."),
  ("What makes it harder", "What a bad report actually does to a case, and when you tell a client plainly that theirs is a harder one.")),

 5: _b(
  ("Death cases tried", "Fatal cases you actually took to a jury, and what that changes when the trucking company's insurer decides how seriously to take you."),
  ("Fatal truck crashes", "Not injury cases generally. Deaths caused by commercial vehicles, how many, and how recently."),
  ("License and record", "Your license and disciplinary history, which a family can verify themselves in about a minute."),
  ("This court, this jury", "The county court, the probate side of it, and how a local jury hears a death case."),
  ("Moving in the first week", "What you get done in the days while the carrier's own people are still working the scene."),
  ("Reading truck data", "The people who pull what the truck recorded and turn it into something a jury understands."),
  ("The preservation letter", "What goes out immediately to stop the truck data and the driver file from cycling out."),
  ("Finding every policy", "How you find every policy stacked behind a commercial truck, not just the one the company hands over first."),
  ("Carrying it for the family", "What you take off the family's plate so nobody is making legal decisions in the worst week of their life."),
  ("The deadline that ends it", "Say the filing deadline out loud as an actual number of years, and give the much shorter one if a government vehicle was involved."),
  ("How you get paid", "The percentage, whether it rises if you file suit, who funds an investigation this size, and what happens if you lose."),
  ("What could go wrong", "What would make this case difficult, including when the person who died was partly at fault.")),

 6: _b(
  ("Cases you took to trial", "The ones you put in front of a jury instead of settling, and how the insurers stacked above the first one behave once they believe you will do it again."),
  ("Business vehicle crashes", "Not injury cases generally. Crashes caused by a commercial vehicle, how many, and how recently."),
  ("Credentials anyone can verify", "Your license and your disciplinary record, which matter more than any directory badge."),
  ("Who the carriers hire here", "The county court, the judges, and the defense firms the insurers around here actually retain."),
  ("Finding every policy", "How you get to the coverage nobody volunteers, including the layers stacked above the first one."),
  ("Reading the front page of the policy", "The one-page summary that lists the limits, and what on it decides whether a second and third policy can be reached at all."),
  ("Getting the limits in writing", "How you make an insurer state its number on paper, and why a number somebody gives you over the phone is worth nothing."),
  ("Putting a number on the future", "The experts who figure out what a lifetime of care actually costs, because that total is what you hold the insurance layers up against."),
  ("Evidence that gets erased", "What you lock down in the first days, before the vehicle data and the company records are overwritten."),
  ("Three separate clocks", "The medical window, the filing deadline, and the much shorter one if a public vehicle was involved."),
  ("Fees and who pays the costs", "What the percentage is, whether it goes up if you file suit, who fronts the cost of chasing every policy, and what happens if you lose."),
  ("When the money is not there", "How you tell somebody the coverage does not exist, and why you say it in the first conversation instead of the tenth.")),

 7: _b(
  ("Tried a drunk driving case", "Cases you took to a jury, and what a jury does once it hears the driver had been drinking."),
  ("Impaired driver crashes", "Not injury cases generally. Crashes caused by a drinking driver, how many, and how recently."),
  ("License, checkable", "Your license and disciplinary record, and where anyone can go to confirm it."),
  ("Two cases, one client", "The county court, the judges, and how the prosecution and your client's claim run alongside each other here."),
  ("Running beside the prosecution", "How you use what the state develops without letting your client's claim wait on it."),
  ("Proving impairment", "Everything you stack on top of the test result, because a defense lawyer will go after that number by itself."),
  ("Records behind the test", "What you secure in the first days, including the maintenance and calibration files sitting behind any reading."),
  ("Toxicology and reconstruction", "The people who explain what the driver's condition actually meant at the moment of impact."),
  ("Finding coverage", "How you get to every policy that could pay when the driver carries little or nothing."),
  ("Clocks that do not wait", "The two-week medical window and the filing deadline, and why neither one pauses for the criminal case."),
  ("What it costs", "The percentage, whether it rises if you file suit, who pays for the toxicology work, and what happens if you lose."),
  ("Why the bar claim fails", "Why a claim against the place that served the driver almost never works here, and why you tell people that up front.")),

 8: _b(
  ("Tried a failure to yield", "Cases you took to a jury, and what they did with a driver who simply did not give way."),
  ("People struck crossing", "Not injury cases generally. People hit while on foot, how many, and how recently."),
  ("Your record beats a rating", "Your license and your disciplinary history are public, and anyone can look them up. A review score is not."),
  ("How a jury here hears it", "The county court, the judges, and what a local jury assumes about somebody who was walking."),
  ("Knowing the crossings", "The corridors and intersections where this keeps happening, and what is actually wrong with them."),
  ("Storefront footage", "What you secure in the first days, because video from a shop facing the crossing is gone inside a month."),
  ("Reading the road", "Crash reconstruction experts, the treating doctors, and engineers who can explain what was wrong with the crossing itself."),
  ("Coverage with no car", "How somebody who does not own a vehicle may still have coverage, and which policy pays first."),
  ("The two deadlines", "The two-week medical window and the filing deadline, said as numbers, and what each one costs if it passes."),
  ("Your fee and the costs", "The percentage, whether it rises if you file suit, who pays to get the footage and the road data, and what happens if you lose."),
  ("Who they reach at night", "Whether the client is hiring you or an intake operation, and who picks up at nine in the evening."),
  ("When the person was in the wrong", "The cases where somebody genuinely was not crossing lawfully, and why you say that up front rather than at the end.")),

 9: _b(
  ("Tried a contested split", "Cases you took to a jury, and what they did with a fault split the insurer thought was settled."),
  ("Blamed-pedestrian cases", "Not injury cases generally. Cases where the insurer put it on the person walking, how many, and how recently."),
  ("Verifiable record", "Your license and disciplinary history, verifiable in a way a testimonial never is."),
  ("What a jury here forgives", "The county court, the judges, and how a local jury reacts to somebody who was partly in the wrong."),
  ("Rebuilding the percentage", "How you take an insurer's number apart and put a defensible one in its place."),
  ("Sightlines and reconstruction", "Crash reconstruction experts, the people who figure out what a driver could actually see, and the treating doctors."),
  ("Witnesses fade", "What you secure in the first days, because memory of where somebody stood is gone inside a week."),
  ("Coverage with no car", "How a person with no vehicle of their own still reaches coverage, and whose policy it comes out of."),
  ("Both clocks", "The two-week medical window and the filing deadline, and the separate, much shorter deadline when a city, county or state agency is involved."),
  ("Fees and case costs", "What the percentage is, whether that percentage goes up if you file suit, who pays for the reconstruction, and what happens if you lose."),
  ("Who argues with the adjuster", "Whether the client is hiring you or an intake operation, and who actually fights the percentage."),
  ("When the client's share is high", "If a big share of the blame is genuinely going to land on the client, tell them the honest number instead of making a promise.")),

 10: _b(
  ("Tried against a national company", "Cases you took to a jury, and what a trucking company that size starts doing differently once it believes you will do it again."),
  ("Commercial truck crashes", "Not injury cases generally. Crashes involving heavy trucks, how many, and how recently."),
  ("License and discipline", "Your license and disciplinary record, which counts for more than an award on a website."),
  ("Who they bring in to defend it", "The county court, the judges, and the firms a carrier flies in to fight one of these."),
  ("Reading the federal file", "What you pull from a carrier's records, and what a single violation buried in there is actually worth."),
  ("The preservation letter", "What has to go out in the first few days, because the company decides when that truck data gets erased, and they are not waiting on you."),
  ("People who read the data", "Crash reconstruction experts, the specialists who pull and read what the truck recorded, and trucking safety people who know the federal rules cold."),
  ("Every policy behind the truck", "How you get past the policy on the truck itself to the bigger policies stacked behind it."),
  ("The deadline people miss", "The window for getting treatment, the separate deadline for filing, and the fact that the evidence is gone well before either one runs out."),
  ("Who pays for the work", "What the percentage is, whether it changes if a lawsuit gets filed, who fronts the cost of digging through the company's records, and what the client owes if the case is lost."),
  ("Who deals with their lawyers", "Whether the client is hiring you or an intake operation, and who handles the carrier's counsel."),
  ("When they followed the rules", "Sometimes the company did everything right and it is just a hard case, and you say that out loud when it is true.")),

 11: _b(
  ("Tried for a rider", "Cases you took to a jury, and what they did with somebody who was not in a car at all."),
  ("Riders with no policy", "Not injury cases generally. People hurt on two wheels with no motor vehicle coverage behind them, how many, and how recently."),
  ("Standing you can look up", "Your license and disciplinary history, which anybody can check before they ever call."),
  ("How a jury sees a rider", "The county court, the judges, and what a local jury already assumes about somebody on an e-bike or a scooter."),
  ("Coverage from nowhere", "How you find a policy for somebody the no-fault system does not cover at all."),
  ("Reading the rental terms", "What is actually in a scooter app's agreement, and what a rider gives up the moment they tap accept."),
  ("Chasing the manufacturer", "Crashes where the e-bike or scooter itself failed, and what you can recover from the company that built it."),
  ("Ride data vanishes", "What you secure in the first days, including data a rental company overwrites on its own schedule."),
  ("Who examines the part", "Reconstructionists, treating physicians, and the engineers who take a failed brake or battery apart."),
  ("The shorter deadline", "Say the filing deadline in plain years, then say how much faster a rental company's ride data disappears."),
  ("Fees and the teardown", "The percentage, whether it rises if you file suit, who pays to have a failed part examined, and what happens if you lose."),
  ("When there is nothing to reach", "The cases where no coverage genuinely exists, and why you tell people that in the first conversation instead of the fourth.")),

 12: _b(
  ("Tried in front of a jury", "Cases you took to a jury, and what changed once the jury had actually met your client."),
  ("Riders hit by cars", "Not injury cases generally. Motorcycle riders struck by drivers, how many, and how recently."),
  ("Record you can check", "Your license and your clean record with the Bar. That is checkable, and it is worth more than any badge on a website."),
  ("What a jury assumes here", "The county court, the judges, and the view a local jury tends to walk in with about motorcycles."),
  ("Countering rider bias", "How you take apart the assumption that the rider must have been doing something reckless."),
  ("Reading the damage", "Reconstructionists and treating physicians, and what the damage on both vehicles says about who did what."),
  ("Before the bike is scrapped", "What you go get in the first few days, because the bike gets scrapped and the security footage gets recorded over fast."),
  ("Every policy that could pay", "How you find coverage that matters more to a rider than to anyone else on the road."),
  ("The helmet argument", "How you handle it when there was no helmet, because the other side will lead with that."),
  ("The filing deadline", "Say the actual number of years out loud, and say what happens the day after it runs out."),
  ("Fees and the examination", "The percentage, whether it rises if you file suit, who pays to have the bike and the damage examined, and what happens if you lose."),
  ("When the rider's choice hurts", "When something the rider did genuinely damages the case, give them the number rather than a promise.")),
}
