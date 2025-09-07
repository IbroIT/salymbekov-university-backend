from rest_framework import serializers
from .models import Publication, ResearchCenter
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class AuthorSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'full_name', 'email']

    def get_full_name(self, obj):
        return f"{obj.last_name} {obj.first_name}"

class ResearchCenterSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = ResearchCenter
        fields = ['id', 'name', 'description']

    def get_name(self, obj):
        # Возвращаем перевод в зависимости от языка запроса
        request = self.context.get('request')
        if request:
            language = request.GET.get('lang', request.LANGUAGE_CODE)
            if language == 'ky' and obj.name_ky:
                return obj.name_ky
            elif language == 'en' and obj.name_en:
                return obj.name_en
        return obj.name

    def get_description(self, obj):
        request = self.context.get('request')
        if request:
            language = request.GET.get('lang', request.LANGUAGE_CODE)
            if language == 'ky' and obj.description_ky:
                return obj.description_ky
            elif language == 'en' and obj.description_en:
                return obj.description_en
        return obj.description

class PublicationSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    center_name = serializers.SerializerMethodField()
    center = serializers.PrimaryKeyRelatedField(queryset=ResearchCenter.objects.all(), write_only=True)
    
    title = serializers.SerializerMethodField()
    journal = serializers.SerializerMethodField()
    abstract = serializers.SerializerMethodField()

    author_names = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False,
        help_text="Список авторов в формате 'Фамилия И.О.'"
    )

    class Meta:
        model = Publication
        fields = [
            'id', 'title', 'authors', 'journal', 'year', 
            'citation_index', 'doi', 'abstract', 'center',
            'center_name', 'is_published', 'created_at', 
            'updated_at', 'author_names'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_title(self, obj):
        request = self.context.get('request')
        if request:
            language = request.GET.get('lang', request.LANGUAGE_CODE)
            if language == 'ky' and obj.title_ky:
                return obj.title_ky
            elif language == 'en' and obj.title_en:
                return obj.title_en
        return obj.title

    def get_journal(self, obj):
        request = self.context.get('request')
        if request:
            language = request.GET.get('lang', request.LANGUAGE_CODE)
            if language == 'ky' and obj.journal_ky:
                return obj.journal_ky
            elif language == 'en' and obj.journal_en:
                return obj.journal_en
        return obj.journal

    def get_abstract(self, obj):
        request = self.context.get('request')
        if request:
            language = request.GET.get('lang', request.LANGUAGE_CODE)
            if language == 'ky' and obj.abstract_ky:
                return obj.abstract_ky
            elif language == 'en' and obj.abstract_en:
                return obj.abstract_en
        return obj.abstract

    def get_center_name(self, obj):
        request = self.context.get('request')
        if request:
            language = request.GET.get('lang', request.LANGUAGE_CODE)
            if language == 'ky' and obj.center.name_ky:
                return obj.center.name_ky
            elif language == 'en' and obj.center.name_en:
                return obj.center.name_en
        return obj.center.name

    def create(self, validated_data):
        author_names = validated_data.pop('author_names', [])
        publication = Publication.objects.create(**validated_data)
        
        self._add_authors(publication, author_names)
        
        return publication

    def update(self, instance, validated_data):
        author_names = validated_data.pop('author_names', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if author_names is not None:
            instance.authors.clear()
            self._add_authors(instance, author_names)
        
        return instance

    def _add_authors(self, publication, author_names):
        for author_name in author_names:
            try:
                parts = author_name.split()
                if len(parts) >= 2:
                    last_name = parts[0]
                    first_name = parts[1].replace('.', '')
                    
                    user, created = User.objects.get_or_create(
                        last_name=last_name,
                        first_name=first_name,
                        defaults={'username': f"{last_name.lower()}_{first_name.lower()}"}
                    )
                    publication.authors.add(user)
            except Exception as e:
                continue