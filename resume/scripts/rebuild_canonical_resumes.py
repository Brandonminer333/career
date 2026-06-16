#!/usr/bin/env python3
"""Rebuild curated canonical role .tex files from job-title checklists."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from resume_builder import ROLE_DEFAULTS, build_resume, get_inventory

SKILLS: dict[str, str] = {
    "ai-engineer": r"""\vspace{-7pt}
    \begin{itemize}[leftmargin=0in, label={}]
        \item {\small
            \textbf{Programming \& Frameworks}{: Python (PyTorch, Transformers, Hugging Face, FastAPI, Pandas, NumPy, Scikit-learn), SQL (PostgreSQL), JavaScript (React.js), Bash} \\

            \textbf{AI / ML}{: LLM integration \& prompting, RAG/agent orchestration, multi-modal AI, NLP (ASR, Whisper, text classification, fine-tuning), GPU-accelerated inference, ROC-AUC threshold optimization, PCA} \\

            \textbf{MLOps \& Deployment}{: Docker, Docker Compose, Google Cloud Run, REST APIs (FastAPI), private-server deployment, GitHub Actions CI/CD, Git} \\

            \textbf{Data}{: multi-source ETL pipelines, web scraping, entity standardization}
        }
    \end{itemize}""",
    "data-scientist": r"""\vspace{-7pt}
    \begin{itemize}[leftmargin=0in, label={}]
        \item {\small
            \textbf{Programming \& Statistical Tools}{: Python (Pandas, NumPy, Scikit-learn, PyTorch, Streamlit), R (tidyverse), SQL (PostgreSQL), Bash} \\

            \textbf{Modeling \& Analysis}{: regression, mixed-effects models, NLP pipelines, classification, PCA, multicollinearity reduction (VIF), ROC-AUC threshold optimization, imbalanced classification, experimental design} \\

            \textbf{Data Engineering}{: multi-source ETL pipelines, web scraping, text normalization, entity standardization} \\

            \textbf{Communication \& Delivery}{: Streamlit dashboards, stakeholder-facing analytics, team leadership}
        }
    \end{itemize}""",
    "forward-deployed-engineer": r"""\vspace{-7pt}
    \begin{itemize}[leftmargin=0in, label={}]
        \item {\small
            \textbf{Programming \& Frameworks}{: Python (FastAPI, PyTorch, Pandas), JavaScript (React.js), SQL (PostgreSQL), Bash} \\

            \textbf{Delivery \& Infrastructure}{: Docker, Docker Compose, Google Cloud Run, private-server deployment, client-hardware deployment, GPU-accelerated inference, REST APIs, GitHub Actions CI/CD} \\

            \textbf{ML Systems}{: LLM-assisted labeling, NLP pipelines, multi-source ETL, batch inference, stakeholder requirements gathering} \\

            \textbf{Soft Skills}{: customer embedding, cross-functional leadership, communication with non-technical stakeholders}
        }
    \end{itemize}""",
    "public-technologist": r"""\vspace{-7pt}
    \begin{itemize}[leftmargin=0in, label={}]
        \item {\small
            \textbf{Programming \& Tools}{: Python (Pandas, PyTorch, FastAPI, Streamlit, Plotly), SQL (PostgreSQL), R, Bash} \\

            \textbf{Civic \& Public-Interest Tech}{: government data pipelines, web scraping, geospatial analysis (DBSCAN, OpenStreetMap), privacy/deanonymization analysis, public dashboards} \\

            \textbf{ML \& NLP}{: multi-stage text classification, LLM-assisted labeling, mixed-effects regression, statistical reporting} \\

            \textbf{Deployment \& Security}{: private-server deployment, Docker, secure off-commercial-cloud delivery, stakeholder communication with legal/advocacy teams}
        }
    \end{itemize}""",
}

BUILDS: dict[str, dict[str, object]] = {
    "ai-engineer": {
        "output": "latex/ai-engineer.tex",
        "items": [
            "education-university-of-san-francisco-1",
            "education-university-of-san-francisco-2",
            "education-university-of-san-francisco-4",
            "education-university-of-san-francisco-6",
            "experience-aclu-3",
            "experience-aclu-10",
            "experience-aclu-16",
            "experience-aclu-19",
            "experience-san-diego-county-taxpayers-association-5",
            "experience-san-diego-county-taxpayers-association-11",
            "experience-san-diego-county-taxpayers-association-14",
            "projects-genai-franchise-personality-quiz-1",
            "projects-genai-franchise-personality-quiz-2",
            "projects-genai-franchise-personality-quiz-3",
            "projects-california-grape-etl-pipeline-dashboard-title-variants-below-6",
            "projects-california-grape-etl-pipeline-dashboard-title-variants-below-9",
            "projects-california-grape-etl-pipeline-dashboard-title-variants-below-15",
            "projects-parkcast-sf-san-francisco-parking-assistant-1",
            "projects-parkcast-sf-san-francisco-parking-assistant-2",
            "projects-parkcast-sf-san-francisco-parking-assistant-3",
            "projects-credit-card-fraud-detection-title-variants-below-2",
            "projects-credit-card-fraud-detection-title-variants-below-8",
        ],
    },
    "data-scientist": {
        "output": "latex/data-science.tex",
        "items": [
            "education-university-of-san-francisco-1",
            "education-university-of-san-francisco-2",
            "education-university-of-san-francisco-4",
            "education-university-of-san-francisco-5",
            "experience-aclu-2",
            "experience-aclu-9",
            "experience-aclu-14",
            "experience-aclu-18",
            "experience-san-diego-county-taxpayers-association-3",
            "experience-san-diego-county-taxpayers-association-9",
            "experience-san-diego-county-taxpayers-association-16",
            "projects-california-grape-etl-pipeline-dashboard-title-variants-below-5",
            "projects-california-grape-etl-pipeline-dashboard-title-variants-below-14",
            "projects-california-grape-etl-pipeline-dashboard-title-variants-below-17",
            "projects-credit-card-fraud-detection-title-variants-below-4",
            "projects-credit-card-fraud-detection-title-variants-below-10",
        ],
    },
    "forward-deployed-engineer": {
        "output": "latex/forward-deployed-engineer.tex",
        "items": [
            "education-university-of-san-francisco-1",
            "education-university-of-san-francisco-2",
            "education-university-of-san-francisco-3",
            "education-university-of-san-francisco-6",
            "experience-aclu-6",
            "experience-aclu-12",
            "experience-aclu-16",
            "experience-aclu-21",
            "experience-san-diego-county-taxpayers-association-6",
            "experience-san-diego-county-taxpayers-association-12",
            "experience-san-diego-county-taxpayers-association-17",
            "projects-genai-franchise-personality-quiz-1",
            "projects-genai-franchise-personality-quiz-3",
            "projects-california-grape-etl-pipeline-dashboard-title-variants-below-7",
            "projects-california-grape-etl-pipeline-dashboard-title-variants-below-10",
            "projects-california-grape-etl-pipeline-dashboard-title-variants-below-16",
            "projects-parkcast-sf-san-francisco-parking-assistant-1",
            "projects-parkcast-sf-san-francisco-parking-assistant-2",
            "projects-parkcast-sf-san-francisco-parking-assistant-3",
        ],
    },
    "public-technologist": {
        "output": "latex/civic.tex",
        "items": [
            "education-university-of-san-francisco-4",
            "education-university-of-san-francisco-6",
            "education-university-of-san-francisco-7",
            "experience-aclu-7",
            "experience-aclu-13",
            "experience-aclu-22",
            "experience-aclu-23",
            "experience-aclu-25",
            "experience-san-diego-county-taxpayers-association-4",
            "experience-san-diego-county-taxpayers-association-7",
            "experience-san-diego-county-taxpayers-association-18",
            "projects-california-grape-etl-pipeline-dashboard-title-variants-below-8",
            "projects-california-grape-etl-pipeline-dashboard-title-variants-below-12",
        ],
    },
}


def main() -> None:
    get_inventory(refresh=True)
    for role, cfg in BUILDS.items():
        path = build_resume(
            role=role,
            tagline=ROLE_DEFAULTS[role]["tagline"],
            item_ids=cfg["items"],  # type: ignore[arg-type]
            output_path=cfg["output"],  # type: ignore[arg-type]
            skills_latex=SKILLS[role],
        )
        print(path)


if __name__ == "__main__":
    main()
