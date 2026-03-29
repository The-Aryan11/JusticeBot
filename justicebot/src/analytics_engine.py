"""Analytics Engine - Success rate prediction"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class AnalyticsEngine:
    def __init__(self):
        self.base_success_rates = {
            "436": 0.85,
            "436A": 0.99,
            "167": 0.95,
            "437": 0.65
        }
    
    def predict_success(self, case_data: Dict[str, Any], bail_section: str) -> Dict[str, Any]:
        """Predict bail success probability"""
        base_rate = self.base_success_rates.get(bail_section, 0.65)
        
        adjustments = 0.0
        
        if case_data.get("criminal_history", []):
            adjustments -= 0.1
        
        if case_data.get("first_time_offender", False):
            adjustments += 0.05
        
        if case_data.get("dependent_children", 0) > 0:
            adjustments += 0.05
        
        if case_data.get("employment_status", False):
            adjustments += 0.03
        
        final_probability = min(1.0, max(0.0, base_rate + adjustments))
        
        return {
            "predicted_success_rate": round(final_probability, 2),
            "base_rate": base_rate,
            "adjustments": adjustments,
            "confidence": "HIGH" if final_probability > 0.8 else "MEDIUM" if final_probability > 0.5 else "LOW"
        }
    
    def generate_analytics_report(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive analytics report"""
        return {
            "detention_analysis": {
                "days_detained": case_data.get("detention_days", 0),
                "legal_limit": case_data.get("max_sentence_days", 0) / 2,
                "status": "ILLEGAL" if case_data.get("detention_days", 0) > case_data.get("max_sentence_days", 0) / 2 else "LEGAL"
            },
            "bail_probability": self.predict_success(case_data, case_data.get("primary_bail_section", "437")),
            "recommendation": "APPLY FOR BAIL IMMEDIATELY"
        }
