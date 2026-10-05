from fastapi import FastAPI, UploadFile, File,Form
from parser import extract_text
from prompts import build_prompt
from llm import generate_response
from Rag.chunker import chunk_text
from Rag.embedder import create_embeddings
from Rag.vectorstore import create_vector_store, search
import shutil
import os
from typing import Optional

from database import (
    init_db,
    create_conversation,
    conversation_exists,
    get_conversations,
    update_conversation_title
)
app = FastAPI()

init_db()


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/conversations")
def conversations():
    return get_conversations()

@app.post("/analyze")
async def analyze(
    user_query: str = Form(...),
    thread_id: str = Form(...),
    resume: Optional[UploadFile] = File(None),
    jd: Optional[UploadFile] = File(None)
):

    from agent.graph import agent

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    if not conversation_exists(thread_id):
        title = user_query[:50]

        create_conversation(
            thread_id,
            title
        )
    # NEW ANALYSIS: files were uploaded
    if resume and jd:

        resume_path = os.path.join(UPLOAD_DIR, resume.filename)
        jd_path = os.path.join(UPLOAD_DIR, jd.filename)

        with open(resume_path, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)

        with open(jd_path, "wb") as buffer:
            shutil.copyfileobj(jd.file, buffer)

        resume_text = extract_text(resume_path)
        jd_text = extract_text(jd_path)

        chunks = chunk_text(resume_text)

        embeddings = create_embeddings(chunks)

        index = create_vector_store(embeddings)

        query_embedding = create_embeddings([jd_text])[0]

        _, indices = search(index, query_embedding)

        retrieved_chunks = [
            chunks[i] for i in indices[0] if i != -1
        ]

        print("Retrieved Chunks:")
        for chunk in retrieved_chunks:
            print("-" * 50)
            print(chunk)

        result = agent.invoke(
    {
        "resume": "\n".join(retrieved_chunks),
        "jd": jd_text,
        "user_query": user_query,
        "plan": [],
        "current_step": 0,
        "results": {}
    },
    config={
        "configurable": {
            "thread_id": thread_id
        }
    }
)

    else:
        previous_state = agent.get_state(config)

        if not previous_state.values:
            return {
                "error": "No previous conversation state found."
            }

        old_state = previous_state.values

        result = agent.invoke(
            {
                "resume": old_state.get("resume", ""),
                "jd": old_state.get("jd", ""),
                "user_query": user_query,
                "plan": [],
                "current_step": 0,
                "results": old_state.get("results", {}),
                "resume_data": old_state.get("resume_data"),
                "jd_data": old_state.get("jd_data")
            },
            config=config
        )

    return result["results"]

@app.get("/conversations/{thread_id}")
def get_conversation(thread_id: str):
    from agent.graph import agent

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    state = agent.get_state(config)

    if state.values is None:
        return {
            "thread_id": thread_id,
            "state": {}
        }

    return {
        "thread_id": thread_id,
        "state": state.values
    }