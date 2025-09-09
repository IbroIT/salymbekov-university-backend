from modeltranslation.translator import register, TranslationOptions
from .models import CareerCategory, Department, Vacancy

# Поскольку мы добавили мультиязычные поля напрямую в модели,
# нам больше не нужно использовать modeltranslation для автоматической генерации полей

# Оставляем пустые настройки для совместимости
@register(CareerCategory)
class CareerCategoryTranslationOptions(TranslationOptions):
    fields = ()


@register(Department)
class DepartmentTranslationOptions(TranslationOptions):
    fields = ()


@register(Vacancy)
class VacancyTranslationOptions(TranslationOptions):
    fields = ()
