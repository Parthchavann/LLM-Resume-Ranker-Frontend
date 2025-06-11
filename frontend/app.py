import streamlit as st
import requests

BACKEND = "http://localhost:8000"

st.title("LLM-Powered Semantic Resume Ranker")

st.header("1. Upload Resumes")
resumes = st.text_area("Paste resumes (one per line, or separated by ---)", height=200)
resume_list = [r.strip() for r in resumes.split('---') if r.strip()]

st.header("2. Job Description")
job_desc = st.text_area("Paste the job description", height=100)

if st.button("Rank Applicants"):
    with st.spinner("Ranking..."):
        resp = requests.post(f"{BACKEND}/rank", json={
            "resumes": resume_list,
            "job_description": job_desc
        })
        if resp.ok:
            ranked = resp.json()["ranked"]
            st.subheader("Ranking Results")
            for i, r in enumerate(ranked, 1):
                st.markdown(f"**{i}. Score:** {r['score']:.2f}")
                st.markdown(f"**Resume:** {r['resume'][:300]}...")
                if "llm_reasoning" in r:
                    st.markdown(f"**LLM Reasoning:** {r['llm_reasoning']}")
                st.markdown("---")
        else:
            st.error("Error in ranking resumes.")

st.header("3. Get Resume Feedback (GPT-4)")
resume_fb = st.text_area("Paste a resume for feedback", height=100)
if st.button("Get Feedback"):
    with st.spinner("Getting feedback..."):
        resp = requests.post(f"{BACKEND}/feedback", json={"resume": resume_fb})
        if resp.ok:
            st.success(resp.json()["feedback"])
        else:
            st.error("Error getting feedback.")
