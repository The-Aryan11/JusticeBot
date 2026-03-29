"""LLM Utilities - Multi-provider fallback system"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.current_provider = None
    
    def chat(self, system: str, user_message: str, temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """Chat with LLM using fallback chain"""
        try:
            return self._call_groq(system, user_message, temperature, max_tokens)
        except:
            try:
                return self._call_gemini(system, user_message, temperature, max_tokens)
            except:
                try:
                    return self._call_together(system, user_message, temperature, max_tokens)
                except:
                    return "Error: All LLM providers failed. Please try again."
    
    def _call_groq(self, system: str, user_message: str, temperature: float, max_tokens: int) -> str:
        """Call Groq API"""
        from groq import Groq
        client = Groq(api_key=self.config.get("GROQ_API_KEY"))
        
        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user_message}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        self.current_provider = "groq"
        return response.choices[0].message.content
    
    def _call_gemini(self, system: str, user_message: str, temperature: float, max_tokens: int) -> str:
        """Call Google Gemini API"""
        import google.generativeai as genai
        genai.configure(api_key=self.config.get("GEMINI_API_KEY"))
        
        model = genai.GenerativeModel("gemini-1.5-flash")
        full_prompt = f"{system}

{user_message}"
        response = model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens
            )
        )
        
        self.current_provider = "gemini"
        return response.text
    
    def _call_together(self, system: str, user_message: str, temperature: float, max_tokens: int) -> str:
        """Call Together AI API"""
        import together
        together.api_key = self.config.get("TOGETHER_API_KEY")
        
        full_prompt = f"{system}

{user_message}"
        response = together.Complete.create(
            prompt=full_prompt,
            model="meta-llama/Llama-3.1-70b-instruct-Turbo",
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        self.current_provider = "together"
        return response["output"]["choices"][0]["text"]
