#!/usr/bin/env python
import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_su_m.settings')
django.setup()

from research.models import ResearchArea

def create_research_areas():
    """Создание областей исследований"""
    
    # Очистка существующих данных
    ResearchArea.objects.all().delete()
    
    areas_data = [
        {
            'title_ru': 'Кардиология',
            'title_en': 'Cardiology',
            'title_kg': 'Кардиология',
            'description_ru': 'Исследования сердечно-сосудистых заболеваний и методов их лечения',
            'description_en': 'Research on cardiovascular diseases and treatment methods',
            'description_kg': 'Жүрөк-кан тамырлар ооруларын жана аларды дарылоо ыкмаларын изилдөө',
            'icon': '🫀',
            'color': 'red',
            'projects_count': 15,
            'publications_count': 45,
            'researchers_count': 28,
        },
        {
            'title_ru': 'Неврология',
            'title_en': 'Neuroscience',
            'title_kg': 'Нейрология',
            'description_ru': 'Изучение нервной системы и неврологических расстройств',
            'description_en': 'Study of the nervous system and neurological disorders',
            'description_kg': 'Нерв системасын жана неврологиялык бузулууларды изилдөө',
            'icon': '🧠',
            'color': 'blue',
            'projects_count': 8,
            'publications_count': 22,
            'researchers_count': 18,
        },
        {
            'title_ru': 'Онкология',
            'title_en': 'Oncology',
            'title_kg': 'Онкология',
            'description_ru': 'Диагностика, лечение и профилактика раковых заболеваний',
            'description_en': 'Diagnosis, treatment and prevention of cancer diseases',
            'description_kg': 'Рак ооруларын диагностикалоо, дарылоо жана алдын алуу',
            'icon': '🦠',
            'color': 'green',
            'projects_count': 12,
            'publications_count': 38,
            'researchers_count': 32,
        },
        {
            'title_ru': 'Генетика',
            'title_en': 'Genetics',
            'title_kg': 'Генетика',
            'description_ru': 'Изучение наследственности и генетических заболеваний',
            'description_en': 'Study of heredity and genetic diseases',
            'description_kg': 'Тукум куучулукту жана генетикалык ооруларды изилдөө',
            'icon': '🧬',
            'color': 'purple',
            'projects_count': 9,
            'publications_count': 31,
            'researchers_count': 21,
        },
        {
            'title_ru': 'Иммунология',
            'title_en': 'Immunology',
            'title_kg': 'Иммунология',
            'description_ru': 'Исследования иммунной системы и аутоиммунных заболеваний',
            'description_en': 'Research on the immune system and autoimmune diseases',
            'description_kg': 'Иммундук системаны жана аутоиммундук ооруларды изилдөө',
            'icon': '🦴',
            'color': 'orange',
            'projects_count': 6,
            'publications_count': 19,
            'researchers_count': 15,
        },
        {
            'title_ru': 'Фармакология',
            'title_en': 'Pharmacology',
            'title_kg': 'Фармакология',
            'description_ru': 'Разработка и исследование лекарственных препаратов',
            'description_en': 'Development and research of pharmaceutical drugs',
            'description_kg': 'Дары каражаттарын иштеп чыгуу жана изилдөө',
            'icon': '💊',
            'color': 'indigo',
            'projects_count': 7,
            'publications_count': 24,
            'researchers_count': 16,
        }
    ]
    
    created_areas = []
    for area_data in areas_data:
        area = ResearchArea.objects.create(**area_data)
        created_areas.append(area)
        print(f"Создана область исследований: {area.title_ru}")
    
    print(f"\nВсего создано областей исследований: {len(created_areas)}")
    return created_areas

if __name__ == "__main__":
    create_research_areas()
