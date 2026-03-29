"""Bias Detection Module"""

import logging
import json
from typing import Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)

class BiasDetector:
    def __init__(self):
        self.demographic_data = self.load_demographic_data()
    
    def load_demographic_data(self) -> Dict[str, Any]:
        """Load demographic analysis data"""
        try:
            data_path = Path(__file__).parent.parent / "data" / "demographic_data.json"
            if data_path.exists():
                with open(data_path, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Could not load demographic data: {e}")
        return {}
    
    def detect_caste_bias(self, accused_caste: str) -> Dict[str, Any]:
        """Detect caste-based bias"""
        caste_data = self.demographic_data.get("caste_analysis", {}).get(accused_caste, {})
        
        return {
            "caste": accused_caste,
            "bail_approval_rate": caste_data.get("bail_approval_rate", 65),
            "discrimination_index": caste_data.get("discrimination_index", 0),
            "bias_detected": caste_data.get("discrimination_index", 0) > 0.1
        }
    
    def detect_gender_bias(self, gender: str) -> Dict[str, Any]:
        """Detect gender-based bias"""
        gender_data = self.demographic_data.get("gender_analysis", {}).get(gender, {})
        
        return {
            "gender": gender,
            "bail_approval_rate": gender_data.get("bail_approval_rate", 65),
            "bias_detected": gender_data.get("bail_approval_rate", 65) < 60
        }
    
    def detect_judge_bias(self, judge_name: str) -> Dict[str, Any]:
        """Detect judge-specific bias"""
        judge_data = self.demographic_data.get("judge_analysis", {}).get(judge_name, {})
        
        return {
            "judge": judge_name,
            "approval_rate": judge_data.get("bail_approval_rate", 65),
            "cases_handled": judge_data.get("cases_handled", 0),
            "bias_indicator": "LOW" if judge_data.get("bail_approval_rate", 65) > 70 else "MEDIUM"
        }
    
    def generate_bias_report(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive bias analysis report"""
        return {
            "caste_bias": self.detect_caste_bias(case_data.get("caste", "General")),
            "gender_bias": self.detect_gender_bias(case_data.get("gender", "Male")),
            "judge_bias": self.detect_judge_bias(case_data.get("judge", "Unknown")),
            "systemic_bias_detected": False
        }
