import streamlit as st
import logging
from pathlib import Path
import os
import sys

sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from config import PAGE_CONFIG, APP_NAME, APP_TAGLINE, COLORS, FEATURES, SUPPORTED_LANGUAGES
except ImportError:
    PAGE_CONFIG = {"page_title": "JusticeBot", "page_icon": "⚖️", "layout": "wide", "initial_sidebar_state": "expanded"}
    APP_NAME = "JusticeBot"
    APP_TAGLINE = "Justice delayed is justice denied. JusticeBot fights back."
    COLORS = {"primary": "#D4AF37", "text_secondary": "#B0B0B0"}
    FEATURES = {}
    SUPPORTED_LANGUAGES = {"en": "English"}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(**PAGE_CONFIG)

def load_custom_css():
    try:
        css_path = Path(__file__).parent / "assets" / "style.css"
        if css_path.exists():
            with open(css_path, 'r', encoding='utf-8') as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception as e:
        logger.warning(f"Could not load custom CSS: {e}")

load_custom_css()

def initialize_session():
    defaults = {"case_input_data": None, "case_analysis_result": None, "generated_bail_application": None, "current_language": "en", "rag_index_loaded": False, "demo_mode": True, "notifications": [], "selected_demo": 0}
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

initialize_session()

def setup_sidebar():
    with st.sidebar:
        st.markdown("<div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #D4AF37, #FFD700); border-radius: 12px; margin-bottom: 20px;'><h2 style='color: #000000; margin: 0;'>Justice Bot</h2><p style='color: #000000; margin: 5px 0;'>Legal AI for Undertrials</p></div>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("**Navigation**")
        if st.button("Home", use_container_width=True):
            st.rerun()

setup_sidebar()

def main():
    try:
        st.markdown(f"<h1 style='color: {COLORS['primary']}; text-align: center;'>Justice Bot</h1>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center; color: {COLORS['text_secondary']};'>{APP_TAGLINE}</h3>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("### Impact Counter")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="Undertrial Prisoners", value="4,00,000+", delta="Critical")
        with col2:
            st.metric(label="Illegally Detained", value="50,000+", delta="Urgent")
        with col3:
            st.metric(label="Analysis Time", value="5 min", delta="vs 2-3 days")
        with col4:
            st.metric(label="Cost", value="₹0", delta="100% Free")
        st.markdown("---")
        st.markdown("### How JusticeBot Works")
        col1, col2, col3, col4, col5 = st.columns(5)
        steps = [("1", "INPUT", "Enter case details"), ("2", "ANALYZE", "Extract information"), ("3", "CHECK", "Assess eligibility"), ("4", "SEARCH", "Find precedents"), ("5", "GENERATE", "Create bail app")]
        for col, (num, title, desc) in zip([col1, col2, col3, col4, col5], steps):
            with col:
                st.markdown(f"<div style='text-align: center; padding: 15px; background-color: #1E2530; border-radius: 10px; border: 2px solid #D4AF37;'><h3>{num}</h3><h4 style='color: #D4AF37;'>{title}</h4><p style='font-size: 11px;'>{desc}</p></div>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("### Try Demo Cases")
        demo_cases = [("Case 1: Petty Theft", "Detained 6 Years (ILLEGAL)"), ("Case 2: Default Bail", "Police Forgot Chargesheet"), ("Case 3: Bailable Offense", "Should Never Be in Jail"), ("Case 4: Complex Case", "Serious Charges")]
        cols = st.columns(2)
        for i, (title, desc) in enumerate(demo_cases):
            with cols[i % 2]:
                if st.button(f"{title} - {desc}", key=f"demo_btn_{i}", use_container_width=True):
                    st.session_state.demo_mode = True
                    st.session_state.selected_demo = i
                    st.success(f"Loaded {title}")
                    st.balloons()
        st.markdown("---")
        st.markdown("### About JusticeBot")
        st.markdown("JusticeBot is a revolutionary GenAI application solving a critical problem. 50,000+ potentially illegally detained prisoners could be freed. 5 minutes to analyze vs 2-3 days manually. 0 cost - completely free. Built for ET GenAI Hackathon 2025")
        st.markdown("---")
        st.markdown("JusticeBot | Built by Aryan Ranjan | ET GenAI Hackathon 2025")
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
