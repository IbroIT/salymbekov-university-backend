from rest_framework import viewsets, generics, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, F
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta

from .models import News, NewsCategory, Event, Announcement, NewsTag, NewsView
from .serializers import (
    NewsListSerializer, NewsDetailSerializer, NewsCreateUpdateSerializer,
    EventListSerializer, EventCreateUpdateSerializer,
    AnnouncementListSerializer, AnnouncementCreateUpdateSerializer,
    NewsCategorySerializer, NewsTagSerializer
)


class NewsCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для категорий новостей"""
    queryset = NewsCategory.objects.all()
    serializer_class = NewsCategorySerializer
    lookup_field = 'slug'


class NewsTagViewSet(viewsets.ModelViewSet):
    """ViewSet для тегов новостей"""
    queryset = NewsTag.objects.all()
    serializer_class = NewsTagSerializer
    lookup_field = 'slug'


class NewsViewSet(viewsets.ModelViewSet):
    """ViewSet для новостей"""
    queryset = News.objects.filter(is_published=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__name', 'is_featured', 'is_pinned']
    search_fields = ['title', 'summary', 'content']
    ordering_fields = ['published_at', 'views_count', 'created_at']
    ordering = ['-published_at']
    
    def get_queryset(self):
        """Переопределяем queryset для поддержки поиска по slug"""
        queryset = News.objects.filter(is_published=True)
        
        # Поддержка поиска по slug в query параметрах
        slug = self.request.query_params.get('slug', None)
        if slug is not None:
            queryset = queryset.filter(slug=slug)
            
        return queryset.select_related('category')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return NewsListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return NewsCreateUpdateSerializer
        return NewsDetailSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """Переопределяем для поддержки ID и slug, и учета просмотров"""
        lookup_value = kwargs.get('pk')
        
        # Проверяем, является ли значение числом (ID) или строкой (slug)
        if lookup_value.isdigit():
            instance = get_object_or_404(News, pk=lookup_value, is_published=True)
        else:
            instance = get_object_or_404(News, slug=lookup_value, is_published=True)
        
        # Увеличиваем счетчик просмотров
        ip_address = self.get_client_ip(request)
        news_view, created = NewsView.objects.get_or_create(
            news=instance,
            ip_address=ip_address,
            defaults={'user_agent': request.META.get('HTTP_USER_AGENT', '')}
        )
        
        if created:
            # Увеличиваем счетчик только для новых просмотров
            News.objects.filter(id=instance.id).update(views_count=F('views_count') + 1)
            instance.refresh_from_db()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def get_client_ip(self, request):
        """Получение IP адреса клиента"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Получение рекомендуемых новостей"""
        featured_news = self.get_queryset().filter(is_featured=True)
        serializer = NewsListSerializer(featured_news, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pinned(self, request):
        """Получение закрепленных новостей"""
        pinned_news = self.get_queryset().filter(is_pinned=True)
        serializer = NewsListSerializer(pinned_news, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Получение популярных новостей"""
        # Популярные новости за последние 30 дней
        thirty_days_ago = datetime.now() - timedelta(days=30)
        popular_news = self.get_queryset().filter(
            published_at__gte=thirty_days_ago
        ).order_by('-views_count')[:10]
        
        serializer = NewsListSerializer(popular_news, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Получение новостей по категориям"""
        category_slug = request.query_params.get('category')
        if not category_slug:
            return Response({'error': 'Параметр category обязателен'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        category = get_object_or_404(NewsCategory, slug=category_slug)
        news = self.get_queryset().filter(category=category)
        
        # Применяем фильтрацию и пагинацию
        page = self.paginate_queryset(news)
        if page is not None:
            serializer = NewsListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = NewsListSerializer(news, many=True, context={'request': request})
        return Response(serializer.data)


class EventViewSet(viewsets.ModelViewSet):
    """ViewSet для событий"""
    queryset = Event.objects.select_related('news').filter(news__is_published=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'news__slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'event_category', 'registration_required']
    search_fields = ['news__title', 'news__summary', 'location']
    ordering_fields = ['event_date', 'event_time', 'news__published_at']
    ordering = ['event_date', 'event_time']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return EventListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return EventCreateUpdateSerializer
        return EventListSerializer  # Для detail используем тот же сериализатор
    
    def get_object(self):
        """Переопределяем для поиска по slug новости"""
        slug = self.kwargs.get('news__slug')
        return get_object_or_404(self.get_queryset(), news__slug=slug)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Предстоящие события"""
        upcoming_events = self.get_queryset().filter(status='upcoming')
        serializer = EventListSerializer(upcoming_events, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def past(self, request):
        """Прошедшие события"""
        past_events = self.get_queryset().filter(status='past')
        serializer = EventListSerializer(past_events, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def this_month(self, request):
        """События этого месяца"""
        today = datetime.now().date()
        first_day = today.replace(day=1)
        if today.month == 12:
            last_day = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            last_day = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        
        month_events = self.get_queryset().filter(
            event_date__gte=first_day,
            event_date__lte=last_day
        )
        
        serializer = EventListSerializer(month_events, many=True, context={'request': request})
        return Response(serializer.data)


class AnnouncementViewSet(viewsets.ModelViewSet):
    """ViewSet для объявлений"""
    queryset = Announcement.objects.select_related('news').filter(news__is_published=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'news__slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['announcement_type', 'priority', 'is_deadline_approaching']
    search_fields = ['news__title', 'news__summary', 'news__content']
    ordering_fields = ['news__published_at', 'deadline', 'priority']
    ordering = ['-priority', '-news__published_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return AnnouncementListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return AnnouncementCreateUpdateSerializer
        return AnnouncementListSerializer
    
    def get_object(self):
        """Переопределяем для поиска по slug новости"""
        slug = self.kwargs.get('news__slug')
        return get_object_or_404(self.get_queryset(), news__slug=slug)
    
    @action(detail=False, methods=['get'])
    def pinned(self, request):
        """Закрепленные объявления"""
        pinned_announcements = self.get_queryset().filter(news__is_pinned=True)
        serializer = AnnouncementListSerializer(pinned_announcements, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def urgent(self, request):
        """Срочные объявления"""
        urgent_announcements = self.get_queryset().filter(
            Q(priority='high') | Q(priority='urgent') | Q(is_deadline_approaching=True)
        )
        serializer = AnnouncementListSerializer(urgent_announcements, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Объявления по типу"""
        announcement_type = request.query_params.get('type')
        if not announcement_type:
            return Response({'error': 'Параметр type обязателен'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        announcements = self.get_queryset().filter(announcement_type=announcement_type)
        
        page = self.paginate_queryset(announcements)
        if page is not None:
            serializer = AnnouncementListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = AnnouncementListSerializer(announcements, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def for_students(self, request):
        """Объявления для студентов"""
        student_announcements = self.get_queryset().filter(target_students=True)
        serializer = AnnouncementListSerializer(student_announcements, many=True, context={'request': request})
        return Response(serializer.data)


# Дополнительные API views для статистики и поиска
class NewsStatsView(generics.GenericAPIView):
    """API для получения статистики новостей"""
    
    def get(self, request):
        stats = {
            'total_news': News.objects.filter(is_published=True).count(),
            'total_events': Event.objects.filter(news__is_published=True).count(),
            'total_announcements': Announcement.objects.filter(news__is_published=True).count(),
            'upcoming_events': Event.objects.filter(
                news__is_published=True, 
                status='upcoming'
            ).count(),
            'urgent_announcements': Announcement.objects.filter(
                news__is_published=True,
                priority__in=['high', 'urgent']
            ).count(),
            'featured_news': News.objects.filter(
                is_published=True, 
                is_featured=True
            ).count(),
        }
        return Response(stats)


class SearchAllView(generics.GenericAPIView):
    """Общий поиск по всем типам контента"""
    
    def get(self, request):
        query = request.query_params.get('q', '')
        if len(query) < 2:
            return Response({'error': 'Поисковый запрос должен содержать минимум 2 символа'})
        
        # Поиск в новостях
        news = News.objects.filter(
            Q(title__icontains=query) | Q(summary__icontains=query) | Q(content__icontains=query),
            is_published=True
        )[:5]
        
        # Поиск в событиях
        events = Event.objects.filter(
            Q(news__title__icontains=query) | Q(news__summary__icontains=query) | Q(location__icontains=query),
            news__is_published=True
        )[:5]
        
        # Поиск в объявлениях
        announcements = Announcement.objects.filter(
            Q(news__title__icontains=query) | Q(news__summary__icontains=query) | Q(news__content__icontains=query),
            news__is_published=True
        )[:5]
        
        results = {
            'news': NewsListSerializer(news, many=True, context={'request': request}).data,
            'events': EventListSerializer(events, many=True, context={'request': request}).data,
            'announcements': AnnouncementListSerializer(announcements, many=True, context={'request': request}).data,
            'total_found': news.count() + events.count() + announcements.count()
        }
        
        return Response(results)
