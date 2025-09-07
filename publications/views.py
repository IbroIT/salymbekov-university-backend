from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Publication, ResearchCenter
from .serializers import PublicationSerializer, ResearchCenterSerializer
from django.db.models import Q

class ResearchCenterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ResearchCenter.objects.all()
    serializer_class = ResearchCenterSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all().select_related('center').prefetch_related('authors')
    serializer_class = PublicationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = {
        'year': ['gte', 'lte'],
        'citation_index': ['gte'],
        'center': ['exact'],
        'journal': ['exact'],
    }
    
    search_fields = ['title', 'title_ky', 'title_en', 
                    'authors__last_name', 'authors__first_name', 
                    'journal', 'journal_ky', 'journal_en']
    ordering_fields = ['year', 'citation_index', 'title', 'created_at']
    ordering = ['-year', '-citation_index']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Фильтрация по автору (по имени)
        author_name = self.request.query_params.get('author', None)
        if author_name:
            queryset = queryset.filter(
                Q(authors__last_name__icontains=author_name) |
                Q(authors__first_name__icontains=author_name)
            )
        
        # Фильтрация по языку
        language = self.request.GET.get('lang')
        if language:
            # Можно добавить дополнительную фильтрацию по языку если нужно
            pass
        
        return queryset.distinct()