from rest_framework import serializers
from .models import ResearchArea, ResearchCenter, Grant, Conference, Publication, GrantApplication


class ResearchAreaSerializer(serializers.ModelSerializer):
    """Сериализатор для областей исследований"""
    
    class Meta:
        model = ResearchArea
        fields = [
            'id', 'title_ru', 'title_en', 'title_kg',
            'description_ru', 'description_en', 'description_kg',
            'icon', 'color', 'projects_count', 'publications_count',
            'researchers_count', 'is_active'
        ]


class ResearchCenterSerializer(serializers.ModelSerializer):
    """Сериализатор для исследовательских центров"""
    
    class Meta:
        model = ResearchCenter
        fields = [
            'id', 'name_ru', 'name_en', 'name_kg',
            'description_ru', 'description_en', 'description_kg',
            'director', 'staff_count', 'established_year',
            'equipment_ru', 'equipment_en', 'equipment_kg',
            'image', 'website', 'email', 'phone', 'is_active'
        ]


class GrantListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка грантов (краткая информация)"""
    is_deadline_soon = serializers.ReadOnlyField()
    
    class Meta:
        model = Grant
        fields = [
            'id', 'title_ru', 'title_en', 'title_kg',
            'organization', 'amount', 'deadline', 'category', 'status',
            'duration_ru', 'duration_en', 'duration_kg',
            'is_deadline_soon'
        ]


class GrantDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детальной информации о гранте"""
    is_deadline_soon = serializers.ReadOnlyField()
    
    class Meta:
        model = Grant
        fields = [
            'id', 'title_ru', 'title_en', 'title_kg',
            'organization', 'amount', 'deadline', 'category', 'status',
            'duration_ru', 'duration_en', 'duration_kg',
            'requirements_ru', 'requirements_en', 'requirements_kg',
            'description_ru', 'description_en', 'description_kg',
            'contact', 'website', 'is_deadline_soon', 'created_at'
        ]


class ConferenceSerializer(serializers.ModelSerializer):
    """Сериализатор для конференций"""
    is_upcoming = serializers.ReadOnlyField()
    
    class Meta:
        model = Conference
        fields = [
            'id', 'title_ru', 'title_en', 'title_kg',
            'start_date', 'end_date', 'deadline',
            'location_ru', 'location_en', 'location_kg',
            'description_ru', 'description_en', 'description_kg',
            'topics_ru', 'topics_en', 'topics_kg',
            'speakers_ru', 'speakers_en', 'speakers_kg',
            'speakers_count', 'participants_limit', 'image',
            'website', 'status', 'is_upcoming'
        ]


class PublicationListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка публикаций (краткая информация)"""
    research_area_name = serializers.CharField(source='research_area.title_ru', read_only=True)
    research_center_name = serializers.CharField(source='research_center.name_ru', read_only=True)
    
    class Meta:
        model = Publication
        fields = [
            'id', 'title_ru', 'title_en', 'title_kg',
            'authors', 'journal', 'publication_date', 'publication_type',
            'impact_factor', 'citations_count', 'doi', 'url',
            'research_area_name', 'research_center_name', 'is_featured'
        ]


class PublicationDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детальной информации о публикации"""
    research_area = ResearchAreaSerializer(read_only=True)
    research_center = ResearchCenterSerializer(read_only=True)
    
    class Meta:
        model = Publication
        fields = [
            'id', 'title_ru', 'title_en', 'title_kg',
            'authors', 'journal', 'publication_date', 'publication_type',
            'impact_factor', 'citations_count', 'doi', 'url',
            'abstract_ru', 'abstract_en', 'abstract_kg',
            'keywords_ru', 'keywords_en', 'keywords_kg',
            'research_area', 'research_center', 'file',
            'is_featured', 'created_at'
        ]


class GrantApplicationCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания заявки на грант"""
    
    class Meta:
        model = GrantApplication
        fields = [
            'grant', 'project_title', 'principal_investigator',
            'email', 'phone', 'department', 'team_members',
            'project_description', 'budget', 'timeline',
            'expected_results', 'files'
        ]
        
    def validate_budget(self, value):
        if value <= 0:
            raise serializers.ValidationError("Бюджет должен быть больше 0")
        return value
        
    def validate_timeline(self, value):
        if value <= 0 or value > 60:
            raise serializers.ValidationError("Срок реализации должен быть от 1 до 60 месяцев")
        return value


class GrantApplicationSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра заявок на грант"""
    grant_title = serializers.CharField(source='grant.title_ru', read_only=True)
    
    class Meta:
        model = GrantApplication
        fields = [
            'id', 'grant', 'grant_title', 'project_title',
            'principal_investigator', 'email', 'phone', 'department',
            'team_members', 'project_description', 'budget', 'timeline',
            'expected_results', 'files', 'status', 'admin_notes',
            'submitted_at', 'reviewed_at'
        ]
        read_only_fields = ['status', 'admin_notes', 'reviewed_at']


# Статистические сериализаторы
class ResearchStatsSerializer(serializers.Serializer):
    """Сериализатор для статистики исследований"""
    total_areas = serializers.IntegerField()
    total_centers = serializers.IntegerField()
    total_grants = serializers.IntegerField()
    active_grants = serializers.IntegerField()
    total_publications = serializers.IntegerField()
    total_conferences = serializers.IntegerField()
    upcoming_conferences = serializers.IntegerField()
    pending_applications = serializers.IntegerField()


class GrantStatsSerializer(serializers.Serializer):
    """Сериализатор для статистики грантов по категориям"""
    category = serializers.CharField()
    count = serializers.IntegerField()
    total_amount = serializers.CharField()


class PublicationStatsSerializer(serializers.Serializer):
    """Сериализатор для статистики публикаций по типам"""
    publication_type = serializers.CharField()
    count = serializers.IntegerField()
    avg_impact_factor = serializers.DecimalField(max_digits=5, decimal_places=2)
