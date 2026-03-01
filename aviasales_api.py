import logging
import requests
from datetime import datetime
from config import AVIASALES_API_KEY

logger = logging.getLogger(__name__)


class FlightSearcher:
    AIRLINE_EMOJIS = {
        'SU': '🇷🇺', 'S7': '🟢', 'UT': '🔵', 'U6': '🔴',
        'TK': '🇹🇷', 'EK': '🇦🇪', 'EY': '🇦🇪', 'QR': '🇶🇦',
        'LH': '🇩🇪', 'AF': '🇫🇷', 'KL': '🇳🇱', 'BA': '🇬🇧',
    }

    def search_flights(self, origin, destination, date):
        try:
            url = "https://api.travelpayouts.com/aviasales/v3/prices_for_dates"
            params = {
                "origin": origin,
                "destination": destination,
                "departure_at": date,
                "currency": "rub",
                "token": AVIASALES_API_KEY,
                "limit": 10,
                "sorting": "price"
            }

            logger.info(f"Ищем билеты: {origin} -> {destination} на {date}")
            response = requests.get(url, params=params, timeout=10)
            data = response.json()

            if response.status_code == 200 and data.get('data'):
                return self._format_flights_list(data['data'][:7], origin, destination, date)
            else:
                return self._format_no_flights(origin, destination, date)

        except Exception as e:
            logger.error(f"Ошибка поиска билетов: {e}")
            return self._format_error(e)

    def _format_flight_info(self, flight):
        airline_code = flight.get('airline', '??')
        airline_emoji = self.AIRLINE_EMOJIS.get(airline_code, '✈️')

        price = int(flight.get('price', 0))
        formatted_price = f"{price:,}".replace(",", " ")

        transfers = flight.get('transfers', 0)
        if transfers == 0:
            transfer_text = "🔴 Прямой рейс"
        elif transfers == 1:
            transfer_text = "🟡 1 пересадка"
        else:
            transfer_text = f"🟢 {transfers} пересадки"

        flight_info = (
            f"{airline_emoji} <b>Авиакомпания:</b> {airline_code}\n"
            f"💰 <b>Цена:</b> {formatted_price} ₽\n"
            f"{transfer_text}\n"
        )

        departure_at = flight.get('departure_at')
        if departure_at:
            try:
                dt = datetime.fromisoformat(departure_at.replace('Z', '+00:00'))
                flight_info += f"🛫 Вылет: {dt.strftime('%d.%m.%Y %H:%M')}\n"
            except:
                pass

        return flight_info

    def _format_flights_list(self, flights, origin, destination, date):
        header = (
            f"🛫 <b>НАЙДЕННЫЕ БИЛЕТЫ</b>\n\n"
            f"<b>Маршрут:</b> {origin} ✈️ {destination}\n"
            f"<b>Дата:</b> {date}\n\n"
        )

        flights_info = [self._format_flight_info(flight) for flight in flights]
        return header + "\n".join(flights_info)

    def _format_no_flights(self, origin, destination, date):
        return (
            f"❌ <b>БИЛЕТЫ НЕ НАЙДЕНЫ</b>\n\n"
            f"Маршрут: {origin} ✈️ {destination}\n"
            f"Дата: {date}\n\n"
            f"💡 <b>Советы:</b>\n"
            f"• Попробуйте изменить дату\n"
            f"• Проверьте правильность кодов городов\n"
            f"• Поищите билеты на ближайшие даты"
        )

    def _format_error(self, error):
        return (
            f"⚠️ <b>ОШИБКА ПОИСКА</b>\n\n"
            f"Произошла ошибка при поиске билетов.\n"
            f"Пожалуйста, попробуйте позже.\n\n"
            f"❌ Детали: {str(error)[:100]}"
        )