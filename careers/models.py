from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.urls import reverse


class CareerCategory(models.Model):
    """Категории вакансий"""
    CATEGORY_CHOICES = [
        ('academic', _('Преподавательские')),
        ('administrative', _('Административные')),
        ('technical', _('Технические')),
        ('service', _('Обслуживающие')),
    ]
    
    name = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        unique=True,
        verbose_name=_('Категория')
    )
    display_name = models.CharField(
        max_length=100,
        verbose_name=_('Название для отображения')
    )
    icon = models.CharField(
        max_length=10,
        default='💼',
        verbose_name=_('Иконка')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Описание категории')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Активна')
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Порядок сортировки')
    )
    
    class Meta:
        verbose_name = _('Категория карьеры')
        verbose_name_plural = _('Категории карьеры')
        ordering = ['order', 'display_name']
    
    def __str__(self):
        return self.display_name


class Department(models.Model):
    """Подразделения университета"""
    name = models.CharField(
        max_length=200,
        verbose_name=_('Название подразделения')
    )
    short_name = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('Краткое название')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Описание подразделения')
    )
    head_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Руководитель')
    )
    contact_email = models.EmailField(
        blank=True,
        verbose_name=_('Email для связи')
    )
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_("Номер телефона должен быть в формате: '+996123456789'")
    )
    contact_phone = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        verbose_name=_('Телефон для связи')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Активно')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Создано')
    )
    
    class Meta:
        verbose_name = _('Подразделение')
        verbose_name_plural = _('Подразделения')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Vacancy(models.Model):
    """Модель вакансий"""
    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', _('Полный рабочий день')),
        ('part_time', _('Неполный рабочий день')),
        ('contract', _('Контракт')),
        ('internship', _('Стажировка')),
        ('temporary', _('Временная работа')),
    ]
    
    STATUS_CHOICES = [
        ('draft', _('Черновик')),
        ('published', _('Опубликовано')),
        ('closed', _('Закрыто')),
        ('archived', _('Архив')),
    ]
    
    title = models.CharField(
        max_length=200,
        verbose_name=_('Название вакансии')
    )
    slug = models.SlugField(
        max_length=250,
        unique=True,
        blank=True,
        verbose_name=_('URL')
    )
    category = models.ForeignKey(
        CareerCategory,
        on_delete=models.CASCADE,
        verbose_name=_('Категория')
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        verbose_name=_('Подразделение')
    )
    location = models.CharField(
        max_length=100,
        default='Бишкек',
        verbose_name=_('Место работы')
    )
    employment_type = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_TYPE_CHOICES,
        default='full_time',
        verbose_name=_('Тип занятости')
    )
    salary_min = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_('Зарплата от (сом)')
    )
    salary_max = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_('Зарплата до (сом)')
    )
    experience_years = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('Опыт работы')
    )
    education_level = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Требования к образованию')
    )
    
    # Основное содержание
    short_description = models.TextField(
        verbose_name=_('Краткое описание')
    )
    description = models.TextField(
        verbose_name=_('Полное описание')
    )
    responsibilities = models.TextField(
        help_text=_('Каждое обязательство с новой строки'),
        verbose_name=_('Обязанности')
    )
    requirements = models.TextField(
        help_text=_('Каждое требование с новой строки'),
        verbose_name=_('Требования')
    )
    conditions = models.TextField(
        blank=True,
        help_text=_('Каждое условие с новой строки'),
        verbose_name=_('Условия работы')
    )
    
    # Мета информация
    tags = models.CharField(
        max_length=500,
        blank=True,
        help_text=_('Теги через запятую'),
        verbose_name=_('Теги')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name=_('Статус')
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name=_('Рекомендуемая вакансия')
    )
    
    # Даты
    posted_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата публикации')
    )
    deadline = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Крайний срок подачи заявок')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Обновлено')
    )
    
    # Контактная информация
    contact_person = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Контактное лицо')
    )
    contact_email = models.EmailField(
        blank=True,
        verbose_name=_('Email для заявок')
    )
    contact_phone = models.CharField(
        max_length=17,
        blank=True,
        verbose_name=_('Телефон для связи')
    )
    
    # Счетчики
    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Количество просмотров')
    )
    applications_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Количество заявок')
    )
    
    class Meta:
        verbose_name = _('Вакансия')
        verbose_name_plural = _('Вакансии')
        ordering = ['-posted_date', '-is_featured']
        indexes = [
            models.Index(fields=['status', 'category']),
            models.Index(fields=['posted_date']),
            models.Index(fields=['deadline']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('careers:vacancy_detail', kwargs={'slug': self.slug})
    
    def get_tags_list(self):
        """Возвращает список тегов"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []
    
    def get_responsibilities_list(self):
        """Возвращает список обязанностей"""
        return [resp.strip() for resp in self.responsibilities.split('\n') if resp.strip()]
    
    def get_requirements_list(self):
        """Возвращает список требований"""
        return [req.strip() for req in self.requirements.split('\n') if req.strip()]
    
    def get_conditions_list(self):
        """Возвращает список условий работы"""
        if self.conditions:
            return [cond.strip() for cond in self.conditions.split('\n') if cond.strip()]
        return []
    
    def get_salary_display(self):
        """Форматированное отображение зарплаты"""
        if self.salary_min and self.salary_max:
            return f"{self.salary_min:,} - {self.salary_max:,} сом"
        elif self.salary_min:
            return f"от {self.salary_min:,} сом"
        elif self.salary_max:
            return f"до {self.salary_max:,} сом"
        return _("По договоренности")
    
    @property
    def is_deadline_soon(self):
        """Проверяет, скоро ли истекает срок подачи заявок"""
        if not self.deadline:
            return False
        
        from datetime import date, timedelta
        today = date.today()
        return self.deadline - today <= timedelta(days=7) and self.deadline > today
    
    @property
    def is_expired(self):
        """Проверяет, истек ли срок подачи заявок"""
        if not self.deadline:
            return False
        
        from datetime import date
        return self.deadline < date.today()


class VacancyApplication(models.Model):
    """Заявки на вакансии"""
    vacancy = models.ForeignKey(
        Vacancy,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name=_('Вакансия')
    )
    first_name = models.CharField(
        max_length=100,
        verbose_name=_('Имя')
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name=_('Фамилия')
    )
    email = models.EmailField(
        verbose_name=_('Email')
    )
    phone = models.CharField(
        max_length=17,
        verbose_name=_('Телефон')
    )
    cover_letter = models.TextField(
        verbose_name=_('Сопроводительное письмо')
    )
    resume = models.FileField(
        upload_to='careers/resumes/%Y/%m/',
        verbose_name=_('Резюме')
    )
    additional_info = models.TextField(
        blank=True,
        verbose_name=_('Дополнительная информация')
    )
    
    # Мета информация
    submitted_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата подачи')
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('new', _('Новая')),
            ('reviewed', _('Рассмотрена')),
            ('interview', _('Собеседование')),
            ('accepted', _('Принята')),
            ('rejected', _('Отклонена')),
        ],
        default='new',
        verbose_name=_('Статус')
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('Заметки HR')
    )
    
    class Meta:
        verbose_name = _('Заявка на вакансию')
        verbose_name_plural = _('Заявки на вакансии')
        ordering = ['-submitted_at']
        unique_together = ['vacancy', 'email']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.vacancy.title}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
