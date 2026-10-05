from typing import TypedDict, Optional


class AgentState(TypedDict, total=False):
    resume: str
    jd: str
    user_query: str

    plan: list
    current_step: int
    results: dict

    resume_data: Optional[dict]
    jd_data: Optional[dict]