from .base import BaseTranslator, TranslationResult, TranslatorFactory

# Import all translator implementations
from .google_translate import GoogleTranslator
from .bing_translate import BingTranslator
from .yandex_translate import YandexTranslator
from .llm_translate import OpenAITranslator, GeminiTranslator, DeepSeekTranslator

# Register all available translators
TranslatorFactory.register('google', GoogleTranslator)
TranslatorFactory.register('bing', BingTranslator)
TranslatorFactory.register('yandex', YandexTranslator)
TranslatorFactory.register('openai', OpenAITranslator)
TranslatorFactory.register('gemini', GeminiTranslator)
TranslatorFactory.register('deepseek', DeepSeekTranslator)