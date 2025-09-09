from django.contrib import admin
from .models import ResearchArea, ResearchCenter, Grant, Conference, Publication, GrantApplication


@admin.register(ResearchArea)
class ResearchAreaAdmin(admin.ModelAdmin):
    list_display = ['title_ru', 'projects_count', 'publications_count', 'researchers_count', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title_ru', 'title_en', 'title_kg']
    list_editable = ['projects_count', 'publications_count', 'researchers_count', 'is_active']
    ordering = ['title_ru']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title_ru', 'title_en', 'title_kg', 'icon', 'color')
        }),
        ('Описание', {
            'fields': ('description_ru', 'description_en', 'description_kg')
        }),
        ('Статистика', {
            'fields': ('projects_count', 'publications_count', 'researchers_count')
        }),
        ('Настройки', {
            'fields': ('is_active',)
        }),
    )


@admin.register(ResearchCenter)
class ResearchCenterAdmin(admin.ModelAdmin):
    list_display = ['name_ru', 'director_ru', 'staff_count', 'established_year', 'is_active']
    list_filter = ['is_active', 'established_year']
    search_fields = ['name_ru', 'name_en', 'name_kg', 'director_ru', 'director_en', 'director_kg']
    list_editable = ['staff_count', 'is_active']
    ordering = ['name_ru']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name_ru', 'name_en', 'name_kg', 'director_ru', 'director_en', 'director_kg', 'established_year', 'staff_count')
        }),
        ('Описание', {
            'fields': ('description_ru', 'description_en', 'description_kg')
        }),
        ('Оборудование', {
            'fields': ('equipment_ru', 'equipment_en', 'equipment_kg')
        }),
        ('Контакты', {
            'fields': ('website', 'email', 'phone')
        }),
        ('Медиа', {
            'fields': ('image',)
        }),
        ('Настройки', {
            'fields': ('is_active',)
        }),
    )


@admin.register(Grant)
class GrantAdmin(admin.ModelAdmin):
    list_display = ['title_ru', 'organization_ru', 'amount', 'deadline', 'category', 'status']
    list_filter = ['category', 'status', 'is_active', 'created_at']
    search_fields = ['title_ru', 'title_en', 'title_kg', 'organization_ru', 'organization_en', 'organization_kg']
    list_editable = ['status']
    date_hierarchy = 'deadline'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title_ru', 'title_en', 'title_kg', 'organization_ru', 'organization_en', 'organization_kg', 'amount')
        }),
        ('Сроки', {
            'fields': ('deadline', 'duration_ru', 'duration_en', 'duration_kg')
        }),
        ('Категория и статус', {
            'fields': ('category', 'status')
        }),
        ('Требования', {
            'fields': ('requirements_ru', 'requirements_en', 'requirements_kg')
        }),
        ('Описание', {
            'fields': ('description_ru', 'description_en', 'description_kg')
        }),
        ('Контакты', {
            'fields': ('contact', 'website')
        }),
        ('Настройки', {
            'fields': ('is_active',)
        }),
    )
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related()


@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ['title_ru', 'start_date', 'end_date', 'location_ru', 'status', 'speakers_count']
    list_filter = ['status', 'start_date', 'is_active']
    search_fields = ['title_ru', 'title_en', 'title_kg', 'location_ru']
    list_editable = ['status', 'speakers_count']
    date_hierarchy = 'start_date'
    ordering = ['start_date']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title_ru', 'title_en', 'title_kg', 'status')
        }),
        ('Даты', {
            'fields': ('start_date', 'end_date', 'deadline')
        }),
        ('Место проведения', {
            'fields': ('location_ru', 'location_en', 'location_kg')
        }),
        ('Описание', {
            'fields': ('description_ru', 'description_en', 'description_kg')
        }),
        ('Темы', {
            'fields': ('topics_ru', 'topics_en', 'topics_kg')
        }),
        ('Спикеры', {
            'fields': ('speakers_ru', 'speakers_en', 'speakers_kg', 'speakers_count')
        }),
        ('Дополнительно', {
            'fields': ('participants_limit', 'website', 'image')
        }),
        ('Настройки', {
            'fields': ('is_active',)
        }),
    )


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ['title_ru', 'authors_ru', 'journal', 'publication_date', 'publication_type', 'impact_factor', 'citations_count', 'is_featured']
    list_filter = ['publication_type', 'publication_date', 'is_featured', 'is_active', 'research_area']
    search_fields = ['title_ru', 'title_en', 'title_kg', 'authors_ru', 'authors_en', 'authors_kg', 'journal']
    list_editable = ['is_featured', 'citations_count']
    date_hierarchy = 'publication_date'
    ordering = ['-publication_date']
    raw_id_fields = ['research_area', 'research_center']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title_ru', 'title_en', 'title_kg', 'authors_ru', 'authors_en', 'authors_kg', 'publication_type')
        }),
        ('Публикация', {
            'fields': ('journal', 'publication_date', 'doi', 'url')
        }),
        ('Метрики', {
            'fields': ('impact_factor', 'citations_count')
        }),
        ('Аннотация', {
            'fields': ('abstract_ru', 'abstract_en', 'abstract_kg')
        }),
        ('Ключевые слова', {
            'fields': ('keywords_ru', 'keywords_en', 'keywords_kg')
        }),
        ('Связи', {
            'fields': ('research_area', 'research_center')
        }),
        ('Файлы', {
            'fields': ('file',)
        }),
        ('Настройки', {
            'fields': ('is_featured', 'is_active')
        }),
    )


@admin.register(GrantApplication)
class GrantApplicationAdmin(admin.ModelAdmin):
    list_display = ['project_title', 'principal_investigator', 'grant', 'status', 'budget', 'submitted_at']
    list_filter = ['status', 'submitted_at', 'grant__category']
    search_fields = ['project_title', 'principal_investigator', 'email', 'department']
    list_editable = ['status']
    date_hierarchy = 'submitted_at'
    ordering = ['-submitted_at']
    raw_id_fields = ['grant']
    readonly_fields = ['submitted_at']
    
    fieldsets = (
        ('Заявка', {
            'fields': ('grant', 'project_title', 'status')
        }),
        ('Контактная информация', {
            'fields': ('principal_investigator', 'email', 'phone', 'department')
        }),
        ('Команда', {
            'fields': ('team_members',)
        }),
        ('Проект', {
            'fields': ('project_description', 'budget', 'timeline', 'expected_results')
        }),
        ('Файлы', {
            'fields': ('files',)
        }),
        ('Администрирование', {
            'fields': ('admin_notes', 'submitted_at', 'reviewed_at')
        }),
    )
    
    actions = ['approve_applications', 'reject_applications']
    
    def approve_applications(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f'{updated} заявок одобрено.')
    approve_applications.short_description = "Одобрить выбранные заявки"
    
    def reject_applications(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} заявок отклонено.')
    reject_applications.short_description = "Отклонить выбранные заявки"
