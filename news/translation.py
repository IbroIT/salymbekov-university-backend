from modeltranslation.translator import register, TranslationOptions
from .models import News, NewsCategory, NewsTag

# Поскольку мы добавили мультиязычные поля напрямую в модели,
# нам больше не нужно использовать modeltranslation для автоматической генерации полей

# Оставляем пустые настройки для совместимости
@register(NewsCategory)  
class NewsCategoryTranslationOptions(TranslationOptions):
    fields = ()


@register(NewsTag)
class NewsTagTranslationOptions(TranslationOptions):
    fields = ()


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ()
