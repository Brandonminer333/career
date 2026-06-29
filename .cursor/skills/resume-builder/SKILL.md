---
name: resume-builder
description: >-
  Build and tailor role-specific LaTeX resumes from CURRICULUM-VITAE.tex using
  resume_builder.py and resume/scripts/rebuild_canonical_resumes.py. Use when the
  user asks to create, update, or optimize a resume for a job title (AI Engineer,
  Data Scientist, Forward Deployed Engineer, Public Technologist), work with
  resume/latex/CURRICULUM-VITAE.tex, compare role variants, pick bullets, rebuild
  canonical .tex files, or compile application-ready PDFs from the CV inventory.
---

# Resume Builder

All resume assets live under **`resume/`**. The full inventory is `resume/latex/CURRICULUM-VITAE.tex` (CV); one-page application resumes are `resume/latex/<role>.tex`. Use `resume/scripts/resume_builder.py` to query tagged content; use `resume/scripts/rebuild_canonical_resumes.py` to persist curated selections and regenerate canonical files.

**Do not submit CURRICULUM-VITAE.tex** — it is intentionally bloated with every bullet variant.

## CV vs application resume

| | **CV** (`CURRICULUM-VITAE.tex`) | **Application resume** (`<role>.tex`) |
|--|--------------------------------|--------------------------------------|
| Purpose | Full inventory / reference | Job applications (target: 1 page) |
| USF course list | Include tagged courses | **Omit** (degrees only) |
| Technical projects | All variants | **At most 2** project sections |
| Enforcement | Manual (compile as-is) | `apply_resume_item_policies()` in rebuild script |

When curating `BUILDS[role].items`, list experience and project IDs in priority order — only the **first two project groups** survive rebuild. Extra project IDs act as trim fallbacks. Do not add `education-university-of-san-francisco-*` course IDs to `BUILDS` (stripped automatically).

## Closed assistance loop

The agent should not hand-edit canonical `.tex` bullets when inventory IDs exist. Close the loop:

```
resume/latex/CURRICULUM-VITAE.tex     ← edit bullets + role tags here
        ↓
resume/scripts/resume_builder.py        ← query IDs, compare variants
        ↓
resume/job-titles/<ROLE>.md             ← curate against checklist
        ↓
resume/scripts/rebuild_canonical_resumes.py  ← persist item_ids + trimmed SKILLS
        ↓
python3 resume/scripts/rebuild_canonical_resumes.py
        ↓
resume/latex/<role>.tex                 ← canonical application resumes
        ↓
resume/scripts/build-pdfs.sh            ← local PDFs (or CI on push to main)
        ↓
resume/pdf/<role>.pdf
```

| Step | Tool | When |
|------|------|------|
| Add/revise bullet variants | Edit `resume/latex/CURRICULUM-VITAE.tex` | New experience, alternate phrasings |
| Discover what exists | `resume/scripts/resume_builder.py inventory` | Every resume task |
| One-off JD tailoring | `resume_builder.py build --items ... --output resume/latex/generated-<role>.tex` | Single application, don't touch canonical |
| Update canonical resumes | Edit `BUILDS` in `resume/scripts/rebuild_canonical_resumes.py`, then run it | User wants role `.tex` files updated repo-wide |
| Compile PDFs | `resume/scripts/build-pdfs.sh` | After `.tex` changes (requires Docker) |

**After curating bullets for a role, always update `resume/scripts/rebuild_canonical_resumes.py` and run the rebuild** — do not leave selections only in chat or a one-off build command.

## Repo map

| Asset | Path |
|-------|------|
| CV inventory | `resume/latex/CURRICULUM-VITAE.tex` |
| Query/build CLI | `resume/scripts/resume_builder.py` |
| Canonical curation manifest | `resume/scripts/rebuild_canonical_resumes.py` |
| Role guide (checklist) | `resume/job-titles/<ROLE>.md` |
| Canonical role resume | `resume/latex/<role-slug>.tex` |
| Generated output | `resume/latex/generated-<role>.tex` (default) |
| Local PDF compile | `resume/scripts/build-pdfs.sh` |
| PDFs | `resume/pdf/` |

## Role slugs

| Slug | Guide | LaTeX |
|------|-------|-------|
| `ai-engineer` | `resume/job-titles/AI-ENGINEER.md` | `resume/latex/ai-engineer.tex` |
| `data-scientist` | `resume/job-titles/DATA-SCIENTIST.md` | `resume/latex/data-science.tex` |
| `forward-deployed-engineer` | `resume/job-titles/FORWARD-DEPLOYED-ENGINEER.md` | `resume/latex/forward-deployed-engineer.tex` |
| `public-technologist` | `resume/job-titles/PUBLIC-TECHNOLOGIST.md` | `resume/latex/civic.tex` |

Tags in master may **overlap** across roles — curate one bullet per theme, not every matching tag.

List slugs anytime: `python resume/scripts/resume_builder.py roles`

## Standard workflow

Copy this checklist for every resume task:

```
Task progress:
- [ ] 1. Read resume/job-titles/<ROLE>.md (checklist + de-emphasize list)
- [ ] 2. Read job posting / user goal (if tailoring to a specific job)
- [ ] 3. Query inventory for the role
- [ ] 4. Curate bullet IDs (do not blind auto-build)
- [ ] 5. Compare against resume/latex/<role>.tex baseline
- [ ] 6. Update resume/scripts/rebuild_canonical_resumes.py BUILDS[role].items
- [ ] 7. Run python3 resume/scripts/rebuild_canonical_resumes.py
- [ ] 8. Optional: resume/scripts/build-pdfs.sh
```

### Step 1 — Read the role guide

Each `resume/job-titles/*.md` file defines:
- What employers look for
- Which master content fits / gaps to acknowledge
- **De-emphasize** bullets to skip
- Checklist (tagline, ACLU title, bullet themes, projects, skills order)

Follow the checklist; do not invent bullets not grounded in master inventory.

### Step 2 — Query inventory

```bash
python resume/scripts/resume_builder.py inventory --role ai-engineer
python resume/scripts/resume_builder.py inventory --role ai-engineer --include-commented
python resume/scripts/resume_builder.py inventory --include-untagged   # full dump + untagged items
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

Compare selections against `resume/latex/<role>.tex` before finalizing.

### Step 4 — Persist curation and rebuild (canonical)

**Preferred for updating role resumes** — edit `resume/scripts/rebuild_canonical_resumes.py`:

- `BUILDS[role]["items"]` — ordered list of inventory IDs (education, experience, projects)
- `SKILLS[role]` — trimmed LaTeX skills block (not master union)
- `BUILDS[role]["output"]` — target path (e.g. `latex/ai-engineer.tex`, relative to `resume/`)

Then regenerate all four canonical files:

```bash
python3 resume/scripts/rebuild_canonical_resumes.py
```

The script uses `ROLE_DEFAULTS` taglines and `build_resume()` — same engine as the CLI.

**One-off build** (JD tailoring without changing canonical):

```bash
python resume/scripts/resume_builder.py build \
  --role ai-engineer \
  --tagline "AI Engineer \$|\$ Multi-modal pipelines, LLM-assisted labeling, and production inference for unstructured video and text" \
  --items experience-aclu-5,experience-aclu-9,experience-aclu-12,... \
  --output resume/latex/generated-ai-engineer.tex
```

**Quick draft** (all active tagged bullets — review only, not for applications):

```bash
python resume/scripts/resume_builder.py build --role data-scientist --output resume/latex/generated-data-scientist.tex
```

Review drafts — they may include redundant variants or miss manually tuned bullets.

### Step 5 — Skills section

Auto-build uses the **full union** skills block from master (bloated). Canonical resumes get trimmed skills from `SKILLS` in `resume/scripts/rebuild_canonical_resumes.py`. When skills change:
- Edit `SKILLS[role]` in the rebuild script, not the generated `.tex` directly
- Re-run `python3 resume/scripts/rebuild_canonical_resumes.py`

Do not leave master-union skills on an application resume.

### Step 6 — Compile PDF (optional)

Requires Docker. Compiles every `resume/latex/*.tex` to `resume/pdf/<basename>.pdf`:

```bash
resume/scripts/build-pdfs.sh
```

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
| New bullet variant for all roles | `resume/latex/CURRICULUM-VITAE.tex` with role tags |
| Which bullets appear on a role resume | `resume/scripts/rebuild_canonical_resumes.py` → `BUILDS[role].items` |
| Trimmed skills for a role | `resume/scripts/rebuild_canonical_resumes.py` → `SKILLS[role]` |
| Final application resume (generated) | `resume/latex/<role>.tex` via rebuild script |
| New role entirely | Add tags to master, create `resume/job-titles/*.md`, add to `BUILDS` + `SKILLS`, run rebuild |

After editing `resume/latex/CURRICULUM-VITAE.tex`:
1. Re-run `python resume/scripts/resume_builder.py inventory --role <slug>` — IDs may shift if headings change
2. Update `BUILDS` if any curated IDs broke
3. Run `python3 resume/scripts/rebuild_canonical_resumes.py`

## Python API (when scripting)

Run from repo root with `resume/scripts` on `PYTHONPATH`, or import after `sys.path` insert:

```python
from resume_builder import get_inventory, get_role_summary, build_resume

summary = get_role_summary("ai-engineer")
path = build_resume(role="ai-engineer", output_path="resume/latex/generated-ai-engineer.tex")
```

See [reference.md](reference.md) for full CLI flags and API.

## Quality bar before delivery

- [ ] **No em-dashes** ("—")
- [ ] Tagline matches role guide or user-requested JD tailoring
- [ ] No duplicate-theme bullets (one platform, one pipeline, one NLP, one deploy)
- [ ] Projects: **at most 2** technical project sections on application resumes
- [ ] No USF course list on application resumes (degrees only)
- [ ] Skills trimmed for role (from `SKILLS` in rebuild script, not master union)
- [ ] No `\textit{[...]}` role tags left in output (builder strips them)
- [ ] `resume/scripts/rebuild_canonical_resumes.py` updated if canonical resumes changed
- [ ] `python3 resume/scripts/rebuild_canonical_resumes.py` run and output verified
