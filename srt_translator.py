import re
import json
from typing import List, Dict, Optional
from dataclasses import dataclass
from translators import TranslatorFactory, TranslationResult

@dataclass
class SubtitleEntry:
    index: int
    timestamp: str
    content: str

class SRTTranslator:
    def __init__(self, translator_name: str, **translator_config):
        """Initialize the translator with specified backend.
        
        Args:
            translator_name: Name of the translator backend to use
            **translator_config: Configuration for the specified translator
        """
        self.translator = TranslatorFactory.create(translator_name, **translator_config)
    
    def parse_srt(self, file_path: str) -> List[SubtitleEntry]:
        """Parse SRT file into a list of SubtitleEntry objects."""
        entries = []
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split file into subtitle blocks
        blocks = re.split(r'\n\n+', content.strip())
        
        for block in blocks:
            lines = block.split('\n')
            if len(lines) >= 3:
                try:
                    index = int(lines[0])
                    timestamp = lines[1]
                    text = '\n'.join(lines[2:])
                    entries.append(SubtitleEntry(index, timestamp, text))
                except ValueError:
                    continue
        
        return entries
    
    def translate_srt(self, input_file: str, output_file: str, target_language: str, source_language: str = None, batch_size: int = 10):
        """Translate entire SRT file and save to new file.
        
        Args:
            input_file: Path to input SRT file
            output_file: Path to output SRT file
            target_language: Target language code
            source_language: Source language code (optional)
            batch_size: Number of subtitles to translate in each batch
        """
        entries = self.parse_srt(input_file)
        
        # Translate subtitles in batches
        for i in range(0, len(entries), batch_size):
            batch = entries[i:i + batch_size]
            texts = [entry.content for entry in batch]
            
            try:
                results = self.translator.batch_translate(texts, target_language, source_language)
                
                # Update entries with translated text
                for entry, result in zip(batch, results):
                    entry.content = result.translated_text
                    
            except Exception as e:
                print(f"Translation error in batch {i//batch_size + 1}: {e}")
                # Keep original text for failed translations
                continue
        
        # Write translated subtitles to new file
        with open(output_file, 'w', encoding='utf-8') as f:
            for entry in entries:
                f.write(f"{entry.index}\n")
                f.write(f"{entry.timestamp}\n")
                f.write(f"{entry.content}\n\n")

def main():
    # Example usage with different translation backends
    
    # Using Google Translate
    # google_translator = SRTTranslator('google', api_key='YOUR_GOOGLE_API_KEY')
    # google_translator.translate_srt('input.srt', 'output_google.srt', 'zh')
    
    # # Using Bing Translate
    # bing_translator = SRTTranslator('bing', api_key='YOUR_AZURE_API_KEY', region='global')
    # bing_translator.translate_srt('input.srt', 'output_bing.srt', 'zh')
    
    # # Using OpenAI
    # openai_translator = SRTTranslator('openai', api_key='YOUR_OPENAI_API_KEY')
    # openai_translator.translate_srt('input.srt', 'output_openai.srt', 'zh')
    
    # Using Gemini
    gemini_translator = SRTTranslator('gemini', api_key='AIzaSyCjbu2s2Ye1OO11AHNXZ8BHY6p4esLbArU')
    gemini_translator.translate_srt('input.srt', 'output_gemini.srt', 'zh')

if __name__ == '__main__':
    main()
