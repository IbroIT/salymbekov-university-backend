from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.db.models import Count
from core_admin import BaseModelAdmin, TranslationAdminMixin, image_preview, format_date_field
from .models import CareerCategory, Department, Vacancy, VacancyApplication


@admin.register(CareerCategory)
class CareerCategoryAdmin(BaseModelAdmin, TranslationAdminMixin):
    list_display = [
        'display_name_ru', 'name', 'icon_preview', 'colored_status', 
        'order', 'vacancies_count_display'
    ]
    list_filter = ['is_active', 'name']
    search_fields = ['display_name_ru', 'display_name_ky', 'display_name_en', 'name']
    list_editable = ['order']
    ordering = ['order', 'display_name_ru']
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            vacancies_count=Count('vacancy', distinct=True)
        )
    
    def icon_preview(self, obj):
        if obj.icon:
            return format_html(
                '<span style="font-size: 20px; padding: 6px; background: #3b82f6; '
                'color: white; border-radius: 6px; display: inline-block; '
                'min-width: 32px; text-align: center; '
                'box-shadow: 0 2px 4px rgba(0,0,0,0.1);">{}</span>',
                obj.icon
            )
        return '📄'
    icon_preview.short_description = '🎯 Иконка'
    
    def vacancies_count_display(self, obj):
        count = getattr(obj, 'vacancies_count', 0)
        return format_html(
            '<span style="background: #10b981; color: white; padding: 4px 8px; '
            'border-radius: 12px; font-size: 12px; font-weight: 600;">'
            '💼 {} вакансий</span>',
            count
        )
    vacancies_count_display.short_description = '💼 Вакансии'
    vacancies_count_display.admin_order_field = 'vacancies_count'


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name_ru', 'short_name', 'head_name_ru', 'contact_email', 'contact_phone', 'is_active', 'vacancies_count']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name_ru', 'name_kg', 'name_en', 'short_name', 'head_name_ru', 'head_name_kg', 'head_name_en']
    list_editable = ['is_active']
    readonly_fields = ['created_at']
    
    fieldsets = (
        (_('Основная информация'), {
            'fields': (('name_ru', 'name_kg', 'name_en'), 'short_name', ('description_ru', 'description_kg', 'description_en'))
        }),
        (_('Руководство'), {
            'fields': (('head_name_ru', 'head_name_kg', 'head_name_en'),)
        }),
        (_('Контактная информация'), {
            'fields': ('contact_email', 'contact_phone')
        }),
        (_('Настройки'), {
            'fields': ('is_active', 'created_at')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            vacancies_count=Count('vacancy', distinct=True)
        )
    
    def vacancies_count(self, obj):
        return obj.vacancies_count
    vacancies_count.short_description = _('Количество вакансий')
    vacancies_count.admin_order_field = 'vacancies_count'


class VacancyApplicationInline(admin.TabularInline):
    model = VacancyApplication
    extra = 0
    readonly_fields = ['submitted_at', 'full_name_display', 'email', 'phone']
    fields = ['full_name_display', 'email', 'phone', 'status', 'submitted_at']
    
    def full_name_display(self, obj):
        return obj.get_full_name()
    full_name_display.short_description = _('ФИО')
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Vacancy)
class VacancyAdmin(BaseModelAdmin, TranslationAdminMixin):
    list_display = [
        'title_ru', 'category', 'department', 'employment_type_display', 
        'status_badge', 'is_featured', 'formatted_deadline', 'applications_count_display'
    ]
    list_filter = [
        'status', 'category', 'department', 'employment_type',
        'is_featured', 'posted_date', 'deadline'
    ]
    search_fields = [
        'title_ru', 'title_ky', 'title_en', 
        'short_description_ru', 'short_description_ky', 'short_description_en', 
        'tags'
    ]
    list_editable = ['is_featured']
    prepopulated_fields = {'slug': ('title_ru',)}
    date_hierarchy = 'posted_date'
    list_per_page = 15
    
    fieldsets = (
        ('📋 Основная информация', {
            'fields': (
                'title_ru', 'title_ky', 'title_en',
                'slug', 'category', 'department', 
                ('status', 'is_featured')
            )
        }),
        ('💼 Детали работы', {
            'fields': (
                ('location_ru', 'location_ky', 'location_en'), 
                'employment_type', 
                ('salary_min', 'salary_max'),
                ('experience_years_ru', 'experience_years_ky', 'experience_years_en'), 
                ('education_level_ru', 'education_level_ky', 'education_level_en')
            )
        }),
        ('📝 Описание', {
            'fields': (
                ('short_description_ru', 'short_description_ky', 'short_description_en'), 
                ('description_ru', 'description_ky', 'description_en')
            ),
            'classes': ['collapse']
        }),
        ('📋 Требования и условия', {
            'fields': (
                ('responsibilities_ru', 'responsibilities_ky', 'responsibilities_en'), 
                ('requirements_ru', 'requirements_ky', 'requirements_en'), 
                ('conditions_ru', 'conditions_ky', 'conditions_en')
            ),
            'classes': ['collapse']
        }),
        ('🏷️ Дополнительно', {
            'fields': ('tags', 'deadline')
        }),
        ('📞 Контактная информация', {
            'fields': ('contact_person', 'contact_email', 'contact_phone')
        }),
        ('📊 Статистика', {
            'fields': ('views_count', 'applications_count', 'posted_date', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def employment_type_display(self, obj):
        type_colors = {
            'full_time': '#10b981',
            'part_time': '#f59e0b', 
            'contract': '#6366f1',
            'internship': '#8b5cf6'
        }
        color = type_colors.get(obj.employment_type, '#6b7280')
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 8px; '
            'border-radius: 12px; font-size: 12px; font-weight: 600;">{}</span>',
            color, obj.get_employment_type_display()
        )
    employment_type_display.short_description = '💼 Тип занятости'
    
    def status_badge(self, obj):
        status_colors = {
            'draft': '#6b7280',
            'active': '#10b981',
            'closed': '#ef4444',
            'paused': '#f59e0b'
        }
        color = status_colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 8px; '
            'border-radius: 12px; font-size: 12px; font-weight: 600;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = '📊 Статус'
    
    def featured_badge(self, obj):
        if obj.is_featured:
            return format_html(
                '<span style="background: #f59e0b; color: white; padding: 4px 8px; '
                'border-radius: 12px; font-size: 12px; font-weight: 600;">⭐ Рекомендуемая</span>'
            )
        return ''
    featured_badge.short_description = '⭐ Рекомендуемая'
    
    def applications_count_display(self, obj):
        count = getattr(obj, 'applications_count', 0) or 0
        return format_html(
            '<span style="background: #3b82f6; color: white; padding: 4px 8px; '
            'border-radius: 12px; font-size: 12px; font-weight: 600;">'
            '📝 {} заявок</span>',
            count
        )
    applications_count_display.short_description = '📝 Заявки'
    
    formatted_deadline = format_date_field('deadline', '⏰ Срок подачи')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category', 'department')
    
    def applications_count_display(self, obj):
        count = obj.applications_count
        if count > 0:
            return format_html('<span style="color: green; font-weight: bold;">{}</span>', count)
        return count
    applications_count_display.short_description = _('Заявки')
    applications_count_display.admin_order_field = 'applications_count'
    
    def deadline_status(self, obj):
        if not obj.deadline:
            return format_html('<span style="color: gray;">Не указан</span>')
        
        if obj.is_expired:
            return format_html('<span style="color: red;">Просрочен</span>')
        elif obj.is_deadline_soon:
            return format_html('<span style="color: orange;">Скоро истекает</span>')
        else:
            return format_html('<span style="color: green;">Активен</span>')
    
    deadline_status.short_description = _('Статус крайнего срока')
    
    actions = ['make_published', 'make_draft', 'make_featured', 'remove_featured']
    
    def make_published(self, request, queryset):
        updated = queryset.update(status='published')
        self.message_user(request, f'Опубликовано {updated} вакансий.')
    make_published.short_description = _('Опубликовать выбранные вакансии')
    
    def make_draft(self, request, queryset):
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} вакансий переведены в черновики.')
    make_draft.short_description = _('Перевести в черновики')
    
    def make_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} вакансий отмечены как рекомендуемые.')
    make_featured.short_description = _('Отметить как рекомендуемые')
    
    def remove_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'У {updated} вакансий убрана отметка "рекомендуемая".')
    remove_featured.short_description = _('Убрать отметку "рекомендуемая"')


@admin.register(VacancyApplication)
class VacancyApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'full_name_display', 'vacancy', 'email', 'phone',
        'status', 'submitted_at'
    ]
    list_filter = ['status', 'submitted_at', 'vacancy__category', 'vacancy__department']
    search_fields = [
        'first_name', 'last_name', 'email', 'phone',
        'vacancy__title', 'vacancy__department__name'
    ]
    list_editable = ['status']
    readonly_fields = ['submitted_at', 'vacancy', 'first_name', 'last_name', 'email', 'phone', 'resume']
    date_hierarchy = 'submitted_at'
    
    fieldsets = (
        (_('Заявка'), {
            'fields': ('vacancy', 'status', 'submitted_at')
        }),
        (_('Персональная информация'), {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        (_('Документы и письма'), {
            'fields': ('cover_letter', 'resume', 'additional_info')
        }),
        (_('Заметки HR'), {
            'fields': ('notes',)
        }),
    )
    
    def full_name_display(self, obj):
        return obj.get_full_name()
    full_name_display.short_description = _('ФИО')
    full_name_display.admin_order_field = 'first_name'
    
    actions = ['mark_reviewed', 'mark_interview', 'mark_accepted', 'mark_rejected']
    
    def mark_reviewed(self, request, queryset):
        updated = queryset.update(status='reviewed')
        self.message_user(request, f'{updated} заявок отмечены как рассмотренные.')
    mark_reviewed.short_description = _('Отметить как рассмотренные')
    
    def mark_interview(self, request, queryset):
        updated = queryset.update(status='interview')
        self.message_user(request, f'{updated} заявок отмечены для собеседования.')
    mark_interview.short_description = _('Пригласить на собеседование')
    
    def mark_accepted(self, request, queryset):
        updated = queryset.update(status='accepted')
        self.message_user(request, f'{updated} заявок приняты.')
    mark_accepted.short_description = _('Принять заявки')
    
    def mark_rejected(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} заявок отклонены.')
    mark_rejected.short_description = _('Отклонить заявки')
