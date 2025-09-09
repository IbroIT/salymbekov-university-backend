from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import (
    News, NewsCategory, Event, Announcement, 
    NewsTag, NewsTagRelation, NewsView
)


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_ru', 'slug']
    prepopulated_fields = {'slug': ('name_ru',)}  # Изменяем источник на name_ru
    # Убираем readonly_fields для name, чтобы избежать конфликта


@admin.register(NewsTag)
class NewsTagAdmin(admin.ModelAdmin):
    list_display = ['name_ru', 'slug', 'color_preview']
    prepopulated_fields = {'slug': ('name_ru',)}
    list_filter = ['color']
    search_fields = ['name_ru', 'name_kg', 'name_en']
    
    def color_preview(self, obj):
        return format_html(
            '<div style="width: 30px; height: 20px; background-color: {}; border: 1px solid #ccc;"></div>',
            obj.color
        )
    color_preview.short_description = 'Цвет'


class NewsTagInline(admin.TabularInline):
    model = NewsTagRelation
    extra = 1
    autocomplete_fields = ['tag']


class EventInline(admin.StackedInline):
    model = Event
    extra = 0
    fieldsets = (
        ('Основная информация', {
            'fields': ('event_date', 'event_time', 'end_time', 'location_ru', 'location_kg', 'location_en')
        }),
        ('Детали события', {
            'fields': ('event_category', 'status', 'max_participants', 'current_participants')
        }),
        ('Регистрация', {
            'fields': ('registration_required', 'registration_deadline', 'registration_link'),
            'classes': ['collapse']
        }),
    )


class AnnouncementInline(admin.StackedInline):
    model = Announcement
    extra = 0
    fieldsets = (
        ('Основная информация', {
            'fields': ('announcement_type', 'priority', 'deadline')
        }),
        ('Вложения', {
            'fields': ('attachment', 'attachment_name'),
            'classes': ['collapse']
        }),
        ('Целевая аудитория', {
            'fields': ('target_students', 'target_staff', 'target_faculty'),
            'classes': ['collapse']
        }),
    )


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = [
        'title_ru', 'category', 'author_ru', 'published_at', 'views_count',
        'is_published', 'is_featured', 'is_pinned', 'image_preview'
    ]
    list_filter = [
        'category', 'is_published', 'is_featured', 'is_pinned',
        'created_at', 'published_at'
    ]
    search_fields = ['title_ru', 'title_kg', 'title_en', 'summary_ru', 'summary_kg', 'summary_en', 'content_ru', 'content_kg', 'content_en', 'author_ru', 'author_kg', 'author_en']
    prepopulated_fields = {'slug': ('title_ru',)}
    readonly_fields = ['created_at', 'updated_at', 'views_count', 'image_preview']
    date_hierarchy = 'published_at'
    
    fieldsets = (
        ('Основная информация', {
            'fields': (
                ('title_ru', 'title_kg', 'title_en'),
                'slug',
                ('summary_ru', 'summary_kg', 'summary_en'),
                ('content_ru', 'content_kg', 'content_en')
            )
        }),
        ('Медиа', {
            'fields': ('image', 'image_url', 'image_preview'),
        }),
        ('Классификация', {
            'fields': ('category', ('author_ru', 'author_kg', 'author_en'))
        }),
        ('Публикация', {
            'fields': ('published_at', 'is_published', 'is_featured', 'is_pinned')
        }),
        ('Метаинформация', {
            'fields': ('created_at', 'updated_at', 'views_count'),
            'classes': ['collapse']
        }),
    )
    
    inlines = [NewsTagInline, EventInline, AnnouncementInline]
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="60" />', obj.image.url)
        elif obj.image_url:
            return format_html('<img src="{}" width="100" height="60" />', obj.image_url)
        return "Нет изображения"
    image_preview.short_description = 'Превью'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')
    
    actions = ['make_published', 'make_unpublished', 'make_featured', 'make_pinned']
    
    def make_published(self, request, queryset):
        queryset.update(is_published=True)
    make_published.short_description = "Опубликовать выбранные новости"
    
    def make_unpublished(self, request, queryset):
        queryset.update(is_published=False)
    make_unpublished.short_description = "Снять с публикации выбранные новости"
    
    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
    make_featured.short_description = "Сделать рекомендуемыми"
    
    def make_pinned(self, request, queryset):
        queryset.update(is_pinned=True)
    make_pinned.short_description = "Закрепить выбранные новости"


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        'get_title', 'event_date', 'event_time', 'location_ru',
        'event_category', 'status', 'participants_info', 'registration_required'
    ]
    list_filter = [
        'event_category', 'status', 'registration_required',
        'event_date', 'news__published_at'
    ]
    search_fields = ['news__title_ru', 'location_ru', 'news__summary_ru']
    date_hierarchy = 'event_date'
    
    fieldsets = (
        ('Связанная новость', {
            'fields': ('news',)
        }),
        ('Время и место', {
            'fields': ('event_date', 'event_time', 'end_time', ('location_ru', 'location_kg', 'location_en'))
        }),
        ('Детали события', {
            'fields': ('event_category', 'status')
        }),
        ('Участники', {
            'fields': ('max_participants', 'current_participants')
        }),
        ('Регистрация', {
            'fields': ('registration_required', 'registration_deadline', 'registration_link'),
            'classes': ['collapse']
        }),
    )
    
    def get_title(self, obj):
        return obj.news.title_ru
    get_title.short_description = 'Название'
    get_title.admin_order_field = 'news__title_ru'
    
    def participants_info(self, obj):
        if obj.max_participants:
            return f"{obj.current_participants}/{obj.max_participants}"
        return f"{obj.current_participants}+"
    participants_info.short_description = 'Участники'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('news')


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = [
        'get_title', 'announcement_type', 'priority', 'deadline',
        'is_deadline_approaching', 'get_is_pinned', 'attachment_preview'
    ]
    list_filter = [
        'announcement_type', 'priority', 'is_deadline_approaching',
        'target_students', 'target_staff', 'target_faculty',
        'news__published_at', 'deadline'
    ]
    search_fields = ['news__title', 'news__summary', 'news__content']
    date_hierarchy = 'deadline'
    
    fieldsets = (
        ('Связанная новость', {
            'fields': ('news',)
        }),
        ('Тип и приоритет', {
            'fields': ('announcement_type', 'priority', 'deadline')
        }),
        ('Вложения', {
            'fields': ('attachment', 'attachment_name')
        }),
        ('Целевая аудитория', {
            'fields': ('target_students', 'target_staff', 'target_faculty')
        }),
        ('Автоматические флаги', {
            'fields': ('is_deadline_approaching',),
            'classes': ['collapse'],
        }),
    )
    
    readonly_fields = ['is_deadline_approaching']
    
    def get_title(self, obj):
        return obj.news.title_ru
    get_title.short_description = 'Название'
    get_title.admin_order_field = 'news__title_ru'
    
    def get_is_pinned(self, obj):
        return obj.news.is_pinned
    get_is_pinned.short_description = 'Закреплено'
    get_is_pinned.boolean = True
    get_is_pinned.admin_order_field = 'news__is_pinned'
    
    def attachment_preview(self, obj):
        if obj.attachment:
            return format_html('<a href="{}" target="_blank">{}</a>', 
                             obj.attachment.url, 
                             obj.attachment_name or obj.attachment.name.split('/')[-1])
        return "Нет вложения"
    attachment_preview.short_description = 'Вложение'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('news')
    
    actions = ['mark_urgent', 'mark_high_priority']
    
    def mark_urgent(self, request, queryset):
        queryset.update(priority='urgent')
    mark_urgent.short_description = "Пометить как срочные"
    
    def mark_high_priority(self, request, queryset):
        queryset.update(priority='high')
    mark_high_priority.short_description = "Пометить как высокоприоритетные"


@admin.register(NewsView)
class NewsViewAdmin(admin.ModelAdmin):
    list_display = ['news', 'ip_address', 'viewed_at']
    list_filter = ['viewed_at']
    search_fields = ['news__title', 'ip_address']
    readonly_fields = ['news', 'ip_address', 'user_agent', 'viewed_at']
    date_hierarchy = 'viewed_at'
    
    def has_add_permission(self, request):
        return False  # Запрещаем ручное добавление просмотров
    
    def has_change_permission(self, request, obj=None):
        return False  # Запрещаем редактирование просмотров


# Настройки админ-панели
admin.site.site_header = "Салымбековский Университет - Управление новостями"
admin.site.site_title = "Новости СУ"
admin.site.index_title = "Панель управления новостями"
