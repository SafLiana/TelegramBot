import logging
import requests
import uuid
import time
from config import GIGACHAT_CREDENTIALS, GIGACHAT_AUTH_URL, GIGACHAT_API_URL

logger = logging.getLogger(__name__)


class GigaChatAPI:
    def __init__(self):
        self.access_token = None
        self.token_expires = 0
        self.auth_key = GIGACHAT_CREDENTIALS

    def _get_access_token(self):
        try:
            if self.access_token and time.time() < self.token_expires:
                logger.info("Используем существующий токен")
                return self.access_token

            logger.info("Запрашиваем новый токен у GigaChat...")

            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
                'RqUID': str(uuid.uuid4()),
                'Authorization': f'Basic {self.auth_key}'
            }

            data = {'scope': 'GIGACHAT_API_PERS'}

            response = requests.post(
                GIGACHAT_AUTH_URL,
                headers=headers,
                data=data,
                verify=False,
                timeout=30
            )

            if response.status_code == 200:
                token_data = response.json()

                if 'access_token' in token_data:
                    self.access_token = token_data['access_token']

                    if 'expires_at' in token_data:
                        self.token_expires = token_data['expires_at']
                    elif 'expires_in' in token_data:
                        self.token_expires = time.time() + token_data['expires_in'] - 60
                    else:
                        self.token_expires = time.time() + 1800 - 60

                    logger.info("✅ Успешно получили новый Access Token")
                    return self.access_token
                else:
                    logger.error(f"В ответе нет access_token: {token_data}")
                    return None
            else:
                logger.error(f"Ошибка получения токена: {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"Ошибка при получении токена: {e}")
            return None

    def send_prompt(self, system_prompt, user_prompt, temperature=0.7, max_tokens=2048):
        """Отправка промпта в GigaChat"""
        try:
            token = self._get_access_token()
            if not token:
                return None

            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

            payload = {
                "model": "GigaChat-Pro",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": temperature,
                "max_tokens": max_tokens
            }

            response = requests.post(
                GIGACHAT_API_URL,
                json=payload,
                headers=headers,
                verify=False,
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                if ('choices' in result and len(result['choices']) > 0 and
                        'message' in result['choices'][0] and
                        'content' in result['choices'][0]['message']):
                    return result['choices'][0]['message']['content']

            logger.error(f"Ошибка API GigaChat: {response.status_code}")
            return None

        except Exception as e:
            logger.error(f"Ошибка при отправке промпта: {e}")
            return None