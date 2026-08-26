# Outro Variations - QA

> Archived from the ROS Prototype v2 Doc on 2026-08-18 before the tab was deleted.

# **Outro Variations - QA**
*Four generated outros for the same episode. Every one hits the same three required beats in the same order: thank and credit the attorney, sign off naming the show, then the reach-out tag. What changes is the wording and which credit approach fires. Pick the ones that sound right and mark the ones that do not.*
**What is fixed and what moves.** The three beats and their order are gated and never change. The credit approach, the sign-off phrasing and all four slots of the reach-out line are drawn from banks in references/outro-banks.json, with a rotation rule that stops any approach repeating within two episodes of a show.
**Two things to look for while reading.** First, does the credit sound like something a person would actually say, or does it sound like praise written to order. Second, does the reach-out land as a natural tag after the sign-off, or does it sound like the host forgot something.
## **Variation 1 - Topical credit**
*Credit anchored to this episode's subject. The strongest source of per-episode uniqueness, because the clause cannot be reused on any other episode. Default choice whenever the topic phrase is concrete.*
*INTERVIEWER*
**{{ATTORNEY}}**, thank you for your time. Nobody actually explains what a car accident case is really worth. You just did.
That is it for this one. **{{PODCAST_NAME}}**. We will see you next episode.
And remember, if you are in **{{STATE}}** and need a lawyer, reach out to **{{FIRM_NAME}}** at **{{PHONE_NUMBER}}**, or online at **{{WEBSITE}}**.
## **Variation 2 - Candor credit**
*Use when the attorney named a weakness, gave an unflattering number, or told someone they did not have a case. Credits the honesty rather than the expertise.*
*INTERVIEWER*
**{{ATTORNEY}}**, I appreciate you taking the time. A lot of attorneys would not have answered that as straight as you did.
That is where we will leave it. **{{PODCAST_NAME}}**. See you next episode.
And one last thing, if you are anywhere in **{{STATE}}** and need help with this, get in touch with **{{FIRM_NAME}}**. The number is **{{PHONE_NUMBER}}**, and the site is **{{WEBSITE}}**.
## **Variation 3 - Clarity credit**
*Best after a technical episode. Credits the explaining rather than the knowing, which is the thing a listener actually just benefited from.*
*INTERVIEWER*
**{{ATTORNEY}}**, thanks for walking through all of that. Most people cannot explain that without making it more confusing, and you just did.
That is the episode. **{{PODCAST_NAME}}**. We will see you on the next one.
And before you go, if this is happening to you in **{{STATE}}**, reach out to **{{FIRM_NAME}}** at **{{PHONE_NUMBER}}**, or find them at **{{WEBSITE}}**.
## **Variation 4 - Depth credit**
*Calls back to the credential from intro line 3. Do NOT use this one on an episode whose introduction already leaned hard on the years token, or the number is the only thing the firm appears to have.*
*INTERVIEWER*
That is a good place to stop. **{{ATTORNEY}}**, thank you. That is the kind of thing you only really know after **{{YEARS_PRACTICING}}** years of it.
We will leave it there. This is **{{PODCAST_NAME}}**, and we will see you next episode.
One more thing, if you are in **{{STATE}}** and you want someone to actually look at it, call **{{FIRM_NAME}}** at **{{PHONE_NUMBER}}**, or online at **{{WEBSITE}}**.
## **Notes for QA**
- **The sign-off is not last, on purpose.** The reach-out lands after it as a tag. "And remember" is the hinge that makes a line after the close sound natural rather than tacked on. The effect is that the contact details are the last thing heard without the episode ending on an ad.
- **The geo is the state, never the city.** S1 is state-governed so one recording serves every city the firm covers. A city in the outro silently makes the whole long-form segment non-reusable. The city lives in S2.
- **"Need a lawyer" is deliberately bland.** It is the phrase that works for personal injury, criminal defense, family law and estate planning alike. An earlier version opened with "if you were hurt", which is nonsense on an estate planning show and describes the wrong person entirely on a criminal defense show.
- **"Produced by Case Engine" was cut.** It is the firm's show and this is the last thing a listener hears. A production credit there puts our name in the client's mouth on their own podcast.
- **No subscribe, like, follow or review.** The show is a search asset, not a channel play, and a CTA stack is the loudest AI-podcast tell there is.
- **No recap.** It is the most common thing a host adds unprompted, and the summary is always worse than the thing it summarizes.

