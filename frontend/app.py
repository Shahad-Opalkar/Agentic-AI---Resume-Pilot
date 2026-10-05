import streamlit as st
import requests
import uuid

API_URL = "http://127.0.0.1:8000"

# ============================================================
# THREAD ID
# ============================================================

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())


# ============================================================
# SIDEBAR HISTORY
# ============================================================

st.sidebar.title("History")

# Make conversation buttons look like plain text
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] button {
        background: none !important;
        border: none !important;
        padding: 4px 0 !important;
        margin: 0 !important;
        box-shadow: none !important;
        text-align: left !important;
        width: 100% !important;
    }

    [data-testid="stSidebar"] button:hover {
        background: none !important;
        border: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Get conversation history
response = requests.get(
    f"{API_URL}/conversations"
)


if response.status_code == 200:

    conversations = response.json()

    if conversations:

        for conversation in conversations:

            if st.sidebar.button(
                conversation["title"],
                key=conversation["thread_id"]
            ):

                thread_id = conversation["thread_id"]

                # Load selected conversation
                result = requests.get(
                    f"{API_URL}/conversations/{thread_id}"
                )

                if result.status_code == 200:

                    data = result.json()

                    if data["state"]:

                        # Use the selected thread
                        st.session_state.thread_id = thread_id

                        # Store conversation for display
                        st.session_state.selected_conversation = data

                        st.rerun()

                    else:

                        st.sidebar.warning(
                            "No saved analysis for this conversation."
                        )

                else:

                    st.sidebar.error(
                        "Could not retrieve conversation."
                    )

    else:

        st.sidebar.write("No conversations yet.")

else:

    st.sidebar.error(
        "Could not load conversations."
    )


# ============================================================
# DISPLAY SELECTED OLD CONVERSATION
# ============================================================

if "selected_conversation" in st.session_state:

    conversation = st.session_state.selected_conversation

    state = conversation["state"]

    st.title("Previous Conversation")

    st.write("### Query")

    st.write(
        state.get("user_query", "")
    )

    st.write("### Result")

    results = state.get("results", {})


    if "ats" in results:

        st.write("#### ATS")

        st.write(
            results["ats"]
        )


    if "skills" in results:

        st.write("#### Skills")

        st.write(
            results["skills"]
        )


    if "rewrite" in results:

        st.write("#### Rewritten Resume")

        st.write(
            results["rewrite"]
        )


    if "interview" in results:

        st.write("#### Interview Questions")

        st.write(
            results["interview"]
        )

    st.divider()
    st.subheader("Ask a follow up question")

    followup_query = st.text_input(

        "Your Question",
        placeholder="e.g. Explain my ATS score",
        key="followup_query"

    )

    if st.button("Send",key="send_followup"):

        if not followup_query.strip():
            st.warning("Please enter a question")

        else:
            response=requests.post(
                f"{API_URL}/analyze",
                data={

                    "user_query":followup_query,
                    "thread_id":st.session_state.thread_id
                }
            )

            if response.status_code == 200:

                # Reload the updated conversation state
                result = requests.get(
                    f"{API_URL}/conversations/"
                    f"{st.session_state.thread_id}"
                )

                if result.status_code == 200:
                    st.session_state.selected_conversation = (
                        result.json()
                    )
                    st.rerun()

                else:
                    st.error("Could not reload conversation.")

            else:
                st.error(
                    f"Follow-up failed: {response.text}"
                )



    


# ============================================================
# NORMAL ANALYSIS SCREEN
# ============================================================

else:

    st.title("AI Resume Analyzer")

    st.write(
        "Upload your resume and job description."
    )


    resume = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx"]
    )


    jd = st.file_uploader(
        "Upload Job Description",
        type=["pdf", "docx"]
    )


    user_query = st.text_input(
        "What would you like the agent to do?",
        "Analyze my resume and tell me what I should improve."
    )


    if st.button("Analyze"):

        data = {
            "user_query": user_query,
            "thread_id": st.session_state.thread_id
        }

        files = {}


        # Both files provided
        if resume and jd:

            files = {
                "resume": (
                    resume.name,
                    resume,
                    resume.type
                ),

                "jd": (
                    jd.name,
                    jd,
                    jd.type
                )
            }


        # Only one file provided
        elif resume or jd:

            st.error(
                "Please upload both Resume and Job Description."
            )

            st.stop()


        # Send request to backend
        response = requests.post(
            f"{API_URL}/analyze",
            files=files,
            data=data
        )


        if response.status_code == 200:

            results = response.json()

            st.write("DEBUG RESPONSE:", results)


            st.subheader("Analysis")


            if "ats" in results:

                st.write("### ATS")

                st.write(
                    results["ats"]
                )


            if "skills" in results:

                st.write("### Missing Skills")

                st.write(
                    results["skills"]
                )


            if "rewrite" in results:

                st.write("### Rewritten Resume")

                st.write(
                    results["rewrite"]
                )


            if "interview" in results:

                st.write("### Interview Questions")

                st.write(
                    results["interview"]
                )


        else:

            st.error(
                "Something went wrong."
            )