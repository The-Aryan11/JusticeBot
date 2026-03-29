"""JusticeBot SECURE REST API - Production Ready"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from werkzeug.exceptions import BadRequest, TooManyRequests
import json
import logging
import os
from pathlib import Path
from datetime import datetime
import sys
import bleach
from functools import wraps

sys.path.insert(0, str(Path(__file__).parent / "src"))

from case_analyzer import CaseAnalyzer
from bail_engine import BailEngine
from rag_pipeline import RAGPipeline
from doc_generator import DocumentGenerator
from analytics_engine import AnalyticsEngine
from bias_detector import BiasDetector
from llm_utils import LLMClient

app = Flask(__name__)

Talisman(
    app,
    force_https=True,
    strict_transport_security=True,
    strict_transport_security_max_age=31536000,
    content_security_policy={
        'default-src': "'self'",
        'script-src': "'self'",
        'style-src': "'self' 'unsafe-inline'",
    }
)

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": allowed_origins,
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Type"],
            "supports_credentials": True,
            "max_age": 3600
        }
    }
)

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
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

class ValidationError(Exception):
    """Custom validation error"""
    pass

def sanitize_input(text: str, max_length: int = 10000) -> str:
    """Sanitize user input"""
    if not isinstance(text, str):
        raise ValidationError("Input must be string")
    
    if len(text) > max_length:
        raise ValidationError(f"Input exceeds max length of {max_length}")
    
    if len(text.strip()) == 0:
        raise ValidationError("Input cannot be empty")
    
    sanitized = bleach.clean(text, tags=[], strip=True)
    return sanitized.strip()

def validate_case_data(data: dict) -> dict:
    """Validate case input data"""
    required_fields = {
        'case_text': str,
        'detention_days': int,
        'max_sentence_days': int,
        'chargesheet_filed': bool
    }
    
    for field, field_type in required_fields.items():
        if field not in data:
            raise ValidationError(f"Missing required field: {field}")
        
        if not isinstance(data[field], field_type):
            raise ValidationError(f"Invalid type for {field}")
    
    data['case_text'] = sanitize_input(data['case_text'])
    
    if data['detention_days'] < 0:
        raise ValidationError("detention_days cannot be negative")
    
    if data['max_sentence_days'] < 0:
        raise ValidationError("max_sentence_days cannot be negative")
    
    return data

def validate_bail_data(data: dict) -> dict:
    """Validate bail check data"""
    required_fields = {
        'detention_days': int,
        'max_sentence_days': int,
        'chargesheet_filed': bool
    }
    
    for field, field_type in required_fields.items():
        if field not in data:
            raise ValidationError(f"Missing required field: {field}")
        
        if not isinstance(data[field], field_type):
            raise ValidationError(f"Invalid type for {field}")
    
    return data

def validate_application_data(data: dict) -> dict:
    """Validate bail application data"""
    required_fields = {
        'accused_name': str,
        'bail_section': str
    }
    
    for field, field_type in required_fields.items():
        if field not in data:
            raise ValidationError(f"Missing required field: {field}")
        
        if not isinstance(data[field], field_type):
            raise ValidationError(f"Invalid type for {field}")
    
    data['accused_name'] = sanitize_input(data['accused_name'], 100)
    
    valid_sections = ['436', '436A', '437', '167']
    if data['bail_section'] not in valid_sections:
        raise ValidationError(f"Invalid bail section: {data['bail_section']}")
    
    return data

def validate_search_data(data: dict) -> dict:
    """Validate precedent search data"""
    if 'section' not in data:
        raise ValidationError("Missing required field: section")
    
    data['section'] = sanitize_input(str(data['section']), 50)
    data['bail_ground'] = sanitize_input(str(data.get('bail_ground', '')), 500)
    
    return data

@app.errorhandler(ValidationError)
def handle_validation_error(e):
    """Handle validation errors"""
    logger.warning(f"Validation error: {str(e)}")
    return jsonify({
        "success": False,
        "error": "Invalid input",
        "message": str(e)
    }), 400

@app.errorhandler(TooManyRequests)
def handle_rate_limit(e):
    """Handle rate limit errors"""
    logger.warning(f"Rate limit exceeded: {get_remote_address()}")
    return jsonify({
        "success": False,
        "error": "Rate limit exceeded",
        "message": "Too many requests. Please try again later."
    }), 429

@app.errorhandler(BadRequest)
def handle_bad_request(e):
    """Handle bad requests"""
    logger.warning(f"Bad request: {str(e)}")
    return jsonify({
        "success": False,
        "error": "Bad request",
        "message": "Invalid request format"
    }), 400

@app.errorhandler(500)
def handle_internal_error(e):
    """Handle internal errors - NO DETAILS LEAKED"""
    logger.error(f"Internal error: {str(e)}")
    return jsonify({
        "success": False,
        "error": "Internal server error",
        "message": "An error occurred. Please try again later."
    }), 500

def require_json(f):
    """Require JSON content type"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            raise BadRequest("Content-Type must be application/json")
        return f(*args, **kwargs)
    return decorated_function

def validate_request(validator_func):
    """Validate request data"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                validated_data = validator_func(request.json or {})
                kwargs['validated_data'] = validated_data
                return f(*args, **kwargs)
            except ValidationError as e:
                raise e
            except Exception as e:
                raise ValidationError(f"Validation failed: {str(e)}")
        return decorated_function
    return decorator

@app.route('/api/health', methods=['GET'])
@limiter.limit("60 per minute")
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "alive",
        "service": "JusticeBot API",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }), 200

@app.route('/api/analyze-case', methods=['POST'])
@limiter.limit("10 per minute")
@require_json
@validate_request(validate_case_data)
def analyze_case(validated_data):
    """Analyze case text"""
    try:
        analysis = case_analyzer.analyze_case(validated_data['case_text'])
        
        bail_sections = case_analyzer.get_bail_sections(
            validated_data['detention_days'],
            validated_data['max_sentence_days'],
            validated_data['chargesheet_filed']
        )
        
        return jsonify({
            "success": True,
            "analysis": analysis,
            "bail_sections": bail_sections,
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Case analysis error: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Analysis failed",
            "message": "Could not analyze case"
        }), 500

@app.route('/api/check-bail', methods=['POST'])
@limiter.limit("10 per minute")
@require_json
@validate_request(validate_bail_data)
def check_bail(validated_data):
    """Check bail eligibility"""
    try:
        eligibility = bail_engine.assess_bail_eligibility(validated_data)
        detention_excess = bail_engine.calculate_detention_excess(
            validated_data['detention_days'],
            validated_data['max_sentence_days']
        )
        
        return jsonify({
            "success": True,
            "eligibility": eligibility,
            "detention_excess": detention_excess,
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Bail check error: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Bail check failed",
            "message": "Could not check bail eligibility"
        }), 500

@app.route('/api/generate-application', methods=['POST'])
@limiter.limit("5 per minute")
@require_json
@validate_request(validate_application_data)
def generate_application(validated_data):
    """Generate bail application"""
    try:
        application = doc_generator.generate_bail_application(
            validated_data,
            validated_data['bail_section']
        )
        
        return jsonify({
            "success": True,
            "application": application,
            "bail_section": validated_data['bail_section'],
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Document generation error: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Document generation failed",
            "message": "Could not generate application"
        }), 500

@app.route('/api/search-precedents', methods=['POST'])
@limiter.limit("10 per minute")
@require_json
@validate_request(validate_search_data)
def search_precedents(validated_data):
    """Search precedents"""
    try:
        precedents = rag_pipeline.search_relevant_precedents(
            validated_data['section'],
            validated_data.get('bail_ground', ''),
            validated_data.get('top_k', 5)
        )
        
        strength = rag_pipeline.get_precedent_strength(precedents)
        
        return jsonify({
            "success": True,
            "precedents": precedents,
            "strength_analysis": strength,
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Precedent search error: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Search failed",
            "message": "Could not search precedents"
        }), 500

@app.route('/api/analytics', methods=['POST'])
@limiter.limit("10 per minute")
@require_json
def get_analytics():
    """Get analytics"""
    try:
        data = request.json or {}
        report = analytics_engine.generate_analytics_report(data)
        
        return jsonify({
            "success": True,
            "analytics": report,
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Analytics error: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Analytics failed",
            "message": "Could not generate analytics"
        }), 500

@app.route('/api/detect-bias', methods=['POST'])
@limiter.limit("5 per minute")
@require_json
def detect_bias():
    """Detect bias"""
    try:
        data = request.json or {}
        bias_report = bias_detector.generate_bias_report(data)
        
        return jsonify({
            "success": True,
            "bias_analysis": bias_report,
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Bias detection error: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Bias detection failed",
            "message": "Could not detect bias"
        }), 500

@app.route('/api/sample-cases', methods=['GET'])
@limiter.limit("30 per minute")
def get_sample_cases():
    """Get sample cases"""
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
            return jsonify({
                "success": False,
                "error": "Not found",
                "message": "Sample cases not found"
            }), 404
            
    except Exception as e:
        logger.error(f"Sample cases error: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Failed to retrieve cases",
            "message": "Could not get sample cases"
        }), 500

@app.route('/api/rights-info', methods=['GET'])
@limiter.limit("30 per minute")
def get_rights_info():
    """Get rights info"""
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
            return jsonify({
                "success": False,
                "error": "Not found",
                "message": "Rights info not found"
            }), 404
            
    except Exception as e:
        logger.error(f"Rights info error: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Failed to retrieve rights",
            "message": "Could not get rights information"
        }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 7860))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    if debug:
        logger.warning("Running in DEBUG mode - do not use in production!")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
