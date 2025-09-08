from django.core.management.base import BaseCommand
from django.utils.translation import activate
from careers.models import CareerCategory, Department, Vacancy

class Command(BaseCommand):
    help = 'Создает переводы для существующих данных careers'

    def handle(self, *args, **options):
        self.stdout.write('Создание переводов для careers данных...')
        
        # Переводы для категорий
        category_translations = {
            'academic': {
                'display_name_en': 'Academic',
                'display_name_ky': 'Академиялык',
                'description_en': 'Positions for teaching staff, professors, and academic researchers',
                'description_ky': 'Окутуучулар, профессорлор жана академиялык изилдөөчүлөр үчүн орундар'
            },
            'administrative': {
                'display_name_en': 'Administrative',
                'display_name_ky': 'Административдик',
                'description_en': 'Administrative positions in various departments',
                'description_ky': 'Ар түрдүү бөлүмдөрдөгү административдик орундар'
            },
            'technical': {
                'display_name_en': 'Technical',
                'display_name_ky': 'Техникалык',
                'description_en': 'Technical and IT positions',
                'description_ky': 'Техникалык жана IT орундар'
            },
            'service': {
                'display_name_en': 'Support Staff',
                'display_name_ky': 'Колдоочу персонал',
                'description_en': 'Support and auxiliary staff positions',
                'description_ky': 'Колдоочу жана жардамчы персонал орундары'
            }
        }

        # Обновляем категории
        for category in CareerCategory.objects.all():
            if category.name in category_translations:
                trans = category_translations[category.name]
                category.display_name_en = trans['display_name_en']
                category.display_name_ky = trans['display_name_ky']
                category.description_en = trans['description_en']
                category.description_ky = trans['description_ky']
                category.save()
                self.stdout.write(f'✓ Обновлена категория: {category.name}')

        # Переводы для подразделений
        dept_translations = {
            'Факультет информационных технологий': {
                'name_en': 'Faculty of Information Technology',
                'name_ky': 'Маалыматтык технологиялар факультети',
                'description_en': 'Faculty responsible for IT education and research',
                'description_ky': 'IT билим берүү жана изилдөө үчүн жооптуу факультет'
            },
            'Отдел кадров': {
                'name_en': 'Human Resources Department',
                'name_ky': 'Кадрлар бөлүмү',
                'description_en': 'Department managing university personnel',
                'description_ky': 'Университеттин персоналын башкаруучу бөлүм'
            },
            'Административное управление': {
                'name_en': 'Administrative Management',
                'name_ky': 'Административдик башкаруу',
                'description_en': 'Administrative management department',
                'description_ky': 'Административдик башкаруу бөлүмү'
            },
            'IT отдел': {
                'name_en': 'IT Department',
                'name_ky': 'IT бөлүмү',
                'description_en': 'Information technology support department',
                'description_ky': 'Маалыматтык технологияларды колдоо бөлүмү'
            }
        }

        # Обновляем подразделения
        for dept in Department.objects.all():
            if dept.name in dept_translations:
                trans = dept_translations[dept.name]
                dept.name_en = trans['name_en']
                dept.name_ky = trans['name_ky']
                dept.description_en = trans['description_en']
                dept.description_ky = trans['description_ky']
                dept.save()
                self.stdout.write(f'✓ Обновлено подразделение: {dept.name}')

        # Переводы для вакансий
        vacancy_translations = {
            'Преподаватель программирования': {
                'title_en': 'Programming Instructor',
                'title_ky': 'Программалоо мугалими',
                'short_description_en': 'Looking for an experienced programming instructor',
                'short_description_ky': 'Тажрыйбалуу программалоо мугалимин издейбиз',
                'description_en': '''We are looking for an experienced programming instructor to join our IT faculty. 

Requirements:
- Higher education in Computer Science or related field
- At least 3 years of teaching experience
- Knowledge of modern programming languages
- Ability to work with students

Responsibilities:
- Conducting programming courses
- Developing curricula
- Working with students
- Participating in research projects''',
                'description_ky': '''Биз IT факультетибизге кошулуу үчүн тажрыйбалуу программалоо мугалимин издейбиз.

Талаптар:
- Компьютердик илимдер же байланыштуу тармактагы жогорку билим
- Кеминде 3 жылдык окутуу тажрыйбасы
- Заманбап программалоо тилдерин билүү
- Студенттер менен иштөө жөндөмү

Милдеттер:
- Программалоо курстарын өткөрүү
- Окуу программаларын иштеп чыгуу
- Студенттер менен иштөө
- Изилдөө долбоорлоруна катышуу'''
            }
        }

        # Обновляем одну вакансию для примера
        try:
            vacancy = Vacancy.objects.filter(title__contains='Преподаватель').first()
            if vacancy and 'Преподаватель программирования' in vacancy_translations:
                trans = vacancy_translations['Преподаватель программирования']
                vacancy.title_en = trans['title_en']
                vacancy.title_ky = trans['title_ky']
                vacancy.short_description_en = trans['short_description_en']
                vacancy.short_description_ky = trans['short_description_ky']
                vacancy.description_en = trans['description_en']
                vacancy.description_ky = trans['description_ky']
                vacancy.save()
                self.stdout.write(f'✓ Обновлена вакансия: {vacancy.title}')
        except Exception as e:
            self.stdout.write(f'Ошибка обновления вакансии: {e}')

        self.stdout.write(self.style.SUCCESS('Переводы успешно созданы!'))
