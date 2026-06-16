# Bag of Stories — Forward Deployed MLE Interview Prep

---

## Story 1: The Diarization Insight

**Competencies:** Problem diagnosis · Creative technical solution · Ownership

**Situation**
Building a police auditor for the ACLU of NorCal. Zero-shot BERT classifiers were underperforming on compliance classification.

**Task**
Improve model accuracy — the obvious move was better models or fine-tuning.

**Action**
Diagnosed the real problem as data quality, not model quality. Audio from freeway traffic stops was heavily degraded. Instead of chasing a model fix, built a new transcription pipeline: pre-trained ML denoiser → diarization model to split audio by speaker → isolated officer speech only, exploiting the logical fact that the officer's mic is closest to the officer during a traffic stop.

**Result**
13% relative improvement in compliance prediction accuracy across the zero-shot BERT classifier suite.

**Use this story for:**
- "Tell me about a time you solved the wrong problem"
- "Most creative technical solution"
- "Tell me about a technical challenge"
- "Bias toward action"

---

## Story 2: Caught Real Noncompliance Before Launch

**Competencies:** Impact · Mission-driven work · Shipping under constraints

**Situation**
Siskiyou County settled a class action racial discrimination lawsuit. The ACLU received bimonthly bodycam footage for auditing — thousands of hours of video that attorneys could not feasibly watch manually.

**Task**
Build an ML auditing tool to surface noncompliance at scale so attorneys could focus their time on the worst offenders.

**Action**
Built an end-to-end pipeline: denoising → diarization → transcription → classification. Made a deliberate choice to optimize for recall over precision — explained to a judge during a presentation that catching the worst offenders matters more than avoiding false positives, because a false negative buries a real violation under thousands of compliant stops.

**Result**
Caught 5 confirmed noncompliance examples before the system was even fully in production. Gives the ACLU concrete, documented leverage for systemic policy change in Siskiyou County.

**Use this story for:**
- "Tell me about work you're proud of"
- "Tell me about impact"
- "Why do you want this role"
- "Tell me about a stakeholder presentation"

---

## Story 3: The Shifting Data Problem

**Competencies:** Dealing with ambiguity · Learning from failure · Prioritization

**Situation**
As part of the ACLU police auditor project, Siskiyou County was slowly coming into compliance with settlement requirements. This meant data formats changed constantly every two weeks — PDFs to CSVs, column names shifting, video metadata inconsistencies.

**Task**
Build a stable ETL pipeline despite unstable, moving inputs.

**Action**
Initially chased the pipeline, rebuilding it every time the data changed — burning hours on code that quickly became legacy. A mentor helped reframe the approach: focus on what's immutable first. Shifted to building inference logic on already-processed data and worked backwards to the pipeline. Stopped over-engineering edge cases, which had been the biggest source of newly written legacy code.

**Result**
Delivered working tools that a data scientist could run independently before the internship ended. The project didn't reach full production — but the lesson fundamentally reshaped how to approach system design under uncertainty: build from the stable core outward.

**Use this story for:**
- "Tell me about a failure or setback"
- "Tell me about a time you had to move fast with incomplete information"
- "What would you do differently"
- "How do you handle ambiguity"

---

## Story 4: Making Creepy Data Tangible

**Competencies:** Technical communication · Stakeholder influence · Translating ML for non-technical audiences

**Situation**
An ACLU attorney was building a legal case against the commercial sale of location data. He understood the legal argument but needed to understand — viscerally — why the data was dangerous in practice.

**Task**
Explain an ML pipeline that automatically extracts locations of interest from raw location data, to someone with no data science background.

**Action**
Used his own location data as the case study. Walked him through exactly what the model surfaced without any manual analysis: his home address, his kids' school, his office. No charts, no visualizations — the output spoke for itself.

**Result**
The attorney immediately and viscerally understood the threat model. The demo didn't just explain the pipeline — it became the argument.

**Use this story for:**
- "Tell me about explaining something technical to a non-technical stakeholder"
- "Tell me about influencing without authority"
- "Customer empathy"

---

## Story 5: The 9,000-Page PDF

**Competencies:** Initiative · Persistence · Resourcefulness · Closing loops

**Situation**
Early in the ACLU internship, was tasked with extracting semi-tabular data from a 9,000+ page PDF. Couldn't crack it at the time and flagged it honestly to the attorney rather than overpromising.

**Task**
Get clean, usable structured data out of an effectively unusable format.

**Action**
Months later, gained access to better tooling (Claude Opus via Cursor Pro). Took another shot at the problem unprompted — no one asked. Got clean results on the first try.

**Result**
Emailed the data to the attorney proactively and offered to handle future PDF extractions. Problem closed. Established a pattern of coming back to unfinished business rather than letting it stay buried.

**Use this story for:**
- "Tell me about taking initiative"
- "Tell me about a time you failed and came back to it"
- "Ownership mindset"

---

## Story 6: The AI Slide Deck Disagreement

**Competencies:** Pushback · Collaboration · Pragmatic judgment

**Situation**
During the Parkcast-SF project, a partner wanted to scrap a manually built slide deck in favor of AI-generated slides — which contained hallucinated, factually incorrect images.

**Task**
Navigate the disagreement without derailing the partnership or the upcoming presentation.

**Action**
Didn't argue about process or ownership. Pointed to specific, objective errors in the AI-generated images. He regenerated the slides. The two decks were merged, taking the best of each.

**Result**
Delivered a solid presentation with no relationship damage.

**Use this story for:**
- "Tell me about a disagreement with a teammate"
- "How do you handle conflict"

---

## Gaps to Patch

Two important story slots that are currently thin:

**"Tell me about working directly with a customer to understand their problem"**
The closest answer is the attorney location data demo, but it's more of a presentation than a discovery conversation. Think through whether there's a moment at either org where you had to ask questions to figure out what someone actually needed — before you knew what to build.

**"Tell me about a time you had to learn something completely new under pressure"**
The React refactor for the ACLU auditor frontend is the right instinct. Worth developing into a full story: what was the scope, what was the timeline, what changed for the attorneys as a result?
