from agent.graph import agent

resume_text = """
Python developer with 2 years of experience.
Skills: Python, Docker, Kubernetees, React.js, Git.
"""
jd_text = """
Required skills: Docker, React, Git, Kubernetes, AWS.
Minimum 3 years of experience.
"""
result = agent.invoke({
    "resume": resume_text,
    "jd": jd_text,
"user_query": "Give me my ATS score and tell me what skills I am missing for this job.",
    "plan": [],
    "results": {}
})

print(result["results"])