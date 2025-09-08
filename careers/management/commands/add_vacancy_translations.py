from django.core.management.base import BaseCommand
from careers.models import Vacancy

class Command(BaseCommand):
    help = 'Добавляет переводы для всех вакансий'

    def handle(self, *args, **options):
        self.stdout.write('Добавление переводов для вакансий...')
        
        # Получаем все вакансии
        vacancies = Vacancy.objects.all()
        
        # Переводы для каждой вакансии по названию
        vacancy_translations = {
            'Системный администратор': {
                'title_en': 'System Administrator',
                'title_ky': 'Система администратору',
                'short_description_en': 'Looking for an experienced system administrator',
                'short_description_ky': 'Тажрыйбалуу система администраторун издейбиз',
                'description_en': '''We are looking for an experienced system administrator to maintain our IT infrastructure.

Requirements:
- Higher education in IT or related field
- At least 2 years of system administration experience
- Knowledge of Windows and Linux systems
- Experience with network administration

Responsibilities:
- Server maintenance and administration
- Network infrastructure support
- User support and training
- System security monitoring''',
                'description_ky': '''Биз IT инфраструктурабызды колдоо үчүн тажрыйбалуу система администраторун издейбиз.

Талаптар:
- IT же байланыштуу тармакта жогорку билим
- Кеминде 2 жылдык система администрациялоо тажрыйбасы
- Windows жана Linux системаларын билүү
- Тармак администрациялоо тажрыйбасы

Милдеттер:
- Сервердин техникалык тейлөөсү жана администрациялоосу
- Тармактык инфраструктураны колдоо
- Колдонуучуларды колдоо жана үйрөтүү
- Системанын коопсуздугун көзөмөлдөө'''
            },
            'Менеджер по персоналу': {
                'title_en': 'HR Manager',
                'title_ky': 'Кадрлар менеджери',
                'short_description_en': 'Seeking an experienced HR manager',
                'short_description_ky': 'Тажрыйбалуу кадрлар менеджерин издейбиз',
                'description_en': '''We are seeking an experienced HR manager to join our team.

Requirements:
- Higher education in HR, Psychology or related field
- At least 3 years of HR experience
- Knowledge of labor legislation
- Excellent communication skills

Responsibilities:
- Recruitment and selection
- Employee relations
- HR policy development
- Training coordination''',
                'description_ky': '''Биз командабызга кошулуу үчүн тажрыйбалуу кадрлар менеджерин издейбиз.

Талаптар:
- Кадрлар, психология же байланыштуу тармакта жогорку билим
- Кеминде 3 жылдык кадрлар тажрыйбасы
- Эмгек мыйзамдарын билүү
- Мыкты коммуникация көндүмдөрү

Милдеттер:
- Кызматкерлерди тандоо жана кабыл алуу
- Кызматкерлер менен мамилелер
- Кадрлар саясатын иштеп чыгуу
- Окутууну координациялоо'''
            },
            'Помощник администратора': {
                'title_en': 'Administrative Assistant',
                'title_ky': 'Административдик жардамчы',
                'short_description_en': 'Looking for an organized administrative assistant',
                'short_description_ky': 'Уюштурулган административдик жардамчыны издейбиз',
                'description_en': '''We are looking for an organized administrative assistant.

Requirements:
- Secondary education or higher
- Computer skills (MS Office)
- Attention to detail
- Good communication skills

Responsibilities:
- Administrative support
- Document management
- Phone and email communication
- Meeting coordination''',
                'description_ky': '''Биз уюштурулган административдик жардамчыны издейбиз.

Талаптар:
- Орто же жогорку билим
- Компьютерди билүү (MS Office)
- деталдарга көңүл буруу
- Жакшы коммуникация көндүмдөрү

Милдеттер:
- Административдик колдоо
- Документтерди башкаруу
- Телефон жана электрондук почта аркылуу байланышуу
- Жолугушууларды координациялоо'''
            }
        }

        # Обновляем вакансии
        for vacancy in vacancies:
            for russian_title, translation in vacancy_translations.items():
                if russian_title.lower() in vacancy.title.lower():
                    vacancy.title_en = translation['title_en']
                    vacancy.title_ky = translation['title_ky']
                    vacancy.short_description_en = translation['short_description_en']
                    vacancy.short_description_ky = translation['short_description_ky']
                    vacancy.description_en = translation['description_en']
                    vacancy.description_ky = translation['description_ky']
                    vacancy.save()
                    self.stdout.write(f'✓ Обновлена вакансия: {vacancy.title} → {translation["title_en"]}')
                    break

        self.stdout.write(self.style.SUCCESS('Все переводы вакансий добавлены!'))
