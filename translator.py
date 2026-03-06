import logging
import re
from gigachat_api import GigaChatAPI
from config import SUPPORTED_LANGUAGES, LANGUAGE_CODES
from sentiment_model import sentiment_analyzer

logger = logging.getLogger(__name__)


class Translator(GigaChatAPI):
    def __init__(self):
        super().__init__()
        self.lang_names = {}
        for code, name in SUPPORTED_LANGUAGES.items():
            lang_name = name.split(' ')[1] if ' ' in name else name
            self.lang_names[lang_name] = code

    def detect_language(self, text):
        if not text:
            return 'unknown'
        if re.search('[а-яА-ЯёЁ]', text):
            return 'ru'
        elif re.search('[a-zA-Z]', text):
            return 'en'
        return 'unknown'

    def parse_language_from_text(self, text):
        try:
            if '→' not in text:
                return None, None
            parts = text.split('→')
            if len(parts) == 2:
                from_part = parts[0].strip()
                to_part = parts[1].strip()
                from_words = from_part.split()
                to_words = to_part.split()
                if from_words and to_words:
                    from_lang = from_words[-1]
                    to_lang = to_words[-1]
                    from_code = self.lang_names.get(from_lang)
                    to_code = self.lang_names.get(to_lang)
                    return from_code, to_code
        except Exception as e:
            logger.error(f"Error parsing language: {e}")
        return None, None

    def translate(self, text, from_lang='auto', to_lang='ru'):
        try:
            sentiment_result = sentiment_analyzer.analyze(text)
            sentiment = sentiment_result['sentiment']
            emoji = sentiment_result['emoji']

            logger.info(f"Sentiment: {sentiment}, confidence: {sentiment_result['confidence']:.2%}")

            source_lang = from_lang
            if from_lang == 'auto':
                detected = self.detect_language(text)
                source_lang = detected if detected in LANGUAGE_CODES else 'unknown'

            to_lang_name = 'русский'
            if to_lang in SUPPORTED_LANGUAGES:
                to_lang_name = SUPPORTED_LANGUAGES[to_lang].split(' ')[1] if ' ' in SUPPORTED_LANGUAGES[to_lang] else \
                SUPPORTED_LANGUAGES[to_lang]

            if sentiment == 'positive':
                system_prompt = "Ты переводчик. Сохрани позитивный тон."
                style = "Сохрани радостный тон, используй восклицания если есть."
            elif sentiment == 'negative':
                system_prompt = "Ты переводчик. Точно передай смысл."
                style = "Переведи точно, без лишних эмоций."
            else:
                system_prompt = "Ты переводчик."
                style = "Переведи точно."

            user_prompt = f"""{style}
Текст: {text}
Переведи на {to_lang_name}.
Только перевод."""

            response = self.send_prompt(system_prompt, user_prompt, temperature=0.3, max_tokens=1024)

            if response:
                translation = response.strip('"\'')
                if sentiment == 'negative' and sentiment_result['confidence'] > 0.7:
                    translation += "\n\n😔 Могу я вам помочь?"
                return f"{emoji} {translation}"
            else:
                return f"{emoji} [Ошибка перевода]"

        except Exception as e:
            logger.error(f"Translation error: {e}")
            return "😐 Ошибка перевода"

    def get_language_code_from_button(self, button_text):
        try:
            if ' ' not in button_text:
                return None
            lang_name = button_text.split(' ')[1]
            return self.lang_names.get(lang_name)
        except:
            return None


translator = Translator()