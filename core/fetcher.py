import time
import logging
import requests

logger = logging.getLogger(__name__)

def fetch_page(url: str, user_agent: str, delay: float = 1.0) -> str:
    """
    Загружает HTML-страницу по URL.
    
    Args:
        url: адрес страницы
        user_agent: строка User-Agent
        delay: пауза после запроса (сек)
    
    Returns:
        HTML-код страницы (строка)
    
    Raises:
        requests.HTTPError: сервер вернул 4xx/5xx
        requests.RequestException: таймаут или ошибка соединения
    """
    logger.info(f"Загрузка: {url}")

    headers = {"User-Agent": user_agent}

    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        response.raise_for_status()
       
    except requests.HTTPError as e:
        logger.error(f"HTTP-ошибка: {e}")
        raise
    except requests.RequestException as e:
        logger.error(f"Ошибка соединения: {e}")
        raise

    time.sleep(delay)
    logger.info(f"Загружено: {len(response.text)} символов")

    return response.text
