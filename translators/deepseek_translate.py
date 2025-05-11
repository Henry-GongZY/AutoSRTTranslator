import json
import requests
from typing import List
from google import genai
from .base import BaseTranslator, TranslationResult, TranslatorFactory


class DeepSeekTranslator(BaseTranslator):
    """DeepSeek API based translator implementation."""
    
    def __init__(self, api_key: str, model: str = 'deepseek-chat', merge: bool = True):
        self.merge = merge
        self.api_key = api_key
        self.model = model
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    def translate(self, text: str, target_language: str, source_language: str = None) -> TranslationResult:
        try:
            messages = [
                {"role": "system", "content": f"You are a translator. Translate the following text to {target_language}. Provide only the translation, no explanations."},
                {"role": "user", "content": text}
            ]
            
            response = requests.post(
                'https://api.deepseek.com/v1/chat/completions',
                headers=self.headers,
                json={
                    'model': self.model,
                    'messages': messages,
                    'temperature': 0.3
                }
            )
            response.raise_for_status()
            
            translated_text = response.json()['choices'][0]['message']['content'].strip()
            return TranslationResult(
                original_text=text,
                translated_text=translated_text,
                target_language=target_language,
                metadata={'provider': 'deepseek', 'model': self.model}
            )
        except Exception as e:
            print(f"DeepSeek translation error: {e}")
            return TranslationResult(
                original_text=text,
                translated_text=text,
                target_language=target_language,
                metadata={'error': str(e), 'provider': 'deepseek'}
            )
