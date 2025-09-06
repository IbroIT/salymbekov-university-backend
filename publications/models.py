from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class ResearchCenter(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название центра")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Научный центр"
        verbose_name_plural = "Научные центры"
        ordering = ['name']

class Publication(models.Model):
    title = models.CharField(max_length=500, verbose_name="Название публикации")
    authors = models.ManyToManyField(User, verbose_name="Авторы", related_name='publications')
    journal = models.CharField(max_length=255, verbose_name="Журнал")
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
    doi = models.CharField(max_length=100, blank=True, verbose_name="DOI", unique=True)
    abstract = models.TextField(blank=True, verbose_name="Аннотация")
    center = models.ForeignKey(
        ResearchCenter,
        on_delete=models.CASCADE,
        verbose_name="Научный центр",
        related_name='publications'
    )
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")  # ЭТО ПОЛЕ ДОЛЖНО БЫТЬ!
    created_at = models.DateTimeField(auto_now_add=True)  # ЭТО ПОЛЕ ДОЛЖНО БЫТЬ!
    updated_at = models.DateTimeField(auto_now=True)  # ЭТО ПОЛЕ ДОЛЖНО БЫТЬ!

    def __str__(self):
        return f"{self.title} ({self.year})"

    def author_names(self):
        return ", ".join([f"{author.last_name} {author.first_name}" for author in self.authors.all()])

    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"
        ordering = ['-year', '-citation_index']
        indexes = [
            models.Index(fields=['year']),
            models.Index(fields=['citation_index']),
            models.Index(fields=['journal']),
        ]