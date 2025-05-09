from abc import ABC, abstractmethod
from typing import List, Dict, Type
from dataclasses import dataclass

@dataclass
class TranslationResult:
    original_text: str
    translated_text: str
    source_language: str = ''
    target_language: str = ''
    metadata: Dict = None

class BaseTranslator(ABC):
    """Base class for all translator implementations."""
    
    @abstractmethod
    def translate(self, text: str, target_language: str, source_language: str = None) -> TranslationResult:
        """Translate text to target language."""
        pass

    # @abstractmethod
    # def batch_translate(self, texts: List[str], target_language: str, source_language: str = None) -> List[TranslationResult]:
    #     """Translate multiple texts in batch."""
    #     return [self.translate(text, target_language, source_language) for text in texts]

class TranslatorFactory:
    """Factory class for creating translator instances."""
    
    _translators: Dict[str, Type[BaseTranslator]] = {}
    
    @classmethod
    def register(cls, name: str, translator_class: Type[BaseTranslator]):
        """Register a new translator implementation."""
        cls._translators[name] = translator_class
    
    @classmethod
    def create(cls, name: str, **kwargs) -> BaseTranslator:
        """Create a translator instance by name."""
        if name not in cls._translators:
            raise ValueError(f"Translator '{name}' not found. Available translators: {list(cls._translators.keys())}")
        return cls._translators[name](**kwargs)
    
    @classmethod
    def available_translators(cls) -> List[str]:
        """Get list of available translator names."""
        return list(cls._translators.keys())