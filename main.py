"""
main.py
-------
Product Comparison Engine — Streamlit Frontend
Two-agent system: Data Collector + Decision Maker
"""

import streamlit as st
import sys
import os


# Ensure local modules are importable
sys.path.insert(0, os.path.dirname(__file__))

from agents.data_collector import collect_product_data
from agents.decision_maker import make_decision
from utils.helpers import parse_vs_input, sanitize_product_name
from dotenv import load_dotenv
load_dotenv()

# Helper for sidebar examples
def set_example(p1, p2):
    st.session_state.pa = p1
    st.session_state.pb = p2


# ─────────────────────────────────────────────
#  Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Product Comparison Engine",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ─────────────────────────────────────────────
#  Custom CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #f0f0f0;
    }

    /* Header */
    .main-header {
        text-align: center;
        padding: 2rem 0 1rem;
    }
    .main-header h1 {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }
    .main-header p {
        color: #9ca3af;
        font-size: 1.05rem;
    }

    /* Cards */
    .product-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    /* Agent badge */
    .agent-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }
    .badge-collector {
        background: rgba(167,139,250,0.2);
        color: #a78bfa;
        border: 1px solid #a78bfa44;
    }
    .badge-decision {
        background: rgba(52,211,153,0.2);
        color: #34d399;
        border: 1px solid #34d39944;
    }

    /* Step indicator */
    .step-box {
        background: rgba(255,255,255,0.04);
        border-left: 3px solid #a78bfa;
        padding: 0.6rem 1rem;
        border-radius: 0 8px 8px 0;
        margin: 0.5rem 0;
        font-size: 0.9rem;
        color: #d1d5db;
    }

    /* Comparison result box */
    .result-box {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 1.5rem;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: rgba(15,12,41,0.8);
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #a78bfa, #60a5fa);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 700;
        font-size: 1rem;
        padding: 0.6rem 2rem;
        width: 100%;
        transition: opacity 0.2s;
    }
    .stButton > button:hover {
        opacity: 0.88;
    }

    /* Input fields */
    .stTextInput input {
        background: rgba(255,255,255,0.07) !important;
        color: #f0f0f0 !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 10px !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.04) !important;
        border-radius: 8px !important;
    }

    /* vs divider */
    .vs-label {
        text-align: center;
        font-size: 2rem;
        font-weight: 900;
        color: #f59e0b;
        padding: 0.5rem 0;
    }

    /* Status boxes */
    .status-running {
        background: rgba(245,158,11,0.15);
        border: 1px solid #f59e0b44;
        border-radius: 10px;
        padding: 0.8rem 1.2rem;
        color: #fcd34d;
        font-size: 0.9rem;
        margin: 0.5rem 0;
    }
    .status-done {
        background: rgba(52,211,153,0.12);
        border: 1px solid #34d39944;
        border-radius: 10px;
        padding: 0.8rem 1.2rem;
        color: #6ee7b7;
        font-size: 0.9rem;
        margin: 0.5rem 0;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔑 API Configuration")
    groq_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
    serp_key = st.text_input("SerpAPI Key", type="password", placeholder="...")
    
    if not groq_key:
        groq_key = os.getenv("GROQ_API_KEY")
    if not serp_key:
        serp_key = os.getenv("SERPAPI_KEY")

    st.markdown("---")
    st.markdown("### 💡 Quick Examples")
    if st.button("📱 iPhone 15 vs S24 Ultra"):
        set_example("iPhone 15 Pro", "Samsung Galaxy S24 Ultra")
    if st.button("💻 MacBook Air vs XPS 13"):
        set_example("MacBook Air M3", "Dell XPS 13")
    if st.button("🎧 Sony XM5 vs Bose QC"):
        set_example("Sony WH-1000XM5", "Bose QuietComfort Ultra")

    st.markdown("---")
    st.caption("Built with LangChain + Groq + Streamlit")


# ─────────────────────────────────────────────
#  Header
# ─────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🔍 Product Comparison Engine</h1>
    <p>AI-powered two-agent system for intelligent product comparisons</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Input Section
# ─────────────────────────────────────────────
st.markdown("### 📦 Enter Products to Compare")

col1, mid, col2 = st.columns([5, 1, 5])

with col1:
    # Auto-fill from sidebar examples

    product_a = st.text_input(
        "Product A",
        placeholder="e.g. iPhone 15 Pro",
        key="pa",
    )

with mid:
    st.markdown("<div class='vs-label'>VS</div>", unsafe_allow_html=True)

with col2:
    product_b = st.text_input(
        "Product B",
        placeholder="e.g. Samsung Galaxy S24",
        key="pb",
    )

st.markdown("")

# Quick parse from "A vs B" combined input
st.markdown("**Or enter as:** `Product A vs Product B`")
combined_input = st.text_input(
    "",
    placeholder="e.g. Sony WH-1000XM5 vs Bose QC45",
    label_visibility="collapsed",
    key="combined",
)

if combined_input:
    parsed = parse_vs_input(combined_input)
    if parsed[0]:
        product_a = parsed[0]
        product_b = parsed[1]

st.markdown("---")


# ─────────────────────────────────────────────
#  Compare Button
# ─────────────────────────────────────────────
col_btn, _ = st.columns([2, 5])
with col_btn:
    run = st.button("🚀 Compare Now", use_container_width=True)


# ─────────────────────────────────────────────
#  Main Logic
# ─────────────────────────────────────────────
if run:
    # Validation
    if not groq_key:
        st.error("⚠️ Please enter your Groq API key in the sidebar.")
        st.stop()
    
    if not serp_key:
        st.error("⚠️ Please enter your SerpAPI key in the sidebar.")
        st.stop()

    if not product_a or not product_b:
        st.error("⚠️ Please enter both products to compare.")
        st.stop()

    product_a = sanitize_product_name(product_a)
    product_b = sanitize_product_name(product_b)

    st.markdown(f"## Comparing **{product_a}** vs **{product_b}**")
    st.markdown("---")

    # ── Phase 1: Data Collection ──
    st.markdown("### 🤖 Agent 1: Data Collector")

    col_a, col_b = st.columns(2)

    data_a = None
    data_b = None

    with col_a:
        st.markdown(f"<div class='agent-badge badge-collector'>🔵 Collecting: {product_a}</div>", unsafe_allow_html=True)
        with st.spinner(f"Fetching data for {product_a}..."):
            try:
                data_a = collect_product_data(product_a, groq_key, serp_key)
                st.markdown(f"<div class='status-done'>✅ Data collected for {product_a}</div>", unsafe_allow_html=True)
                with st.expander(f"📋 {product_a} — Raw Profile"):
                    st.markdown(data_a)
            except Exception as e:
                st.error(f"Error collecting {product_a}: {str(e)}")

    with col_b:
        st.markdown(f"<div class='agent-badge badge-collector'>🔵 Collecting: {product_b}</div>", unsafe_allow_html=True)
        with st.spinner(f"Fetching data for {product_b}..."):
            try:
                data_b = collect_product_data(product_b, groq_key, serp_key)
                st.markdown(f"<div class='status-done'>✅ Data collected for {product_b}</div>", unsafe_allow_html=True)
                with st.expander(f"📋 {product_b} — Raw Profile"):
                    st.markdown(data_b)
            except Exception as e:
                st.error(f"Error collecting {product_b}: {str(e)}")

    # ── Phase 2: Decision Making ──
    if data_a and data_b:
        st.markdown("---")
        st.markdown("### 🤖 Agent 2: Decision Maker")
        st.markdown(f"<div class='agent-badge badge-decision'>🟢 Analysing: {product_a} vs {product_b}</div>", unsafe_allow_html=True)

        with st.spinner("Generating comparison & recommendation..."):
            try:
                comparison = make_decision(product_a, data_a, product_b, data_b, groq_key)
                st.markdown(f"<div class='status-done'>✅ Analysis complete!</div>", unsafe_allow_html=True)

                st.markdown("---")
                st.markdown("### 📊 Full Comparison Report")
                st.markdown(
                    f"<div class='result-box'>{comparison}</div>",
                    unsafe_allow_html=True,
                )

            except Exception as e:
                st.error(f"Decision Agent error: {str(e)}")
    else:
        st.warning("⚠️ Could not collect data for one or both products. Please try again.")


# ─────────────────────────────────────────────
#  Footer Info
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color: #6b7280; font-size: 0.85rem; padding: 1rem 0;'>
    🔍 Product Comparison Engine &nbsp;|&nbsp; 
    Built with LangChain + Groq (LLaMA 3) + Streamlit &nbsp;|&nbsp;
    Two-Agent Architecture
</div>
""", unsafe_allow_html=True)
