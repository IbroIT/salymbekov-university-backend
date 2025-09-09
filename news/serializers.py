from rest_framework import serializers
from django.utils import translation
from .models import News, NewsCategory, Event, Announcement, NewsTag, NewsTagRelation


class LanguageAwareSerializer(serializers.ModelSerializer):
    """Базовый сериализатор с поддержкой языков"""
    
    def get_localized_field(self, instance, field_name):
        """Получить переведенное поле в зависимости от текущего языка"""
        # Получаем язык из заголовка запроса или используем текущий язык Django
        request = self.context.get('request')
        if request:
            current_language = request.headers.get('Accept-Language', 'ru')
        else:
            current_language = translation.get_language() or 'ru'
        
        # Попробуем получить поле для текущего языка
        localized_field = f"{field_name}_{current_language}"
        if hasattr(instance, localized_field):
            value = getattr(instance, localized_field)
            if value:
                return value
        
        # Если нет перевода для текущего языка, вернем русский (по умолчанию)
        default_field = f"{field_name}_ru"
        if hasattr(instance, default_field):
            value = getattr(instance, default_field)
            if value:
                return value
        
        # Если и русского нет, вернем базовое поле
        return getattr(instance, field_name, 'not given')
    
    def to_representation(self, instance):
        """Переопределяем представление для автоматической локализации"""
        data = super().to_representation(instance)
        
        # Переводимые поля
        translatable_fields = getattr(self.Meta, 'translatable_fields', [])
        
        for field in translatable_fields:
            if field in data:
                data[field] = self.get_localized_field(instance, field)
        
        return data


class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ['id', 'name', 'slug', 'name_ru', 'name_kg', 'name_en', 'description_ru', 'description_kg', 'description_en']


class NewsTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsTag
        fields = ['id', 'name_ru', 'name_kg', 'name_en', 'slug', 'color']


class EventDetailSerializer(serializers.ModelSerializer):
    """Детализированный сериализатор для событий"""
    event_category_display = serializers.CharField(source='get_event_category_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    participants_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = [
            'event_date', 'event_time', 'end_time', 
            'location_ru', 'location_kg', 'location_en',
            'event_category', 'event_category_display',
            'status', 'status_display',
            'max_participants', 'current_participants', 'participants_info',
            'registration_required', 'registration_deadline', 'registration_link'
        ]
    
    def get_participants_info(self, obj):
        if obj.max_participants:
            return f"{obj.current_participants}/{obj.max_participants}"
        return f"{obj.current_participants}+"


class AnnouncementDetailSerializer(serializers.ModelSerializer):
    """Детализированный сериализатор для объявлений"""
    announcement_type_display = serializers.CharField(source='get_announcement_type_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    attachment_url = serializers.SerializerMethodField()
    target_audience = serializers.SerializerMethodField()
    
    class Meta:
        model = Announcement
        fields = [
            'announcement_type', 'announcement_type_display',
            'priority', 'priority_display',
            'deadline', 'is_deadline_approaching',
            'attachment', 'attachment_url', 'attachment_name',
            'target_students', 'target_staff', 'target_faculty', 'target_audience'
        ]
    
    def get_attachment_url(self, obj):
        if obj.attachment:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.attachment.url)
        return None
    
    def get_target_audience(self, obj):
        audiences = []
        if obj.target_students:
            audiences.append('Студенты')
        if obj.target_staff:
            audiences.append('Сотрудники')
        if obj.target_faculty:
            audiences.append('Преподаватели')
        return audiences


class NewsListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка новостей (краткая информация)"""
    category = NewsCategorySerializer(read_only=True)
    image_url = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    read_time = serializers.SerializerMethodField()
    
    class Meta:
        model = News
        fields = [
            'id', 'title_ru', 'title_kg', 'title_en', 'slug', 
            'summary_ru', 'summary_kg', 'summary_en', 'image_url',
            'category', 'author_ru', 'author_kg', 'author_en', 
            'published_at', 'is_featured', 'is_pinned', 'views_count', 
            'tags', 'read_time'
        ]
    
    def get_image_url(self, obj):
        return obj.image_url_or_default
    
    def get_tags(self, obj):
        # Получаем связанные теги через промежуточную модель
        tag_relations = NewsTagRelation.objects.filter(news=obj).select_related('tag')
        tags = [relation.tag for relation in tag_relations]
        return NewsTagSerializer(tags, many=True, context=self.context).data
    
    def get_read_time(self, obj):
        # Примерный расчет времени чтения (200 слов в минуту)
        content = obj.content_ru or obj.content_kg or obj.content_en or ''
        if content:
            word_count = len(content.split())
            return max(1, word_count // 200)
        return 1


class NewsDetailSerializer(serializers.ModelSerializer):
    """Детализированный сериализатор для новости"""
    category = NewsCategorySerializer(read_only=True)
    image_url = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    event_details = EventDetailSerializer(read_only=True)
    announcement_details = AnnouncementDetailSerializer(read_only=True)
    related_news = serializers.SerializerMethodField()
    read_time = serializers.SerializerMethodField()
    
    class Meta:
        model = News
        fields = [
            'id', 'title_ru', 'title_kg', 'title_en', 'slug', 
            'summary_ru', 'summary_kg', 'summary_en', 
            'content_ru', 'content_kg', 'content_en', 'image_url',
            'category', 'author_ru', 'author_kg', 'author_en', 
            'created_at', 'updated_at', 'published_at',
            'is_featured', 'is_pinned', 'views_count', 'tags', 'read_time',
            'event_details', 'announcement_details', 'related_news'
        ]
    
    def get_image_url(self, obj):
        return obj.image_url
    
    def get_tags(self, obj):
        # Получаем связанные теги
        tag_relations = NewsTagRelation.objects.filter(news=obj).select_related('tag')
        tags = [relation.tag for relation in tag_relations]
        return NewsTagSerializer(tags, many=True, context=self.context).data
    
    def get_read_time(self, obj):
        # Расчет времени чтения
        content = obj.content_ru or obj.content_kg or obj.content_en or ''
        if content:
            word_count = len(content.split())
            return max(1, word_count // 200)
        return 1
    
    def get_related_news(self, obj):
        """Получение связанных новостей той же категории"""
        related = News.objects.filter(
            category=obj.category,
            is_published=True
        ).exclude(id=obj.id)[:3]
        
        return NewsListSerializer(related, many=True, context=self.context).data


class EventListSerializer(LanguageAwareSerializer):
    """Сериализатор для списка событий"""
    title = serializers.SerializerMethodField()
    slug = serializers.CharField(source='news.slug', read_only=True)
    summary = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    published_at = serializers.DateTimeField(source='news.published_at', read_only=True)
    location = serializers.SerializerMethodField()
    
    event_category_display = serializers.CharField(source='get_event_category_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    participants_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'slug', 'summary', 'image_url', 'author', 'published_at',
            'event_date', 'event_time', 'location',
            'event_category', 'event_category_display',
            'status', 'status_display',
            'participants_info', 'registration_required'
        ]
    
    def get_title(self, obj):
        return self.get_localized_field(obj.news, 'title')
    
    def get_summary(self, obj):
        return self.get_localized_field(obj.news, 'summary')
    
    def get_author(self, obj):
        return self.get_localized_field(obj.news, 'author')
    
    def get_location(self, obj):
        """Получает локализованное поле места проведения события"""
        language = self.context.get('request').headers.get('Accept-Language', 'ru')
        if language == 'ky':
            return obj.location_kg or obj.location_ru
        elif language == 'en':
            return obj.location_en or obj.location_ru
        return obj.location_ru
    
    def get_image_url(self, obj):
        """Получает URL изображения события"""
        return obj.news.image_url_or_default
    
    def get_participants_info(self, obj):
        if obj.max_participants:
            return f"{obj.current_participants}/{obj.max_participants}"
        return f"{obj.current_participants}+"


class AnnouncementListSerializer(LanguageAwareSerializer):
    """Сериализатор для списка объявлений"""
    title = serializers.SerializerMethodField()
    summary = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    slug = serializers.CharField(source='news.slug', read_only=True)
    author = serializers.CharField(source='news.author_ru', read_only=True)
    published_at = serializers.DateTimeField(source='news.published_at', read_only=True)
    is_pinned = serializers.BooleanField(source='news.is_pinned', read_only=True)
    
    announcement_type_display = serializers.CharField(source='get_announcement_type_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    attachment_name_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'slug', 'summary', 'content', 'author', 
            'published_at', 'is_pinned',
            'announcement_type', 'announcement_type_display',
            'priority', 'priority_display',
            'deadline', 'is_deadline_approaching',
            'attachment_name', 'attachment_name_display'
        ]
    
    def get_title(self, obj):
        return self.get_localized_field(obj.news, 'title')
    
    def get_summary(self, obj):
        return self.get_localized_field(obj.news, 'summary')
    
    def get_content(self, obj):
        return self.get_localized_field(obj.news, 'content')
    
    def get_attachment_name_display(self, obj):
        if obj.attachment:
            return obj.attachment_name or obj.attachment.name.split('/')[-1]
        return None


# Сериализаторы для создания и обновления
class NewsCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления новостей"""
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=NewsTag.objects.all(), required=False
    )
    
    class Meta:
        model = News
        fields = [
            'title', 'slug', 'summary', 'content', 'image', 'image_url',
            'category', 'author', 'published_at', 'is_published',
            'is_featured', 'is_pinned', 'tags'
        ]
    
    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        news = News.objects.create(**validated_data)
        
        # Добавляем теги
        for tag in tags_data:
            NewsTagRelation.objects.create(news=news, tag=tag)
        
        return news
    
    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Обновляем теги если они переданы
        if tags_data is not None:
            instance.tags.all().delete()  # Удаляем старые связи
            for tag in tags_data:
                NewsTagRelation.objects.create(news=instance, tag=tag)
        
        return instance


class EventCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления событий"""
    news_data = NewsCreateUpdateSerializer()
    
    class Meta:
        model = Event
        fields = [
            'news_data', 'event_date', 'event_time', 'end_time', 'location',
            'event_category', 'status', 'max_participants', 'current_participants',
            'registration_required', 'registration_deadline', 'registration_link'
        ]
    
    def create(self, validated_data):
        news_data = validated_data.pop('news_data')
        # Устанавливаем категорию как 'events'
        news_data['category'] = NewsCategory.objects.get(name=NewsCategory.EVENTS)
        
        news_serializer = NewsCreateUpdateSerializer(data=news_data)
        news_serializer.is_valid(raise_exception=True)
        news = news_serializer.save()
        
        event = Event.objects.create(news=news, **validated_data)
        return event


class AnnouncementCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления объявлений"""
    news_data = NewsCreateUpdateSerializer()
    
    class Meta:
        model = Announcement
        fields = [
            'news_data', 'announcement_type', 'priority', 'deadline',
            'attachment', 'attachment_name', 'target_students',
            'target_staff', 'target_faculty'
        ]
    
    def create(self, validated_data):
        news_data = validated_data.pop('news_data')
        # Устанавливаем категорию как 'announcements'
        news_data['category'] = NewsCategory.objects.get(name=NewsCategory.ANNOUNCEMENTS)
        
        news_serializer = NewsCreateUpdateSerializer(data=news_data)
        news_serializer.is_valid(raise_exception=True)
        news = news_serializer.save()
        
        announcement = Announcement.objects.create(news=news, **validated_data)
        return announcement
