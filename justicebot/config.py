import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", str(BASE_DIR / "chroma_db"))
PRECEDENTS_DIR = DATA_DIR / "precedents"
CACHE_DIR = BASE_DIR / "cache"

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY", "")

LLM_SETTINGS = {
    "groq": {
        "model_primary": "llama-3.1-70b-versatile",
        "model_secondary": "llama-3.1-8b-instant",
        "temperature": 0.7,
        "max_tokens": 2000,
        "rate_limit": 30
    },
    "gemini": {
        "model_flash": "gemini-1.5-flash",
        "model_pro": "gemini-1.5-pro",
        "temperature": 0.7,
        "max_tokens": 2000,
        "rate_limit": 15
    },
    "together": {
        "model": "meta-llama/Llama-3.1-70b-instruct-Turbo",
        "temperature": 0.7,
        "max_tokens": 2000,
    }
}

RAG_SETTINGS = {
    "chunk_size": 1000,
    "chunk_overlap": 200,
    "retrieval_top_k": 8,
    "embedding_model": "all-MiniLM-L6-v2",
    "similarity_threshold": 0.3
}

COLORS = {
    "primary": "#D4AF37",
    "secondary": "#FFD700",
    "background": "#0E1117",
    "card_bg": "#1E2530",
    "alert": "#FF4444",
    "success": "#00CC66",
    "warning": "#FFB800",
    "info": "#0099FF",
    "text": "#FFFFFF",
    "text_secondary": "#B0B0B0"
}

BAIL_SETTINGS = {
    "section_436a_enabled": True,
    "section_167_enabled": True,
    "section_436_enabled": True,
    "section_437_enabled": True,
    "default_bail_days_limit": 90,
    "extended_bail_days_limit": 60,
}

ANALYTICS_SETTINGS = {
    "calculate_success_rate": True,
    "detect_bias": True,
    "show_timeline": True,
    "analyze_judge_bias": True,
    "analyze_caste_bias": True,
    "analyze_gender_bias": True,
    "min_similar_cases": 10,
}

APP_NAME = "JusticeBot"
APP_TAGLINE = "Justice delayed is justice denied. JusticeBot fights back."
APP_VERSION = "1.0.0"
APP_AUTHOR = "Aryan Ranjan"
APP_HACKATHON = "ET GenAI Hackathon 2025"

PAGE_CONFIG = {
    "page_title": f"{APP_NAME} - Legal AI for Undertrial Prisoners",
    "page_icon": "⚖️",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

DEMO_CASES = ["demo_001", "demo_002", "demo_003", "demo_004"]

SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "ta": "Tamil",
    "gu": "Gujarati",
    "mr": "Marathi",
    "bn": "Bengali"
}

SESSION_KEYS = {
    "case_input": "case_input_data",
    "case_analysis": "case_analysis_result",
    "bail_app": "generated_bail_application",
    "current_language": "current_language",
    "rag_index": "rag_index_loaded"
}

VALIDATION = {
    "min_case_text_length": 50,
    "max_case_text_length": 10000,
    "min_accused_age": 10,
    "max_accused_age": 120,
    "valid_states": ["Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", "Uttar Pradesh", "Other"]
}

FEATURES = {
    "voice_input_enabled": True,
    "ocr_enabled": True,
    "pdf_export_enabled": True,
    "multi_language_enabled": True,
    "bias_detection_enabled": True,
    "success_rate_prediction_enabled": True,
    "ecourts_integration_enabled": True,
    "advanced_analytics_enabled": True,
    "demo_mode": True,
}

SAMPLE_DATA = {
    "num_demo_cases": 15,
    "num_precedents": 150,
    "num_ipc_sections": 80,
    "include_cached_results": True,
}

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(CHROMA_DB_PATH, exist_ok=True)
