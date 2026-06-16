# Project Framing Guide — Forward Deployed MLE Interview Prep

Two versions for each project: **Technical** (for an MLE interviewer) and **Recruiter** (for Cate).
The recruiter version leads with *what it does and why it matters*, not how it works.

---

## Anchor Project: ACLU Police Auditor

**Recruiter Version (60–90 sec)**

> "At the ACLU of NorCal, I built an end-to-end ML system to audit police bodycam footage at scale. Siskiyou County had just settled a racial discrimination lawsuit, and the ACLU was receiving thousands of hours of footage every two months — way too much for attorneys to watch manually. I built a pipeline that transcribes the footage, isolates the officer's speech, and runs it through a suite of classifiers to flag likely noncompliance. Before the system was even fully live, it had already surfaced five confirmed violations — giving the ACLU concrete evidence to push for real policy change."

**Technical Version (2 min)**

> "The core challenge was data quality. These were traffic stops on the side of freeways — terrible audio. My first instinct was to improve the models, but I diagnosed the real problem as the input data. I built a preprocessing pipeline: a pre-trained ML denoiser followed by a diarization model that splits audio by speaker. Since the officer is always closest to the mic, I could reliably isolate their speech and throw away ambient noise and bystander audio. That single intervention gave us a 13% relative improvement in accuracy across our zero-shot BERT classifier suite. I deliberately optimized for recall over precision — explained to a judge that in this domain, a false negative is far more costly than a false positive, because a buried violation never gets reviewed."

**One-liner**

> "I built an ML system that catches police noncompliance in bodycam footage — and it found real violations before it even launched."

---

## Supporting Project: GenAI Franchise Personality Quiz

**Recruiter Version (45–60 sec)**

> "I did a Pokemon personality quiz online and thought it was terrible, so I built a better one — then kept pushing until it worked for any franchise. You type in something like 'Hogwarts Houses' or 'Pokemon gym leader types' and it generates a fully custom quiz grounded in that franchise's actual lore, scraped live from Fandom wikis. The result matching uses weighted cosine similarity against a generated character dataset — so you're not just getting a random assignment, you're being compared to how each character actually answered the same questions. It's live on Vercel and I could market it tomorrow if I wanted to."

**Technical Version (90 sec)**

> "The core design problem was: how do you go from an arbitrary franchise and class system to grounded, character-accurate roleplay answers? The solution was constraining the wiki source to Fandom, which gives consistent URL patterns across franchises and predictable page structure for scraping. The pipeline is: user inputs franchise → LLM searches Fandom → scrapes character pages → generates a roster, roleplay answers, and a classifier dataset asynchronously. The async piece matters — users start taking the quiz while the backend is still generating character responses, so there's no blocking wait. Matching is cosine similarity on a tabular dataset of character × question answer vectors, weighted by class. Infrastructure is Next.js on Vercel, FastAPI on Cloud Run, Docker, GCS for shareable quiz IDs, and GitHub Actions for CI/CD."

**One-liner**

> "I built a generative personality quiz engine that works for any franchise, grounded in live wiki data — because I was annoyed by a bad Pokemon quiz."

---

## Background Project: California Grape ETL Pipeline

**When to mention it:** Don't lead with this one. Use it only as supporting evidence for "I can onboard to a new domain fast and deliver something usable quickly" — which is exactly what forward deployment requires.

**One-liner to slot in**

> "I also built a multi-source ETL pipeline and Streamlit dashboard for California agricultural data — containerized, deployed to Cloud Run, reproducible infrastructure. Mainly to show I can parachute into an unfamiliar domain, figure out the data landscape, and ship something a non-technical stakeholder can actually use."

---

## For Cate's Call Specifically

She asked two things: past projects and how you're picturing your next move. Here's how to frame the "next move" answer in a way that lands at Adaption:

> "I'm finishing my grad program in three weeks and looking for a role where I'm solving real problems with real data — not just building models in a vacuum. The work I found most energizing at the ACLU was the full loop: understanding the domain, figuring out what the data actually looked like in practice versus what we assumed, and building something that an attorney could use to do their job better. I want more of that — closer to the problem, closer to the impact. A forward deployed role at an early stage company where what I build in the field shapes the product is exactly that."

This answer does three things: it mirrors Adaption's language ("field becomes the product"), it frames your scrappy background as an asset, and it signals you understand what makes this role different from a standard MLE position.
