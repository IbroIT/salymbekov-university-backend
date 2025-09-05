from modeltranslation.translator import register, TranslationOptions
from .models import News, NewsCategory, NewsTag


@register(NewsCategory)
class NewsCategoryTranslationOptions(TranslationOptions):
    fields = ()  # Категории будут фиксированными


@register(NewsTag)
class NewsTagTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'summary', 'content')
    required_languages = {'ru': ('title', 'summary', 'content')}
