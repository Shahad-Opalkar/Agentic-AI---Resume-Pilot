from llm import generate_response
import json


def create_plan(user_query, previous_results=None):

   if previous_results is None:
         previous_results = {}
   prompt = f"""
You are the planning component of an AI Resume & Interview Agent.

Available tools:

1. ats
   - Calculates how well the resume matches the job description.
   - Returns an ATS score and resume weaknesses.

2. skills
   - Finds skills required by the job description that are missing from the resume.

3. rewrite
   - Rewrites resume content to address identified weaknesses and missing skills.

4. interview
   - Generates technical and behavioral interview questions based on the resume and job description.


Previous analysis results:
{json.dumps(previous_results, indent=2)}

Your task:
Decide which tools are necessary to satisfy the user's request.

Rules:
- Select ONLY relevant tools.
- You may select multiple tools.
- Return tools in the order they should execute.
- A tool can depend on the result of a previous tool.
- Do not select unnecessary tools.
- Return ONLY valid JSON.

User request:
{user_query}

Return:
{{
    "plan": ["tool1", "tool2"]
}}
"""

   response = generate_response(prompt)


   plan = response["plan"]

   if "ats" in plan and "skills" not in plan:
        plan.insert(0, "skills")

   if "ats" in plan and plan.index("ats") < plan.index("skills"):
        plan.remove("ats")
        plan.insert(plan.index("skills") + 1, "ats")

   return plan

