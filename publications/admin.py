from django.contrib import admin
from .models import ResearchCenter, Publication

@admin.register(ResearchCenter)
class ResearchCenterAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_created_at']
    search_fields = ['name']
    list_filter = ['created_at']  # Убедитесь, что created_at есть в модели
    
    def get_created_at(self, obj):
        return obj.created_at
    get_created_at.short_description = 'Дата создания'
    get_created_at.admin_order_field = 'created_at'

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ['title', 'journal', 'year', 'citation_index', 'center', 'get_created_at', 'is_published']
    list_filter = ['year', 'journal', 'center', 'is_published']  # Убедитесь, что is_published есть в модели
    search_fields = ['title', 'journal', 'authors__last_name', 'authors__first_name']
    filter_horizontal = ['authors']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_created_at(self, obj):
        return obj.created_at
    get_created_at.short_description = 'Дата создания'
    get_created_at.admin_order_field = 'created_at'

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'authors', 'journal', 'year')
        }),
        ('Детали', {
            'fields': ('citation_index', 'doi', 'abstract', 'center')
        }),
        ('Статус', {
            'fields': ('is_published',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )