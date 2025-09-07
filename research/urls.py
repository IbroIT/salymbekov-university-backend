from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Создаем роутер для ViewSets
router = DefaultRouter()
router.register(r'areas', views.ResearchAreaViewSet, basename='researcharea')
router.register(r'centers', views.ResearchCenterViewSet, basename='researchcenter')
router.register(r'grants', views.GrantViewSet, basename='grant')
router.register(r'conferences', views.ConferenceViewSet, basename='conference')
router.register(r'publications', views.PublicationViewSet, basename='publication')

app_name = 'research'

urlpatterns = [
    # API endpoints через router
    path('api/', include(router.urls)),
    
    # Заявки на гранты
    path('api/grant-applications/', views.GrantApplicationCreateView.as_view(), name='grant-application-create'),
    path('api/grant-applications/list/', views.GrantApplicationListView.as_view(), name='grant-application-list'),
    
    # Статистика
    path('api/stats/', views.research_stats, name='research-stats'),
    path('api/stats/grants/', views.grant_stats_by_category, name='grant-stats'),
    path('api/stats/publications/', views.publication_stats_by_type, name='publication-stats'),
    
    # Поиск
    path('api/search/', views.search_all, name='search-all'),
]

"""
Доступные API endpoints:

ОБЛАСТИ ИССЛЕДОВАНИЙ:
GET /research/api/areas/ - список областей исследований
GET /research/api/areas/{id}/ - детали области исследований

ИССЛЕДОВАТЕЛЬСКИЕ ЦЕНТРЫ:
GET /research/api/centers/ - список центров
GET /research/api/centers/{id}/ - детали центра

ГРАНТЫ:
GET /research/api/grants/ - список грантов
GET /research/api/grants/{id}/ - детали гранта
GET /research/api/grants/active/ - активные гранты
GET /research/api/grants/upcoming/ - предстоящие гранты
GET /research/api/grants/deadline_soon/ - гранты с близким дедлайном

Параметры фильтрации для грантов:
- category: youth, international, fundamental, applied, innovative, clinical
- status: active, upcoming, closed
- organization: название организации
- search: поиск по названию, описанию, организации

КОНФЕРЕНЦИИ:
GET /research/api/conferences/ - список конференций
GET /research/api/conferences/{id}/ - детали конференции
GET /research/api/conferences/upcoming/ - предстоящие конференции
GET /research/api/conferences/registration_open/ - конференции с открытой регистрацией

Параметры фильтрации для конференций:
- status: registration-open, early-bird, call-for-papers, completed
- search: поиск по названию, месту, описанию

ПУБЛИКАЦИИ:
GET /research/api/publications/ - список публикаций
GET /research/api/publications/{id}/ - детали публикации
GET /research/api/publications/featured/ - рекомендуемые публикации
GET /research/api/publications/recent/ - недавние публикации
GET /research/api/publications/by_research_area/?area_id={id} - публикации по области исследований

Параметры фильтрации для публикаций:
- publication_type: article, book, conference, patent, thesis
- research_area: ID области исследований
- research_center: ID исследовательского центра
- is_featured: true/false
- search: поиск по названию, авторам, журналу

ЗАЯВКИ НА ГРАНТЫ:
POST /research/api/grant-applications/ - подача заявки на грант
GET /research/api/grant-applications/list/ - список заявок (только для авторизованных)

СТАТИСТИКА:
GET /research/api/stats/ - общая статистика
GET /research/api/stats/grants/ - статистика грантов по категориям
GET /research/api/stats/publications/ - статистика публикаций по типам

ПОИСК:
GET /research/api/search/?q={query}&lang={lang} - поиск по всем сущностям
- q: поисковый запрос (обязательный)
- lang: язык поиска (ru, en, kg, по умолчанию ru)

ПРИМЕРЫ ЗАПРОСОВ:

# Получить все активные гранты
GET /research/api/grants/active/

# Получить молодежные гранты с поиском по "медицина"
GET /research/api/grants/?category=youth&search=медицина

# Получить предстоящие конференции
GET /research/api/conferences/upcoming/

# Получить рекомендуемые публикации
GET /research/api/publications/featured/

# Подать заявку на грант
POST /research/api/grant-applications/
{
    "grant": 1,
    "project_title": "Название проекта",
    "principal_investigator": "Иван Иванов",
    "email": "ivan@example.com",
    "department": "Кафедра биологии",
    "project_description": "Описание проекта...",
    "budget": 100000,
    "timeline": 12,
    "expected_results": "Ожидаемые результаты..."
}

# Поиск по всем данным
GET /research/api/search/?q=кардиология&lang=ru

# Получить статистику
GET /research/api/stats/
"""
