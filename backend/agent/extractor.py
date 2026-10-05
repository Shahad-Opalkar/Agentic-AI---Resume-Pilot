from llm import generate_response
from .skill_cleaner import clean_jd_skills


from .matcher import extract_skills, TAXONOMY


def extract_resume_data(resume_text):

    prompt = f"""
Extract information from the resume below.

Return ONLY a JSON object in this format:

{{
    "experience_years": 0,
    "experience": [],
    "education": []
}}

Rules:
- Extract only information explicitly present in the resume.
- Do not invent experience.
- "experience_years" should be the total years of professional experience explicitly supported by the resume.
- If the total cannot be determined, return null.
- Return valid JSON only.

Resume:
{resume_text}
"""

    result = generate_response(prompt)

    result["skills"] = extract_skills(
        resume_text,
        TAXONOMY
    )

    print("EXTRACTED RESUME DATA:", result)

    return result

from .matcher import extract_skills, TAXONOMY


def extract_jd_data(jd_text):

    prompt = f"""
Extract structured requirements from the job description below.

Return ONLY a JSON object in this exact format:

{{
    "minimum_experience_years": null,
    "experience_requirements": [],
    "education_requirements": []
}}

Rules:

1. "minimum_experience_years" should contain a numeric value only
   when the JD explicitly states a minimum number of years.
   Otherwise return null.

2. Put textual experience requirements in "experience_requirements".

3. Put education requirements in "education_requirements".

Return valid JSON only.

Job Description:
{jd_text}
"""

    result = generate_response(prompt)

    # Deterministic skill extraction
    result["required_skills"] = extract_skills(
        jd_text,
        TAXONOMY
    )

    result["preferred_skills"] = []

    print("EXTRACTED JD SKILLS:", result["required_skills"])

    return result