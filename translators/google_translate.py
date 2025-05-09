from typing import List
from google.cloud import translate_v2 as translate
from .base import BaseTranslator, TranslationResult, TranslatorFactory

class GoogleTranslator(BaseTranslator):
    """Google Cloud Translation API implementation."""
    
    def __init__(self, api_key: str = None):
        """Initialize with Google Cloud API key."""
        self.client = translate.Client(api_key)
    
    def translate(self, text: str, target_language: str, source_language: str = None) -> TranslationResult:
        try:
            result = self.client.translate(
                text,
                target_language=target_language,
                source_language=source_language
            )
            return TranslationResult(
                original_text=text,
                translated_text=result['translatedText'],
                source_language=result.get('detectedSourceLanguage', source_language),
                target_language=target_language,
                metadata={'provider': 'google'}
            )
        except Exception as e:
            # Log error and return original text
            print(f"Google Translate error: {e}")
            return TranslationResult(
                original_text=text,
                translated_text=text,
                target_language=target_language,
                metadata={'error': str(e), 'provider': 'google'}
            )
    
    def batch_translate(self, texts: List[str], target_language: str, source_language: str = None) -> List[TranslationResult]:
        # Google Translate API supports batch translation natively
        try:
            results = self.client.translate(
                texts,
                target_language=target_language,
                source_language=source_language
            )
            return [
                TranslationResult(
                    original_text=text,
                    translated_text=result['translatedText'],
                    source_language=result.get('detectedSourceLanguage', source_language),
                    target_language=target_language,
                    metadata={'provider': 'google'}
                )
                for text, result in zip(texts, results)
            ]
        except Exception as e:
            # Log error and return original texts
            print(f"Google Translate batch error: {e}")
            return [
                TranslationResult(
                    original_text=text,
                    translated_text=text,
                    target_language=target_language,
                    metadata={'error': str(e), 'provider': 'google'}
                )
                for text in texts
            ]

# Register the translator
TranslatorFactory.register('google', GoogleTranslator)