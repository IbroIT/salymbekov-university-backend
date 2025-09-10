from rest_framework import generics, viewsets, status, filters
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q, Avg
from django.utils import timezone
from datetime import timedelta

from .models import ResearchArea, ResearchCenter, Grant, Conference, Publication, GrantApplication
from .serializers import (
    ResearchAreaSerializer, ResearchCenterSerializer,
    GrantListSerializer, GrantDetailSerializer,
    ConferenceSerializer, PublicationListSerializer, PublicationDetailSerializer,
    GrantApplicationCreateSerializer, GrantApplicationSerializer,
    ResearchStatsSerializer, GrantStatsSerializer, PublicationStatsSerializer
)


class ResearchAreaViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для областей исследований"""
    queryset = ResearchArea.objects.filter(is_active=True)
    serializer_class = ResearchAreaSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Можно добавить фильтрацию по параметрам
        return queryset.order_by('id')


class ResearchCenterViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для исследовательских центров"""
    queryset = ResearchCenter.objects.filter(is_active=True)
    serializer_class = ResearchCenterSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('name_ru')


class GrantViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для грантов"""
    queryset = Grant.objects.filter(is_active=True)
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status', 'organization_ru', 'organization_en', 'organization_kg']
    search_fields = ['title_ru', 'title_en', 'title_kg', 'organization_ru', 'organization_en', 'organization_kg', 'description_ru']
    ordering_fields = ['deadline', 'amount', 'created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return GrantDetailSerializer
        return GrantListSerializer
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Активные гранты"""
        queryset = self.get_queryset().filter(status='active')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Предстоящие гранты"""
        queryset = self.get_queryset().filter(status='upcoming')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def deadline_soon(self, request):
        """Гранты с близким дедлайном"""
        soon_date = timezone.now().date() + timedelta(days=30)
        queryset = self.get_queryset().filter(
            deadline__lte=soon_date,
            deadline__gte=timezone.now().date(),
            status='active'
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ConferenceViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для конференций"""
    queryset = Conference.objects.filter(is_active=True)
    serializer_class = ConferenceSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['title_ru', 'title_en', 'title_kg', 'location_ru', 'description_ru']
    ordering_fields = ['start_date', 'deadline']
    ordering = ['start_date']
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Предстоящие конференции"""
        queryset = self.get_queryset().filter(start_date__gte=timezone.now().date())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def registration_open(self, request):
        """Конференции с открытой регистрацией"""
        queryset = self.get_queryset().filter(
            status__in=['registration-open', 'early-bird'],
            deadline__gte=timezone.now().date()
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PublicationViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для публикаций"""
    queryset = Publication.objects.filter(is_active=True)
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['publication_type', 'research_area', 'research_center', 'is_featured']
    search_fields = ['title_ru', 'title_en', 'title_kg', 'authors', 'journal']
    ordering_fields = ['publication_date', 'impact_factor', 'citations_count']
    ordering = ['-publication_date']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PublicationDetailSerializer
        return PublicationListSerializer
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Рекомендуемые публикации"""
        queryset = self.get_queryset().filter(is_featured=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Недавние публикации"""
        recent_date = timezone.now().date() - timedelta(days=365)
        queryset = self.get_queryset().filter(publication_date__gte=recent_date)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_research_area(self, request):
        """Публикации по областям исследований"""
        area_id = request.query_params.get('area_id')
        if area_id:
            queryset = self.get_queryset().filter(research_area_id=area_id)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response({"error": "area_id parameter is required"}, status=400)


class GrantApplicationCreateView(generics.CreateAPIView):
    """Создание заявки на грант"""
    queryset = GrantApplication.objects.all()
    serializer_class = GrantApplicationCreateSerializer
    permission_classes = [AllowAny]  # Можно изменить на IsAuthenticated если нужна авторизация
    
    def perform_create(self, serializer):
        serializer.save()
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response({
            "message": "Заявка успешно подана!",
            "application_id": serializer.instance.id
        }, status=status.HTTP_201_CREATED)


class GrantApplicationListView(generics.ListAPIView):
    """Список заявок на грант (для администраторов)"""
    queryset = GrantApplication.objects.all()
    serializer_class = GrantApplicationSerializer
    permission_classes = [IsAuthenticated]  # Только для авторизованных пользователей
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'grant__category']
    search_fields = ['project_title', 'principal_investigator', 'department']
    ordering_fields = ['submitted_at', 'budget']
    ordering = ['-submitted_at']


@api_view(['GET'])
def research_stats(request):
    """Общая статистика исследований"""
    stats = {
        'total_areas': ResearchArea.objects.filter(is_active=True).count(),
        'total_centers': ResearchCenter.objects.filter(is_active=True).count(),
        'total_grants': Grant.objects.filter(is_active=True).count(),
        'active_grants': Grant.objects.filter(is_active=True, status='active').count(),
        'total_publications': Publication.objects.filter(is_active=True).count(),
        'total_conferences': Conference.objects.filter(is_active=True).count(),
        'upcoming_conferences': Conference.objects.filter(
            is_active=True, 
            start_date__gte=timezone.now().date()
        ).count(),
        'pending_applications': GrantApplication.objects.filter(status='pending').count(),
    }
    
    serializer = ResearchStatsSerializer(stats)
    return Response(serializer.data)


@api_view(['GET'])
def grant_stats_by_category(request):
    """Статистика грантов по категориям"""
    stats = Grant.objects.filter(is_active=True).values('category').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Добавим человеко-читаемые названия категорий
    category_names = dict(Grant.CATEGORY_CHOICES)
    for stat in stats:
        stat['category_name'] = category_names.get(stat['category'], stat['category'])
        stat['total_amount'] = 'Различные'  # Можно добавить подсчет сумм если нужно
    
    serializer = GrantStatsSerializer(stats, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def publication_stats_by_type(request):
    """Статистика публикаций по типам"""
    stats = Publication.objects.filter(is_active=True).values('publication_type').annotate(
        count=Count('id'),
        avg_impact_factor=Avg('impact_factor')
    ).order_by('-count')
    
    # Добавим человеко-читаемые названия типов
    type_names = dict(Publication.PUBLICATION_TYPE_CHOICES)
    for stat in stats:
        stat['type_name'] = type_names.get(stat['publication_type'], stat['publication_type'])
        if stat['avg_impact_factor'] is None:
            stat['avg_impact_factor'] = 0
    
    serializer = PublicationStatsSerializer(stats, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def search_all(request):
    """Поиск по всем сущностям"""
    query = request.query_params.get('q', '')
    lang = request.query_params.get('lang', 'ru')
    
    if not query:
        return Response({"error": "Query parameter 'q' is required"}, status=400)
    
    # Определяем поля для поиска в зависимости от языка
    title_field = f'title_{lang}' if lang in ['ru', 'en', 'kg'] else 'title_ru'
    name_field = f'name_{lang}' if lang in ['ru', 'en', 'kg'] else 'name_ru'
    desc_field = f'description_{lang}' if lang in ['ru', 'en', 'kg'] else 'description_ru'
    
    results = {
        'grants': [],
        'conferences': [],
        'publications': [],
        'research_areas': [],
        'research_centers': []
    }
    
    # Поиск грантов
    grants = Grant.objects.filter(
        Q(**{f'{title_field}__icontains': query}) |
        Q(organization__icontains=query) |
        Q(**{f'{desc_field}__icontains': query}),
        is_active=True
    )[:5]
    results['grants'] = GrantListSerializer(grants, many=True).data
    
    # Поиск конференций
    conferences = Conference.objects.filter(
        Q(**{f'{title_field}__icontains': query}) |
        Q(**{f'location_{lang}__icontains': query}) |
        Q(**{f'{desc_field}__icontains': query}),
        is_active=True
    )[:5]
    results['conferences'] = ConferenceSerializer(conferences, many=True).data
    
    # Поиск публикаций
    publications = Publication.objects.filter(
        Q(**{f'{title_field}__icontains': query}) |
        Q(authors__icontains=query) |
        Q(journal__icontains=query),
        is_active=True
    )[:5]
    results['publications'] = PublicationListSerializer(publications, many=True).data
    
    # Поиск областей исследований
    areas = ResearchArea.objects.filter(
        Q(**{f'{title_field}__icontains': query}) |
        Q(**{f'{desc_field}__icontains': query}),
        is_active=True
    )[:5]
    results['research_areas'] = ResearchAreaSerializer(areas, many=True).data
    
    # Поиск исследовательских центров
    centers = ResearchCenter.objects.filter(
        Q(**{f'{name_field}__icontains': query}) |
        Q(**{f'{desc_field}__icontains': query}) |
        Q(director__icontains=query),
        is_active=True
    )[:5]
    results['research_centers'] = ResearchCenterSerializer(centers, many=True).data
    
    return Response(results)
