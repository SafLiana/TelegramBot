import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from config import TELEGRAM_TOKEN
from keyboards import (
    get_main_keyboard, get_back_keyboard,
    get_translate_keyboard, get_language_selection_keyboard
)
from handlers import (
    start, handle_flights, handle_route, handle_translate,
    handle_translate_lang_select, handle_help, handle_back_to_main,
    handle_translation_request, USER_STATE, translator, flight_searcher, guide
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user.username or update.effective_user.first_name
    state = context.user_data.get('state', USER_STATE['MAIN'])

    logger.info(f"Пользователь {user}: {text} (state: {state})")

    if text == "🔍 Поиск билетов":
        await handle_flights(update, context)

    elif text == "🗺️ Составить маршрут (ИИ)":
        await handle_route(update, context)

    elif text == "🌐 Переводчик":
        await handle_translate(update, context)

    elif text == "❓ Помощь":
        await handle_help(update, context)

    elif text == "🔙 Главное меню":
        await handle_back_to_main(update, context)

    elif text == "🔄 Другой язык":
        await handle_translate_lang_select(update, context)

    elif text == "🔙 Назад к переводчику":
        await handle_translate(update, context)

    elif state == USER_STATE['TRANSLATE_LANG_SELECT']:
        lang_code = translator.get_language_code_from_button(text)
        if lang_code:
            context.user_data['translate_to'] = lang_code
            context.user_data['state'] = USER_STATE['TRANSLATE_CUSTOM']
            await update.message.reply_text(
                f"Отлично! Теперь отправьте текст для перевода на {text}:",
                reply_markup=get_back_keyboard()
            )
        else:
            await update.message.reply_text(
                "Пожалуйста, выберите язык из списка",
                reply_markup=get_language_selection_keyboard()
            )

    elif state == USER_STATE['TRANSLATE'] and '→' in text:
        from_lang, to_lang = translator.parse_language_from_text(text)
        if from_lang and to_lang:
            context.user_data['translate_from'] = from_lang
            context.user_data['translate_to'] = to_lang
            context.user_data['state'] = USER_STATE['TRANSLATE_CUSTOM']
            await update.message.reply_text(
                f"Отлично! Теперь отправьте текст для перевода:",
                reply_markup=get_back_keyboard()
            )
        else:
            await update.message.reply_text(
                "Пожалуйста, выберите направление из меню",
                reply_markup=get_translate_keyboard()
            )

    elif state == USER_STATE['TRANSLATE_CUSTOM']:
        to_lang = context.user_data.get('translate_to', 'ru')
        from_lang = context.user_data.get('translate_from', 'auto')
        # Убрал лишний импорт, translator уже импортирован вверху
        result = translator.translate(text, from_lang, to_lang)
        await update.message.reply_text(
            result,
            reply_markup=get_main_keyboard()
        )
        context.user_data['state'] = USER_STATE['MAIN']

    elif state == USER_STATE['FLIGHTS']:
        parts = text.split()
        if len(parts) == 3:
            await update.message.reply_text("🔎 Ищу лучшие предложения... ⏳")
            result = flight_searcher.search_flights(parts[0].upper(), parts[1].upper(), parts[2])
            await update.message.reply_text(
                result,
                parse_mode='HTML',
                reply_markup=get_main_keyboard(),
                disable_web_page_preview=True
            )
            context.user_data['state'] = USER_STATE['MAIN']
        else:
            await update.message.reply_text(
                "❌ Неверный формат. Используйте: <code>MOW LED 2026-06-01</code>",
                reply_markup=get_back_keyboard(),
                parse_mode='HTML'
            )

    elif state == USER_STATE['ROUTE']:
        await update.message.reply_text(f"🚀 Составляю маршрут для города {text}...\n")
        await update.message.chat.send_action(action="typing")

        route_plan = guide.generate_route(text)

        if route_plan:
            if len(route_plan) > 4096:
                parts = [route_plan[i:i + 4096] for i in range(0, len(route_plan), 4096)]
                for part in parts:
                    await update.message.reply_text(part)
            else:
                await update.message.reply_text(route_plan, reply_markup=get_main_keyboard())
        else:
            await update.message.reply_text(
                "❌ Временно недоступно. Пожалуйста, подождите немного и попробуйте снова.",
                reply_markup=get_main_keyboard()
            )

        context.user_data['state'] = USER_STATE['MAIN']
    else:
        await update.message.reply_text(
            "Пожалуйста, используйте кнопки меню для навигации:",
            reply_markup=get_main_keyboard()
        )


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()


if __name__ == '__main__':
    main()