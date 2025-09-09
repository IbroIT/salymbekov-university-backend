from rest_framework import serializers
from django.utils import translation
from .models import CareerCategory, Department, Vacancy, VacancyApplication


class LanguageAwareSerializer(serializers.ModelSerializer):
    """Базовый сериализатор с поддержкой языков"""
    
    def get_localized_field(self, instance, field_name):
        """Получить переведенное поле в зависимости от текущего языка"""
        # Получаем язык из заголовка запроса или используем текущий язык Django
        request = self.context.get('request')
        if request:
            current_language = request.headers.get('Accept-Language', 'ru')
            # Преобразуем 'ky' в 'kg' для совместимости с полями базы данных
            if current_language == 'ky':
                current_language = 'kg'
        else:
            current_language = translation.get_language() or 'ru'
            if current_language == 'ky':
                current_language = 'kg'
        
        # Попробуем получить поле для текущего языка
        localized_field = f"{field_name}_{current_language}"
        if hasattr(instance, localized_field):
            value = getattr(instance, localized_field)
            if value:
                return value
        
        # Если нет перевода для текущего языка, попробуем русский (по умолчанию)
        default_field = f"{field_name}_ru"
        if hasattr(instance, default_field):
            value = getattr(instance, default_field)
            if value:
                return value
        
        # Если русского тоже нет, попробуем английский
        english_field = f"{field_name}_en"
        if hasattr(instance, english_field):
            value = getattr(instance, english_field)
            if value:
                return value
        
        # Если ничего нет, вернем пустую строку
        return ""


class CareerCategorySerializer(LanguageAwareSerializer):
    """Сериализатор для категорий карьеры"""
    display_name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    
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
    
    def get_display_name(self, obj):
        return self.get_localized_field(obj, 'display_name')
    
    def get_description(self, obj):
        return self.get_localized_field(obj, 'description')


class DepartmentSerializer(LanguageAwareSerializer):
    """Сериализатор для подразделений"""
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    head_name = serializers.SerializerMethodField()
    
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
    
    def get_name(self, obj):
        return self.get_localized_field(obj, 'name')
    
    def get_description(self, obj):
        return self.get_localized_field(obj, 'description')
    
    def get_head_name(self, obj):
        return self.get_localized_field(obj, 'head_name')


class VacancyListSerializer(LanguageAwareSerializer):
    """Сериализатор для списка вакансий (краткая информация)"""
    category = CareerCategorySerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    tags_list = serializers.SerializerMethodField()
    salary_display = serializers.SerializerMethodField()
    is_deadline_soon = serializers.ReadOnlyField()
    is_expired = serializers.ReadOnlyField()
    
    # Мультиязычные поля
    title = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    experience_years = serializers.SerializerMethodField()
    education_level = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    
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
    
    def get_title(self, obj):
        return self.get_localized_field(obj, 'title')
    
    def get_location(self, obj):
        return self.get_localized_field(obj, 'location')
    
    def get_experience_years(self, obj):
        return self.get_localized_field(obj, 'experience_years')
    
    def get_education_level(self, obj):
        return self.get_localized_field(obj, 'education_level')
    
    def get_short_description(self, obj):
        return self.get_localized_field(obj, 'short_description')
    
    def get_tags_list(self, obj):
        return obj.get_tags_list()
    
    def get_salary_display(self, obj):
        return obj.get_salary_display()


class VacancyDetailSerializer(LanguageAwareSerializer):
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
    
    # Мультиязычные поля
    title = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    experience_years = serializers.SerializerMethodField()
    education_level = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    responsibilities = serializers.SerializerMethodField()
    requirements = serializers.SerializerMethodField()
    conditions = serializers.SerializerMethodField()
    
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
            'responsibilities',
            'requirements',
            'conditions',
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
    
    def get_title(self, obj):
        return self.get_localized_field(obj, 'title')
    
    def get_location(self, obj):
        return self.get_localized_field(obj, 'location')
    
    def get_experience_years(self, obj):
        return self.get_localized_field(obj, 'experience_years')
    
    def get_education_level(self, obj):
        return self.get_localized_field(obj, 'education_level')
    
    def get_short_description(self, obj):
        return self.get_localized_field(obj, 'short_description')
    
    def get_description(self, obj):
        return self.get_localized_field(obj, 'description')
    
    def get_responsibilities(self, obj):
        return self.get_localized_field(obj, 'responsibilities')
    
    def get_requirements(self, obj):
        return self.get_localized_field(obj, 'requirements')
    
    def get_conditions(self, obj):
        return self.get_localized_field(obj, 'conditions')
    
    def get_tags_list(self, obj):
        return obj.get_tags_list()
    
    def get_responsibilities_list(self, obj):
        # Получаем текущий язык из запроса
        request = self.context.get('request')
        if request:
            current_language = request.headers.get('Accept-Language', 'ru')
        else:
            current_language = 'ru'
        
        return obj.get_responsibilities_list(current_language)
    
    def get_requirements_list(self, obj):
        # Получаем текущий язык из запроса
        request = self.context.get('request')
        if request:
            current_language = request.headers.get('Accept-Language', 'ru')
        else:
            current_language = 'ru'
        
        return obj.get_requirements_list(current_language)
    
    def get_conditions_list(self, obj):
        # Получаем текущий язык из запроса
        request = self.context.get('request')
        if request:
            current_language = request.headers.get('Accept-Language', 'ru')
        else:
            current_language = 'ru'
        
        return obj.get_conditions_list(current_language)
    
    def get_salary_display(self, obj):
        return obj.get_salary_display()


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
