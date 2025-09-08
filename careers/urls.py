from django.urls import path
from . import views

app_name = 'careers'

urlpatterns = [
    # Список категорий
    path('categories/', views.CareerCategoryListAPIView.as_view(), name='categories_list'),
    
    # Список подразделений
    path('departments/', views.DepartmentListAPIView.as_view(), name='departments_list'),
    
    # Основные API для вакансий
    path('vacancies/', views.VacancyListAPIView.as_view(), name='vacancy_list'),
    path('vacancies/<slug:slug>/', views.VacancyDetailAPIView.as_view(), name='vacancy_detail'),
    
    # API для заявок
    path('applications/', views.VacancyApplicationCreateAPIView.as_view(), name='application_create'),
    path('applications/list/', views.VacancyApplicationListAPIView.as_view(), name='applications_list'),
    path('applications/<int:pk>/', views.VacancyApplicationDetailAPIView.as_view(), name='application_detail'),
    
    # Статистика и специальные эндпоинты
    path('stats/', views.vacancy_stats_api, name='vacancy_stats'),
    path('featured/', views.featured_vacancies_api, name='featured_vacancies'),
    path('latest/', views.latest_vacancies_api, name='latest_vacancies'),
    path('expiring-soon/', views.expiring_soon_vacancies_api, name='expiring_soon_vacancies'),
]
