import streamlit as st
import requests
import json
from datetime import datetime

# ================= CONFIG =================
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3"

st.set_page_config(
    page_title="ARGUS Intelligence Platform",
    layout="wide"
)

# ================= STYLING =================
st.markdown("""
<style>
body {
    background-color: #0b1220;
}
.block-container {
    padding-top: 2rem;
}
.panel {
    background: #020617;
    border-radius: 14px;
    padding: 18px;
    color: #e5e7eb;
    border: 1px solid #1e293b;
}
.panel-title {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 12px;
    color: #c7d2fe;
}
.audit-box {
    background: #020617;
    border-radius: 10px;
    padding: 12px;
    font-size: 13px;
    color: #94a3b8;
    border-left: 3px solid #334155;
}
</style>
""", unsafe_allow_html=True)

# ================= STATE =================
if "audit_log" not in st.session_state:
    st.session_state.audit_log = []

# ================= LLM CALL =================
def call_llm(prompt, role):
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": f"You are acting as a {role} in a professional AI decision-support system. Be precise, neutral, and analytical."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(OLLAMA_URL, json=payload, stream=True)

    output = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))
            if "message" in data:
                output += data["message"]["content"]

    st.session_state.audit_log.append({
        "role": role,
        "time": datetime.now().strftime("%H:%M:%S"),
        "content": output
    })

    return output

# ================= HEADER =================
st.title("ARGUS Intelligence Platform")
st.caption("Structured multi-agent analysis for high-quality decision support")

st.divider()

# ================= INPUT =================
question = st.text_input(
    "Enter a strategic, technical, or analytical question:",
    placeholder="e.g. What are the long-term risks of adopting autonomous AI systems in healthcare?"
)

# ================= MAIN PIPELINE =================
if question:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("<div class='panel'><div class='panel-title'>Analyst</div>", unsafe_allow_html=True)
        analyst = call_llm(
            f"Analyze the question and present key facts, assumptions, and background:\n{question}",
            "Analyst"
        )
        st.write(analyst)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='panel'><div class='panel-title'>Risk & Counterpoint</div>", unsafe_allow_html=True)
        critic = call_llm(
            f"Identify weaknesses, risks, uncertainties, and counter-arguments in the analysis:\n{analyst}",
            "Risk Analyst"
        )
        st.write(critic)
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div class='panel'><div class='panel-title'>Synthesis</div>", unsafe_allow_html=True)
        synthesis = call_llm(
            f"Reconcile analysis and risks into a balanced, well-reasoned perspective:\nAnalysis:\n{analyst}\n\nRisks:\n{critic}",
            "Synthesizer"
        )
        st.write(synthesis)
        st.markdown("</div>", unsafe_allow_html=True)

    with col4:
        st.markdown("<div class='panel'><div class='panel-title'>Executive Summary</div>", unsafe_allow_html=True)
        final = call_llm(
            f"Produce a concise executive-level summary suitable for decision-makers:\n{synthesis}",
            "Executive Writer"
        )
        st.write(final)
        st.markdown("</div>", unsafe_allow_html=True)

# ================= AUDIT LOG =================
with st.expander("Analysis Audit Trail"):
    st.caption("Internal reasoning trace for transparency and review")
    for item in st.session_state.audit_log:
        st.markdown(
            f"""
            <div class='audit-box'>
            <b>{item['role']}</b> — {item['time']}<br><br>
            {item['content']}
            </div><br>
            """,
            unsafe_allow_html=True
        )