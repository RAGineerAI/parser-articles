import logging
from pathlib import Path
from typing import Any, Dict

import yaml

logger = logging.getLogger(__name__)

REQUIRED_FIELDS = ["name", "base_url", "list_selector", "fields"]

def load_site_config(site_name: str, sites_dir: str = "sites") -> Dict[str, Any]:
    """
    Загружает конфиг сайта из YAML и валидирует обязательные поля.
    
    Args:
        site_name: имя сайта (без .yaml)
        sites_dir: папка с конфигами
    
    Returns:
        Словарь с настройками сайта
    
    Raises:
        FileNotFoundError: если YAML не найден
        ValueError: если отсутствуют обязательные поля
    """
    config_path = Path(sites_dir) / f"{site_name}.yaml"
    if not config_path.exists():
        logger.error(f"Конфигурационный файл {site_name}.yaml отсутствует ")
        raise FileNotFoundError(f"Конфигурационный файл {site_name}.yaml отсутствует ")

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    if not config:
        logger.error(f"Конфиг пустой: {config_path}")
        raise ValueError(f"Конфиг пустой: {config_path}")

    missing = [field for field in REQUIRED_FIELDS if field not in config]
    if missing:
        logger.error(f"В конфиге {config_path} отсутствуют поля: {', '.join(missing)}")
        raise ValueError(f"В конфиге {config_path} отсутствуют поля: {', '.join(missing)}")
    logger.info(f"Конфиг загружен: {config_path}")
    return config
