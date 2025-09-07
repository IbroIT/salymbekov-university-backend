from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import ResearchCenter, Publication
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthorFilter(admin.SimpleListFilter):
    """Фильтр по авторам"""
    title = _('Авторы')
    parameter_name = 'author'

    def lookups(self, request, model_admin):
        authors = User.objects.filter(publications__isnull=False).distinct()
        return [(author.id, f"{author.last_name} {author.first_name}") for author in authors]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(authors__id=self.value())
        return queryset

@admin.register(ResearchCenter)
class ResearchCenterAdmin(admin.ModelAdmin):
    list_display = ['name', 'publications_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'name_ky', 'name_en', 'description', 'description_ky', 'description_en']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (_('Основная информация'), {
            'fields': ('name', 'description')
        }),
        (_('Кыргызский перевод'), {
            'fields': ('name_ky', 'description_ky'),
            'classes': ('collapse',)
        }),
        (_('Английский перевод'), {
            'fields': ('name_en', 'description_en'),
            'classes': ('collapse',)
        }),
        (_('Мета информация'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def publications_count(self, obj):
        return obj.publications.count()
    publications_count.short_description = _('Количество публикаций')

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ['title', 'year', 'journal', 'citation_index', 'center', 'is_published', 'created_at']
    list_filter = ['year', 'center', 'is_published', 'created_at', AuthorFilter]
    search_fields = [
        'title', 'title_ky', 'title_en', 
        'journal', 'journal_ky', 'journal_en', 
        'abstract', 'abstract_ky', 'abstract_en',
        'authors__last_name', 'authors__first_name'
    ]
    filter_horizontal = ['authors']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (_('Основная информация'), {
            'fields': ('title', 'journal', 'abstract', 'authors', 'year', 'citation_index', 'doi', 'center', 'is_published')
        }),
        (_('Кыргызский перевод'), {
            'fields': ('title_ky', 'journal_ky', 'abstract_ky'),
            'classes': ('collapse',)
        }),
        (_('Английский перевод'), {
            'fields': ('title_en', 'journal_en', 'abstract_en'),
            'classes': ('collapse',)
        }),
        (_('Мета информация'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Делаем поле DOI необязательным при создании
        if obj is None:
            form.base_fields['doi'].required = False
        return form