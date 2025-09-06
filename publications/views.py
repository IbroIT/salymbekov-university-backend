from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Publication, ResearchCenter
from .serializers import PublicationSerializer, ResearchCenterSerializer
from django.db.models import Q

class ResearchCenterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ResearchCenter.objects.all()
    serializer_class = ResearchCenterSerializer

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
    
    search_fields = ['title', 'authors__last_name', 'authors__first_name', 'journal']
    ordering_fields = ['year', 'citation_index', 'title', 'created_at']
    ordering = ['-year', '-citation_index']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Фильтрация по автору (по имени)
        author_name = self.request.query_params.get('author', None)
        if author_name:
            queryset = queryset.filter(
                Q(authors__last_name__icontains=author_name) |
                Q(authors__first_name__icontains=author_name)
            )
        
        return queryset.distinct()