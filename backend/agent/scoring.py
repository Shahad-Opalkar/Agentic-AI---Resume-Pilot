def calculate_ats_score(matched_skills, missing_skills):

    total_skills = len(matched_skills) + len(missing_skills)

    if total_skills == 0:
        return 0

    score = (len(matched_skills) / total_skills) * 100

    return round(score)