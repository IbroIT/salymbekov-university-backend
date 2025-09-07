from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class ResearchCenter(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название центра", default="Новый научный центр")
    name_ky = models.CharField(max_length=255, verbose_name="Борбордун аты (кырг)", blank=True, default="")
    name_en = models.CharField(max_length=255, verbose_name="Center name (eng)", blank=True, default="")
    
    description = models.TextField(blank=True, verbose_name="Описание", default="")
    description_ky = models.TextField(blank=True, verbose_name="Сүрөттөө (кырг)", default="")
    description_en = models.TextField(blank=True, verbose_name="Description (eng)", default="")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Научный центр"
        verbose_name_plural = "Научные центры"
        ordering = ['name']

class Publication(models.Model):
    title = models.CharField(max_length=500, verbose_name="Название публикации", default="Новая публикация")
    title_ky = models.CharField(max_length=500, verbose_name="Жарыялоонун аты (кырг)", blank=True, default="")
    title_en = models.CharField(max_length=500, verbose_name="Publication title (eng)", blank=True, default="")
    
    authors = models.ManyToManyField(User, verbose_name="Авторы", related_name='publications')
    
    journal = models.CharField(max_length=255, verbose_name="Журнал", default="")
    journal_ky = models.CharField(max_length=255, verbose_name="Журнал (кырг)", blank=True, default="")
    journal_en = models.CharField(max_length=255, verbose_name="Journal (eng)", blank=True, default="")
    
    year = models.IntegerField(
        verbose_name="Год публикации",
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2100)
        ]
    )
    citation_index = models.IntegerField(
        default=0,
        verbose_name="Индекс цитирования",
        validators=[MinValueValidator(0)]
    )
    doi = models.CharField(max_length=100, blank=True, verbose_name="DOI", unique=True, default="")
    
    abstract = models.TextField(blank=True, verbose_name="Аннотация", default="")
    abstract_ky = models.TextField(blank=True, verbose_name="Аннотация (кырг)", default="")
    abstract_en = models.TextField(blank=True, verbose_name="Abstract (eng)", default="")
    
    center = models.ForeignKey(
        ResearchCenter,
        on_delete=models.CASCADE,
        verbose_name="Научный центр",
        related_name='publications'
    )
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.year})"

    def author_names(self):
        return ", ".join([f"{author.last_name} {author.first_name}" for author in self.authors.all()])

    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"
        ordering = ['-year', '-citation_index']