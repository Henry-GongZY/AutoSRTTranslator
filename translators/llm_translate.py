import json
import requests
from typing import List
from google import genai
from . import BaseTranslator, TranslationResult, TranslatorFactory

class OpenAITranslator(BaseTranslator):
    """OpenAI API based translator implementation."""
    
    def __init__(self, api_key: str, model: str = 'gpt-3.5-turbo'):
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
                'https://api.openai.com/v1/chat/completions',
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
                metadata={'provider': 'openai', 'model': self.model}
            )
        except Exception as e:
            print(f"OpenAI translation error: {e}")
            return TranslationResult(
                original_text=text,
                translated_text=text,
                target_language=target_language,
                metadata={'error': str(e), 'provider': 'openai'}
            )


class GeminiTranslator(BaseTranslator):
    """Google Gemini API based translator implementation using official genai library."""
    
    def __init__(self, api_key: str, model: str = 'gemini-2.0-flash'):
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

class DeepSeekTranslator(BaseTranslator):
    """DeepSeek API based translator implementation."""
    
    def __init__(self, api_key: str, model: str = 'deepseek-chat'):
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

# Register the translators
TranslatorFactory.register('openai', OpenAITranslator)
TranslatorFactory.register('gemini', GeminiTranslator)
TranslatorFactory.register('deepseek', DeepSeekTranslator)