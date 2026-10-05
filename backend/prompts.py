def build_prompt(retrieved_chunks, jd_text):
    resume_context = "\n\n".join(retrieved_chunks)

    return f"""
    You are an expert ATS resume reviewer.

    Below is the candidate's resume:

    {resume_context}

    ----------------------------------------

    Below is the job description:

    {jd_text}

    Analyze the resume against the job description.

    Rules:
    - Do not invent skills.
    - Only compare information explicitly present in the resume.
    - If a skill is not mentioned, mark it as missing.
    - Return ONLY valid JSON.
    - Do not include markdown or explanations outside the JSON.

    Return this exact JSON format:

    {{
        "ats_score":  <integer>,
        "matching_skills": [],
        "missing_skills": [],
        "weak_sections": [],
        "suggestions": []
    }}
    """