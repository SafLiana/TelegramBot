import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = "8402156897:AAGRKpk-vB9MJYnlv1gS62kmJnSpFFpFHH0"
AVIASALES_API_KEY = "88db943c8b18bb11fae9e4ae19006872"
GIGACHAT_CREDENTIALS = "MDE5Y2UzZjYtY2UyZi03NjRiLWE2NWUtODM4M2UyNTBkY2YxOjQ5YzhjMzUyLTc3N2ItNDllOC04ZGJiLTM3NjI4MzVlZGY2NQ=="

GIGACHAT_AUTH_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
GIGACHAT_API_URL = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

SUPPORTED_LANGUAGES = {
    'ru': '🇷🇺 Русский',
    'en': '🇬🇧 Английский',
    'es': '🇪🇸 Испанский',
    'fr': '🇫🇷 Французский',
    'de': '🇩🇪 Немецкий',
    'it': '🇮🇹 Итальянский',
    'zh': '🇨🇳 Китайский',
    'ja': '🇯🇵 Японский',
    'ko': '🇰🇷 Корейский',
    'ar': '🇸🇦 Арабский',
    'tr': '🇹🇷 Турецкий',
    'he': '🇮🇱 Иврит',
    'hi': '🇮🇳 Хинди',
    'th': '🇹🇭 Тайский',
    'vi': '🇻🇳 Вьетнамский'
}

LANGUAGE_CODES = {
    'ru': 'ru',
    'en': 'en',
    'es': 'es',
    'fr': 'fr',
    'de': 'de',
    'it': 'it',
    'zh': 'zh',
    'ja': 'ja',
    'ko': 'ko',
    'ar': 'ar',
    'tr': 'tr',
    'he': 'he',
    'hi': 'hi',
    'th': 'th',
    'vi': 'vi'
}