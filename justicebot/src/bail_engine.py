"""Bail Engine Module - Rule-based bail eligibility"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class BailEngine:
    def __init__(self):
        self.section_436_limit = 1095
        self.section_436a_threshold = 0.5
        self.default_bail_limit_normal = 60
        self.default_bail_limit_serious = 90
    
    def assess_bail_eligibility(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive bail eligibility assessment"""
        
        detention_days = case_data.get("detention_days", 0)
        max_sentence_days = case_data.get("max_sentence_days", 0)
        chargesheet_filed = case_data.get("chargesheet_filed", False)
        
        result = {
            "overall_eligible": False,
            "applicable_sections": [],
            "primary_section": None,
            "success_probability": 0.0,
            "reasoning": []
        }
        
        if max_sentence_days <= self.section_436_limit:
            result["applicable_sections"].append("436")
            result["reasoning"].append("Bailable offence")
            result["overall_eligible"] = True
        
        if detention_days >= (max_sentence_days * self.section_436a_threshold):
            result["applicable_sections"].append("436A")
            result["reasoning"].append("Mandatory bail - half sentence exceeded")
            result["overall_eligible"] = True
            result["primary_section"] = "436A"
            result["success_probability"] = 0.99
        
        if not chargesheet_filed and detention_days >= self.default_bail_limit_normal:
            result["applicable_sections"].append("167")
            result["reasoning"].append("Default bail - chargesheet not filed")
            result["overall_eligible"] = True
        
        if not result["primary_section"] and result["applicable_sections"]:
            result["primary_section"] = result["applicable_sections"][0]
            result["success_probability"] = 0.85
        
        return result
    
    def calculate_detention_excess(self, detention_days: int, max_sentence_days: int) -> Dict[str, Any]:
        """Calculate detention excess"""
        half_sentence = max_sentence_days * 0.5
        excess = max(0, detention_days - half_sentence)
        
        return {
            "detention_days": detention_days,
            "legal_limit": half_sentence,
            "excess_days": excess,
            "is_illegal": excess > 0,
            "excess_months": round(excess / 30, 1)
        }
