def match_experience(candidate_years, required_years):

    if candidate_years is None or required_years is None:
        return {
            "score": None,
            "status": "not_available"
        }

    if candidate_years >= required_years:
        score = 100
        status = "meets_requirement"
    else:
        score = round(
            (candidate_years / required_years) * 100,
            2
        )
        status = "below_requirement"

    return {
        "candidate_years": candidate_years,
        "required_years": required_years,
        "score": score,
        "status": status
    }