import csv
import json
import logging
from pathlib import Path
from typing import Any, Dict, List


logger = logging.getLogger(__name__)


def save_json(data: List[Dict[str, Any]], site_name: str, output_dir: str = "output") -> Path:
    """
    Сохраняет данные в JSON-файл.
    
    Args:
        data: список словарей
        site_name: имя сайта (для имени файла)
        output_dir: папка для сохранения
    
    Returns:
        Path к сохранённому файлу
    """
    if not data:
        logger.warning("Нет данных для JSON")
        return Path()
    
    Path(output_dir).mkdir(exist_ok=True)
    filepath = Path(output_dir) / f"{site_name}.json"
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    logger.info(f"JSON сохранён: {filepath} ({len(data)} записей)")
    return filepath

 
def save_csv(data: List[Dict[str, Any]], site_name: str, output_dir: str = "output") -> Path:
    """
    Сохраняет данные в CSV-файл.
    
    Списки превращаются в строки через ", ".join(...).
    
    Args:
        data: список словарей
        site_name: имя сайта (для имени файла)
        output_dir: папка для сохранения
    
    Returns:
        Path к сохранённому файлу
    """
    if not data:
        return Path()
    
    # 2. Создать папку
    Path(output_dir).mkdir(exist_ok=True)
    
    # 3. Путь к файлу
    filepath = Path(output_dir) / f"{site_name}.csv"
    
    # 4. Колонки = ключи первого словаря
    fieldnames = list(data[0].keys())
    
    # 5. Открыть файл
    with open(filepath, "w", encoding="utf-8", newline="") as f:
        # 6. Создать писателя CSV
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        # 7. Записать заголовки
        writer.writeheader()
        
        # 8. Пройти по строкам
        for row in data:
            clean_row = {}
            for key, value in row.items():
                # 9. Если список — в строку
                if isinstance(value, list):
                    clean_row[key] = ", ".join(str(v) for v in value)
                else:
                    clean_row[key] = value
            # 10. Записать строку
            writer.writerow(clean_row)
    
    logger.info(f"CSV сохранён: {filepath}")
    return filepath
    

def export_all(data: List[Dict[str, Any]], site_name: str, output_dir: str = "output") -> Dict[str, Path]:
    """
    Сохраняет данные в JSON и CSV.
    
    Args:
        data: список словарей
        site_name: имя сайта
        output_dir: папка для сохранения
    
    Returns:
        Словарь {формат: путь к файлу}
    """
    json_path = save_json(data, site_name,output_dir)
    csv_path = save_csv(data, site_name,output_dir)

    return json_path, csv_path