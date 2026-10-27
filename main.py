import argparse
import logging
import sys
from pathlib import Path

from core.fetcher import fetch_page
from core.config_loader import load_site_config
from core.extractor import extract_all
from core.exporter import export_all

logger = logging.getLogger(__name__)   # ← для этого модуля


def setup_logging(log_file: str = "parser.log") -> None:
    """Настраивает логирование: в консоль (INFO) и в файл (DEBUG)."""
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)


def process_site(site_name: str) -> bool:
    """
    Обрабатывает один сайт: конфиг → HTML → данные → экспорт.
    
    Returns:
        True если успешно, False при ошибке
    """
    logger.info(f"Обработка сайта: {site_name}")

    try: 
        config = load_site_config(site_name)
        html = fetch_page(
            config["base_url"],
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            delay=config.get("request_delay", 1.0)
        )
        data = extract_all(
            html,
            config["list_selector"],
            config["fields"]
        )
        if not data:
            logger.warning(f"Нет данных для {site_name}")
            return False
        paths = export_all(data, site_name)
        logger.info(f"Сохранено: {paths['json']}")
        logger.info(f"Сохранено: {paths['csv']}")
        return True
        
    except FileNotFoundError as e:
        logger.error(f"Конфиг не найден: {e}")
        return False
    except Exception as e:
        logger.error(f"Ошибка при обработке {site_name}: {e}")
        return False



def parse_args() -> argparse.Namespace:
    """Разбирает аргументы командной строки."""
    parser = argparse.ArgumentParser(description="Парсер сайтов")
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("--site", type=str, help="Один сайт")
    group.add_argument("--sites", type=str, help="Несколько через запятую")
    group.add_argument("--all", action="store_true", help="Все сайты")

    return parser.parse_args()



def main():
    setup_logging()
    args = parse_args()

    if args.site:
        sites = [args.site]
    elif args.sites:
        sites = [s.strip() for s in args.sites.split(",")]
    else:  # --all
        sites = [f.stem for f in Path("sites").glob("*.yaml")]

    logger.info(f"Сайтов к обработке: {len(sites)} → {', '.join(sites)}")
    
    success = 0
    for site in sites:
        if process_site(site):
            success += 1

    logger.info(f"Итог: {success}/{len(sites)} сайтов обработано")


if __name__ == "__main__":
    main()