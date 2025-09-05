#!/usr/bin/env python
import os
import sys
import django

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_su_m.settings')
django.setup()

from news.models import News, Event, Announcement, NewsCategory
from django.utils import timezone
from datetime import timedelta, time

def create_test_data():
    # Создаем категории, если их нет
    news_cat, _ = NewsCategory.objects.get_or_create(
        name='news',
        defaults={'slug': 'news'}
    )
    events_cat, _ = NewsCategory.objects.get_or_create(
        name='events', 
        defaults={'slug': 'events'}
    )
    announcements_cat, _ = NewsCategory.objects.get_or_create(
        name='announcements',
        defaults={'slug': 'announcements'}
    )
    
    # Удаляем существующие данные
    News.objects.all().delete()
    
    # Создаем тестовые новости
    news1 = News.objects.create(
        title="Новый учебный год в Салымбеков Университете",
        title_ru="Новый учебный год в Салымбеков Университете",
        title_ky="Салымбеков университетинде жаңы окуу жылы",
        title_en="New Academic Year at Salymbekov University",
        slug="new-academic-year-2025",
        summary="Начался новый учебный год с множеством инноваций",
        summary_ru="Начался новый учебный год с множеством инноваций",
        summary_ky="Көптөгөн инновациялар менен жаңы окуу жылы башталды",
        summary_en="New academic year has started with many innovations",
        content="Университет объявляет о начале нового учебного года с множеством новых программ.",
        content_ru="Университет объявляет о начале нового учебного года с множеством новых программ.",
        content_ky="Университет көптөгөн жаңы программалар менен жаңы окуу жылынын башталышын жарыялайт.",
        content_en="The university announces the start of a new academic year with many new programs.",
        category=news_cat,
        is_published=True
    )
    
    news2 = News.objects.create(
        title="Международное сотрудничество расширяется",
        title_ru="Международное сотрудничество расширяется", 
        title_ky="Эл аралык кызматташтык кеңейип жатат",
        title_en="International Cooperation Expands",
        slug="international-cooperation-expands",
        summary="Новые соглашения с зарубежными партнерами",
        summary_ru="Новые соглашения с зарубежными партнерами",
        summary_ky="Чет элдик өнөктөштөр менен жаңы келишимдер",
        summary_en="New agreements with foreign partners",
        content="Салымбеков Университет подписал новые соглашения с зарубежными партнерами.",
        content_ru="Салымбеков Университет подписал новые соглашения с зарубежными партнерами.",
        content_ky="Салымбеков университети чет элдик өнөктөштөр менен жаңы келишимдерди кол койду.",
        content_en="Salymbekov University signed new agreements with foreign partners.",
        category=news_cat,
        is_published=True
    )
    
    # Создаем новость для события
    event_news = News.objects.create(
        title="Научная конференция",
        title_ru="Научная конференция",
        title_ky="Илимий конференция",
        title_en="Scientific Conference",
        slug="scientific-conference-2025",
        summary="Ежегодная конференция студентов",
        summary_ru="Ежегодная конференция студентов",
        summary_ky="Студенттердин жылдык конференциясы",
        summary_en="Annual student conference",
        content="Ежегодная научная конференция студентов и преподавателей.",
        content_ru="Ежегодная научная конференция студентов и преподавателей.",
        content_ky="Студенттердин жана окутуучулардын жылдык илимий конференциясы.",
        content_en="Annual scientific conference of students and teachers.",
        category=events_cat,
        is_published=True
    )
    
    # Создаем событие
    event1 = Event.objects.create(
        news=event_news,
        event_date=timezone.now().date() + timedelta(days=30),
        event_time=time(10, 0),
        end_time=time(17, 0),
        location="Главный корпус",
        event_category="conference",
        registration_required=True
    )
    
    # Создаем новость для объявления
    announcement_news = News.objects.create(
        title="Стипендиальная программа",
        title_ru="Стипендиальная программа",
        title_ky="Стипендиялык программа", 
        title_en="Scholarship Program",
        slug="scholarship-program-2025",
        summary="Прием заявок на стипендии",
        summary_ru="Прием заявок на стипендии",
        summary_ky="Стипендия үчүн арыздарды кабыл алуу",
        summary_en="Scholarship applications open",
        content="Открыт прием заявок на получение стипендии для отличников.",
        content_ru="Открыт прием заявок на получение стипендии для отличников.",
        content_ky="Мыкты окуучулар үчүн стипендия алуу үчүн арыздарды кабыл алуу ачылды.",
        content_en="Applications are open for scholarships for excellent students.",
        category=announcements_cat,
        is_published=True
    )
    
    # Создаем объявление
    announcement1 = Announcement.objects.create(
        news=announcement_news,
        announcement_type="scholarship",
        priority="high",
        deadline=timezone.now() + timedelta(days=60)
    )
    
    print("✅ Тестовые данные созданы успешно!")
    print(f"Создано новостей: {News.objects.count()}")
    print(f"Создано событий: {Event.objects.count()}")
    print(f"Создано объявлений: {Announcement.objects.count()}")
    print(f"Создано категорий: {NewsCategory.objects.count()}")

if __name__ == '__main__':
    create_test_data()
