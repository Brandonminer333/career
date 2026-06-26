#!/usr/bin/env python3
"""
Resume builder for role-specific LaTeX resumes.

Parses resume/latex/CURRICULUM-VITAE.tex (tagged content inventory) and exposes tools for
an AI agent to query, select, and assemble job-targeted resumes.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

RESUME_ROOT = Path(__file__).resolve().parent.parent
CV_PATH = RESUME_ROOT / "latex" / "CURRICULUM-VITAE.tex"
LATEX_DIR = RESUME_ROOT / "latex"

# Application resumes (not the CV): omit USF course lists; cap project sections.
RESUME_MAX_PROJECTS = 2
EDUCATION_COURSE_ID_PREFIX = "education-university-of-san-francisco-"

PACKAGES = r"""
\documentclass[letterpaper,11pt]{article}
\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}
\usepackage{fontawesome5}
\usepackage{multicol}
\setlength{\multicolsep}{-3.0pt}
\setlength{\columnsep}{-1pt}
\input{glyphtounicode}
\pagestyle{fancy}
\fancyhf{} % clear all header and footer fields
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
% Adjust margins
\addtolength{\oddsidemargin}{-0.6in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1.19in}
\addtolength{\topmargin}{-.7in}
\addtolength{\textheight}{1.4in}
\urlstyle{same}
\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}
% Sections formatting
\titleformat{\section}{
  \vspace{-7pt}\scshape\raggedright\large\bfseries
}{}{0em}{}[\color{black}\titlerule \vspace{0pt}]
% Ensure that generate pdf is machine readable/ATS parsable
\pdfgentounicode=1
"""

COMMANDS = r"""
\newcommand{\resumeItem}[1]{
  \item\small{
    {#1 \vspace{-3pt}}
  }
}
\newcommand{\resumeSubheading}[4]{
  \vspace{-3pt}\item
    \begin{tabular*}{1.0\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & \textbf{\small #2} \\
      \textit{\small#3} & \textit{\small #4} \\
    \end{tabular*}\vspace{-7pt}
}
\newcommand{\resumeSubheadingContinue}[2]{
  \vspace{-3pt}
    \begin{tabular*}{1.0\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textit{\small#1} & \textit{\small #2} \\
    \end{tabular*}\vspace{-7pt}
}
\newcommand{\resumeProjectHeading}[2]{
  \vspace{-3pt}\item
    \begin{tabular*}{1.0\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & \textbf{\small #2} \\
    \end{tabular*}\vspace{-7pt}
}
\newcommand{\resumeSubItem}[1]{\resumeItem{#1}\vspace{0pt}}
\renewcommand\labelitemi{$\vcenter{\hbox{\tiny$\bullet$}}$}
\renewcommand\labelitemii{$\vcenter{\hbox{\tiny$\bullet$}}$}
\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.0in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{0pt}}
"""

HEADER = r"""
\begin{document}
    \begin{center}
        % NAME
        {\Huge\scshape Brandon Miner}
        % SUBHEADING
        \\ San Francisco, CA\\
        \small
        % EMAIL
        \href{mailto:brandonm333@outlook.com}{\raisebox{-0.2\height}\ {brandonm333@outlook.com}} ~
        % PHONE
        % \href{callto:+1 408-335-5436}{\raisebox{-0.2\height}\ {+1 408-335-5436}} ~
        % LINKEDIN
        \href{https://www.linkedin.com/in/brandon-miner-3x3}{\raisebox{-0.2\height}{linkedin.com/in/brandon-miner-3x3}}  ~
        % GITHUB
        \href{https://github.com/Brandonminer333/}{\raisebox{-0.2\height}{github.com/Brandonminer333/} }
    \end{center}
"""

FOOTER = r"""
\end{document}
"""

ROLE_TAG_PATTERN = re.compile(r"\s*\\textit\{\[([^\]]+)\]\}\s*$")
SECTION_PATTERN = re.compile(r"\\section\{([^}]+)\}")

# Fallback defaults when MASTER has no tagline or job-title variant for a role.
ROLE_DEFAULTS: dict[str, dict[str, Any]] = {
    "ai-engineer": {
        "tagline": (
            "AI Engineer — Multi-modal pipelines, LLM-assisted labeling, "
            "and production inference for unstructured video and text"
        ),
        "aclu_title": "AI/ML Engineer",
    },
    "public-technologist": {
        "tagline": (
            "Public Technologist — Data systems for civil liberties, "
            "government accountability, and privacy advocacy"
        ),
        "aclu_title": "Data Scientist",
    },
    "data-scientist": {
        "tagline": (
            "Data Scientist — Statistical modeling, NLP pipelines, and "
            "end-to-end ML products in civic and public-interest contexts"
        ),
        "aclu_title": "Data Scientist",
    },
    "forward-deployed-engineer": {
        "tagline": (
            "Forward Deployed Engineer — End-to-end ML systems on customer "
            "infrastructure --- from stakeholder needs through production deployment"
        ),
        "aclu_title": "Forward Deployed Engineer",
    },
}

SD_COUNTY_JOB = {
    "title": "Data Scientist, Lead Intern",
    "location": "San Diego, CA",
    "organization": "San Diego County Taxpayers Association",
    "dates": "Mar 2024 -- Aug 2025",
}

ACLU_JOB_BASE = {
    "location": "San Francisco, CA",
    "organization": "ACLU",
    "dates": "Oct 2025 -- Present",
}


@dataclass
class InventoryItem:
    """A single tagged (or untagged) bullet from CURRICULUM-VITAE.tex."""

    id: str
    section: str
    subsection: str
    content: str
    roles: list[str] = field(default_factory=list)
    commented: bool = False

    def matches_role(
        self,
        role: str,
        *,
        include_commented: bool = False,
        include_untagged: bool = False,
    ) -> bool:
        if not self.roles:
            return include_untagged
        if self.commented and not include_commented:
            return False
        return role in self.roles

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class EducationSchool:
    institution: str
    location: str
    degree: str
    dates: str
    highlights: list[InventoryItem] = field(default_factory=list)


@dataclass
class ExperienceJob:
    key: str
    title: str
    location: str
    subtitle: str
    dates: str
    bullets: list[InventoryItem] = field(default_factory=list)


@dataclass
class Project:
    key: str
    title: str
    date: str
    bullets: list[InventoryItem] = field(default_factory=list)


@dataclass
class MasterInventory:
    taglines: list[InventoryItem] = field(default_factory=list)
    education: list[EducationSchool] = field(default_factory=list)
    experience: list[ExperienceJob] = field(default_factory=list)
    projects: list[Project] = field(default_factory=list)
    skills_latex: str = ""
    items_by_id: dict[str, InventoryItem] = field(default_factory=dict)

    def all_roles(self) -> list[str]:
        roles: set[str] = set(ROLE_DEFAULTS)
        for item in self.items_by_id.values():
            roles.update(item.roles)
        return sorted(roles)

    def filter_items(
        self,
        role: str | None = None,
        *,
        section: str | None = None,
        subsection: str | None = None,
        include_commented: bool = False,
        include_untagged: bool = False,
    ) -> list[InventoryItem]:
        results: list[InventoryItem] = []
        for item in self.items_by_id.values():
            if section and item.section != section:
                continue
            if subsection and item.subsection != subsection:
                continue
            if role and not item.matches_role(
                role,
                include_commented=include_commented,
                include_untagged=include_untagged,
            ):
                continue
            if not role and not include_untagged and not item.roles:
                continue
            results.append(item)
        return results

    def get_item(self, item_id: str) -> InventoryItem:
        try:
            return self.items_by_id[item_id]
        except KeyError as exc:
            raise KeyError(f"Unknown inventory item id: {item_id}") from exc

    def role_summary(self, role: str) -> dict[str, Any]:
        active = self.filter_items(role, include_commented=False)
        commented = self.filter_items(role, include_commented=True)
        commented_only = [item for item in commented if item.commented]
        tagline = self._tagline_for_role(role)
        return {
            "role": role,
            "suggested_tagline": tagline,
            "active_item_count": len(active),
            "commented_variant_count": len(commented_only),
            "taglines": [item.to_dict() for item in self.taglines if item.matches_role(role)],
            "education_highlights": [
                item.to_dict()
                for item in self.filter_items(role, section="education")
            ],
            "experience": self._grouped_items(active, "experience"),
            "projects": self._grouped_items(active, "projects"),
            "untagged_inventory": [
                item.to_dict()
                for item in self.items_by_id.values()
                if not item.roles and item.section in {"experience", "projects"}
            ],
        }

    def _tagline_for_role(self, role: str) -> str:
        for item in self.taglines:
            if item.matches_role(role):
                return item.content
        return ROLE_DEFAULTS.get(role, {}).get("tagline", "")

    def _grouped_items(
        self, items: list[InventoryItem], section: str
    ) -> dict[str, list[dict[str, Any]]]:
        grouped: dict[str, list[dict[str, Any]]] = {}
        for item in items:
            if item.section != section:
                continue
            grouped.setdefault(item.subsection, []).append(item.to_dict())
        return grouped


def extract_braced_arg(text: str, open_brace_index: int) -> tuple[str, int]:
    """Return (argument, index after closing brace) for a LaTeX braced argument."""
    if open_brace_index >= len(text) or text[open_brace_index] != "{":
        raise ValueError(f"Expected '{{' at index {open_brace_index}")

    depth = 0
    start = open_brace_index + 1
    for index in range(open_brace_index, len(text)):
        char = text[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start:index], index + 1
    raise ValueError("Unbalanced braces while parsing LaTeX")


def parse_braced_arguments(text: str, start_index: int, count: int) -> tuple[list[str], int]:
    args: list[str] = []
    index = start_index
    for _ in range(count):
        while index < len(text) and text[index].isspace():
            index += 1
        if index >= len(text) or text[index] != "{":
            raise ValueError(f"Expected braced argument at index {index}")
        arg, index = extract_braced_arg(text, index)
        args.append(arg.strip())
    return args, index


def find_command(text: str, command: str, start: int = 0) -> int:
    needle = f"\\{command}"
    index = text.find(needle, start)
    while index != -1:
        next_char_index = index + len(needle)
        while next_char_index < len(text) and text[next_char_index].isspace():
            next_char_index += 1
        if next_char_index >= len(text) or text[next_char_index] in "{%":
            return index
        index = text.find(needle, index + 1)
    return -1


def parse_role_tag(raw_content: str) -> tuple[str, list[str], bool]:
    match = ROLE_TAG_PATTERN.search(raw_content)
    if not match:
        return raw_content.strip(), [], False

    content = raw_content[: match.start()].strip()
    parts = [part.strip() for part in match.group(1).split(",")]
    commented = any(part.lower() == "commented" for part in parts)
    roles = [part for part in parts if part.lower() != "commented"]
    return content, roles, commented


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "item"


def _clean_project_title(title: str) -> str:
    cleaned = re.sub(
        r"\s*\(title variants below\)\s*",
        "",
        title.strip(),
        flags=re.IGNORECASE,
    )
    return cleaned


def _format_project_title(title: str) -> str:
    stripped = title.strip()
    if not stripped:
        return ""
    if stripped.startswith("\\textbf"):
        return stripped
    return f"\\textbf{{{stripped}}}"


def make_item(
    *,
    section: str,
    subsection: str,
    raw_content: str,
    counters: dict[str, int],
) -> InventoryItem:
    content, roles, commented = parse_role_tag(raw_content)
    key = f"{section}-{slugify(subsection)}"
    counters[key] = counters.get(key, 0) + 1
    item_id = f"{key}-{counters[key]}"
    return InventoryItem(
        id=item_id,
        section=section,
        subsection=subsection,
        content=content,
        roles=roles,
        commented=commented,
    )


def parse_item_list(
    text: str,
    *,
    section: str,
    subsection: str,
    counters: dict[str, int],
) -> list[InventoryItem]:
    items: list[InventoryItem] = []
    search_from = 0
    while True:
        marker = find_command(text, "resumeItem", search_from)
        if marker == -1:
            break
        brace_index = text.find("{", marker + len("\\resumeItem"))
        raw_content, after = extract_braced_arg(text, brace_index)
        items.append(
            make_item(
                section=section,
                subsection=subsection,
                raw_content=raw_content,
                counters=counters,
            )
        )
        search_from = after
    return items


def parse_sections(master_text: str) -> dict[str, str]:
    matches = list(SECTION_PATTERN.finditer(master_text))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        name = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(master_text)
        sections[name] = master_text[start:end]
    return sections


def parse_education(section_text: str, counters: dict[str, int]) -> list[EducationSchool]:
    schools: list[EducationSchool] = []
    search_from = 0
    while True:
        marker = find_command(section_text, "resumeSubheading", search_from)
        if marker == -1:
            break
        args, after = parse_braced_arguments(
            section_text, marker + len("\\resumeSubheading"), 4
        )
        list_start = section_text.find("\\resumeItemListStart", after)
        next_heading = find_command(section_text, "resumeSubheading", after)
        list_end = section_text.find("\\resumeItemListEnd", after)
        highlights: list[InventoryItem] = []
        if list_start != -1 and list_end != -1 and (
            next_heading == -1 or list_start < next_heading
        ):
            list_text = section_text[list_start:list_end]
            highlights = parse_item_list(
                list_text,
                section="education",
                subsection=args[0],
                counters=counters,
            )
        schools.append(
            EducationSchool(
                institution=args[0],
                location=args[1],
                degree=args[2],
                dates=args[3],
                highlights=highlights,
            )
        )
        search_from = after
    return schools


def experience_key(title: str, subtitle: str) -> str:
    combined = f"{title} {subtitle}".lower()
    if "aclu" in combined:
        return "ACLU"
    if "taxpayers" in combined or "san diego county" in combined:
        return "San Diego County Taxpayers Association"
    return slugify(title)


def parse_experience(section_text: str, counters: dict[str, int]) -> list[ExperienceJob]:
    jobs: list[ExperienceJob] = []
    search_from = 0
    while True:
        marker = find_command(section_text, "resumeSubheading", search_from)
        if marker == -1:
            break
        args, after = parse_braced_arguments(
            section_text, marker + len("\\resumeSubheading"), 4
        )
        list_start = section_text.find("\\resumeItemListStart", after)
        list_end = section_text.find("\\resumeItemListEnd", after)
        bullets: list[InventoryItem] = []
        if list_start != -1 and list_end != -1:
            bullets = parse_item_list(
                section_text[list_start:list_end],
                section="experience",
                subsection=experience_key(args[0], args[2]),
                counters=counters,
            )
        key = experience_key(args[0], args[2])
        jobs.append(
            ExperienceJob(
                key=key,
                title=args[0],
                location=args[1],
                subtitle=args[2],
                dates=args[3],
                bullets=bullets,
            )
        )
        search_from = after
    return jobs


def project_key(title: str, fallback_index: int) -> str:
    plain = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", title)
    plain = plain.replace("\\textbf", "").strip()
    if plain:
        return plain
    return f"untitled-project-{fallback_index}"


def parse_projects(section_text: str, counters: dict[str, int]) -> list[Project]:
    projects: list[Project] = []
    current: Project | None = None
    project_index = 0
    search_from = 0

    while search_from < len(section_text):
        heading_marker = find_command(section_text, "resumeProjectHeading", search_from)
        item_marker = find_command(section_text, "resumeItem", search_from)

        if heading_marker == -1 and item_marker == -1:
            break
        if heading_marker != -1 and (item_marker == -1 or heading_marker < item_marker):
            args, after = parse_braced_arguments(
                section_text, heading_marker + len("\\resumeProjectHeading"), 2
            )
            project_index += 1
            key = project_key(args[0], project_index)
            current = Project(key=key, title=args[0], date=args[1], bullets=[])
            projects.append(current)
            search_from = after
            continue

        if current is None:
            project_index += 1
            current = Project(
                key=f"untitled-project-{project_index}",
                title="",
                date="",
                bullets=[],
            )
            projects.append(current)

        brace_index = section_text.find("{", item_marker + len("\\resumeItem"))
        raw_content, after = extract_braced_arg(section_text, brace_index)
        current.bullets.append(
            make_item(
                section="projects",
                subsection=current.key,
                raw_content=raw_content,
                counters=counters,
            )
        )
        search_from = after

    return projects


def parse_skills(section_text: str) -> str:
    begin_document = section_text.find("\\begin{itemize}")
    if begin_document == -1:
        return section_text.strip()
    end_document = section_text.find("\\end{document}")
    if end_document != -1:
        section_text = section_text[:end_document]
    return section_text.strip()


def apply_resume_item_policies(
    item_ids: list[str],
    inventory: MasterInventory,
    *,
    max_projects: int = RESUME_MAX_PROJECTS,
    include_education_courses: bool = False,
) -> list[str]:
    """Trim curated IDs for one-page application resumes (not the CV)."""
    filtered: list[str] = []
    project_keys: list[str] = []

    for item_id in item_ids:
        item = inventory.items_by_id.get(item_id)
        if item is None:
            continue

        if (
            not include_education_courses
            and item.section == "education"
            and item_id.startswith(EDUCATION_COURSE_ID_PREFIX)
        ):
            continue

        if item.section == "projects":
            key = item.subsection
            if key not in project_keys:
                if len(project_keys) >= max_projects:
                    continue
                project_keys.append(key)

        filtered.append(item_id)

    return filtered


def load_inventory(path: Path | None = None) -> MasterInventory:
    source = Path(path) if path else CV_PATH
    text = source.read_text(encoding="utf-8")
    sections = parse_sections(text)
    counters: dict[str, int] = {}
    inventory = MasterInventory()

    tagline_section = sections.get("Summary Taglines (pick one per derivative)", "")
    inventory.taglines = parse_item_list(
        tagline_section,
        section="taglines",
        subsection="summary",
        counters=counters,
    )

    inventory.education = parse_education(sections.get("Education", ""), counters)
    inventory.experience = parse_experience(sections.get("Experience", ""), counters)
    inventory.projects = parse_projects(sections.get("Technical Projects", ""), counters)
    inventory.skills_latex = parse_skills(sections.get("Technical Skills", ""))

    for item in inventory.taglines:
        inventory.items_by_id[item.id] = item
    for school in inventory.education:
        for item in school.highlights:
            inventory.items_by_id[item.id] = item
    for job in inventory.experience:
        for item in job.bullets:
            inventory.items_by_id[item.id] = item
    for project in inventory.projects:
        for item in project.bullets:
            inventory.items_by_id[item.id] = item

    return inventory


@dataclass
class JobBlock:
    title: str
    location: str
    organization: str
    dates: str
    bullets: list[str] = field(default_factory=list)


@dataclass
class ProjectBlock:
    title: str
    date: str
    bullets: list[str] = field(default_factory=list)


class Resume:
    """Assemble a role-specific LaTeX resume from selected content."""

    def __init__(self, tagline: str):
        self.tagline = tagline.strip()
        self.education_schools: list[EducationSchool] = []
        self.jobs: list[JobBlock] = []
        self.projects: list[ProjectBlock] = []
        self.skills_latex: str | None = None

    @classmethod
    def from_role(
        cls,
        role: str,
        inventory: MasterInventory | None = None,
        *,
        include_commented: bool = False,
        include_untagged_projects: bool = False,
        item_ids: list[str] | None = None,
        tagline: str | None = None,
        skills_latex: str | None = None,
    ) -> Resume:
        inv = inventory or load_inventory()
        header = tagline or inv._tagline_for_role(role)
        if not header:
            raise ValueError(f"No tagline found for role '{role}'")

        resume = cls(header)
        resume.set_education_from_inventory(inv, role, include_commented=include_commented)
        resume.set_experience_from_inventory(
            inv,
            role,
            include_commented=include_commented,
            item_ids=item_ids,
        )
        resume.set_projects_from_inventory(
            inv,
            role,
            include_commented=include_commented,
            include_untagged=include_untagged_projects,
            item_ids=item_ids,
        )
        resume.skills_latex = skills_latex if skills_latex is not None else inv.skills_latex
        return resume

    @classmethod
    def from_item_ids(
        cls,
        tagline: str,
        item_ids: list[str],
        inventory: MasterInventory | None = None,
        *,
        role: str | None = None,
        skills_latex: str | None = None,
    ) -> Resume:
        inv = inventory or load_inventory()
        resume = cls(tagline)
        resume.set_education_from_inventory(inv, role=role, item_ids=item_ids)
        resume.set_experience_from_inventory(inv, role=role, item_ids=item_ids)
        resume.set_projects_from_inventory(inv, role=role, item_ids=item_ids)
        resume.skills_latex = skills_latex if skills_latex is not None else inv.skills_latex
        return resume

    def set_education_from_inventory(
        self,
        inventory: MasterInventory,
        role: str | None = None,
        *,
        include_commented: bool = False,
        item_ids: list[str] | None = None,
    ) -> None:
        selected_ids = set(item_ids or [])
        schools: list[EducationSchool] = []
        for school in inventory.education:
            highlights: list[InventoryItem] = []
            for item in school.highlights:
                if item_ids is not None:
                    if item.id in selected_ids:
                        highlights.append(item)
                    continue
                if role and item.matches_role(role, include_commented=include_commented):
                    highlights.append(item)
            schools.append(
                EducationSchool(
                    institution=school.institution,
                    location=school.location,
                    degree=school.degree,
                    dates=school.dates,
                    highlights=highlights,
                )
            )
        self.education_schools = schools

    def set_experience_from_inventory(
        self,
        inventory: MasterInventory,
        role: str | None = None,
        *,
        include_commented: bool = False,
        item_ids: list[str] | None = None,
    ) -> None:
        selected_ids = set(item_ids or [])
        self.jobs = []

        for job in inventory.experience:
            bullets: list[str] = []
            for item in job.bullets:
                if item_ids is not None:
                    if item.id in selected_ids:
                        bullets.append(item.content)
                    continue
                if role and item.matches_role(role, include_commented=include_commented):
                    bullets.append(item.content)

            if not bullets:
                continue

            if job.key == "ACLU" and role:
                aclu_title = ROLE_DEFAULTS.get(role, {}).get("aclu_title", job.subtitle)
                self.jobs.append(
                    JobBlock(
                        title=aclu_title,
                        location=ACLU_JOB_BASE["location"],
                        organization=ACLU_JOB_BASE["organization"],
                        dates=ACLU_JOB_BASE["dates"],
                        bullets=bullets,
                    )
                )
            elif job.key == "San Diego County Taxpayers Association":
                self.jobs.append(
                    JobBlock(
                        title=SD_COUNTY_JOB["title"],
                        location=SD_COUNTY_JOB["location"],
                        organization=SD_COUNTY_JOB["organization"],
                        dates=SD_COUNTY_JOB["dates"],
                        bullets=bullets,
                    )
                )
            else:
                self.jobs.append(
                    JobBlock(
                        title=job.subtitle,
                        location=job.location,
                        organization=job.title,
                        dates=job.dates,
                        bullets=bullets,
                    )
                )

    def set_projects_from_inventory(
        self,
        inventory: MasterInventory,
        role: str | None = None,
        *,
        include_commented: bool = False,
        include_untagged: bool = False,
        item_ids: list[str] | None = None,
    ) -> None:
        selected_ids = set(item_ids or [])
        self.projects = []

        for project in inventory.projects:
            bullets: list[str] = []
            for item in project.bullets:
                if item_ids is not None:
                    if item.id in selected_ids:
                        bullets.append(item.content)
                    continue
                if role and item.matches_role(
                    role,
                    include_commented=include_commented,
                    include_untagged=include_untagged,
                ):
                    bullets.append(item.content)

            if not bullets:
                continue

            title = _clean_project_title(project.title)
            if not title.strip():
                title = project.key.replace("-", " ").title()

            self.projects.append(ProjectBlock(title=title, date=project.date, bullets=bullets))

    def add_job(self, job: JobBlock) -> None:
        self.jobs.append(job)

    def add_project(self, project: ProjectBlock) -> None:
        self.projects.append(project)

    def render(self) -> str:
        parts = [
            "% Auto-generated by resume_builder.py",
            PACKAGES.strip(),
            COMMANDS.strip(),
            self._render_header(),
            self._render_education(),
            self._render_experience(),
            self._render_projects(),
            self._render_skills(),
            FOOTER.strip(),
        ]
        return "\n\n".join(part for part in parts if part) + "\n"

    def save_to_file(self, path: str | Path) -> Path:
        output = Path(path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(self.render(), encoding="utf-8")
        return output

    def _render_header(self) -> str:
        return (
            HEADER.strip()
            + "\n\n    \\begin{center}\n    \\small\n    "
            + self.tagline
            + "\n    \\end{center}\n"
        )

    def _render_education(self) -> str:
        if not self.education_schools:
            return ""
        lines = [r"\section{Education}", r"  \resumeSubHeadingListStart", ""]
        for school in self.education_schools:
            lines.extend(
                [
                    r"    \resumeSubheading",
                    f"    {{{school.institution}}}{{{school.location}}}",
                    f"    {{{school.degree}}}{{{school.dates}}}",
                ]
            )
            if school.highlights:
                lines.append("        \\resumeItemListStart")
                for item in school.highlights:
                    lines.append(f"            \\resumeItem{{{item.content}}}")
                lines.append("        \\resumeItemListEnd")
            lines.append("")
        lines.append(r"  \resumeSubHeadingListEnd")
        return "\n".join(lines)

    def _render_experience(self) -> str:
        if not self.jobs:
            return ""
        lines = [r"\section{Experience}", r"    \resumeSubHeadingListStart", ""]
        for job in self.jobs:
            lines.extend(
                [
                    r"        \resumeSubheading",
                    f"        {{{job.title}}}{{{job.location}}}",
                    f"           {{{job.organization}}}{{{job.dates}}}",
                    r"            \resumeItemListStart",
                ]
            )
            for bullet in job.bullets:
                lines.append(f"                \\resumeItem{{{bullet}}}")
            lines.extend([r"           \resumeItemListEnd", ""])
        lines.append(r"    \resumeSubHeadingListEnd")
        return "\n".join(lines)

    def _render_projects(self) -> str:
        if not self.projects:
            return ""
        lines = [r"\section{Technical Projects}", r"    \resumeSubHeadingListStart", ""]
        for project in self.projects:
            lines.extend(
                [
                    r"        \resumeProjectHeading",
                    f"        {{{_format_project_title(project.title)}}}{{{project.date}}}",
                    r"        \resumeItemListStart",
                ]
            )
            for bullet in project.bullets:
                lines.append(f"            \\resumeItem{{{bullet}}}")
            lines.extend([r"        \resumeItemListEnd", ""])
        lines.append(r"    \resumeSubHeadingListEnd")
        return "\n".join(lines)

    def _render_skills(self) -> str:
        if not self.skills_latex:
            return ""
        return r"\section{Technical Skills}" + "\n" + self.skills_latex


# --- Agent-facing helpers -------------------------------------------------

_INVENTORY_CACHE: MasterInventory | None = None


def get_inventory(*, refresh: bool = False) -> MasterInventory:
    global _INVENTORY_CACHE
    if refresh or _INVENTORY_CACHE is None:
        _INVENTORY_CACHE = load_inventory()
    return _INVENTORY_CACHE


def list_roles() -> list[str]:
    return get_inventory().all_roles()


def get_role_summary(role: str) -> dict[str, Any]:
    return get_inventory().role_summary(role)


def get_items_for_role(
    role: str,
    *,
    section: str | None = None,
    include_commented: bool = False,
    include_untagged: bool = False,
) -> list[dict[str, Any]]:
    items = get_inventory().filter_items(
        role,
        section=section,
        include_commented=include_commented,
        include_untagged=include_untagged,
    )
    return [item.to_dict() for item in items]


def build_resume(
    *,
    role: str | None = None,
    tagline: str | None = None,
    item_ids: list[str] | None = None,
    output_path: str | Path | None = None,
    include_commented: bool = False,
    include_untagged_projects: bool = False,
    skills_latex: str | None = None,
) -> Path:
    inventory = get_inventory()
    if item_ids:
        if not tagline:
            raise ValueError("tagline is required when building from explicit item_ids")
        resume = Resume.from_item_ids(
            tagline,
            item_ids,
            inventory,
            role=role,
            skills_latex=skills_latex,
        )
    elif role:
        resume = Resume.from_role(
            role,
            inventory,
            include_commented=include_commented,
            include_untagged_projects=include_untagged_projects,
            item_ids=item_ids,
            tagline=tagline,
            skills_latex=skills_latex,
        )
    else:
        raise ValueError("Either role or item_ids must be provided")

    if output_path is None:
        slug = role or "custom"
        output_path = LATEX_DIR / f"generated-{slug}.tex"
    else:
        output_path = Path(output_path)
        if not output_path.is_absolute():
            output_path = RESUME_ROOT / output_path
    return resume.save_to_file(output_path)


def inventory_as_json(
    role: str | None = None,
    *,
    include_commented: bool = False,
    include_untagged: bool = False,
) -> str:
    inventory = get_inventory()
    if role:
        payload = inventory.role_summary(role)
    else:
        payload = {
            "roles": inventory.all_roles(),
            "taglines": [item.to_dict() for item in inventory.taglines],
            "education": [
                {
                    "institution": school.institution,
                    "location": school.location,
                    "degree": school.degree,
                    "dates": school.dates,
                    "highlights": [item.to_dict() for item in school.highlights],
                }
                for school in inventory.education
            ],
            "experience": [
                {
                    "key": job.key,
                    "title": job.title,
                    "location": job.location,
                    "subtitle": job.subtitle,
                    "dates": job.dates,
                    "bullets": [item.to_dict() for item in job.bullets],
                }
                for job in inventory.experience
            ],
            "projects": [
                {
                    "key": project.key,
                    "title": project.title,
                    "date": project.date,
                    "bullets": [item.to_dict() for item in project.bullets],
                }
                for project in inventory.projects
            ],
            "skills_present": bool(inventory.skills_latex),
        }
        if include_untagged:
            payload["untagged_items"] = [
                item.to_dict()
                for item in inventory.items_by_id.values()
                if not item.roles
            ]
        if include_commented:
            payload["commented_items"] = [
                item.to_dict() for item in inventory.items_by_id.values() if item.commented
            ]
    return json.dumps(payload, indent=2)


def _build_cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Parse CURRICULUM-VITAE.tex and build role-specific resumes."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    roles_parser = subparsers.add_parser("roles", help="List known role slugs")
    roles_parser.set_defaults(func=lambda args: print("\n".join(list_roles())))

    inventory_parser = subparsers.add_parser(
        "inventory", help="Dump parsed inventory as JSON"
    )
    inventory_parser.add_argument("--role", help="Limit to one role summary")
    inventory_parser.add_argument(
        "--include-commented", action="store_true", help="Include commented variants"
    )
    inventory_parser.add_argument(
        "--include-untagged", action="store_true", help="Include untagged bullets"
    )

    def run_inventory(args: argparse.Namespace) -> None:
        print(
            inventory_as_json(
                args.role,
                include_commented=args.include_commented,
                include_untagged=args.include_untagged,
            )
        )

    inventory_parser.set_defaults(func=run_inventory)

    build_parser = subparsers.add_parser("build", help="Build a .tex resume")
    build_parser.add_argument("--role", help="Role slug, e.g. ai-engineer")
    build_parser.add_argument("--tagline", help="Override tagline text")
    build_parser.add_argument(
        "--items",
        help="Comma-separated inventory item ids (requires --tagline)",
    )
    build_parser.add_argument(
        "--output",
        help="Output .tex path (default: latex/generated-<role>.tex)",
    )
    build_parser.add_argument(
        "--include-commented",
        action="store_true",
        help="Include commented master variants",
    )
    build_parser.add_argument(
        "--include-untagged-projects",
        action="store_true",
        help="Include untagged project bullets for the role",
    )

    def run_build(args: argparse.Namespace) -> None:
        item_ids = [part.strip() for part in args.items.split(",")] if args.items else None
        path = build_resume(
            role=args.role,
            tagline=args.tagline,
            item_ids=item_ids,
            output_path=args.output,
            include_commented=args.include_commented,
            include_untagged_projects=args.include_untagged_projects,
        )
        print(path)

    build_parser.set_defaults(func=run_build)
    return parser


def main() -> None:
    parser = _build_cli_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
