# banner/models.py
from django.db import models 
from django.utils.translation import gettext_lazy as _

class Banner(models.Model):
    image = models.ImageField(upload_to='banners/', verbose_name=_("Изображение"))
    title_ru = models.CharField(max_length=200, verbose_name=_("Заголовок (русский)"))
    title_kg = models.CharField(max_length=200, verbose_name=_("Заголовок (кыргызский)"))
    title_en = models.CharField(max_length=200, verbose_name=_("Заголовок (английский)"))
    subtitle_ru = models.CharField(max_length=300, verbose_name=_("Подзаголовок (русский)"))
    subtitle_kg = models.CharField(max_length=300, verbose_name=_("Подзаголовок (кыргызский)"))
    subtitle_en = models.CharField(max_length=300, verbose_name=_("Подзаголовок (английский)"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активный"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Порядок"))
    
    class Meta:
        ordering = ['order']
        verbose_name = _("Баннер")
        verbose_name_plural = _("Баннеры")
    
    def __str__(self):
        return self.title_ru