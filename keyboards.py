from telegram import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    keyboard = [
        [KeyboardButton("🔍 Поиск билетов")],
        [KeyboardButton("🗺️ Составить маршрут (ИИ)")],
        [KeyboardButton("🌐 Переводчик"), KeyboardButton("❓ Помощь")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_back_keyboard():
    keyboard = [[KeyboardButton("🔙 Главное меню")]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_translate_keyboard():
    keyboard = [
        [KeyboardButton("🇷🇺 Русский → 🇬🇧 Английский")],
        [KeyboardButton("🇬🇧 Английский → 🇷🇺 Русский")],
        [KeyboardButton("🇷🇺 Русский → 🇪🇸 Испанский")],
        [KeyboardButton("🇪🇸 Испанский → 🇷🇺 Русский")],
        [KeyboardButton("🇫🇷 Французский → 🇷🇺 Русский")],
        [KeyboardButton("🇩🇪 Немецкий → 🇷🇺 Русский")],
        [KeyboardButton("🇨🇳 Китайский → 🇷🇺 Русский")],
        [KeyboardButton("🔄 Другой язык"), KeyboardButton("🔙 Главное меню")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_language_selection_keyboard():
    keyboard = [
        [KeyboardButton("🇬🇧 Английский"), KeyboardButton("🇪🇸 Испанский"), KeyboardButton("🇫🇷 Французский")],
        [KeyboardButton("🇩🇪 Немецкий"), KeyboardButton("🇮🇹 Итальянский"), KeyboardButton("🇨🇳 Китайский")],
        [KeyboardButton("🇯🇵 Японский"), KeyboardButton("🇰🇷 Корейский"), KeyboardButton("🇹🇷 Турецкий")],
        [KeyboardButton("🇦🇪 Арабский"), KeyboardButton("🇮🇱 Иврит"), KeyboardButton("🇹🇭 Тайский")],
        [KeyboardButton("🔙 Назад к переводчику")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)