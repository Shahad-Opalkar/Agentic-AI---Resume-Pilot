from rapidfuzz import process, fuzz


ALIASES = {
    "react.js": "react",
    "reactjs": "react",
    "react js": "react",

    "node.js": "node",
    "nodejs": "node",
    "node js": "node",

    "postgresql": "postgres",
    "postgre sql": "postgres",

    "amazon web services": "aws",

    "retrieval augmented generation": "rag",
}


import json
import re
from pathlib import Path


TAXONOMY_PATH = Path(__file__).parent / "skills.json"

with open(TAXONOMY_PATH, "r", encoding="utf-8") as f:
    TAXONOMY = json.load(f)


def extract_skills(text, taxonomy):
    found = []

    for skill, aliases in taxonomy.items():
        for alias in aliases:
            pattern = r"(?<!\w)" + re.escape(alias.lower()) + r"(?!\w)"

            if re.search(pattern, text.lower()):
                found.append(skill)
                break

    return found

def normalize_skill(skill):
    skill = skill.strip().lower()
    return ALIASES.get(skill, skill)


def match_skills(resume_skills, jd_skills):

    # Normalized skill -> original resume skill
    normalized_resume = {
        normalize_skill(skill): skill
        for skill in resume_skills
    }

    normalized_resume_skills = list(normalized_resume.keys())

    matched_skills = []
    missing_skills = []

    for jd_skill in jd_skills:

        normalized_jd_skill = normalize_skill(jd_skill)

        # -------------------------
        # 1. Exact / alias match
        # -------------------------
        if normalized_jd_skill in normalized_resume:
            matched_skills.append(jd_skill)
            continue

        # -------------------------
        # 2. Fuzzy match
        # -------------------------
        fuzzy_result = process.extractOne(
            normalized_jd_skill,
            normalized_resume_skills,
            scorer=fuzz.ratio
        )

        if fuzzy_result:
            best_match, similarity, _ = fuzzy_result

            if similarity >= 90:
                matched_skills.append(jd_skill)
                continue

        # -------------------------
        # 3. Missing
        # -------------------------
        missing_skills.append(jd_skill)

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }