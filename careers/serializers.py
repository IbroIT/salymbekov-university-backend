from rest_framework import serializers
from django.utils.translation import get_language
from .models import CareerCategory, Department, Vacancy, VacancyApplication


class CareerCategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий карьеры"""
    
    class Meta:
        model = CareerCategory
        fields = [
            'id',
            'name', 
            'display_name',
            'icon',
            'description',
            'is_active',
            'order'
        ]
    
    def to_representation(self, instance):
        """Переопределяем для возврата переведенных полей"""
        data = super().to_representation(instance)
        current_lang = get_language() or 'ru'
        
        # Возвращаем переведенные поля
        data['display_name'] = getattr(instance, f'display_name_{current_lang}', instance.display_name)
        data['description'] = getattr(instance, f'description_{current_lang}', instance.description)
        
        return data


class DepartmentSerializer(serializers.ModelSerializer):
    """Сериализатор для подразделений"""
    
    class Meta:
        model = Department
        fields = [
            'id',
            'name',
            'short_name',
            'description',
            'head_name',
            'contact_email',
            'contact_phone',
            'is_active'
        ]
    
    def to_representation(self, instance):
        """Переопределяем для возврата переведенных полей"""
        data = super().to_representation(instance)
        current_lang = get_language() or 'ru'
        
        # Возвращаем переведенные поля
        data['name'] = getattr(instance, f'name_{current_lang}', instance.name)
        data['description'] = getattr(instance, f'description_{current_lang}', instance.description)
        
        return data


class VacancyListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка вакансий (краткая информация)"""
    category = CareerCategorySerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    tags_list = serializers.SerializerMethodField()
    salary_display = serializers.SerializerMethodField()
    is_deadline_soon = serializers.ReadOnlyField()
    is_expired = serializers.ReadOnlyField()
    
    class Meta:
        model = Vacancy
        fields = [
            'id',
            'title',
            'slug',
            'category',
            'department',
            'location',
            'employment_type',
            'salary_display',
            'experience_years',
            'education_level',
            'short_description',
            'tags_list',
            'status',
            'is_featured',
            'posted_date',
            'deadline',
            'is_deadline_soon',
            'is_expired',
            'views_count',
            'applications_count'
        ]
    
    def get_tags_list(self, obj):
        return obj.get_tags_list()
    
    def get_salary_display(self, obj):
        return obj.get_salary_display()
    
    def to_representation(self, instance):
        """Переопределяем для возврата переведенных полей"""
        data = super().to_representation(instance)
        current_lang = get_language() or 'ru'
        
        # Возвращаем переведенные поля
        data['title'] = getattr(instance, f'title_{current_lang}', instance.title)
        data['short_description'] = getattr(instance, f'short_description_{current_lang}', instance.short_description)
        
        return data


class VacancyDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детальной информации о вакансии"""
    category = CareerCategorySerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    tags_list = serializers.SerializerMethodField()
    responsibilities_list = serializers.SerializerMethodField()
    requirements_list = serializers.SerializerMethodField()
    conditions_list = serializers.SerializerMethodField()
    salary_display = serializers.SerializerMethodField()
    is_deadline_soon = serializers.ReadOnlyField()
    is_expired = serializers.ReadOnlyField()
    
    class Meta:
        model = Vacancy
        fields = [
            'id',
            'title',
            'slug',
            'category',
            'department',
            'location',
            'employment_type',
            'salary_min',
            'salary_max',
            'salary_display',
            'experience_years',
            'education_level',
            'short_description',
            'description',
            'responsibilities_list',
            'requirements_list',
            'conditions_list',
            'tags_list',
            'status',
            'is_featured',
            'posted_date',
            'deadline',
            'updated_at',
            'contact_person',
            'contact_email',
            'contact_phone',
            'is_deadline_soon',
            'is_expired',
            'views_count',
            'applications_count'
        ]
    
    def get_tags_list(self, obj):
        return obj.get_tags_list()
    
    def get_responsibilities_list(self, obj):
        return obj.get_responsibilities_list()
    
    def get_requirements_list(self, obj):
        return obj.get_requirements_list()
    
    def get_conditions_list(self, obj):
        return obj.get_conditions_list()
    
    def get_salary_display(self, obj):
        return obj.get_salary_display()
    
    def to_representation(self, instance):
        """Переопределяем для возврата переведенных полей"""
        data = super().to_representation(instance)
        current_lang = get_language() or 'ru'
        
        # Возвращаем переведенные поля
        data['title'] = getattr(instance, f'title_{current_lang}', instance.title)
        data['short_description'] = getattr(instance, f'short_description_{current_lang}', instance.short_description)
        data['description'] = getattr(instance, f'description_{current_lang}', instance.description)
        data['responsibilities'] = getattr(instance, f'responsibilities_{current_lang}', instance.responsibilities)
        data['requirements'] = getattr(instance, f'requirements_{current_lang}', instance.requirements)
        data['working_conditions'] = getattr(instance, f'working_conditions_{current_lang}', instance.working_conditions)
        
        return data


class VacancyApplicationSerializer(serializers.ModelSerializer):
    """Сериализатор для заявок на вакансии"""
    vacancy_title = serializers.CharField(source='vacancy.title', read_only=True)
    full_name = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = VacancyApplication
        fields = [
            'id',
            'vacancy',
            'vacancy_title',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'phone',
            'cover_letter',
            'resume',
            'additional_info',
            'submitted_at',
            'status'
        ]
        read_only_fields = ['id', 'submitted_at', 'status']
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    
    def validate_email(self, value):
        """Проверка уникальности email для вакансии"""
        vacancy_id = self.initial_data.get('vacancy')
        if vacancy_id:
            existing = VacancyApplication.objects.filter(
                vacancy_id=vacancy_id, 
                email=value
            ).exists()
            if existing:
                raise serializers.ValidationError(
                    "Вы уже подали заявку на эту вакансию с данным email адресом."
                )
        return value


class VacancyApplicationListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка заявок (для админов)"""
    vacancy_title = serializers.CharField(source='vacancy.title', read_only=True)
    full_name = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = VacancyApplication
        fields = [
            'id',
            'vacancy',
            'vacancy_title',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'phone',
            'submitted_at',
            'status',
            'notes'
        ]
    
    def get_full_name(self, obj):
        return obj.get_full_name()


# Статистические сериализаторы
class VacancyStatsSerializer(serializers.Serializer):
    """Сериализатор для статистики вакансий"""
    total_vacancies = serializers.IntegerField()
    active_vacancies = serializers.IntegerField()
    featured_vacancies = serializers.IntegerField()
    total_applications = serializers.IntegerField()
    categories_stats = serializers.ListField()
    departments_stats = serializers.ListField()


class CategoryStatsSerializer(serializers.Serializer):
    """Сериализатор для статистики по категориям"""
    category_name = serializers.CharField()
    category_display = serializers.CharField()
    vacancies_count = serializers.IntegerField()
    applications_count = serializers.IntegerField()


class DepartmentStatsSerializer(serializers.Serializer):
    """Сериализатор для статистики по подразделениям"""
    department_name = serializers.CharField()
    vacancies_count = serializers.IntegerField()
    applications_count = serializers.IntegerField()
