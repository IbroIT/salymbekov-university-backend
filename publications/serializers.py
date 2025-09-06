from rest_framework import serializers
from .models import Publication, ResearchCenter
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthorSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'full_name']

    def get_full_name(self, obj):
        return f"{obj.last_name} {obj.first_name}"

class ResearchCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchCenter
        fields = ['id', 'name']

class PublicationSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    authors_list = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )
    center_name = serializers.CharField(source='center.name', read_only=True)

    class Meta:
        model = Publication
        fields = [
            'id', 'title', 'authors', 'journal', 'year', 
            'citation_index', 'doi', 'abstract', 'center',
            'center_name', 'created_at', 'updated_at', 'authors_list'
        ]
        extra_kwargs = {
            'center': {'write_only': True}
        }

    def create(self, validated_data):
        authors_list = validated_data.pop('authors_list', [])
        publication = Publication.objects.create(**validated_data)
        
        # Добавление авторов
        for author_name in authors_list:
            try:
                last_name, first_name = author_name.split('.')
                user, created = User.objects.get_or_create(
                    last_name=last_name.strip(),
                    first_name=first_name.strip().replace('.', '')
                )
                publication.authors.add(user)
            except:
                continue
        
        return publication