import logging
from typing import Dict, Any, List

from bs4 import BeautifulSoup
from bs4.element import Tag

logger = logging.getLogger(__name__)

def extract_field(
        element: Tag,
        field_name: str,
        field_config: Dict[str, Any]
) -> str:

    """
    Извлекает одно поле из HTML-элемента.
    
    Args:
        element: HTML-элемент (например, <article>)
        field_name: имя поля (для логов)
        field_config: конфиг поля из YAML
    
    Returns:
        Извлечённое значение или "" если не найдено
    """
    selector = field_config.get("selector")
    field_type = field_config.get("type", "text")

    found = element.select_one(selector)

    if found is None:
        logger.warning(f"Поле '{field_name}' не найдено: {selector}")
        return ""

    if field_type == "text":
        return found.text.strip()

    if field_type == "attribute":
        attribute_name = field_config.get("attribute")
        if not attribute_name:
            logger.warning(f"Поле '{field_name}': type=attribute, но attribute не указан")
            return ""
        value = found.get(attribute_name)
        return value.strip() if value else ""

