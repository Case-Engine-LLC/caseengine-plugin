# Attribute Extraction Test - Houston

> Archived from the ROS Prototype v2 Doc on 2026-08-18 before the tab was deleted.

# **Attribute Extraction Test**
*Same source both times: one Google AI Mode answer for "best car accident lawyer houston tx", pulled 08-18-2026. One pull, so any ranking is confidence: low.*
## **Table 1 - Extracted with the rules**
*Gated through attribute-rules.md: firm property, screening instruction, discriminating, distinct in substance. Every row carries a checkable ask and a verbatim quote, or it does not exist.*

| **Attribute** | **The ask a client can actually put to the firm** | **Verbatim evidence** | **Ruling** |
|---|---|---|---|
| Board certification | Are you board certified in personal injury trial law? | "Are you board-certified in personal injury trial law? (Fewer than 3-5% of Texas attorneys hold this specialization)" | Engine wrote the ask itself and quantified the rarity. Not in the 08-14 set. |
| Trial willingness | Do you prepare cases for trial, or do you settle them? | "Do you prepare cases to go to trial? (Firms that are trial-ready command much higher settlement offers)" | Merged with "extensive trial experience" - same substance, Gate 4. |
| Case-type experience | How many crashes like mine specifically, and how recently? | "What is your success rate with car accidents specifically like mine? (Rear-end, rideshare, highway, commercial vehicle)" | Kept separate from practice-area experience. |
| Who handles the case | Who is my point of contact, and is it an attorney? | "Who will be my primary point of contact? (Ensure you will speak to an actual attorney, not just paralegals or intake staff)" | Explicit screening question. |
| Results track record | What have you recovered in cases like mine, and when? | "a track record of securing high payouts"; "record-setting verdicts and settlements" | Kept the outcome claim, cut "nationally recognized" as marketing. |
| Ratings and reviews | How many people have reviewed the firm, and what do they say about being kept informed? | "strong client reviews", plus review counts on every firm | Surfaces high here because AI Mode renders the local pack. ChatGPT ranks bar standing above it. |
| Expert network | Which experts do you bring in, and for what? | "leverage medical and accident reconstruction experts" | Passed on the comparison-column ruling below. |
| Availability | Who answers at 2am, and is it someone at the firm? | "24/7" on every firm in the comparison table | Discriminating - plenty of firms do not. |
| Local tenure | How long have you been trying these here specifically? | "Over 37 years of experience in the Houston legal community" | Distinct from knowing the local courts. |
| Appellate capability | If this gets appealed, do you handle it or hand it off? | "Deep appellate court experience" | Comparison-column ruling. |
| Language access | Can my case be handled in Spanish start to finish, by staff? | "bilingual staff" | New. Surfaced as a competitive advantage, not a courtesy. |

## **Table 2 - Extracted without the rules**
*No gates, no dedupe, no ask, no quote. This is the raw list, in the order it appears in the answer.*

| **What a model returns when you just ask it to pull the attributes** |
|---|
| extensive trial experience |
| strong client reviews |
| track record of securing high payouts |
| contingency fee basis |
| free consultations |
| no out-of-pocket cost unless they win |
| board certifications |
| community reputation |
| nationally recognized |
| undefeated trial reputation |
| recovered billions of dollars |
| record-setting verdicts and settlements |
| board certified in personal injury trial law |
| aggressive representation against large insurance providers |
| massively reviewed |
| Latino-owned |
| extensive track record in state, federal and appellate courts |
| proactive client communication |
| over 37 years of experience |
| specializes in maximum payouts |
| board-certified trial attorneys |
| highly personalized attention |
| medical and accident reconstruction experts |
| 24/7 availability |
| bilingual staff |
| success rate with specific crash types |
| primary point of contact |
| trial preparation |

## **What the rules changed**
28 items became 11 attributes, and the difference is not compression for its own sake.
Seven items are one attribute said seven ways. Extensive trial experience, undefeated trial reputation, board-certified trial attorneys, trial preparation, and prepares cases for trial all collapse into trial willingness. A list that carries them separately looks thorough and double-counts the same signal when you rank it.
Five are marketing with no test behind them. Aggressive representation, nationally recognized, highly personalized attention, massively reviewed, community reputation. None of them survives the question "what would a client ask to check this?", which is the gate that does the most work.
Three are category table stakes. Contingency fee, free consultation, and no out-of-pocket cost are true of every personal injury firm in Houston, and the engine says so itself - "because personal injury attorneys work on a contingency fee basis." A criterion nobody can fail does not help anyone choose.
One is a firm identity fact rather than a screening criterion. Latino-owned is not something a client screens on, but the bilingual staff underneath it is, and that survives as language access.
The naive list also has no ask, no quote, no engine mix, and no rank. It cannot be scored against next month's pull, cannot be defended to a client who asks where it came from, and cannot tell you which surface to optimize for. That is the real difference: the gated table is comparable over time and the raw list is a snapshot of one afternoon.
Both lists agree on the substance underneath. The rules are not finding different attributes - they are deduping, killing the marketing language, forcing a checkable question, and making the output something a database can hold.
*One judgment call in Table 1: appellate capability, expert network, and language access appear only as "Key Advantage" items in the comparison table, which describes firms rather than instructing the reader. Passed on the logic that a side-by-side comparison exists to help someone choose. Flag it if you disagree - a ruling invoked twice belongs in the rule file.*

## **Table 3 - The same attributes as response guidance**
*What the attorney actually reads. Same rows as Table 1, inverted: the catalog stores the question a client would ask, this stores what the attorney covers when answering. No question ever appears on this page - an attorney reading a client's question aloud is the failure that made these blocks sound like checklists.*

| **Attributes to hit** | **What to cover** | **Why it lands** |
|---|---|---|
| **Board certification** | Board certified in personal injury trial law, and how few attorneys in the state hold it. | The engine asks this one first, and quantifies the rarity itself. |
| **Trial willingness** | Cases actually tried rather than settled, and what that changes at the table before a jury is picked. | The first thing these answers tell people to look for. |
| **Case type** | The exact crash - rear-end, rideshare, eighteen-wheeler - and how many of that kind recently. | Answers segment by vehicle type, not by practice area. |
| **Fee structure** | Contingency, what happens on a loss, and who fronts records, filing fees and experts. | Fee language runs through nearly every answer. Kept here even though this pull treats it as table stakes. |
| **Who handles it** | Who the client talks to day to day, and that it is an attorney rather than intake staff. | Framed as a consultation question the client should ask outright. |
| **Results** | What cases like this one have recovered, and roughly when. | Outcome claims are what the listing highlights lead with. |
| **Reviews** | How many people have reviewed the firm, and what they say about being kept informed. | AI Mode renders the local pack, so the review count sits next to the firm name. |
| **Expert network** | Reconstructionists, treating physicians, life-care planners. The roles, not the names. | Cited as a firm's key advantage in the comparison. |
| **Availability** | Who picks up at 2am on a Saturday, and whether that is someone at the firm. | Every firm in the comparison carries a 24/7 column. |
| **Time in the market** | Years trying these cases here, and what that means in front of these judges and these defense firms. | Local tenure is called out firm by firm. |
| **Appellate depth** | What happens if the verdict gets appealed - handled in house or handed off. | Named as a differentiator, not assumed. |
| **Language access** | Whether a case can run start to finish in Spanish, with staff rather than a phone line. | Surfaced as a competitive advantage on the most-reviewed firm in the answer. |

Two differences from the catalog worth noticing. Fee structure is in this table and absent from Table 1, because it failed the discriminating gate - the engine frames contingency as something every personal injury firm does. That makes it bad research and necessary script: a listener still needs to hear how they get paid. The catalog decides what is a signal; the script decides what belongs on air, and they are not the same list.
And the order is different. Table 1 is ordered by how consistently each attribute surfaced. This one is ordered by what an attorney would naturally cover in an answer, credentials through logistics, because it is read top to bottom while somebody is talking.

