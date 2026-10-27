import logging
from typing import List

from core.fetcher import fetch_page
from core.extractor import extract_all

"""
Модуль обхода страниц.

Отвечает за:
    - Генерацию URL для пагинации
    - Обход всех страниц списка
    - Извлечение данных с каждой страницы
"""

logger = logging.getLogger(__name__)

def get_page_urls(base_url: str, max_pages: int = 3) -> List[str]:
    """
    Генерирует URL всех страниц списка.
    
    Args:
        base_url: базовый URL (например, https://habr.com/ru/articles/)
        max_pages: сколько страниц собрать
    
    Returns:
        Список URL
    """

    base = base_url.rstrip("/")

    urls = []

    for page in range(1, max_pages +1):
        if page == 1:
            urls.append(f"{base}/")
        else:
            urls.append(f"{base}/page{page}/")

    return urls