import logging
from gigachat_api import GigaChatAPI

logger = logging.getLogger(__name__)


class TravelGuide(GigaChatAPI):

    def generate_route(self, city):
        try:
            logger.info(f"Начинаем генерацию маршрута для города: {city}")

            system_prompt = "Ты опытный гид. Отвечай на русском языке, используй эмодзи для оформления."

            user_prompt = f"""Ты профессиональный гид-экскурсовод. Составь подробный туристический маршрут по городу {city}.

            Требования к маршруту:
            📍 Перечисли ТОП-10 самых интересных мест города
            📝 Для каждого места укажи:
               • Название
               • Почему это место стоит посетить
               • Интересный факт
               • Практический совет (лучшее время, стоимость, лайфхак)
            🍜 Добавь рекомендации по местной кухне

            Оформи ответ красиво, используя эмодзи.
            Ответ дай на русском языке в структурированном виде."""

            response = self.send_prompt(system_prompt, user_prompt)

            if response:
                logger.info(f"Маршрут получен, длина: {len(response)} символов")
                return response
            else:
                logger.error(f"Не удалось получить маршрут для города {city}")
                return None

        except Exception as e:
            logger.error(f"Ошибка при генерации маршрута: {e}")
            return None