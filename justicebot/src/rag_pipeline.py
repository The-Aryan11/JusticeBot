"""RAG Pipeline Module - Vector search for precedents"""

import logging
import json
from typing import List, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self, db_path: str = None):
        self.db_path = db_path
        self.precedents = []
        self.load_precedents()
    
    def load_precedents(self):
        """Load all precedent cases into memory"""
        try:
            precedents_dir = Path(__file__).parent.parent / "data" / "precedents"
            
            if precedents_dir.exists():
                for precedent_file in precedents_dir.glob("*.json"):
                    try:
                        with open(precedent_file, "r", encoding="utf-8") as f:
                            precedent = json.load(f)
                            self.precedents.append(precedent)
                    except Exception as e:
                        logger.warning(f"Could not load {precedent_file}: {e}")
        except Exception as e:
            logger.error(f"Error loading precedents: {e}")
    
    def search_relevant_precedents(self, case_section: str, bail_ground: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant precedent cases"""
        relevant = []
        
        for precedent in self.precedents:
            relevance_score = 0.0
            
            if case_section in precedent.get("applicable_sections", []):
                relevance_score += 0.5
            
            if bail_ground.lower() in str(precedent.get("key_holding", "")).lower():
                relevance_score += 0.3
            
            if relevance_score > 0:
                precedent["relevance_score"] = min(relevance_score, 1.0)
                relevant.append(precedent)
        
        relevant.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        return relevant[:top_k]
    
    def get_precedent_strength(self, precedents: List[Dict]) -> Dict[str, Any]:
        """Calculate strength of collected precedents"""
        if not precedents:
            return {"total_precedents": 0, "average_strength": 0, "strength_rating": "WEAK"}
        
        total_strength = sum(p.get("precedent_strength", 5) for p in precedents)
        avg_strength = total_strength / len(precedents)
        
        if avg_strength >= 9:
            rating = "VERY STRONG"
        elif avg_strength >= 8:
            rating = "STRONG"
        elif avg_strength >= 7:
            rating = "MODERATE"
        else:
            rating = "WEAK"
        
        return {
            "total_precedents": len(precedents),
            "average_strength": round(avg_strength, 1),
            "strength_rating": rating
        }
