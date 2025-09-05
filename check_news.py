#!/usr/bin/env python
import os
import sys
import django

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_su_m.settings')
django.setup()

from news.models import News

def check_news():
    print("=== Новости в базе данных ===")
    news_list = News.objects.all()
    if not news_list:
        print("❌ Новостей не найдено!")
    else:
        for news in news_list:
            print(f"ID: {news.id}")
            print(f"Slug: {news.slug}")
            print(f"Title: {news.title}")
            print(f"Published: {news.is_published}")
            print("-" * 40)
    
    print(f"\nВсего новостей: {news_list.count()}")
    print(f"Опубликованных: {News.objects.filter(is_published=True).count()}")

if __name__ == '__main__':
    check_news()
