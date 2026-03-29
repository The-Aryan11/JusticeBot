"""JusticeBot REST API - Backend for HuggingFace Spaces"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import logging
import os
from pathlib import Path
from datetime import datetime
import sys

sys.path.insert(0, str(Path(__file__).parent / "src"))

from case_analyzer import CaseAnalyzer
from bail_engine import BailEngine
from rag_pipeline import RAGPipeline
from doc_generator import DocumentGenerator
from analytics_engine import AnalyticsEngine
from bias_detector import BiasDetector
from llm_utils import LLMClient

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = {
    "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
    "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
    "TOGETHER_API_KEY": os.getenv("TOGETHER_API_KEY")
}

llm_client = LLMClient(config)
case_analyzer = CaseAnalyzer(llm_client)
bail_engine = BailEngine()
rag_pipeline = RAGPipeline()
doc_generator = DocumentGenerator()
analytics_engine = AnalyticsEngine()
bias_detector = BiasDetector()

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "alive",
        "service": "JusticeBot API",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }), 200

@app.route('/api/analyze-case', methods=['POST'])
def analyze_case():
    try:
        data = request.json
        case_text = data.get('case_text', '')
        
        if not case_text:
            return jsonify({"error": "case_text required"}), 400
        
        analysis = case_analyzer.analyze_case(case_text)
        detention_days = data.get('detention_days', 0)
        max_sentence_days = data.get('max_sentence_days', 0)
        chargesheet_filed = data.get('chargesheet_filed', False)
        
        bail_sections = case_analyzer.get_bail_sections(
            detention_days, max_sentence_days, chargesheet_filed
        )
        
        return jsonify({
            "success": True,
            "analysis": analysis,
            "bail_sections": bail_sections,
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Case analysis error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/check-bail', methods=['POST'])
def check_bail():
    try:
        data = request.json
        eligibility = bail_engine.assess_bail_eligibility(data)
        detention_excess = bail_engine.calculate_detention_excess(
            data.get('detention_days', 0),
            data.get('max_sentence_days', 0)
        )
        
        return jsonify({
            "success": True,
            "eligibility": eligibility,
            "detention_excess": detention_excess,
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Bail check error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate-application', methods=['POST'])
def generate_application():
    try:
        data = request.json
        bail_section = data.get('bail_section', '437')
        
        application = doc_generator.generate_bail_application(data, bail_section)
        
        return jsonify({
            "success": True,
            "application": application,
            "bail_section": bail_section,
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Document generation error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/search-precedents', methods=['POST'])
def search_precedents():
    try:
        data = request.json
        section = data.get('section', '')
        bail_ground = data.get('bail_ground', '')
        top_k = data.get('top_k', 5)
        
        precedents = rag_pipeline.search_relevant_precedents(section, bail_ground, top_k)
        strength = rag_pipeline.get_precedent_strength(precedents)
        
        return jsonify({
            "success": True,
            "precedents": precedents,
            "strength_analysis": strength,
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Precedent search error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/analytics', methods=['POST'])
def get_analytics():
    try:
        data = request.json
        report = analytics_engine.generate_analytics_report(data)
        
        return jsonify({
            "success": True,
            "analytics": report,
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Analytics error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/detect-bias', methods=['POST'])
def detect_bias():
    try:
        data = request.json
        bias_report = bias_detector.generate_bias_report(data)
        
        return jsonify({
            "success": True,
            "bias_analysis": bias_report,
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Bias detection error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/sample-cases', methods=['GET'])
def get_sample_cases():
    try:
        data_path = Path(__file__).parent / "data" / "sample_cases.json"
        if data_path.exists():
            with open(data_path, 'r', encoding='utf-8') as f:
                cases = json.load(f)
            return jsonify({
                "success": True,
                "cases": cases.get('cases', []),
                "total": len(cases.get('cases', [])),
                "timestamp": datetime.now().isoformat()
            }), 200
        else:
            return jsonify({"error": "Sample cases not found"}), 404
            
    except Exception as e:
        logger.error(f"Sample cases error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/rights-info', methods=['GET'])
def get_rights_info():
    try:
        data_path = Path(__file__).parent / "data" / "rights_info.json"
        if data_path.exists():
            with open(data_path, 'r', encoding='utf-8') as f:
                rights = json.load(f)
            return jsonify({
                "success": True,
                "rights": rights.get('rights', []),
                "total": len(rights.get('rights', [])),
                "timestamp": datetime.now().isoformat()
            }), 200
        else:
            return jsonify({"error": "Rights info not found"}), 404
            
    except Exception as e:
        logger.error(f"Rights info error: {e}")
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 7860))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    print(f"""
    {'='*80}
    JusticeBot API Server
    {'='*80}
    Starting on http://0.0.0.0:{port}
    Debug: {debug}
    {'='*80}
    """)
    
    app.run(host='0.0.0.0', port=port, debug=debug)
