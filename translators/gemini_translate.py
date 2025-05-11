import json
import requests
from typing import List
from google import genai
from .base import BaseTranslator, TranslationResult, TranslatorFactory


class GeminiTranslator(BaseTranslator):
    """Google Gemini API based translator implementation using official genai library."""
    
    def __init__(self, api_key: str, model: str = 'gemini-2.0-flash', merge: bool = True):
        self.merge = merge
        self.model = model
        self.client = genai.Client(api_key=api_key)
    
    def translate(self, text: str, target_language: str, source_language: str = None) -> TranslationResult:
        try:
            prompt = f"Translate the following text to {target_language}. Provide only the translation, no explanations:\n{text}"
            response = self.client.models.generate_content(
                model = self.model,
                contents = prompt
            )
            
            translated_text = response.text.strip()
            print(translated_text)
            return TranslationResult(
                original_text=text,
                translated_text=translated_text,
                target_language=target_language,
                metadata={'provider': 'gemini', 'model': self.model}
            )
        except Exception as e:
            print(f"Gemini translation error: {e}")
            return TranslationResult(
                original_text=text,
                translated_text=text,
                target_language=target_language,
                metadata={'error': str(e), 'provider': 'gemini'}
            )
    
    def batch_translate(self, texts: List[str], target_language: str, source_language: str = None) -> List[TranslationResult]:
        results = []
        for text in texts:
            result = self.translate(text, target_language, source_language)
            results.append(result)
        return results
