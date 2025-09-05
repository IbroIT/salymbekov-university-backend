from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    NewsViewSet, EventViewSet, AnnouncementViewSet,
    NewsCategoryViewSet, NewsTagViewSet,
    NewsStatsView, SearchAllView
)

app_name = 'news'

# Создаем роутер для ViewSets
router = DefaultRouter()
router.register(r'categories', NewsCategoryViewSet, basename='category')
router.register(r'tags', NewsTagViewSet, basename='tag')
router.register(r'news', NewsViewSet, basename='news')
router.register(r'events', EventViewSet, basename='event')
router.register(r'announcements', AnnouncementViewSet, basename='announcement')

urlpatterns = [
    # ViewSets через роутер
    path('', include(router.urls)),
    
    # Дополнительные эндпоинты
    path('stats/', NewsStatsView.as_view(), name='news-stats'),
    path('search/', SearchAllView.as_view(), name='search-all'),
]

# Итоговые URL patterns:
# GET /news/api/categories/ - список категорий
# GET /news/api/categories/{slug}/ - детали категории
# 
# GET /news/api/tags/ - список тегов
# POST /news/api/tags/ - создать тег
# GET /news/api/tags/{slug}/ - детали тега
# PUT /news/api/tags/{slug}/ - обновить тег
# DELETE /news/api/tags/{slug}/ - удалить тег
#
# GET /news/api/news/ - список новостей
# POST /news/api/news/ - создать новость
# GET /news/api/news/{slug}/ - детали новости
# PUT /news/api/news/{slug}/ - обновить новость
# DELETE /news/api/news/{slug}/ - удалить новость
# GET /news/api/news/featured/ - рекомендуемые новости
# GET /news/api/news/pinned/ - закрепленные новости
# GET /news/api/news/popular/ - популярные новости
# GET /news/api/news/by_category/?category={slug} - новости по категории
#
# GET /news/api/events/ - список событий
# POST /news/api/events/ - создать событие
# GET /news/api/events/{news__slug}/ - детали события
# PUT /news/api/events/{news__slug}/ - обновить событие
# DELETE /news/api/events/{news__slug}/ - удалить событие
# GET /news/api/events/upcoming/ - предстоящие события
# GET /news/api/events/past/ - прошедшие события
# GET /news/api/events/this_month/ - события этого месяца
#
# GET /news/api/announcements/ - список объявлений
# POST /news/api/announcements/ - создать объявление
# GET /news/api/announcements/{news__slug}/ - детали объявления
# PUT /news/api/announcements/{news__slug}/ - обновить объявление
# DELETE /news/api/announcements/{news__slug}/ - удалить объявление
# GET /news/api/announcements/pinned/ - закрепленные объявления
# GET /news/api/announcements/urgent/ - срочные объявления
# GET /news/api/announcements/by_type/?type={type} - объявления по типу
# GET /news/api/announcements/for_students/ - объявления для студентов
#
# GET /news/api/stats/ - статистика
# GET /news/api/search/?q={query} - поиск по всем типам контента
