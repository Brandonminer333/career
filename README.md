# Brandon Miner's Career Repo

Resumes, interview prep, portfolio source, and public GitHub profile content.

## Resumes

Specialized resumes for four overlapping tech roles. Each role has a **job guide** (research + resume checklist) and a matching **`.tex`** file.

| Role | Guide | LaTeX |
|------|-------|-------|
| AI Engineer | [AI-ENGINEER.md](resume/job-titles/AI-ENGINEER.md) | [ai-engineer.tex](resume/latex/ai-engineer.tex) |
| Data Scientist | [DATA-SCIENTIST.md](resume/job-titles/DATA-SCIENTIST.md) | [data-science.tex](resume/latex/data-science.tex) |
| Forward Deployed Engineer | [FORWARD-DEPLOYED-ENGINEER.md](resume/job-titles/FORWARD-DEPLOYED-ENGINEER.md) | [forward-deployed-engineer.tex](resume/latex/forward-deployed-engineer.tex) |
| Public Technologist | [PUBLIC-TECHNOLOGIST.md](resume/job-titles/PUBLIC-TECHNOLOGIST.md) | [civic.tex](resume/latex/civic.tex) |

**CV inventory (not for applications):** [CURRICULUM-VITAE.tex](resume/latex/CURRICULUM-VITAE.tex)

**Builder:** `python resume/scripts/resume_builder.py roles` — see [.cursor/skills/resume-builder/SKILL.md](.cursor/skills/resume-builder/SKILL.md).

**Rebuild canonical resumes:** `python3 resume/scripts/rebuild_canonical_resumes.py` (after curating bullet IDs).

**PDFs:** [resume/pdf/](resume/pdf/) — compile locally with `resume/scripts/build-pdfs.sh` (requires [Docker](https://www.docker.com/); pulls `ghcr.io/xu-cheng/texlive-debian` on first run).

## Public presence

| Asset | Source in this repo | Published to |
|-------|---------------------|--------------|
| GitHub profile README | [GITHUB_README.md](GITHUB_README.md) | [Brandonminer333/Brandonminer333](https://github.com/Brandonminer333/Brandonminer333) via GitHub Actions |
| Portfolio site | [portfolio/](portfolio/) | [Vercel](https://brandonminer-portfolio.vercel.app/) |

Profile README sync requires the `PROFILE_README_DEPLOY_KEY` repository secret (SSH deploy key with write access to `Brandonminer333/Brandonminer333`).
