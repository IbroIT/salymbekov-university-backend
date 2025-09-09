#!/usr/bin/env python
"""
Скрипт для обновления существующих данных с добавлением мультиязычности
"""

import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_su_m.settings')
django.setup()

from news.models import News, NewsCategory, NewsTag
from careers.models import CareerCategory, Department, Vacancy
from research.models import ResearchArea, ResearchCenter, Grant, Conference, Publication

def update_news_data():
    """Обновление данных новостей"""
    print("Обновление данных новостей...")
    
    # Обновляем категории новостей
    categories = NewsCategory.objects.all()
    for category in categories:
        if not category.name_ru:
            category.name_ru = category.get_name_display()
            category.name_kg = category.get_name_display()  # Заглушка
            category.name_en = category.get_name_display()  # Заглушка
            category.save()
    
    print(f"Обновлено {categories.count()} категорий новостей")
    
    # Обновляем теги
    tags = NewsTag.objects.all()
    for tag in tags:
        if not tag.name_ru:
            tag.name_ru = "Тег"  # Заглушка
            tag.name_kg = "Тег"  # Заглушка
            tag.name_en = "Tag"  # Заглушка
            tag.save()
    
    print(f"Обновлено {tags.count()} тегов")

def update_careers_data():
    """Обновление данных карьер"""
    print("Обновление данных карьер...")
    
    # Обновляем категории карьер
    categories = CareerCategory.objects.all()
    for category in categories:
        if not category.display_name_ru:
            category.display_name_ru = category.get_name_display()
            category.display_name_kg = category.get_name_display()  # Заглушка
            category.display_name_en = category.get_name_display()  # Заглушка
            category.save()
    
    print(f"Обновлено {categories.count()} категорий карьер")
    
    # Обновляем подразделения
    departments = Department.objects.all()
    for dept in departments:
        if not dept.name_ru:
            dept.name_ru = "Подразделение"  # Заглушка
            dept.name_kg = "Бөлүм"  # Заглушка
            dept.name_en = "Department"  # Заглушка
            dept.save()
    
    print(f"Обновлено {departments.count()} подразделений")

def main():
    """Основная функция"""
    print("Начинаем обновление мультиязычных данных...")
    
    try:
        update_news_data()
        update_careers_data()
        
        print("\n✅ Обновление завершено успешно!")
        print("\n📝 Рекомендации:")
        print("1. Зайдите в админ-панель Django")
        print("2. Заполните корректные переводы для всех языков")
        print("3. Обновите API сериализаторы для поддержки мультиязычности")
        print("4. Обновите фронтенд для работы с тремя языками")
        
    except Exception as e:
        print(f"❌ Ошибка при обновлении: {e}")

if __name__ == "__main__":
    main()
