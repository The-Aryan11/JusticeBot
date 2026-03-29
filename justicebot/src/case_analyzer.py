"""Case Analyzer Module - LLM-powered case extraction"""

import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class CaseAnalyzer:
    def __init__(self, llm_client):
        self.llm = llm_client
        
    def analyze_case(self, case_text: str) -> Dict[str, Any]:
        """Analyze case text and extract structured information"""
        try:
            prompt = f"Analyze this case: {case_text}"
            response = self.llm.chat(
                system="You are a legal AI",
                user_message=prompt,
                temperature=0.3,
                max_tokens=1500
            )
            analysis = self._parse_response(response)
            return analysis
        except Exception as e:
            logger.error(f"Case analysis error: {e}")
            return self._default_response()
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response into structured format"""
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
        except:
            pass
        return self._default_response()
    
    def _default_response(self) -> Dict[str, Any]:
        return {
            "accused_name": "Unknown",
            "accused_age": "Unknown",
            "sections_charged": [],
            "detention_days": 0,
            "max_sentence_days": 0,
            "bail_eligible": False,
            "bail_sections": [],
            "error": "Could not analyze case"
        }
    
    def check_436a_eligibility(self, detention_days: int, max_sentence_days: int) -> bool:
        """Check if case is eligible for Section 436A bail"""
        return detention_days >= (max_sentence_days / 2)
    
    def check_167_eligibility(self, chargesheet_filed: bool, days_limit: int = 90) -> bool:
        """Check if case is eligible for default bail"""
        return not chargesheet_filed
    
    def check_436_eligibility(self, max_sentence_days: int) -> bool:
        """Check if offence is bailable"""
        return max_sentence_days <= 1095
    
    def get_bail_sections(self, detention_days: int, max_sentence_days: int, chargesheet_filed: bool) -> list:
        """Get applicable bail sections"""
        sections = []
        
        if self.check_436_eligibility(max_sentence_days):
            sections.append("436")
        
        if self.check_436a_eligibility(detention_days, max_sentence_days):
            sections.append("436A")
        
        if self.check_167_eligibility(chargesheet_filed):
            sections.append("167")
        
        if not sections:
            sections.append("437")
        
        return sections
