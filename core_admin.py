from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

class SalymbekovAdminSite(AdminSite):
    site_header = "🎓 Университет Салымбекова"
    site_title = "Админ-панель"
    index_title = "Добро пожаловать в административную панель"
    
    def each_context(self, request):
        """
        Return a dictionary of variables to put in the template context for
        *every* page in the admin site.
        """
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
    
    def get_readonly_fields(self, request, obj=None):
        """Автоматически делаем поля created_at и updated_at только для чтения"""
        readonly_fields = list(super().get_readonly_fields(request, obj))
        
        # Добавляем поля даты создания и обновления если они есть
        for field in ['created_at', 'updated_at', 'date_created', 'date_updated']:
            if hasattr(self.model, field) and field not in readonly_fields:
                readonly_fields.append(field)
                
        return readonly_fields
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

# Миксин для моделей с переводами
class TranslationAdminMixin:
    """Миксин для удобной работы с переводами"""
    
    def get_fieldsets(self, request, obj=None):
        """Группируем поля по языкам для удобства"""
        fieldsets = super().get_fieldsets(request, obj)
        
        if hasattr(self.model, 'title_ru'):  # Проверяем наличие переводимых полей
            # Создаем группы для каждого языка
            language_fieldsets = [
                ('🇷🇺 Русский', {
                    'fields': self._get_language_fields('ru'),
                    'classes': ('collapse',)
                }),
                ('🇰🇬 Кыргызча', {
                    'fields': self._get_language_fields('ky'),
                    'classes': ('collapse',)
                }),
                ('🇺🇸 English', {
                    'fields': self._get_language_fields('en'),
                    'classes': ('collapse',)
                }),
            ]
            
            # Добавляем основные поля
            main_fields = self._get_non_language_fields()
            if main_fields:
                main_fieldset = ('📋 Основная информация', {
                    'fields': main_fields
                })
                return (main_fieldset,) + tuple(language_fieldsets)
            else:
                return tuple(language_fieldsets)
        
        return fieldsets
    
    def _get_language_fields(self, lang_code):
        """Получаем поля для определенного языка"""
        fields = []
        for field in self.model._meta.get_fields():
            if field.name.endswith(f'_{lang_code}'):
                fields.append(field.name)
        return fields
    
    def _get_non_language_fields(self):
        """Получаем поля, которые не являются переводами"""
        fields = []
        excluded_suffixes = ['_ru', '_ky', '_en']
        
        for field in self.get_fields(None):
            if not any(field.endswith(suffix) for suffix in excluded_suffixes):
                fields.append(field)
        return fields

# Функция для красивого отображения изображений в админке
def image_preview(image_field):
    """Создает превью изображения для админки"""
    def preview(obj):
        if image_field and hasattr(obj, image_field.name):
            image = getattr(obj, image_field.name)
            if image:
                return format_html(
                    '<img src="{}" style="max-height: 100px; max-width: 150px; '
                    'border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" />',
                    image.url
                )
        return "Нет изображения"
    preview.short_description = "Превью"
    return preview

# Декоратор для красивого отображения дат
def format_date_field(field_name, title="Дата"):
    """Форматирует дату красиво"""
    def formatted_date(obj):
        if hasattr(obj, field_name):
            date_value = getattr(obj, field_name)
            if date_value:
                return format_html(
                    '<span style="color: #6366f1; font-weight: 500;">📅 {}</span>',
                    date_value.strftime("%d.%m.%Y в %H:%M")
                )
        return "-"
    formatted_date.short_description = title
    formatted_date.admin_order_field = field_name
    return formatted_date
