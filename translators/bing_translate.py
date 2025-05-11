import requests
from typing import List
from .base import BaseTranslator, TranslationResult, TranslatorFactory

class BingTranslator(BaseTranslator):
    """Microsoft Azure Translator API implementation."""
    
    def __init__(self, api_key: str, region: str = 'global'):
        """Initialize with Azure Translator API key and region."""
        self.api_key = api_key
        self.region = region
        self.base_url = 'https://api.cognitive.microsofttranslator.com'
        self.headers = {
            'Ocp-Apim-Subscription-Key': api_key,
            'Ocp-Apim-Subscription-Region': region,
            'Content-Type': 'application/json'
        }
    
    def translate(self, text: str, target_language: str, source_language: str = None) -> TranslationResult:
        try:
            url = f"{self.base_url}/translate?api-version=3.0&to={target_language}"
            if source_language:
                url += f"&from={source_language}"
            
            body = [{'text': text}]
            response = requests.post(url, headers=self.headers, json=body)
            response.raise_for_status()
            
            result = response.json()[0]['translations'][0]
            detected_language = response.json()[0].get('detectedLanguage', {}).get('language', source_language)
            
            return TranslationResult(
                original_text=text,
                translated_text=result['text'],
                source_language=detected_language,
                target_language=target_language,
                metadata={'provider': 'bing'}
            )
        except Exception as e:
            print(f"Bing Translate error: {e}")
            return TranslationResult(
                original_text=text,
                translated_text=text,
                target_language=target_language,
                metadata={'error': str(e), 'provider': 'bing'}
            )
    
    def batch_translate(self, texts: List[str], target_language: str, source_language: str = None) -> List[TranslationResult]:
        try:
            url = f"{self.base_url}/translate?api-version=3.0&to={target_language}"
            if source_language:
                url += f"&from={source_language}"
            
            body = [{'text': text} for text in texts]
            response = requests.post(url, headers=self.headers, json=body)
            response.raise_for_status()
            
            results = []
            for text, translation in zip(texts, response.json()):
                result = translation['translations'][0]
                detected_language = translation.get('detectedLanguage', {}).get('language', source_language)
                
                results.append(TranslationResult(
                    original_text=text,
                    translated_text=result['text'],
                    source_language=detected_language,
                    target_language=target_language,
                    metadata={'provider': 'bing'}
                ))
            return results
        except Exception as e:
            print(f"Bing Translate batch error: {e}")
            return [
                TranslationResult(
                    original_text=text,
                    translated_text=text,
                    target_language=target_language,
                    metadata={'error': str(e), 'provider': 'bing'}
                )
                for text in texts
            ]

# Register the translator
TranslatorFactory.register('bing', BingTranslator)