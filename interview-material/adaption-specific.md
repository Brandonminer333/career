# Cate Recruiter Screen — Q&A Answer Guide

Bullet points only. These are the main points to hit for each question — not a script.

---

## Q1: "Tell me about yourself and what's drawing you to Adaption?"

- Stats background in undergrad → first real ML experience at SDCTA
- Hit a ceiling: everything I produced was static, wanted to build moving systems
- That pushed me toward grad school
- At the ACLU I built a full product for non-technical attorneys — proper frontend, backend, the whole system
- Before it was even fully live, we were already catching real officer noncompliance
- Why Adaption: "intelligence shouldn't only be for those who know how to build it" — I've lived that working with attorneys
- Continual learning is the culmination of what production ML should look like
- Forward deployed role is the perfect bridge: my experience with non-technical stakeholders + Adaption's bleeding edge research

---

## Q2: "What was the hardest part of translating technical work for non-technical stakeholders? Give me a specific moment."

- Context: building a traffic stop auditor for the ACLU to flag officer noncompliance
- Lead investigator asked me to build a model that could predict if a stop reason was legally justified
- I knew immediately that was a fine-tuning problem, not a zero-shot problem
- Had to explain to a non-technical investigator: pretrained models understand language, not law — we need labeled legal examples to bridge that gap
- They ended up getting 85 manually labeled examples across the full classification suite
- Now we can actually fine-tune the language model into a legal model

---

## Q3: "85 labeled examples — is that enough for fine-tuning? What would you do if it wasn't?"

- Honestly, 85 is probably not enough
- First move: data augmentation — swap words in stop reason text where I can predict the label impact, test if the model catches it
- Try AI pseudo-labeling: use Gemini or similar to generate synthetic labels, validate before using
- Always validate — never assume augmented data is good enough without testing
- Be transparent with stakeholders: here's what the data gives us, here's the limitation, here are the options

---

## Q4: "In a forward deployed role you might not have mentors on site — you're the expert. How do you handle hitting a hard constraint with a customer?"

- First: consider all possible options before bringing problems to the customer — State the problem and possible solutions
- Explore all available workarounds (augmentation, pseudo-labels, different model approaches, Adaption's own platform capabilities)
- Come to the customer with honest assessment *plus* concrete options — not just problems
- Transparency early matters: don't hide constraints, but don't surface them until you understand them
- Goal: be the expert in the room who says "here's the situation, here's what I'd recommend, here's why"

---

## Q5: "Walk me through your last month — what are you actually spending time on right now?"

- Job search + finishing grad program in 3 weeks
- Main project: GenAI Franchise Personality Quiz — a live web app
- Why I built it: wanted real end-to-end product experience — CI/CD, deployment, the full stack
- How it works: user inputs a franchise (e.g. Hogwarts Houses) → system pulls character list → scrapes Fandom wiki → LLM roleplays as each character answering quiz questions → user answers same questions → cosine similarity match
- Why this approach: started from hating a mediocre BuzzFeed quiz, realized abstract questions made it impossible to get labeled data manually → AI roleplay was the solution
- What I learned: GitHub Actions CI/CD (first time), Vercel for continuous deployment, full stack production infrastructure
- It's live and usable — not just a portfolio piece
