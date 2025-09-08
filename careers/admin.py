from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.db.models import Count
from .models import CareerCategory, Department, Vacancy, VacancyApplication


@admin.register(CareerCategory)
class CareerCategoryAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'name', 'icon', 'is_active', 'order', 'vacancies_count']
    list_filter = ['is_active', 'name']
    search_fields = ['display_name', 'name']
    list_editable = ['is_active', 'order']
    ordering = ['order', 'display_name']
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            vacancies_count=Count('vacancy', distinct=True)
        )
    
    def vacancies_count(self, obj):
        return obj.vacancies_count
    vacancies_count.short_description = _('Количество вакансий')
    vacancies_count.admin_order_field = 'vacancies_count'


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_name', 'head_name', 'contact_email', 'contact_phone', 'is_active', 'vacancies_count']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'short_name', 'head_name']
    list_editable = ['is_active']
    readonly_fields = ['created_at']
    
    fieldsets = (
        (_('Основная информация'), {
            'fields': ('name', 'short_name', 'description')
        }),
        (_('Руководство'), {
            'fields': ('head_name',)
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
class VacancyAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'department', 'employment_type', 
        'status', 'is_featured', 'posted_date', 'deadline_status', 
        'views_count', 'applications_count_display'
    ]
    list_filter = [
        'status', 'category', 'department', 'employment_type',
        'is_featured', 'posted_date', 'deadline'
    ]
    search_fields = ['title', 'short_description', 'tags']
    list_editable = ['status', 'is_featured']
    readonly_fields = ['slug', 'posted_date', 'updated_at', 'views_count', 'applications_count']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [VacancyApplicationInline]
    date_hierarchy = 'posted_date'
    
    fieldsets = (
        (_('Основная информация'), {
            'fields': ('title', 'slug', 'category', 'department', 'status', 'is_featured')
        }),
        (_('Детали работы'), {
            'fields': (
                'location', 'employment_type', 'salary_min', 'salary_max',
                'experience_years', 'education_level'
            )
        }),
        (_('Описание'), {
            'fields': ('short_description', 'description')
        }),
        (_('Требования и условия'), {
            'fields': ('responsibilities', 'requirements', 'conditions')
        }),
        (_('Дополнительно'), {
            'fields': ('tags', 'deadline')
        }),
        (_('Контактная информация'), {
            'fields': ('contact_person', 'contact_email', 'contact_phone')
        }),
        (_('Статистика'), {
            'fields': ('views_count', 'applications_count', 'posted_date', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
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
