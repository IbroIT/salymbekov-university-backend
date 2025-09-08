from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from research.models import ResearchArea, ResearchCenter, Grant, Conference, Publication, GrantApplication


class Command(BaseCommand):
    help = 'Создает тестовые данные для research приложения'

    def handle(self, *args, **options):
        self.stdout.write('Создание тестовых данных для research...')
        
        # Создаем области исследований
        self.create_research_areas()
        
        # Создаем исследовательские центры
        self.create_research_centers()
        
        # Создаем гранты
        self.create_grants()
        
        # Создаем конференции
        self.create_conferences()
        
        # Создаем публикации
        self.create_publications()
        
        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно созданы!'))

    def create_research_areas(self):
        """Создание областей исследований"""
        areas = [
            {
                'title_ru': 'Кардиоваскулярные исследования',
                'title_en': 'Cardiovascular Research',
                'title_kg': 'Кардиоваскулярдык изилдөөлөр',
                'description_ru': 'Исследования в области сердечно-сосудистых заболеваний',
                'description_en': 'Research in cardiovascular diseases',
                'description_kg': 'Жүрөк-кан тамыр оорулары боюнча изилдөөлөр',
                'icon': '💓',
                'color': 'red',
                'projects_count': 15,
                'publications_count': 45,
                'researchers_count': 25
            },
            {
                'title_ru': 'Молекулярная биология',
                'title_en': 'Molecular Biology',
                'title_kg': 'Молекулярдык биология',
                'description_ru': 'Исследования на молекулярном уровне',
                'description_en': 'Molecular level research',
                'description_kg': 'Молекулярдык деңгээлдеги изилдөөлөр',
                'icon': '🧬',
                'color': 'blue',
                'projects_count': 20,
                'publications_count': 60,
                'researchers_count': 30
            },
            {
                'title_ru': 'Онкологические исследования',
                'title_en': 'Cancer Research',
                'title_kg': 'Онкологиялык изилдөөлөр',
                'description_ru': 'Исследования в области онкологии',
                'description_en': 'Cancer research studies',
                'description_kg': 'Онкология тармагындагы изилдөөлөр',
                'icon': '🎗️',
                'color': 'purple',
                'projects_count': 12,
                'publications_count': 35,
                'researchers_count': 18
            },
            {
                'title_ru': 'Нейронаука',
                'title_en': 'Neuroscience',
                'title_kg': 'Нейроилим',
                'description_ru': 'Исследования нервной системы',
                'description_en': 'Nervous system research',
                'description_kg': 'Нерв системасын изилдөө',
                'icon': '🧠',
                'color': 'green',
                'projects_count': 18,
                'publications_count': 52,
                'researchers_count': 22
            },
        ]
        
        for area_data in areas:
            area, created = ResearchArea.objects.get_or_create(
                title_ru=area_data['title_ru'],
                defaults=area_data
            )
            if created:
                self.stdout.write(f'Создана область исследований: {area.title_ru}')

    def create_research_centers(self):
        """Создание исследовательских центров"""
        centers = [
            {
                'name_ru': 'Центр кардиоваскулярной медицины',
                'name_en': 'Cardiovascular Medicine Center',
                'name_kg': 'Кардиоваскулярдык медицина борбору',
                'description_ru': 'Ведущий центр исследований сердечно-сосудистых заболеваний',
                'description_en': 'Leading center for cardiovascular disease research',
                'description_kg': 'Жүрөк-кан тамыр оорулары боюнча алдыңкы изилдөө борбору',
                'director': 'Профессор Иванов И.И.',
                'staff_count': 45,
                'established_year': 2010,
                'equipment_ru': 'МРТ, КТ, эхокардиограф, катетерная лаборатория',
                'equipment_en': 'MRI, CT, echocardiograph, cardiac catheterization lab',
                'equipment_kg': 'МРТ, КТ, эхокардиограф, катетер лабораториясы',
            },
            {
                'name_ru': 'Лаборатория молекулярной биологии',
                'name_en': 'Molecular Biology Laboratory',
                'name_kg': 'Молекулярдык биология лабораториясы',
                'description_ru': 'Современная лаборатория для молекулярно-биологических исследований',
                'description_en': 'Modern laboratory for molecular biological research',
                'description_kg': 'Молекулярдык-биологиялык изилдөөлөр үчүн заманбап лаборатория',
                'director': 'Доктор Петрова А.С.',
                'staff_count': 32,
                'established_year': 2015,
                'equipment_ru': 'ПЦР-машины, секвенаторы, микроскопы, спектрометры',
                'equipment_en': 'PCR machines, sequencers, microscopes, spectrometers',
                'equipment_kg': 'ПЦР машиналар, секвенаторлор, микроскоптор, спектрометрлер',
            }
        ]
        
        for center_data in centers:
            center, created = ResearchCenter.objects.get_or_create(
                name_ru=center_data['name_ru'],
                defaults=center_data
            )
            if created:
                self.stdout.write(f'Создан исследовательский центр: {center.name_ru}')

    def create_grants(self):
        """Создание грантов"""
        grants = [
            {
                'title_ru': 'Исследование новых методов лечения сердечной недостаточности',
                'title_en': 'Research on new methods for treating heart failure',
                'title_kg': 'Жүрөк жетишсиздигин дарылоонун жаңы ыкмаларын изилдөө',
                'organization': 'Национальный научный фонд',
                'amount': '$50,000',
                'deadline': date.today() + timedelta(days=60),
                'category': 'fundamental',
                'status': 'active',
                'duration_ru': '2 года',
                'duration_en': '2 years',
                'duration_kg': '2 жыл',
                'requirements_ru': 'Кандидатская степень, опыт работы в кардиологии',
                'requirements_en': 'PhD degree, experience in cardiology',
                'requirements_kg': 'Кандидаттык даража, кардиология боюнча тажрыйба',
                'description_ru': 'Грант на исследование инновационных подходов к лечению сердечной недостаточности',
                'description_en': 'Grant for research on innovative approaches to heart failure treatment',
                'description_kg': 'Жүрөк жетишсиздигин дарылоонун инновациялык ыкмаларын изилдөө гранты',
                'contact': 'grants@nsf.kg',
                'website': 'https://nsf.kg/grants'
            },
            {
                'title_ru': 'Молодежный грант по онкологическим исследованиям',
                'title_en': 'Youth grant for oncological research',
                'title_kg': 'Онкологиялык изилдөөлөр боюнча жаштар гранты',
                'organization': 'Международный фонд здравоохранения',
                'amount': '$25,000',
                'deadline': date.today() + timedelta(days=45),
                'category': 'youth',
                'status': 'active',
                'duration_ru': '1 год',
                'duration_en': '1 year',
                'duration_kg': '1 жыл',
                'requirements_ru': 'Возраст до 35 лет, магистерская степень',
                'requirements_en': 'Age under 35, Master\'s degree',
                'requirements_kg': '35 жашка чейин, магистр даражасы',
                'description_ru': 'Грант для молодых исследователей в области онкологии',
                'description_en': 'Grant for young researchers in oncology',
                'description_kg': 'Онкология тармагындагы жаш изилдөөчүлөр үчүн грант',
                'contact': 'youth@ihf.org',
                'website': 'https://ihf.org/youth-grants'
            },
            {
                'title_ru': 'Международный грант по нейронаукам',
                'title_en': 'International neuroscience grant',
                'title_kg': 'Нейроилим боюнча эл аралык грант',
                'organization': 'Европейский исследовательский совет',
                'amount': '€75,000',
                'deadline': date.today() + timedelta(days=90),
                'category': 'international',
                'status': 'active',
                'duration_ru': '3 года',
                'duration_en': '3 years',
                'duration_kg': '3 жыл',
                'requirements_ru': 'Докторская степень, международные публикации',
                'requirements_en': 'PhD degree, international publications',
                'requirements_kg': 'Докторлук даража, эл аралык басылмалар',
                'description_ru': 'Престижный международный грант для исследований в области нейронаук',
                'description_en': 'Prestigious international grant for neuroscience research',
                'description_kg': 'Нейроилим изилдөөлөрү үчүн беделдүү эл аралык грант',
                'contact': 'erc@europa.eu',
                'website': 'https://erc.europa.eu'
            }
        ]
        
        for grant_data in grants:
            grant, created = Grant.objects.get_or_create(
                title_ru=grant_data['title_ru'],
                defaults=grant_data
            )
            if created:
                self.stdout.write(f'Создан грант: {grant.title_ru}')

    def create_conferences(self):
        """Создание конференций"""
        conferences = [
            {
                'title_ru': 'Международная конференция по кардиологии',
                'title_en': 'International Conference on Cardiology',
                'title_kg': 'Кардиология боюнча эл аралык конференция',
                'start_date': date.today() + timedelta(days=120),
                'end_date': date.today() + timedelta(days=123),
                'location_ru': 'Бишкек, Кыргызстан',
                'location_en': 'Bishkek, Kyrgyzstan',
                'location_kg': 'Бишкек, Кыргызстан',
                'deadline': date.today() + timedelta(days=90),
                'website': 'https://cardio-conf.kg',
                'description_ru': 'Ведущая конференция по кардиоваскулярной медицине в Центральной Азии',
                'description_en': 'Leading cardiovascular medicine conference in Central Asia',
                'description_kg': 'Борбордук Азиядагы кардиоваскулярдык медицина боюнча алдыңкы конференция',
                'topics_ru': ['Сердечная недостаточность', 'Аритмии', 'Кардиохирургия', 'Профилактика'],
                'topics_en': ['Heart failure', 'Arrhythmias', 'Cardiac surgery', 'Prevention'],
                'topics_kg': ['Жүрөк жетишсиздиги', 'Аритмиялар', 'Кардиохирургия', 'Профилактика'],
                'speakers_ru': ['Проф. Иванов И.И.', 'Д-р Петрова А.С.', 'Проф. Смит Дж.'],
                'speakers_en': ['Prof. Ivanov I.I.', 'Dr. Petrova A.S.', 'Prof. Smith J.'],
                'speakers_kg': ['Проф. Иванов И.И.', 'Д-р Петрова А.С.', 'Проф. Смит Дж.'],
                'speakers_count': 15,
                'participants_limit': 300,
                'status': 'registration-open'
            },
            {
                'title_ru': 'Симпозиум по молекулярной биологии',
                'title_en': 'Molecular Biology Symposium',
                'title_kg': 'Молекулярдык биология боюнча симпозиум',
                'start_date': date.today() + timedelta(days=180),
                'end_date': date.today() + timedelta(days=182),
                'location_ru': 'Алматы, Казахстан',
                'location_en': 'Almaty, Kazakhstan',
                'location_kg': 'Алматы, Казакстан',
                'deadline': date.today() + timedelta(days=150),
                'website': 'https://molbio-symp.kz',
                'description_ru': 'Региональный симпозиум по современным достижениям в молекулярной биологии',
                'description_en': 'Regional symposium on modern achievements in molecular biology',
                'description_kg': 'Молекулярдык биологиядагы заманбап жетишкендиктер боюнча аймактык симпозиум',
                'topics_ru': ['Генная терапия', 'CRISPR технологии', 'Белковая инженерия'],
                'topics_en': ['Gene therapy', 'CRISPR technologies', 'Protein engineering'],
                'topics_kg': ['Ген терапиясы', 'CRISPR технологиялары', 'Белок инженериясы'],
                'speakers_ru': ['Проф. Назарбаев А.К.', 'Д-р Кожомкулов Б.'],
                'speakers_en': ['Prof. Nazarbayev A.K.', 'Dr. Kozhomkulov B.'],
                'speakers_kg': ['Проф. Назарбаев А.К.', 'Д-р Кожомкулов Б.'],
                'speakers_count': 10,
                'participants_limit': 150,
                'status': 'call-for-papers'
            }
        ]
        
        for conf_data in conferences:
            conference, created = Conference.objects.get_or_create(
                title_ru=conf_data['title_ru'],
                defaults=conf_data
            )
            if created:
                self.stdout.write(f'Создана конференция: {conference.title_ru}')

    def create_publications(self):
        """Создание публикаций"""
        # Получаем области исследований для связи
        cardio_area = ResearchArea.objects.filter(title_ru__icontains='Кардиоваскулярные').first()
        molbio_area = ResearchArea.objects.filter(title_ru__icontains='Молекулярная биология').first()
        
        publications = [
            {
                'title_ru': 'Новые подходы к лечению острого инфаркта миокарда',
                'title_en': 'Novel approaches to acute myocardial infarction treatment',
                'title_kg': 'Курч миокард инфарктын дарылоонун жаңы ыкмалары',
                'authors': 'Иванов И.И., Петрова А.С., Сидоров П.П.',
                'journal': 'Кардиология и сердечно-сосудистая хирургия',
                'publication_date': date.today() - timedelta(days=30),
                'publication_type': 'article',
                'impact_factor': 2.45,
                'citations_count': 12,
                'doi': '10.1234/cardio.2024.001',
                'url': 'https://journal.cardio.kg/articles/001',
                'abstract_ru': 'В данной статье рассматриваются современные методы лечения острого инфаркта миокарда',
                'abstract_en': 'This article reviews modern methods for treating acute myocardial infarction',
                'abstract_kg': 'Бул макалада курч миокард инфарктын дарылоонун заманбап ыкмалары каралган',
                'keywords_ru': ['инфаркт миокарда', 'кардиология', 'лечение'],
                'keywords_en': ['myocardial infarction', 'cardiology', 'treatment'],
                'keywords_kg': ['миокард инфаркты', 'кардиология', 'дарылоо'],
                'research_area': cardio_area,
                'is_featured': True
            },
            {
                'title_ru': 'Генетические маркеры предрасположенности к сердечно-сосудистым заболеваниям',
                'title_en': 'Genetic markers of cardiovascular disease predisposition',
                'title_kg': 'Жүрөк-кан тамыр оорулары боюнча генетикалык маркерлер',
                'authors': 'Абдраимов К.А., Токтосунова Г.Б.',
                'journal': 'Медицинская генетика',
                'publication_date': date.today() - timedelta(days=60),
                'publication_type': 'article',
                'impact_factor': 3.12,
                'citations_count': 8,
                'doi': '10.1234/medgen.2024.002',
                'abstract_ru': 'Исследование генетических факторов риска развития сердечно-сосудистых заболеваний',
                'abstract_en': 'Study of genetic risk factors for cardiovascular disease development',
                'abstract_kg': 'Жүрөк-кан тамыр оорулары өнүгүүнүн генетикалык тобокелдик факторлорун изилдөө',
                'keywords_ru': ['генетика', 'сердечно-сосудистые заболевания', 'маркеры'],
                'keywords_en': ['genetics', 'cardiovascular diseases', 'markers'],
                'keywords_kg': ['генетика', 'жүрөк-кан тамыр оорулары', 'маркерлер'],
                'research_area': molbio_area,
                'is_featured': False
            },
            {
                'title_ru': 'Применение CRISPR-Cas9 в кардиомиопатии',
                'title_en': 'Application of CRISPR-Cas9 in cardiomyopathy',
                'title_kg': 'Кардиомиопатияда CRISPR-Cas9 колдонуу',
                'authors': 'Молдокулов Т.М., Жунусова А.К., Brown S.M.',
                'journal': 'Nature Biotechnology',
                'publication_date': date.today() - timedelta(days=90),
                'publication_type': 'article',
                'impact_factor': 54.9,
                'citations_count': 156,
                'doi': '10.1038/nbt.2024.003',
                'abstract_ru': 'Использование технологии редактирования генома для лечения кардиомиопатии',
                'abstract_en': 'Using genome editing technology for cardiomyopathy treatment',
                'abstract_kg': 'Кардиомиопатияны дарылоо үчүн геном түзөтүү технологиясын колдонуу',
                'keywords_ru': ['CRISPR', 'генная терапия', 'кардиомиопатия'],
                'keywords_en': ['CRISPR', 'gene therapy', 'cardiomyopathy'],
                'keywords_kg': ['CRISPR', 'ген терапиясы', 'кардиомиопатия'],
                'research_area': molbio_area,
                'is_featured': True
            }
        ]
        
        for pub_data in publications:
            publication, created = Publication.objects.get_or_create(
                title_ru=pub_data['title_ru'],
                defaults=pub_data
            )
            if created:
                self.stdout.write(f'Создана публикация: {publication.title_ru}')
