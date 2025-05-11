import requests
from typing import List
from .base import BaseTranslator, TranslationResult, TranslatorFactory

class YandexTranslator(BaseTranslator):
    """Yandex Translate API implementation."""
    
    def __init__(self, api_key: str):
        """Initialize with Yandex Translate API key."""
        self.api_key = api_key
        self.base_url = 'https://translate.api.cloud.yandex.net/translate/v2'
        self.headers = {
            'Authorization': f'Api-Key {api_key}',
            'Content-Type': 'application/json'
        }
    
    def translate(self, text: str, target_language: str, source_language: str = None) -> TranslationResult:
        try:
            url = f"{self.base_url}/translate"
            body = {
                'texts': [text],
                'targetLanguageCode': target_language,
            }
            if source_language:
                body['sourceLanguageCode'] = source_language
            
            response = requests.post(url, headers=self.headers, json=body)
            response.raise_for_status()
            
            result = response.json()['translations'][0]
            return TranslationResult(
                original_text=text,
                translated_text=result['text'],
                source_language=result.get('detectedLanguageCode', source_language),
                target_language=target_language,
                metadata={'provider': 'yandex'}
            )
        except Exception as e:
            print(f"Yandex Translate error: {e}")
            return TranslationResult(
                original_text=text,
                translated_text=text,
                target_language=target_language,
                metadata={'error': str(e), 'provider': 'yandex'}
            )
    
    def batch_translate(self, texts: List[str], target_language: str, source_language: str = None) -> List[TranslationResult]:
        try:
            url = f"{self.base_url}/translate"
            body = {
                'texts': texts,
                'targetLanguageCode': target_language,
            }
            if source_language:
                body['sourceLanguageCode'] = source_language
            
            response = requests.post(url, headers=self.headers, json=body)
            response.raise_for_status()
            
            results = []
            for text, translation in zip(texts, response.json()['translations']):
                results.append(TranslationResult(
                    original_text=text,
                    translated_text=translation['text'],
                    source_language=translation.get('detectedLanguageCode', source_language),
                    target_language=target_language,
                    metadata={'provider': 'yandex'}
                ))
            return results
        except Exception as e:
            print(f"Yandex Translate batch error: {e}")
            return [
                TranslationResult(
                    original_text=text,
                    translated_text=text,
                    target_language=target_language,
                    metadata={'error': str(e), 'provider': 'yandex'}
                )
                for text in texts
            ]

# Register the translator
TranslatorFactory.register('yandex', YandexTranslator)