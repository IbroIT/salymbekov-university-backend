# banner/admin.py
from django.contrib import admin
from django.utils.html import format_html
from core_admin import BaseModelAdmin, TranslationAdminMixin, image_preview
from .models import Banner

@admin.register(Banner)
class BannerAdmin(BaseModelAdmin, TranslationAdminMixin):
    list_display = ['title_ru', 'banner_image_preview', 'colored_status', 'order']
    list_editable = ['order']
    list_filter = ['is_active']
    search_fields = ['title_ru', 'title_ky', 'title_en']
    ordering = ['order', 'title_ru']
    
    fieldsets = (
        ('🎯 Основная информация', {
            'fields': ('title_ru', 'title_ky', 'title_en')
        }),
        ('📝 Описание', {
            'fields': ('description_ru', 'description_ky', 'description_en'),
            'classes': ['collapse']
        }),
        ('🖼️ Медиа', {
            'fields': ('image', 'banner_image_preview')
        }),
        ('🔗 Ссылка', {
            'fields': ('link_url',)
        }),
        ('⚙️ Настройки', {
            'fields': (('is_active', 'order'),)
        }),
    )
    
    def banner_image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 60px; max-width: 120px; '
                'border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); '
                'object-fit: cover;" />',
                obj.image.url
            )
        return format_html('<div style="color: #9ca3af; font-style: italic;">🖼️ Нет изображения</div>')
    banner_image_preview.short_description = '🖼️ Превью'