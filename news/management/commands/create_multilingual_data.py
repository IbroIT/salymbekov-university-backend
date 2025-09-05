from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from news.models import NewsCategory, NewsTag, News, Event, Announcement, NewsTagRelation


class Command(BaseCommand):
    help = 'Create sample multilingual news data'

    def handle(self, *args, **options):
        # Удаляем старые данные
        News.objects.all().delete()
        NewsTag.objects.all().delete()
        self.stdout.write('Старые данные удалены')

        # Создаем категории
        categories = [
            'Новости университета',
            'Студенческая жизнь', 
            'Научная деятельность',
            'Международное сотрудничество',
            'Достижения',
        ]
        
        category_objects = []
        for cat_name in categories:
            category, created = NewsCategory.objects.get_or_create(
                name=cat_name,
                defaults={'slug': cat_name.lower().replace(' ', '-')}
            )
            category_objects.append(category)
            if created:
                self.stdout.write(f'Создана категория: {cat_name}')

        # Создаем теги с переводами
        tag_data = [
            {'ru': 'медицина', 'ky': 'медицина', 'en': 'medicine'},
            {'ru': 'образование', 'ky': 'билим берүү', 'en': 'education'},
            {'ru': 'студенты', 'ky': 'студенттер', 'en': 'students'},
            {'ru': 'преподаватели', 'ky': 'мугалимдер', 'en': 'teachers'},
            {'ru': 'конференция', 'ky': 'конференция', 'en': 'conference'},
            {'ru': 'исследования', 'ky': 'изилдөө', 'en': 'research'},
            {'ru': 'партнерство', 'ky': 'өнөктөштүк', 'en': 'partnership'},
            {'ru': 'стипендия', 'ky': 'стипендия', 'en': 'scholarship'},
            {'ru': 'выпускники', 'ky': 'бүтүрүүчүлөр', 'en': 'graduates'},
            {'ru': 'международное', 'ky': 'эл аралык', 'en': 'international'},
            {'ru': 'практика', 'ky': 'практика', 'en': 'practice'},
            {'ru': 'волонтерство', 'ky': 'ыктыярчылык', 'en': 'volunteering'}
        ]
        
        tag_objects = []
        for tag_translations in tag_data:
            tag_name = tag_translations['ru']
            slug = tag_name.replace(' ', '-').lower()
            tag, created = NewsTag.objects.get_or_create(
                name=tag_name,
                defaults={'slug': slug, 'color': '#3B82F6'}
            )
            if created:
                tag.name_ru = tag_translations['ru']
                tag.name_ky = tag_translations['ky'] 
                tag.name_en = tag_translations['en']
                tag.save()
                self.stdout.write(f'Создан тег: {tag_translations["ru"]}')
            tag_objects.append(tag)

        # Создаем многоязычные новости
        news_data = [
            {
                'ru': {
                    'title': 'Новая лаборатория биомедицинских технологий',
                    'summary': 'В университете открылась современная лаборатория для исследований в области биомедицинских технологий.',
                    'content': 'Университет Салымбекова гордится объявить об открытии новой лаборатории биомедицинских технологий. Это современное исследовательское пространство оборудовано передовыми приборами и технологиями для проведения научных исследований в области медицины и биотехнологий. Лаборатория станет центром для студентов и преподавателей, желающих заниматься инновационными проектами.'
                },
                'ky': {
                    'title': 'Биомедициналык технологиялардын жаңы лабораториясы',
                    'summary': 'Университетте биомедициналык технологиялар тармагында изилдөө жүргүзүү үчүн заманбап лаборатория ачылды.',
                    'content': 'Салымбеков университети биомедициналык технологиялардын жаңы лабораториясынын ачылышын сүйүнүч менен жарыялайт. Бул заманбап изилдөө мейкиндиги медицина жана биотехнологиялар тармагында илимий изилдөөлөрдү жүргүзүү үчүн алдыңкы аспаптар жана технологиялар менен жабдылган. Лаборатория инновациялык долбоорлор менен алектенүүнү каалаган студенттер жана мугалимдер үчүн борбор болуп калат.'
                },
                'en': {
                    'title': 'New Biomedical Technologies Laboratory',
                    'summary': 'The university has opened a modern laboratory for research in biomedical technologies.',
                    'content': 'Salymbekov University is proud to announce the opening of a new biomedical technologies laboratory. This modern research space is equipped with advanced instruments and technologies for conducting scientific research in medicine and biotechnology. The laboratory will become a center for students and faculty who wish to engage in innovative projects.'
                },
                'image_url': 'https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=800&h=450&fit=crop&crop=center',
                'tags': ['медицина', 'исследования', 'образование']
            },
            {
                'ru': {
                    'title': 'Международная медицинская конференция 2024',
                    'summary': 'Приглашаем на ежегодную международную медицинскую конференцию, которая пройдет в марте 2024 года.',
                    'content': 'Университет Салымбекова организует международную медицинскую конференцию, которая соберет ведущих специалистов из разных стран. На конференции будут представлены последние достижения в области медицины, обсуждены перспективы развития здравоохранения и возможности международного сотрудничества.'
                },
                'ky': {
                    'title': 'Эл аралык медициналык конференция 2024',
                    'summary': 'Бизди 2024-жылдын март айында өтүүчү жыл сайынкы эл аралык медициналык конференцияга чакырабыз.',
                    'content': 'Салымбеков университети ар кайсы өлкөлөрдөн алдыңкы адистерди чогултуучу эл аралык медициналык конференцияны уюштуруп жатат. Конференцияда медицина тармагындагы акыркы жетишкендиктер көрсөтүлөт, ден соолукту сактоону өнүктүрүүнүн келечеги жана эл аралык кызматташтыктын мүмкүнчүлүктөрү талкуланат.'
                },
                'en': {
                    'title': 'International Medical Conference 2024',
                    'summary': 'We invite you to the annual international medical conference to be held in March 2024.',
                    'content': 'Salymbekov University organizes an international medical conference that will bring together leading specialists from different countries. The conference will present the latest achievements in medicine, discuss prospects for healthcare development and opportunities for international cooperation.'
                },
                'image_url': 'https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=800&h=450&fit=crop&crop=center',
                'tags': ['конференция', 'международное', 'медицина']
            },
            {
                'ru': {
                    'title': 'Программа обмена с европейскими университетами',
                    'summary': 'Студенты медицинского факультета получили возможность обучения в ведущих университетах Европы.',
                    'content': 'Благодаря новому соглашению о партнерстве, студенты нашего университета смогут пройти семестр обучения в престижных европейских медицинских университетах. Программа обмена включает изучение современных методов диагностики и лечения, а также возможность участия в научных исследованиях.'
                },
                'ky': {
                    'title': 'Европалык университеттер менен алмашуу программасы',
                    'summary': 'Медициналык факультеттин студенттери Европанын алдыңкы университеттеринде окуу мүмкүнчүлүгүн алышты.',
                    'content': 'Жаңы өнөктөштүк келишими аркасында биздин университеттин студенттери Европанын престиждүү медициналык университеттеринде бир семестр окуу мүмкүнчүлүгүн алышат. Алмашуу программасы заманбап диагностика жана дарылоо методдорун үйрөнүүнү, ошондой эле илимий изилдөөлөргө катышуу мүмкүнчүлүгүн камтыйт.'
                },
                'en': {
                    'title': 'Exchange Program with European Universities',
                    'summary': 'Medical faculty students have gained the opportunity to study at leading European universities.',
                    'content': 'Thanks to a new partnership agreement, students from our university will be able to complete a semester of study at prestigious European medical universities. The exchange program includes studying modern diagnostic and treatment methods, as well as the opportunity to participate in scientific research.'
                },
                'image_url': 'https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=800&h=450&fit=crop&crop=center',
                'tags': ['студенты', 'международное', 'образование']
            },
            {
                'ru': {
                    'title': 'Стипендиальная программа для отличников',
                    'summary': 'Объявлен конкурс на получение стипендии имени основателя университета для лучших студентов.',
                    'content': 'Университет Салымбекова объявляет о начале приема заявок на получение именной стипендии. Конкурс открыт для студентов всех курсов, показывающих выдающиеся академические результаты и активно участвующих в научной деятельности университета.'
                },
                'ky': {
                    'title': 'Мыкты студенттер үчүн стипендиялык программа',
                    'summary': 'Мыкты студенттер үчүн университеттин негиздөөчүсүнүн атындагы стипендияны алуу боюнча конкурс жарыяланды.',
                    'content': 'Салымбеков университети атайын стипендия алуу үчүн арыз кабыл алууну баштагандыгын жарыялайт. Конкурс өзгөчө академиялык жыйынтыктарды көрсөткөн жана университеттин илимий иш-аракеттерине активдүү катышкан бардык курстардын студенттери үчүн ачык.'
                },
                'en': {
                    'title': 'Scholarship Program for Top Students',
                    'summary': 'A competition has been announced for receiving a scholarship named after the university founder for the best students.',
                    'content': 'Salymbekov University announces the opening of applications for a named scholarship. The competition is open to students of all courses who show outstanding academic results and actively participate in the scientific activities of the university.'
                },
                'image_url': 'https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=800&h=450&fit=crop&crop=center',
                'tags': ['стипендия', 'студенты', 'образование']
            },
            {
                'ru': {
                    'title': 'Новое медицинское оборудование в клинике',
                    'summary': 'Университетская клиника получила современное диагностическое оборудование для более точной диагностики.',
                    'content': 'В рамках программы модернизации медицинского оборудования университетская клиника приобрела новейшие аппараты для диагностики. Это позволит не только улучшить качество медицинских услуг, но и предоставить студентам возможность изучать работу с самым современным оборудованием.'
                },
                'ky': {
                    'title': 'Клиникадагы жаңы медициналык жабдуулар',
                    'summary': 'Университет клиникасы так диагностика үчүн заманбап диагностикалык жабдууларды алды.',
                    'content': 'Медициналык жабдууларды модернизациялоо программасынын алкагында университет клиникасы диагностика үчүн эң жаңы аппараттарды сатып алды. Бул медициналык кызматтардын сапатын жакшыртууга гана эмес, ошондой эле студенттерге эң заманбап жабдуулар менен иштөөнү үйрөнүү мүмкүнчүлүгүн берүүгө мүмкүндүк берет.'
                },
                'en': {
                    'title': 'New Medical Equipment in the Clinic',
                    'summary': 'The university clinic has received modern diagnostic equipment for more accurate diagnosis.',
                    'content': 'As part of the medical equipment modernization program, the university clinic has acquired the latest diagnostic devices. This will not only improve the quality of medical services but also provide students with the opportunity to study working with the most modern equipment.'
                },
                'image_url': 'https://images.unsplash.com/photo-1530026405186-ed1f139313f8?w=800&h=450&fit=crop&crop=center',
                'tags': ['медицина', 'образование']
            },
            {
                'ru': {
                    'title': 'Волонтерская программа в детской больнице',
                    'summary': 'Студенты университета запустили волонтерскую программу помощи детям в больнице.',
                    'content': 'Группа студентов медицинского факультета инициировала волонтерскую программу для работы с детьми в городской детской больнице. Волонтеры проводят развивающие занятия, помогают в организации досуга и поддерживают маленьких пациентов и их семьи в трудный период.'
                },
                'ky': {
                    'title': 'Балдар ооруканасындагы ыктыярчылык программасы',
                    'summary': 'Университеттин студенттери ооруканадагы балдарга жардам берүү боюнча ыктыярчылык программасын иштетишти.',
                    'content': 'Медициналык факультеттин студенттеринин тобу шаардык балдар ооруканасында балдар менен иштөө үчүн ыктыярчылык программасын баштады. Ыктыярчылар өнүктүрүүчү сабактарды өткөрүшөт, эс алуу уюштурууга жардам беришет жана кичинекей пациенттерге жана алардын үй-бүлөлөрүнө кыйын мезгилде колдоо көрсөтүшөт.'
                },
                'en': {
                    'title': 'Volunteer Program at Children\'s Hospital',
                    'summary': 'University students launched a volunteer program to help children in the hospital.',
                    'content': 'A group of medical faculty students initiated a volunteer program to work with children at the city children\'s hospital. Volunteers conduct educational activities, help organize leisure activities, and support young patients and their families during difficult times.'
                },
                'image_url': 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=800&h=450&fit=crop&crop=center',
                'tags': ['студенты', 'волонтерство', 'медицина']
            }
        ]

        # Создаем новости
        for i, news_item in enumerate(news_data):
            # Создаем новость
            news = News.objects.create(
                title=news_item['ru']['title'],
                title_ru=news_item['ru']['title'],
                title_ky=news_item['ky']['title'],
                title_en=news_item['en']['title'],
                
                summary=news_item['ru']['summary'],
                summary_ru=news_item['ru']['summary'],
                summary_ky=news_item['ky']['summary'],
                summary_en=news_item['en']['summary'],
                
                content=news_item['ru']['content'],
                content_ru=news_item['ru']['content'],
                content_ky=news_item['ky']['content'],
                content_en=news_item['en']['content'],
                
                slug=f'news-{i+1}',
                image_url=news_item['image_url'],
                author='Пресс-служба университета',
                category=random.choice(category_objects),
                is_featured=(i < 3),
                published_at=timezone.now() - timedelta(days=i)
            )
            
            # Добавляем теги
            if 'tags' in news_item:
                for tag_name in news_item['tags']:
                    try:
                        tag = NewsTag.objects.get(name=tag_name)
                        NewsTagRelation.objects.get_or_create(news=news, tag=tag)
                    except NewsTag.DoesNotExist:
                        pass
            
            self.stdout.write(f'Создана новость: {news.title}')

        # Создаем события
        event_data = [
            {
                'ru': {
                    'title': 'День открытых дверей',
                    'summary': 'Приглашаем абитуриентов и их родителей на день открытых дверей университета.',
                    'content': 'Университет Салымбекова приглашает всех желающих на день открытых дверей. Вы сможете познакомиться с факультетами, программами обучения, преподавателями и студентами.'
                },
                'ky': {
                    'title': 'Ачык эшиктер күнү',
                    'summary': 'Абитуриенттерди жана алардын ата-энелерин университеттин ачык эшиктер күнүнө чакырабыз.',
                    'content': 'Салымбеков университети баарын ачык эшиктер күнүнө чакырат. Силер факультеттер, окуу программалары, мугалимдер жана студенттер менен тааныша аласыздар.'
                },
                'en': {
                    'title': 'Open House Day',
                    'summary': 'We invite prospective students and their parents to the university open house day.',
                    'content': 'Salymbekov University invites everyone to the open house day. You will be able to meet faculties, study programs, teachers and students.'
                },
                'date': timezone.now() + timedelta(days=15),
                'location': 'Главный корпус университета',
                'image_url': 'https://images.unsplash.com/photo-1523050854058-8df90110c9d1?w=800&h=450&fit=crop&crop=center'
            },
            {
                'ru': {
                    'title': 'Научная конференция молодых ученых',
                    'summary': 'Ежегодная конференция для студентов и молодых исследователей.',
                    'content': 'Конференция даст возможность молодым ученым представить свои исследования, обменяться опытом и найти новых партнеров для научного сотрудничества.'
                },
                'ky': {
                    'title': 'Жаш окумуштуулардын илимий конференциясы',
                    'summary': 'Студенттер жана жаш изилдөөчүлөр үчүн жыл сайынкы конференция.',
                    'content': 'Конференция жаш окумуштууларга өз изилдөөлөрүн көрсөтүү, тажрыйба алмашуу жана илимий кызматташтык үчүн жаңы өнөктөштөрдү табуу мүмкүнчүлүгүн берет.'
                },
                'en': {
                    'title': 'Scientific Conference of Young Scientists',
                    'summary': 'Annual conference for students and young researchers.',
                    'content': 'The conference will provide young scientists with the opportunity to present their research, share experiences and find new partners for scientific collaboration.'
                },
                'date': timezone.now() + timedelta(days=30),
                'location': 'Конференц-зал',
                'image_url': 'https://images.unsplash.com/photo-1475721027785-f74eccf877e2?w=800&h=450&fit=crop&crop=center'
            }
        ]

        for i, event_item in enumerate(event_data):
            # Сначала создаем базовую новость
            news = News.objects.create(
                title=event_item['ru']['title'],
                title_ru=event_item['ru']['title'],
                title_ky=event_item['ky']['title'],
                title_en=event_item['en']['title'],
                
                summary=event_item['ru']['summary'],
                summary_ru=event_item['ru']['summary'],
                summary_ky=event_item['ky']['summary'],
                summary_en=event_item['en']['summary'],
                
                content=event_item['ru']['content'],
                content_ru=event_item['ru']['content'],
                content_ky=event_item['ky']['content'],
                content_en=event_item['en']['content'],
                
                slug=f'event-{i+1}',
                image_url=event_item['image_url'],
                author='Пресс-служба университета',
                category=random.choice(category_objects),
                published_at=timezone.now() - timedelta(days=i)
            )
            
            # Теперь создаем событие
            event = Event.objects.create(
                news=news,
                event_date=event_item['date'].date(),
                event_time=event_item['date'].time(),
                location=event_item['location'],
                event_category='conference',
                status='upcoming'
            )
            
            self.stdout.write(f'Создано событие: {news.title}')

        # Создаем объявления
        announcement_data = [
            {
                'ru': {
                    'title': 'ВАЖНО: Изменения в расписании экзаменов',
                    'summary': 'Уведомляем о переносе некоторых экзаменов в зимнюю сессию.',
                    'content': 'В связи с производственной необходимостью некоторые экзамены зимней сессии переносятся на более поздние даты. Подробная информация доступна в деканатах факультетов.'
                },
                'ky': {
                    'title': 'МААНИЛҮҮ: Экзамен программасындагы өзгөрүүлөр',
                    'summary': 'Кышкы сессиядагы кээ бир экзамендердин көчүрүлүшү жөнүндө билдиребиз.',
                    'content': 'Өндүрүштүк зарылчылыкка байланыштуу кышкы сессиянын кээ бир экзамендери кийинкы даталарга көчүрүлөт. Толук маалымат факультеттердин деканаттарынан алса болот.'
                },
                'en': {
                    'title': 'IMPORTANT: Changes in exam schedule',
                    'summary': 'We notify about the postponement of some exams in the winter session.',
                    'content': 'Due to production necessity, some exams of the winter session are postponed to later dates. Detailed information is available at faculty deans\' offices.'
                },
                'priority': 'urgent',
                'image_url': 'https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=800&h=450&fit=crop&crop=center'
            },
            {
                'ru': {
                    'title': 'Стипендиальная комиссия: прием документов',
                    'summary': 'Объявляется прием документов на получение повышенной академической стипендии.',
                    'content': 'Студенты, имеющие выдающиеся академические достижения, могут подать документы на получение повышенной стипендии до 25 числа текущего месяца.'
                },
                'ky': {
                    'title': 'Стипендиялык комиссия: документтерди кабыл алуу',
                    'summary': 'Жогорулатылган академиялык стипендия алуу үчүн документтерди кабыл алуу жарыяланат.',
                    'content': 'Өзгөчө академиялык жетишкендиктери бар студенттер агымдагы айдын 25не чейин жогорулатылган стипендия алуу үчүн документтерди тапшыра алышат.'
                },
                'en': {
                    'title': 'Scholarship Commission: document acceptance',
                    'summary': 'Document acceptance for receiving increased academic scholarship is announced.',
                    'content': 'Students with outstanding academic achievements can submit documents for receiving increased scholarship until the 25th of the current month.'
                },
                'priority': 'normal',
                'image_url': 'https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=800&h=450&fit=crop&crop=center'
            }
        ]

        for i, announcement_item in enumerate(announcement_data):
            # Сначала создаем базовую новость
            news = News.objects.create(
                title=announcement_item['ru']['title'],
                title_ru=announcement_item['ru']['title'],
                title_ky=announcement_item['ky']['title'],
                title_en=announcement_item['en']['title'],
                
                summary=announcement_item['ru']['summary'],
                summary_ru=announcement_item['ru']['summary'],
                summary_ky=announcement_item['ky']['summary'],
                summary_en=announcement_item['en']['summary'],
                
                content=announcement_item['ru']['content'],
                content_ru=announcement_item['ru']['content'],
                content_ky=announcement_item['ky']['content'],
                content_en=announcement_item['en']['content'],
                
                slug=f'announcement-{i+1}',
                image_url=announcement_item['image_url'],
                author='Администрация университета',
                category=random.choice(category_objects),
                published_at=timezone.now() - timedelta(days=i)
            )
            
            # Теперь создаем объявление
            announcement = Announcement.objects.create(
                news=news,
                priority=announcement_item['priority'],
                announcement_type='academic'
            )
            
            self.stdout.write(f'Создано объявление: {news.title}')

        self.stdout.write(
            self.style.SUCCESS(f'Успешно создано: {News.objects.count()} новостей, {Event.objects.count()} событий, {Announcement.objects.count()} объявлений')
        )
