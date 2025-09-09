from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class NewsCategory(models.Model):
    """Категории новостей"""
    NEWS = 'news'
    EVENTS = 'events'
    ANNOUNCEMENTS = 'announcements'
    
    CATEGORY_CHOICES = [
        (NEWS, 'Новости'),
        (EVENTS, 'События'),
        (ANNOUNCEMENTS, 'Объявления'),
    ]
    
    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL slug')
    
    # Мультиязычные поля
    name_ru = models.CharField(max_length=100, verbose_name='Название (русский)')
    name_kg = models.CharField(max_length=100, verbose_name='Название (кыргызский)')
    name_en = models.CharField(max_length=100, verbose_name='Название (английский)')
    
    description_ru = models.TextField(blank=True, verbose_name='Описание (русский)')
    description_kg = models.TextField(blank=True, verbose_name='Описание (кыргызский)')
    description_en = models.TextField(blank=True, verbose_name='Описание (английский)')
    
    class Meta:
        verbose_name = 'Категория новостей'
        verbose_name_plural = 'Категории новостей'
    
    def __str__(self):
        return self.name_ru or self.get_name_display()


class News(models.Model):
    """Основная модель для новостей, событий и объявлений"""
    # Мультиязычные текстовые поля
    title_ru = models.CharField(max_length=200, verbose_name='Заголовок (русский)')
    title_kg = models.CharField(max_length=200, verbose_name='Заголовок (кыргызский)')
    title_en = models.CharField(max_length=200, verbose_name='Заголовок (английский)')
    
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL slug')
    
    summary_ru = models.TextField(max_length=500, verbose_name='Краткое описание (русский)')
    summary_kg = models.TextField(max_length=500, verbose_name='Краткое описание (кыргызский)')
    summary_en = models.TextField(max_length=500, verbose_name='Краткое описание (английский)')
    
    content_ru = models.TextField(verbose_name='Полное содержание (русский)')
    content_kg = models.TextField(verbose_name='Полное содержание (кыргызский)')
    content_en = models.TextField(verbose_name='Полное содержание (английский)')
    
    image = models.ImageField(upload_to='news/images/', blank=True, null=True, verbose_name='Изображение')
    image_url = models.URLField(blank=True, null=True, verbose_name='URL изображения')
    
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE, verbose_name='Категория')
    
    author_ru = models.CharField(max_length=100, verbose_name='Автор (русский)', default='Администрация университета')
    author_kg = models.CharField(max_length=100, verbose_name='Автор (кыргызский)', default='Университеттин администрациясы')
    author_en = models.CharField(max_length=100, verbose_name='Автор (английский)', default='University Administration')
    
    # Основные временные поля
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    published_at = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    
    # Статус публикации
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    is_featured = models.BooleanField(default=False, verbose_name='Рекомендуемое')
    is_pinned = models.BooleanField(default=False, verbose_name='Закреплено')
    
    # Счетчики
    views_count = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')
    
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-published_at']
    
    def __str__(self):
        return self.title_ru
    
    @property
    def image_url_or_default(self):
        """Возвращает URL изображения или дефолтный URL"""
        if self.image:
            return self.image.url
        elif self.image_url:
            return self.image_url
        return None


class Event(models.Model):
    """Модель для событий с дополнительными полями"""
    EVENT_CATEGORIES = [
        ('conference', 'Конференция'),
        ('open-day', 'День открытых дверей'),
        ('competition', 'Конкурс'),
        ('ceremony', 'Церемония'),
        ('workshop', 'Мастер-класс'),
        ('seminar', 'Семинар'),
        ('lecture', 'Лекция'),
    ]
    
    EVENT_STATUS = [
        ('upcoming', 'Предстоящее'),
        ('ongoing', 'Текущее'),
        ('past', 'Прошедшее'),
        ('cancelled', 'Отменено'),
    ]
    
    news = models.OneToOneField(News, on_delete=models.CASCADE, related_name='event_details', verbose_name='Новость')
    
    # Детали события
    event_date = models.DateField(verbose_name='Дата события')
    event_time = models.TimeField(verbose_name='Время начала')
    end_time = models.TimeField(blank=True, null=True, verbose_name='Время окончания')
    
    location_ru = models.CharField(max_length=200, verbose_name='Место проведения (русский)')
    location_kg = models.CharField(max_length=200, verbose_name='Место проведения (кыргызский)')
    location_en = models.CharField(max_length=200, verbose_name='Место проведения (английский)')
    
    event_category = models.CharField(max_length=50, choices=EVENT_CATEGORIES, verbose_name='Тип события')
    status = models.CharField(max_length=20, choices=EVENT_STATUS, default='upcoming', verbose_name='Статус')
    
    max_participants = models.PositiveIntegerField(blank=True, null=True, verbose_name='Максимум участников')
    current_participants = models.PositiveIntegerField(default=0, verbose_name='Текущее количество участников')
    
    # Регистрация
    registration_required = models.BooleanField(default=False, verbose_name='Требуется регистрация')
    registration_deadline = models.DateTimeField(blank=True, null=True, verbose_name='Крайний срок регистрации')
    registration_link = models.URLField(blank=True, null=True, verbose_name='Ссылка на регистрацию')
    
    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
        ordering = ['event_date', 'event_time']
    
    def __str__(self):
        return f"{self.news.title_ru} - {self.event_date}"


class Announcement(models.Model):
    """Модель для объявлений с дополнительными полями"""
    ANNOUNCEMENT_TYPES = [
        ('academic', 'Учебное'),
        ('scholarship', 'Стипендия'),
        ('schedule', 'Расписание'),
        ('competition', 'Конкурс'),
        ('health', 'Здоровье'),
        ('technical', 'Техническое'),
        ('administrative', 'Административное'),
    ]
    
    PRIORITY_LEVELS = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
        ('urgent', 'Срочный'),
    ]
    
    news = models.OneToOneField(News, on_delete=models.CASCADE, related_name='announcement_details', verbose_name='Новость')
    
    # Детали объявления
    announcement_type = models.CharField(max_length=50, choices=ANNOUNCEMENT_TYPES, verbose_name='Тип объявления')
    priority = models.CharField(max_length=20, choices=PRIORITY_LEVELS, default='medium', verbose_name='Приоритет')
    
    # Сроки
    deadline = models.DateTimeField(blank=True, null=True, verbose_name='Крайний срок')
    is_deadline_approaching = models.BooleanField(default=False, verbose_name='Приближается дедлайн')
    
    # Вложения
    attachment = models.FileField(upload_to='announcements/attachments/', blank=True, null=True, verbose_name='Вложение')
    attachment_name = models.CharField(max_length=100, blank=True, verbose_name='Название вложения')
    
    # Целевая аудитория
    target_students = models.BooleanField(default=True, verbose_name='Для студентов')
    target_staff = models.BooleanField(default=False, verbose_name='Для сотрудников')
    target_faculty = models.BooleanField(default=False, verbose_name='Для преподавателей')
    
    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-priority', '-deadline']
    
    def __str__(self):
        return f"{self.news.title_ru} ({self.get_priority_display()})"
    
    def save(self, *args, **kwargs):
        # Автоматически определяем приближающийся дедлайн
        if self.deadline:
            from datetime import datetime, timedelta
            if self.deadline <= timezone.now() + timedelta(days=7):
                self.is_deadline_approaching = True
            else:
                self.is_deadline_approaching = False
        super().save(*args, **kwargs)


class NewsView(models.Model):
    """Модель для отслеживания просмотров новостей"""
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='news_views')
    ip_address = models.GenericIPAddressField(verbose_name='IP адрес')
    user_agent = models.TextField(blank=True, verbose_name='User Agent')
    viewed_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата просмотра')
    
    class Meta:
        verbose_name = 'Просмотр новости'
        verbose_name_plural = 'Просмотры новостей'
        unique_together = ['news', 'ip_address']  # Один просмотр с одного IP


class NewsTag(models.Model):
    """Теги для новостей"""
    name_ru = models.CharField(max_length=50, verbose_name='Название тега (русский)')
    name_kg = models.CharField(max_length=50, verbose_name='Название тега (кыргызский)')
    name_en = models.CharField(max_length=50, verbose_name='Название тега (английский)')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='URL slug')
    color = models.CharField(max_length=7, default='#3B82F6', verbose_name='Цвет (hex)')
    
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
    
    def __str__(self):
        return self.name_ru


class NewsTagRelation(models.Model):
    """Связь между новостями и тегами"""
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='tags')
    tag = models.ForeignKey(NewsTag, on_delete=models.CASCADE, related_name='news')
    
    class Meta:
        unique_together = ['news', 'tag']
        verbose_name = 'Связь новости с тегом'
        verbose_name_plural = 'Связи новостей с тегами'
