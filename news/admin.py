from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.db import models
from django.forms import Textarea
from core_admin import BaseModelAdmin, TranslationAdminMixin, image_preview, format_date_field
from .models import (
    News, NewsCategory, Event, Announcement, 
    NewsTag, NewsTagRelation, NewsView
)


@admin.register(NewsCategory)
class NewsCategoryAdmin(BaseModelAdmin, TranslationAdminMixin):
    list_display = ['name_ru', 'slug']
    prepopulated_fields = {'slug': ('name_ru',)}
    search_fields = ['name_ru', 'name_ky', 'name_en']
    
    def get_fields(self, request, obj=None):
        fields = ['name_ru', 'name_ky', 'name_en', 'slug']
        return fields


@admin.register(NewsTag)
class NewsTagAdmin(BaseModelAdmin, TranslationAdminMixin):
    list_display = ['name_ru', 'slug', 'color_preview']
    prepopulated_fields = {'slug': ('name_ru',)}
    list_filter = ['color']
    search_fields = ['name_ru', 'name_ky', 'name_en']
    
    def color_preview(self, obj):
        return format_html(
            '<div style="width: 40px; height: 25px; background-color: {}; '
            'border: 2px solid #e2e8f0; border-radius: 6px; display: inline-block; '
            'box-shadow: 0 2px 4px rgba(0,0,0,0.1);"></div> '
            '<span style="margin-left: 10px; font-weight: 500; color: #374151;">{}</span>',
            obj.color, obj.color
        )
    color_preview.short_description = '🎨 Цвет'


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
class NewsAdmin(BaseModelAdmin, TranslationAdminMixin):
    list_display = [
        'title_ru', 'category', 'author_ru', 'formatted_published_at', 
        'views_count', 'status_badges', 'news_image_preview'
    ]
    list_filter = [
        'category', 'is_published', 'is_featured', 'is_pinned',
        'created_at', 'published_at'
    ]
    search_fields = [
        'title_ru', 'title_ky', 'title_en', 
        'summary_ru', 'summary_ky', 'summary_en', 
        'content_ru', 'content_ky', 'content_en', 
        'author_ru', 'author_ky', 'author_en'
    ]
    prepopulated_fields = {'slug': ('title_ru',)}
    date_hierarchy = 'published_at'
    list_per_page = 20
    
    fieldsets = (
        ('📝 Основная информация', {
            'fields': (
                'title_ru', 'title_ky', 'title_en',
                'slug',
                'summary_ru', 'summary_ky', 'summary_en',
            )
        }),
        ('📖 Содержание', {
            'fields': (
                'content_ru', 'content_ky', 'content_en',
            ),
            'classes': ['collapse']
        }),
        ('🖼️ Медиа', {
            'fields': ('image', 'image_url', 'news_image_preview'),
        }),
        ('📂 Классификация', {
            'fields': ('category', 'author_ru', 'author_ky', 'author_en')
        }),
        ('🚀 Публикация', {
            'fields': (
                'published_at', 
                ('is_published', 'is_featured', 'is_pinned')
            )
        }),
        ('📊 Статистика', {
            'fields': ('created_at', 'updated_at', 'views_count'),
            'classes': ['collapse']
        }),
    )
    
    inlines = [NewsTagInline, EventInline, AnnouncementInline]
    
    # Кастомные методы для красивого отображения
    def news_image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 80px; max-width: 120px; '
                'border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); '
                'object-fit: cover;" />',
                obj.image.url
            )
        elif obj.image_url:
            return format_html(
                '<img src="{}" style="max-height: 80px; max-width: 120px; '
                'border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); '
                'object-fit: cover;" />',
                obj.image_url
            )
        return format_html('<div style="color: #9ca3af; font-style: italic;">📷 Нет изображения</div>')
    news_image_preview.short_description = '🖼️ Превью'
    
    def status_badges(self, obj):
        badges = []
        if obj.is_published:
            badges.append('<span style="background: #10b981; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: 600;">✅ Опубликовано</span>')
        else:
            badges.append('<span style="background: #6b7280; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: 600;">⏳ Черновик</span>')
        
        if obj.is_featured:
            badges.append('<span style="background: #f59e0b; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: 600;">⭐ Рекомендуемое</span>')
        
        if obj.is_pinned:
            badges.append('<span style="background: #ef4444; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: 600;">📌 Закрепленное</span>')
        
        return format_html('<br>'.join(badges))
    status_badges.short_description = '🏷️ Статусы'
    
    formatted_published_at = format_date_field('published_at', '📅 Опубликовано')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')
    
    actions = ['make_published', 'make_unpublished', 'make_featured', 'make_pinned']
    
    def make_published(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f'✅ Опубликовано {updated} новостей.')
    make_published.short_description = "📢 Опубликовать выбранные новости"
    
    def make_unpublished(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f'⏸️ Сняты с публикации {updated} новостей.')
    make_unpublished.short_description = "⏸️ Снять с публикации выбранные новости"
    
    def make_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'⭐ Сделаны рекомендуемыми {updated} новостей.')
    make_featured.short_description = "⭐ Сделать рекомендуемыми"
    
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
