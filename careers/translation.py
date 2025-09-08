from modeltranslation.translator import register, TranslationOptions
from .models import CareerCategory, Department, Vacancy


@register(CareerCategory)
class CareerCategoryTranslationOptions(TranslationOptions):
    fields = ('display_name', 'description')


@register(Department)
class DepartmentTranslationOptions(TranslationOptions):
    fields = ('name', 'short_name', 'description')


@register(Vacancy)
class VacancyTranslationOptions(TranslationOptions):
    fields = (
        'title', 'location', 'experience_years', 'education_level',
        'short_description', 'description', 'responsibilities', 
        'requirements', 'conditions', 'tags', 'contact_person'
    )
