from llm import generate_response
from .scoring import calculate_ats_score
from .extractor import extract_resume_data, extract_jd_data
from .matcher import match_skills
from .experience_matcher import match_experience

def ats_tool(state):

    # Get deterministic skill matching result
    skills_result = state["results"]["skills"]

    matched_skills = skills_result["matched_skills"]
    missing_skills = skills_result["missing_skills"]

    total_required = len(matched_skills) + len(missing_skills)

    # -------------------------
    # 1. Skill score
    # -------------------------
    if total_required == 0:
        skill_score = None
    else:
        skill_score = round(
            (len(matched_skills) / total_required) * 100,
            2
        )

    # -------------------------
    # 2. Experience score
    # -------------------------
    resume_data = state["resume_data"]
    jd_data = state["jd_data"]

    experience_result = match_experience(
        resume_data.get("experience_years"),
        jd_data.get("minimum_experience_years")
    )

    experience_score = experience_result["score"]

    # -------------------------
    # 3. Composite score
    # -------------------------
    available_scores = []

    if skill_score is not None:
        available_scores.append(skill_score)

    if experience_score is not None:
        available_scores.append(experience_score)

    if available_scores:
        overall_score = round(
            sum(available_scores) / len(available_scores),
            2
        )
    else:
        overall_score = None

    # -------------------------
    # 4. Store result
    # -------------------------
    result = {
        "overall_score": overall_score,
        "skill_score": skill_score,
        "experience": experience_result,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }

    state["results"]["ats"] = result

    return state


from llm import generate_response
from .extractor import extract_resume_data, extract_jd_data
from .matcher import match_skills

def skill_match_tool(state):

    # Extract structured information
    resume_data = extract_resume_data(state["resume"])
    jd_data = extract_jd_data(state["jd"])

    # Match skills
    result = match_skills(
        resume_data["skills"],
        jd_data["required_skills"]
    )

    # Add extracted skills to the result
    result["resume_skills"] = resume_data["skills"]
    result["jd_required_skills"] = jd_data["required_skills"]

    # IMPORTANT: Save structured data in state
    # ATS will use this for experience scoring
    state["resume_data"] = resume_data
    state["jd_data"] = jd_data

    state["results"]["skills"] = result

    return state

def rewrite_tool(state):
    prompt = f"""
Rewrite the resume content to better align with the job description.

Resume:
{state["resume"]}

Job Description:
{state["jd"]}

Return ONLY valid JSON in exactly this format:

{{
    "rewritten_resume": ""
}}

Rules:
- Rewrite only information already present in the resume.
- Do not invent skills, experience, projects, companies, or achievements.
- Do not create a cover letter.
- Do not add information that is not supported by the resume.
"""

    result = generate_response(prompt)

    state["results"]["rewrite"] = result

    return state

def interview_tool(state):
    prompt = f"""
Generate interview questions based on the resume and job description.

Resume:
{state["resume"]}

Job Description:
{state["jd"]}

Return ONLY valid JSON in exactly this format:

{{
    "questions": []
}}

Rules:
- Generate only interview questions.
- Base questions on skills, projects, and experience present in the resume or required in the job description.
- Do not include answers.
- Do not include explanations.
"""

    result = generate_response(prompt)

    state["results"]["interview"] = result

    return state

def experience_tool(state):

    candidate_years = state["resume_data"]["experience_years"]
    required_years = state["jd_data"]["minimum_experience_years"]

    result = match_experience(
        candidate_years,
        required_years
    )

    state["results"]["experience"] = result

    return state