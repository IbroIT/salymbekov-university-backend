from django.shortcuts import render
from django.db.models import Q, Count
from django.utils import translation
from django.utils.translation import activate
import logging

logger = logging.getLogger(__name__)
from rest_framework import generics, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as django_filters

from .models import CareerCategory, Department, Vacancy, VacancyApplication
from .serializers import (
    CareerCategorySerializer,
    DepartmentSerializer,
    VacancyListSerializer,
    VacancyDetailSerializer,
    VacancyApplicationSerializer,
    VacancyApplicationListSerializer,
    VacancyStatsSerializer
)


class CareerCategoryListAPIView(generics.ListAPIView):
    """API для получения списка категорий карьеры"""
    queryset = CareerCategory.objects.filter(is_active=True)
    serializer_class = CareerCategorySerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        # Активация языка из заголовков
        lang = self.request.META.get('HTTP_ACCEPT_LANGUAGE', 'ru')
        logger.info(f"CareerCategoryListAPIView - Accept-Language: {lang}")
        logger.info(f"CareerCategoryListAPIView - Current language before activation: {translation.get_language()}")
        
        if lang and lang in ['ru', 'en', 'ky']:
            activate(lang)
            logger.info(f"CareerCategoryListAPIView - Language activated: {lang}")
        
        logger.info(f"CareerCategoryListAPIView - Current language after activation: {translation.get_language()}")
        return super().get_queryset()


class DepartmentListAPIView(generics.ListAPIView):
    """API для получения списка подразделений"""
    queryset = Department.objects.filter(is_active=True)
    serializer_class = DepartmentSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        # Активация языка из заголовков
        lang = self.request.META.get('HTTP_ACCEPT_LANGUAGE', 'ru')
        logger.info(f"DepartmentListAPIView - Accept-Language: {lang}")
        logger.info(f"DepartmentListAPIView - Current language before activation: {translation.get_language()}")
        
        if lang and lang in ['ru', 'en', 'ky']:
            activate(lang)
            logger.info(f"DepartmentListAPIView - Language activated: {lang}")
        
        logger.info(f"DepartmentListAPIView - Current language after activation: {translation.get_language()}")
        return super().get_queryset()


class VacancyFilter(django_filters.FilterSet):
    """Фильтр для вакансий"""
    category = django_filters.CharFilter(field_name='category__name')
    department = django_filters.CharFilter(field_name='department__name')
    employment_type = django_filters.CharFilter()
    location = django_filters.CharFilter(lookup_expr='icontains')
    salary_min = django_filters.NumberFilter(field_name='salary_min', lookup_expr='gte')
    salary_max = django_filters.NumberFilter(field_name='salary_max', lookup_expr='lte')
    is_featured = django_filters.BooleanFilter()
    posted_after = django_filters.DateFilter(field_name='posted_date', lookup_expr='gte')
    posted_before = django_filters.DateFilter(field_name='posted_date', lookup_expr='lte')
    deadline_after = django_filters.DateFilter(field_name='deadline', lookup_expr='gte')
    deadline_before = django_filters.DateFilter(field_name='deadline', lookup_expr='lte')
    
    class Meta:
        model = Vacancy
        fields = [
            'category', 'department', 'employment_type', 
            'location', 'salary_min', 'salary_max', 
            'is_featured', 'posted_after', 'posted_before',
            'deadline_after', 'deadline_before'
        ]


class VacancyListAPIView(generics.ListAPIView):
    """API для получения списка вакансий"""
    serializer_class = VacancyListSerializer
    permission_classes = [AllowAny]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = VacancyFilter
    search_fields = ['title', 'short_description', 'description', 'tags']
    ordering_fields = ['posted_date', 'deadline', 'title', 'views_count', 'applications_count']
    ordering = ['-is_featured', '-posted_date']
    
    def get_queryset(self):
        # Активация языка из заголовков
        lang = self.request.META.get('HTTP_ACCEPT_LANGUAGE', 'ru')
        logger.info(f"VacancyListAPIView - Accept-Language: {lang}")
        logger.info(f"VacancyListAPIView - Current language before activation: {translation.get_language()}")
        
        if lang and lang in ['ru', 'en', 'ky']:
            activate(lang)
            logger.info(f"VacancyListAPIView - Language activated: {lang}")
        
        logger.info(f"VacancyListAPIView - Current language after activation: {translation.get_language()}")
            
        return Vacancy.objects.filter(
            status='published'
        ).select_related(
            'category', 'department'
        ).prefetch_related()


class VacancyDetailAPIView(generics.RetrieveAPIView):
    """API для получения детальной информации о вакансии"""
    serializer_class = VacancyDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    
    def get_queryset(self):
        # Активация языка из заголовков
        lang = self.request.META.get('HTTP_ACCEPT_LANGUAGE', 'ru')
        logger.info(f"VacancyDetailAPIView - Accept-Language: {lang}")
        logger.info(f"VacancyDetailAPIView - Current language before activation: {translation.get_language()}")
        
        if lang and lang in ['ru', 'en', 'ky']:
            activate(lang)
            logger.info(f"VacancyDetailAPIView - Language activated: {lang}")
        
        logger.info(f"VacancyDetailAPIView - Current language after activation: {translation.get_language()}")
            
        return Vacancy.objects.filter(
            status='published'
        ).select_related('category', 'department')
    
    def retrieve(self, request, *args, **kwargs):
        """Увеличиваем счетчик просмотров при получении деталей"""
        instance = self.get_object()
        
        # Увеличиваем счетчик просмотров
        Vacancy.objects.filter(pk=instance.pk).update(
            views_count=instance.views_count + 1
        )
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class VacancyApplicationCreateAPIView(generics.CreateAPIView):
    """API для подачи заявки на вакансию"""
    queryset = VacancyApplication.objects.all()
    serializer_class = VacancyApplicationSerializer
    permission_classes = [AllowAny]
    
    def perform_create(self, serializer):
        """При создании заявки увеличиваем счетчик в вакансии"""
        application = serializer.save()
        
        # Увеличиваем счетчик заявок в вакансии
        Vacancy.objects.filter(pk=application.vacancy.pk).update(
            applications_count=application.vacancy.applications_count + 1
        )


class VacancyApplicationListAPIView(generics.ListAPIView):
    """API для получения списка заявок (только для администраторов)"""
    queryset = VacancyApplication.objects.all()
    serializer_class = VacancyApplicationListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['vacancy', 'status']
    search_fields = ['first_name', 'last_name', 'email', 'vacancy__title']
    ordering_fields = ['submitted_at', 'status']
    ordering = ['-submitted_at']


class VacancyApplicationDetailAPIView(generics.RetrieveUpdateAPIView):
    """API для получения и обновления заявки (только для администраторов)"""
    queryset = VacancyApplication.objects.all()
    serializer_class = VacancyApplicationListSerializer
    permission_classes = [IsAuthenticated]


@api_view(['GET'])
@permission_classes([AllowAny])
def vacancy_stats_api(request):
    """API для получения статистики по вакансиям"""
    
    # Основная статистика
    total_vacancies = Vacancy.objects.count()
    active_vacancies = Vacancy.objects.filter(status='published').count()
    featured_vacancies = Vacancy.objects.filter(is_featured=True, status='published').count()
    total_applications = VacancyApplication.objects.count()
    
    # Статистика по категориям
    categories_stats = []
    for category in CareerCategory.objects.filter(is_active=True):
        vacancies_count = Vacancy.objects.filter(
            category=category,
            status='published'
        ).count()
        applications_count = VacancyApplication.objects.filter(
            vacancy__category=category
        ).count()
        
        categories_stats.append({
            'category_name': category.name,
            'category_display': category.display_name,
            'icon': category.icon,
            'vacancies_count': vacancies_count,
            'applications_count': applications_count
        })
    
    # Статистика по подразделениям
    departments_stats = []
    for department in Department.objects.filter(is_active=True):
        vacancies_count = Vacancy.objects.filter(
            department=department,
            status='published'
        ).count()
        applications_count = VacancyApplication.objects.filter(
            vacancy__department=department
        ).count()
        
        if vacancies_count > 0:  # Показываем только подразделения с вакансиями
            departments_stats.append({
                'department_name': department.name,
                'vacancies_count': vacancies_count,
                'applications_count': applications_count
            })
    
    data = {
        'total_vacancies': total_vacancies,
        'active_vacancies': active_vacancies,
        'featured_vacancies': featured_vacancies,
        'total_applications': total_applications,
        'categories_stats': categories_stats,
        'departments_stats': departments_stats
    }
    
    return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
def featured_vacancies_api(request):
    """API для получения рекомендуемых вакансий"""
    
    limit = request.GET.get('limit', 6)
    try:
        limit = int(limit)
    except (ValueError, TypeError):
        limit = 6
    
    vacancies = Vacancy.objects.filter(
        status='published',
        is_featured=True
    ).select_related(
        'category', 'department'
    )[:limit]
    
    serializer = VacancyListSerializer(vacancies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def latest_vacancies_api(request):
    """API для получения последних вакансий"""
    
    limit = request.GET.get('limit', 6)
    try:
        limit = int(limit)
    except (ValueError, TypeError):
        limit = 6
    
    vacancies = Vacancy.objects.filter(
        status='published'
    ).select_related(
        'category', 'department'
    ).order_by('-posted_date')[:limit]
    
    serializer = VacancyListSerializer(vacancies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def expiring_soon_vacancies_api(request):
    """API для получения вакансий с истекающим скоро сроком"""
    from datetime import date, timedelta
    
    limit = request.GET.get('limit', 6)
    try:
        limit = int(limit)
    except (ValueError, TypeError):
        limit = 6
    
    soon_date = date.today() + timedelta(days=7)
    
    vacancies = Vacancy.objects.filter(
        status='published',
        deadline__lte=soon_date,
        deadline__gt=date.today()
    ).select_related(
        'category', 'department'
    ).order_by('deadline')[:limit]
    
    serializer = VacancyListSerializer(vacancies, many=True)
    return Response(serializer.data)
