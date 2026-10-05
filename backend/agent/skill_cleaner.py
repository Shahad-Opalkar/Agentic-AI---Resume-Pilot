SOFT_SKILLS = {
    "problem solving",
    "analytical skills",
    "communication skills",
    "teamwork",
    "leadership",
    "passion",
    "eagerness",
}

GENERIC_SKILL_CATEGORIES = {
    "llm frameworks",
}

ALIASES = {
    "natural language processing (nlp)": "NLP",
    "natural language processing": "NLP",
}


def clean_jd_skills(skills):

    cleaned = []

    for skill in skills:
        normalized = skill.strip().lower()

        # Remove soft skills
        if normalized in SOFT_SKILLS:
            continue

        # Remove generic categories
        if normalized in GENERIC_SKILL_CATEGORIES:
            continue

        # Normalize terminology
        skill = ALIASES.get(normalized, skill.strip())

        # Remove duplicates
        if skill not in cleaned:
            cleaned.append(skill)

    return cleaned