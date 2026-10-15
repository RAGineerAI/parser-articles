import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.fetcher import fetch_page
from core.config_loader import load_site_config
from core.extractor import extract_all

# 1. Загружаем конфиг (нужен test.yaml)
config = load_site_config("test")
print(f"🔧 Конфиг: {config['name']}")

# 2. Загружаем HTML с Habr (или другого сайта)
html = fetch_page(
    "https://habr.com/ru/articles/",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    delay=10
)
print(f"📥 Загружено: {len(html)} символов")

# 3. Извлекаем данные
results = extract_all(
    html,
    list_selector="article.tm-articles-list__item",
    fields_config={
        "title": {"selector": "a.tm-title__link", "type": "text"},
        "author": {"selector": "a.tm-user-info__username", "type": "text"},
        "link": {
            "selector": "a.tm-title__link",
            "type": "attribute",
            "attribute": "href"
        },
    }
)

print(f"✅ Извлечено: {len(results)}")
print(f"\n📊 Первые 2:")
for article in results[:2]:
    print(f"  {article}")
