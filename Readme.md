"Initially, I used an LLM to directly evaluate resume-JD similarity, but I found that generative outputs could produce inconsistent factual matches. I redesigned the system into a hybrid pipeline: document parsing and structured extraction, deterministic normalization and matching, separate compatibility sub-scores, and LLM-based explanations. This reduced hallucination in the scoring layer while retaining semantic reasoning where it was useful."

That is a genuinely strong engineering story.

So the immediate next thing we should implement is structured extraction of the resume and JD separately, because that is the foundation currently causing your incorrect matched_skills: [] and ATS score of 0.

"I added stateful conversational memory using LangGraph checkpointing and thread-based persistence, allowing the agent to retain previous resume analysis and handle contextual follow-up queries."

I used Redis-backed checkpointing for fast, thread-based conversational state. Each conversation is isolated using a unique thread ID, allowing LangGraph to retrieve previous workflow state and support contextual follow-up queries."