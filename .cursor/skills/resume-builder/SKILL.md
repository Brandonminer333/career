---
name: resume-builder
description: >-
  Build and tailor role-specific LaTeX resumes from MASTER-RESUME.tex using
  resume_builder.py. Use when the user asks to create, update, or optimize a
  resume for a job title (AI Engineer, Data Scientist, Forward Deployed Engineer,
  Public Technologist), work with latex/MASTER-RESUME.tex, compare role variants, pick bullets, or compile
  application-ready .tex files from the master inventory.
---

# Resume Builder

This repo maintains one **master inventory** (`latex/MASTER-RESUME.tex`) and **role-specific resumes** (`latex/<role>.tex`). Use `resume_builder.py` to query tagged content and assemble derivatives.

**Do not submit MASTER-RESUME.tex** — it is intentionally bloated with every bullet variant.

## Repo map

| Asset | Path |
|-------|------|
| Master inventory | `latex/MASTER-RESUME.tex` |
| Builder script | `resume_builder.py` |
| Role guide (checklist) | `job-titles/<ROLE>.md` |
| Canonical role resume | `latex/<role-slug>.tex` |
| Generated output | `latex/generated-<role>.tex` (default) |
| PDFs | `pdf/` |

## Role slugs

| Slug | Guide | LaTeX |
|------|-------|-------|
| `ai-engineer` | `job-titles/AI-ENGINEER.md` | `latex/ai-engineer.tex` |
| `data-scientist` | `job-titles/DATA-SCIENTIST.md` | `latex/data-science.tex` |
| `forward-deployed-engineer` | `job-titles/FORWARD-DEPLOYED-ENGINEER.md` | `latex/forward-deployed-engineer.tex` |
| `public-technologist` | `job-titles/PUBLIC-TECHNOLOGIST.md` | `latex/civic.tex` |

Tags in master may **overlap** across roles — curate one bullet per theme, not every matching tag.

List slugs anytime: `python resume_builder.py roles`

## Standard workflow

Copy this checklist for every resume task:

```
Task progress:
- [ ] 1. Read job-titles/<ROLE>.md (checklist + de-emphasize list)
- [ ] 2. Read job posting / user goal (if tailoring to a specific job)
- [ ] 3. Query inventory for the role
- [ ] 4. Curate bullet IDs (do not blind auto-build)
- [ ] 5. Compare against latex/<role>.tex baseline
- [ ] 6. Build .tex and update canonical file if user wants
- [ ] 7. Optional: compile PDF
```

### Step 1 — Read the role guide

Each `job-titles/*.md` file defines:
- What employers look for
- Which master content fits / gaps to acknowledge
- **De-emphasize** bullets to skip
- Checklist (tagline, ACLU title, bullet themes, projects, skills order)

Follow the checklist; do not invent bullets not grounded in master inventory.

### Step 2 — Query inventory

```bash
python resume_builder.py inventory --role ai-engineer
python resume_builder.py inventory --role ai-engineer --include-commented
python resume_builder.py inventory --include-untagged   # full dump + untagged items
```

JSON fields for `--role`:
- `suggested_tagline` — from master tags or `ROLE_DEFAULTS`
- `experience` — bullets grouped by employer (`ACLU`, `San Diego County Taxpayers Association`)
- `projects` — bullets grouped by project
- `education_highlights` — tagged USF courses
- `untagged_inventory` — bullets with no role tag (quiz app, Parkcast, etc.)

Each bullet has an `id` (e.g. `experience-aclu-12`) — **use IDs for explicit builds**.

### Step 3 — Curate, don't auto-dump

**Prefer curated builds over naive `--role` auto-build.**

Master tags are variant phrasings, not 1:1 with final resumes. Pitfalls:
- Multiple architecture/ETL/NLP bullets may all match one role — pick **one per theme**
- Some bullets are tagged for **multiple roles** — pick one phrasing per theme, not every match
- `[role, commented]` variants are alternate phrasings excluded by default — use only when intentionally reviving old wording
- **Untagged** project bullets require explicit `--items` selection

Compare selections against `latex/<role>.tex` before finalizing.

### Step 4 — Build

**Curated build (preferred):**

```bash
python resume_builder.py build \
  --role ai-engineer \
  --tagline "AI Engineer \$|\$ Multi-modal pipelines, LLM-assisted labeling, and production inference for unstructured video and text" \
  --items experience-aclu-5,experience-aclu-9,experience-aclu-12,... \
  --output latex/ai-engineer.tex
```

**Quick draft (all active tagged bullets for role):**

```bash
python resume_builder.py build --role data-scientist --output latex/generated-data-scientist.tex
```

Review drafts — they may include redundant variants or miss manually tuned bullets.

### Step 5 — Skills section

Auto-build uses the **full union** skills block from master (bloated). Role `.tex` files have trimmed skills. After building:
- Copy/adapt skills from the canonical `latex/<role>.tex`, or
- Hand-edit the skills section in the output file

Do not leave master-union skills on an application resume.

### Step 6 — Compile PDF (optional)

If `pdflatex` is available and `glyphtounicode` is on the TeX path:

```bash
cd latex && pdflatex -interaction=nonstopmode ai-engineer.tex
```

Output naming in `pdf/` follows user convention (e.g. `aie-brandon-miner-resume.pdf`).

## Master tag format

Bullets end with role tags like `\textit{[ai-engineer]}` or `\textit{[data-scientist, public-technologist]}`.

| Tag | Meaning |
|-----|---------|
| `[ai-engineer]` | Active variant for that role |
| `[data-scientist, forward-deployed-engineer]` | Shared across both roles |
| `[public-technologist, commented]` | Alternate phrasing; excluded unless `--include-commented` |
| *(no tag)* | In inventory only; must be selected explicitly |

Valid slugs: `ai-engineer`, `data-scientist`, `forward-deployed-engineer`, `public-technologist`.

## ACLU job title mapping

Builder applies role-specific ACLU titles automatically when `--role` is set:

| Role | ACLU title |
|------|------------|
| `ai-engineer` | AI/ML Engineer |
| `forward-deployed-engineer` | Forward Deployed Engineer |
| `data-scientist` / `public-technologist` | Data Scientist |

## Tailoring to a job posting

When the user provides a JD:

1. Extract top keywords (stack, responsibilities, seniority signals)
2. Read role guide de-emphasize list — drop mismatched bullets
3. From inventory, pick bullets whose **content** aligns (not just role tag)
4. Adjust tagline to mirror JD language (keep truthful; use `$|$` separator in LaTeX)
5. Reorder projects so the most relevant project is first
6. Trim skills to match JD keywords

Do not add experience the user does not have in master inventory.

## Updating master vs role files

| Change | Where |
|--------|-------|
| New bullet variant for all roles | `latex/MASTER-RESUME.tex` with role tags |
| Final application resume | `latex/<role>.tex` |
| New role entirely | Add tags to master, create `job-titles/*.md`, run builder |

After editing `MASTER-RESUME.tex`, re-run inventory — parser reads from disk (no stale cache across CLI invocations).

## Python API (when scripting)

```python
from resume_builder import get_inventory, get_role_summary, build_resume

summary = get_role_summary("ai-engineer")
path = build_resume(role="ai-engineer", output_path="latex/generated-ai-engineer.tex")
```

See [reference.md](reference.md) for full CLI flags and API.

## Quality bar before delivery

- [ ] Tagline matches role guide or user-requested JD tailoring
- [ ] ACLU + SD County titles correct for role
- [ ] No duplicate-theme bullets (one platform, one pipeline, one NLP, one deploy)
- [ ] Projects match checklist count and ordering
- [ ] Skills trimmed for role (not master union)
- [ ] No `\textit{[...]}` role tags left in output (builder strips them)
- [ ] Compared against existing `latex/<role>.tex` if updating canonical file
