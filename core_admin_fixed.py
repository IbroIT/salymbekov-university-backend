from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils import timezone

class SalymbekovAdminSite(AdminSite):
    site_header = "🎓 Университет Салымбекова"
    site_title = "Админ-панель"
    index_title = "Добро пожаловать в административную панель"
    
    def each_context(self, request):
        context = super().each_context(request)
        context.update({
            'site_header': self.site_header,
            'site_title': self.site_title,
            'index_title': self.index_title,
        })
        return context

# Создаем кастомный экземпляр админки
admin_site = SalymbekovAdminSite(name='salymbekov_admin')

class BaseModelAdmin(admin.ModelAdmin):
    """Базовый класс для всех моделей админки с общими настройками"""
    
    def get_readonly_fields(self, request, obj=None):
        """Автоматически делаем created_at, updated_at readonly"""
        readonly_fields = list(super().get_readonly_fields(request, obj))
        
        # Добавляем timestamp поля
        for field in ['created_at', 'updated_at', 'date_created', 'date_updated', 'submitted_at']:
            if hasattr(self.model, field) and field not in readonly_fields:
                readonly_fields.append(field)
                
        return readonly_fields
    
    def get_list_display(self, request):
        """Автоматически добавляем цветные статусы если есть поле is_active"""
        list_display = list(super().get_list_display(request))
        if hasattr(self.model, 'is_active') and 'colored_status' not in list_display:
            if 'is_active' in list_display:
                list_display[list_display.index('is_active')] = 'colored_status'
            else:
                list_display.append('colored_status')
        return tuple(list_display)
    
    def colored_status(self, obj):
        """Цветной статус активности"""
        if hasattr(obj, 'is_active'):
            if obj.is_active:
                return format_html(
                    '<span style="color: #059669; font-weight: bold;">✅ Активно</span>'
                )
            else:
                return format_html(
                    '<span style="color: #dc2626; font-weight: bold;">❌ Неактивно</span>'
                )
        return '-'
    colored_status.short_description = 'Статус'
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

# Миксин для моделей с переводами
class TranslationAdminMixin:
    """Миксин для удобной работы с переводами"""
    pass

# Утилитные функции
def image_preview(obj, field_name='image', max_height=100):
    """Безопасное отображение превью изображения"""
    if not obj or not hasattr(obj, field_name):
        return mark_safe('<span style="color: #94a3b8;">Нет изображения</span>')
    
    image_field = getattr(obj, field_name)
    if not image_field:
        return mark_safe('<span style="color: #94a3b8;">Нет изображения</span>')
        
    try:
        return format_html(
            '<img src="{}" style="max-height: {}px; max-width: 150px; '
            'border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); '
            'object-fit: cover;" />',
            image_field.url, max_height
        )
    except:
        return mark_safe('<span style="color: #ef4444;">Ошибка загрузки</span>')

def format_date_field(obj, field_name, date_format='%d.%m.%Y %H:%M'):
    """Безопасное форматирование даты"""
    if not obj or not hasattr(obj, field_name):
        return '-'
        
    date_field = getattr(obj, field_name)
    if not date_field:
        return '-'
        
    try:
        if hasattr(date_field, 'strftime'):
            return date_field.strftime(date_format)
        return str(date_field)
    except:
        return '-'

def status_badges(obj, field_mapping=None):
    """Создает цветные бейджи для статусов"""
    if not field_mapping:
        field_mapping = {
            'is_published': ('✅ Опубликовано', '❌ Черновик'),
            'is_featured': ('⭐ Рекомендуемое', ''),
            'is_pinned': ('📌 Закреплено', ''),
            'is_active': ('✅ Активно', '❌ Неактивно')
        }
    
    badges = []
    for field, (active_text, inactive_text) in field_mapping.items():
        if hasattr(obj, field):
            value = getattr(obj, field)
            if value and active_text:
                badges.append(f'<span style="background: #10b981; color: white; padding: 2px 6px; border-radius: 12px; font-size: 11px; margin: 1px;">{active_text}</span>')
            elif not value and inactive_text:
                badges.append(f'<span style="background: #ef4444; color: white; padding: 2px 6px; border-radius: 12px; font-size: 11px; margin: 1px;">{inactive_text}</span>')
    
    return mark_safe(' '.join(badges)) if badges else '-'
