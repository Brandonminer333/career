# Resume Builder — CLI & API Reference

All paths are under `resume/` unless noted. Commands assume the **career repo root** as the working directory.

## Canonical rebuild script

Persists curated bullet IDs and trimmed skills for all four roles. **Run this after changing which bullets belong on canonical resumes.**

```bash
python3 resume/scripts/rebuild_canonical_resumes.py
```

| Dict key | Purpose |
|----------|---------|
| `BUILDS[role]["items"]` | Ordered inventory IDs (experience → projects; no USF courses) |
| `BUILDS[role]["output"]` | Target `.tex` path (relative to `resume/`) |
| `SKILLS[role]` | Trimmed LaTeX skills block |

Roles: `ai-engineer`, `data-scientist`, `forward-deployed-engineer`, `public-technologist`.

Outputs:
- `resume/latex/ai-engineer.tex`
- `resume/latex/data-science.tex`
- `resume/latex/forward-deployed-engineer.tex`
- `resume/latex/civic.tex`

## Local PDF compile

```bash
resume/scripts/build-pdfs.sh
```

Requires Docker. Writes `resume/pdf/<basename>.pdf` for each `resume/latex/*.tex`.

## CLI

### `roles`

```bash
python resume/scripts/resume_builder.py roles
```

Prints one role slug per line.

### `inventory`

```bash
python resume/scripts/resume_builder.py inventory
python resume/scripts/resume_builder.py inventory --role ai-engineer
python resume/scripts/resume_builder.py inventory --role ai-engineer --include-commented
python resume/scripts/resume_builder.py inventory --include-untagged
python resume/scripts/resume_builder.py inventory --include-commented --include-untagged
```

| Flag | Effect |
|------|--------|
| `--role` | Role summary JSON instead of full inventory |
| `--include-commented` | Include `[..., commented]` variants |
| `--include-untagged` | Include bullets with no role tag |

### `build`

```bash
python resume/scripts/resume_builder.py build --role ai-engineer
python resume/scripts/resume_builder.py build --role ai-engineer --output resume/latex/generated-ai-engineer.tex
python resume/scripts/resume_builder.py build \
  --role ai-engineer \
  --tagline "AI Engineer \$|\$ ..." \
  --items id1,id2,id3 \
  --output resume/latex/ai-engineer.tex
python resume/scripts/resume_builder.py build --role data-scientist --include-commented
python resume/scripts/resume_builder.py build --role ai-engineer --include-untagged-projects
```

| Flag | Required | Effect |
|------|----------|--------|
| `--role` | One of `--role` or `--items` | Role slug for filtering and ACLU title |
| `--tagline` | Required with `--items` | Header tagline (LaTeX; use `\$|\$` for `\|$`) |
| `--items` | Optional | Comma-separated inventory IDs for curated build |
| `--output` | Optional | Output path (default: `resume/latex/generated-<role>.tex`) |
| `--include-commented` | Optional | Include commented master variants |
| `--include-untagged-projects` | Optional | Include untagged project bullets for role filter |

## Python API

```python
from resume_builder import (
    get_inventory,
    list_roles,
    get_role_summary,
    get_items_for_role,
    build_resume,
    inventory_as_json,
    Resume,
    load_inventory,
)

# Query
roles = list_roles()
inv = get_inventory()
summary = get_role_summary("ai-engineer")
items = get_items_for_role("ai-engineer", section="experience")
json_str = inventory_as_json("ai-engineer")

# Build
path = build_resume(role="ai-engineer", output_path="resume/latex/generated-ai-engineer.tex")

# Curated build
path = build_resume(
    role="ai-engineer",
    tagline=r"AI Engineer $|$ Multi-modal pipelines...",
    item_ids=["experience-aclu-5", "experience-aclu-9"],
    output_path="resume/latex/ai-engineer.tex",
)

# Manual assembly
inv = load_inventory()
resume = Resume.from_item_ids(
    tagline=r"AI Engineer $|$ ...",
    item_ids=["experience-aclu-5"],
    inv,
    role="ai-engineer",
)
resume.save_to_file("resume/latex/custom.tex")
```

## Inventory item shape

Each item in JSON:

```json
{
  "id": "experience-aclu-12",
  "section": "experience",
  "subsection": "ACLU",
  "content": "Bullet text without role tag",
  "roles": ["ai-engineer"],
  "commented": false
}
```

Sections: `taglines`, `education`, `experience`, `projects`.

## ROLE_DEFAULTS (fallback taglines & ACLU titles)

Used when master has no tagged tagline for a role (all four current roles have tagged taglines in master; defaults remain as fallback).

Defined in `resume/scripts/resume_builder.py` → `ROLE_DEFAULTS` dict.

## Output document structure

Generated `.tex` files contain:

1. `PACKAGES` + `COMMANDS` (from `resume/scripts/resume_builder.py`)
2. Contact header + tagline
3. Education (degrees always; USF courses if tagged/selected)
4. Experience (role-formatted job headers)
5. Technical Projects
6. Technical Skills (master union unless hand-edited)

## Common item ID prefixes

| Prefix | Section |
|--------|---------|
| `taglines-summary-N` | Summary taglines |
| `education-university-of-san-francisco-N` | USF course highlights |
| `experience-aclu-N` | ACLU bullets |
| `experience-san-diego-county-taxpayers-association-N` | SD County bullets |
| `projects-<project-slug>-N` | Project bullets |

Run `inventory --role <slug>` to get exact IDs for the current master file.
