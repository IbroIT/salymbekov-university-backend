from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from news.models import NewsCategory, News, Event, Announcement, NewsTag, NewsTagRelation


class Command(BaseCommand):
    help = 'Создает начальные данные для новостей на основе frontend компонентов'

    def handle(self, *args, **options):
        self.stdout.write('Создание начальных данных для новостей...')
        
        # Создаем категории
        self.create_categories()
        
        # Создаем теги
        self.create_tags()
        
        # Создаем новости
        self.create_news()
        
        # Создаем события
        self.create_events()
        
        # Создаем объявления
        self.create_announcements()
        
        self.stdout.write(
            self.style.SUCCESS('Начальные данные успешно созданы!')
        )

    def create_categories(self):
        """Создание категорий новостей"""
        categories_data = [
            ('news', 'Новости', 'news'),
            ('events', 'События', 'events'),
            ('announcements', 'Объявления', 'announcements'),
        ]
        
        for name, display_name, slug in categories_data:
            category, created = NewsCategory.objects.get_or_create(
                name=name,
                defaults={'slug': slug}
            )
            if created:
                self.stdout.write(f'Создана категория: {display_name}')

    def create_tags(self):
        """Создание тегов"""
        tags_data = [
            ('Образование', 'obrazovanie', '#3B82F6'),
            ('Медицина', 'medicina', '#EF4444'),
            ('Конференции', 'konferentsii', '#10B981'),
            ('Студенты', 'studenty', '#F59E0B'),
            ('Наука', 'nauka', '#8B5CF6'),
            ('Международное', 'mezhdunarodnoe', '#06B6D4'),
        ]
        
        for name, slug, color in tags_data:
            tag, created = NewsTag.objects.get_or_create(
                name=name,
                defaults={'slug': slug, 'color': color}
            )
            if created:
                self.stdout.write(f'Создан тег: {name}')

    def create_news(self):
        """Создание обычных новостей"""
        news_category = NewsCategory.objects.get(name='news')
        
        news_data = [
            {
                'title': 'Открытие нового симуляционного центра',
                'slug': 'otkrytie-novogo-simulyatsionnogo-tsentra',
                'summary': 'В университете открылся современный симуляционный центр с передовым медицинским оборудованием',
                'content': '''
                <p>Салымбековский университет гордится объявить об открытии нового современного симуляционного центра, который станет важной частью образовательного процесса для будущих медицинских работников.</p>
                
                <h3>Современное оборудование</h3>
                <p>Новый центр оснащен самым современным медицинским оборудованием, включая:</p>
                <ul>
                  <li>Высокотехнологичные манекены для отработки различных медицинских процедур</li>
                  <li>Симуляторы хирургических операций</li>
                  <li>Оборудование для изучения анестезиологии и реаниматологии</li>
                  <li>Современные мониторы жизненно важных функций</li>
                </ul>
                
                <h3>Возможности для студентов</h3>
                <p>Центр предоставляет студентам уникальную возможность отрабатывать практические навыки в безопасной и контролируемой среде. Это особенно важно для формирования профессиональных компетенций будущих врачей.</p>
                
                <p>Занятия в симуляционном центре будут проводиться под руководством опытных преподавателей и практикующих врачей, что обеспечит высокое качество подготовки специалистов.</p>
                
                <h3>График работы</h3>
                <p>Симуляционный центр будет работать ежедневно с 8:00 до 20:00. Записаться на занятия можно через деканат соответствующего факультета.</p>
                ''',
                'image_url': 'https://images.unsplash.com/photo-1582719471384-894e35a4b48f?w=800&h=400&fit=crop',
                'author': 'Пресс-служба университета',
                'is_featured': True,
                'tags': ['Образование', 'Медицина']
            },
            {
                'title': 'Стипендиальная программа для отличников',
                'slug': 'stipendialnaya-programma-dlya-otlichnikov',
                'summary': 'Новые возможности получения стипендии для лучших студентов университета',
                'content': '''
                <p>Салымбековский университет объявляет о запуске новой стипендиальной программы для студентов с выдающимися академическими достижениями.</p>
                
                <h3>Условия получения стипендии</h3>
                <p>Для участия в программе студенты должны:</p>
                <ul>
                  <li>Иметь средний балл не ниже 4.5</li>
                  <li>Не иметь академических задолженностей</li>
                  <li>Проявлять активность в научной деятельности</li>
                  <li>Участвовать в общественной жизни университета</li>
                </ul>
                
                <h3>Размер стипендии</h3>
                <p>Повышенная стипендия составляет 15,000 сом в месяц и выплачивается в течение семестра при условии поддержания высоких академических показателей.</p>
                
                <h3>Подача документов</h3>
                <p>Заявления принимаются до 10 декабря 2024 года в деканате соответствующего факультета. Результаты будут объявлены до 20 декабря.</p>
                ''',
                'image_url': 'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800&h=400&fit=crop',
                'author': 'Отдел по работе со студентами',
                'is_featured': True,
                'tags': ['Студенты', 'Образование']
            }
        ]
        
        for news_item in news_data:
            tags_names = news_item.pop('tags', [])
            news, created = News.objects.get_or_create(
                slug=news_item['slug'],
                defaults={
                    **news_item,
                    'category': news_category,
                    'published_at': timezone.now() - timedelta(days=1)
                }
            )
            
            if created:
                # Добавляем теги
                for tag_name in tags_names:
                    try:
                        tag = NewsTag.objects.get(name=tag_name)
                        NewsTagRelation.objects.get_or_create(news=news, tag=tag)
                    except NewsTag.DoesNotExist:
                        continue
                
                self.stdout.write(f'Создана новость: {news.title}')

    def create_events(self):
        """Создание событий"""
        events_category = NewsCategory.objects.get(name='events')
        
        events_data = [
            {
                'news_data': {
                    'title': 'Международная конференция по кардиологии',
                    'slug': 'mezhdunarodnaya-konferentsiya-po-kardiologii',
                    'summary': '25-26 января состоится международная конференция с участием ведущих специалистов',
                    'content': '''
                    <p>25-26 января 2025 года в Салымбековском университете состоится масштабная международная конференция "Современные подходы в кардиологии и кардиохирургии".</p>
                    
                    <h3>Программа конференции</h3>
                    <p>В рамках конференции будут рассмотрены актуальные вопросы:</p>
                    <ul>
                      <li>Инновационные методы диагностики сердечно-сосудистых заболеваний</li>
                      <li>Современные подходы к лечению ишемической болезни сердца</li>
                      <li>Роль телемедицины в кардиологии</li>
                      <li>Профилактика сердечно-сосудистых заболеваний</li>
                    </ul>
                    
                    <h3>Выдающиеся спикеры</h3>
                    <p>К участию в конференции приглашены ведущие кардиологи из России, Казахстана, Узбекистана и других стран региона. Ожидается участие более 200 специалистов.</p>
                    
                    <h3>Регистрация</h3>
                    <p>Регистрация участников открыта до 20 января 2025 года. Для студентов университета участие бесплатное при предварительной регистрации в деканате.</p>
                    ''',
                    'image_url': 'https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=800&h=400&fit=crop',
                    'author': 'Кафедра кардиологии',
                },
                'event_data': {
                    'event_date': datetime(2025, 1, 25).date(),
                    'event_time': datetime.strptime('09:00', '%H:%M').time(),
                    'end_time': datetime.strptime('18:00', '%H:%M').time(),
                    'location': 'Главный корпус, Актовый зал',
                    'event_category': 'conference',
                    'status': 'upcoming',
                    'max_participants': 200,
                    'current_participants': 45,
                    'registration_required': True,
                    'registration_deadline': timezone.now() + timedelta(days=40),
                },
                'tags': ['Конференции', 'Медицина', 'Международное']
            },
            {
                'news_data': {
                    'title': 'День открытых дверей',
                    'slug': 'den-otkrytykh-dverey',
                    'summary': 'Приглашаем абитуриентов и их родителей познакомиться с университетом',
                    'content': '''
                    <p>15 февраля 2025 года Салымбековский университет проводит День открытых дверей для будущих студентов и их родителей.</p>
                    
                    <h3>Программа мероприятия</h3>
                    <ul>
                      <li>10:00 - Презентация университета и образовательных программ</li>
                      <li>11:00 - Экскурсия по учебным корпусам</li>
                      <li>12:00 - Посещение симуляционного центра</li>
                      <li>13:00 - Встреча с преподавателями и студентами</li>
                      <li>14:00 - Информация о поступлении и стипендиях</li>
                    </ul>
                    
                    <h3>Что вы узнаете</h3>
                    <p>Во время мероприятия вы сможете:</p>
                    <ul>
                      <li>Ознакомиться с учебными программами</li>
                      <li>Посетить современные аудитории и лаборатории</li>
                      <li>Получить консультацию по поступлению</li>
                      <li>Узнать о студенческой жизни</li>
                    </ul>
                    ''',
                    'image_url': 'https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=800&h=400&fit=crop',
                    'author': 'Приемная комиссия',
                },
                'event_data': {
                    'event_date': datetime(2025, 2, 15).date(),
                    'event_time': datetime.strptime('10:00', '%H:%M').time(),
                    'end_time': datetime.strptime('15:00', '%H:%M').time(),
                    'location': 'Все корпуса университета',
                    'event_category': 'open-day',
                    'status': 'upcoming',
                    'max_participants': 500,
                    'current_participants': 120,
                    'registration_required': False,
                },
                'tags': ['Образование', 'Студенты']
            }
        ]
        
        for event_item in events_data:
            tags_names = event_item.pop('tags', [])
            news_data = event_item['news_data']
            event_data = event_item['event_data']
            
            news, created = News.objects.get_or_create(
                slug=news_data['slug'],
                defaults={
                    **news_data,
                    'category': events_category,
                    'published_at': timezone.now() - timedelta(days=2)
                }
            )
            
            if created:
                # Создаем событие
                Event.objects.get_or_create(
                    news=news,
                    defaults=event_data
                )
                
                # Добавляем теги
                for tag_name in tags_names:
                    try:
                        tag = NewsTag.objects.get(name=tag_name)
                        NewsTagRelation.objects.get_or_create(news=news, tag=tag)
                    except NewsTag.DoesNotExist:
                        continue
                
                self.stdout.write(f'Создано событие: {news.title}')

    def create_announcements(self):
        """Создание объявлений"""
        announcements_category = NewsCategory.objects.get(name='announcements')
        
        announcements_data = [
            {
                'news_data': {
                    'title': 'Объявление о зимней экзаменационной сессии 2024-2025',
                    'slug': 'obyavlenie-o-zimney-sessii-2024-2025',
                    'summary': 'Информация о расписании экзаменов, требованиях к допуску и правилах проведения зимней сессии',
                    'content': '''
                    <p>Уважаемые студенты! Информируем вас о начале зимней экзаменационной сессии 2024-2025 учебного года.</p>
                    
                    <h3>Сроки проведения</h3>
                    <p>Зимняя экзаменационная сессия для студентов всех курсов начнется 20 декабря 2024 года и завершится 15 января 2025 года.</p>
                    
                    <h3>Требования к допуску</h3>
                    <ul>
                      <li>Выполнение всех лабораторных и практических работ</li>
                      <li>Сдача всех промежуточных контрольных работ</li>
                      <li>Отсутствие академических задолженностей</li>
                      <li>Выполнение курсовых работ (при наличии)</li>
                    </ul>
                    
                    <h3>Расписание экзаменов</h3>
                    <p>Подробное расписание экзаменов будет опубликовано до 15 декабря 2024 года на сайте университета и информационных стендах факультетов.</p>
                    ''',
                    'author': 'Учебный отдел',
                    'is_pinned': True,
                },
                'announcement_data': {
                    'announcement_type': 'academic',
                    'priority': 'high',
                    'deadline': timezone.now() + timedelta(days=25),
                    'attachment_name': 'winter_session_schedule.pdf',
                    'target_students': True,
                    'target_staff': False,
                    'target_faculty': True,
                },
                'tags': ['Студенты', 'Образование']
            },
            {
                'news_data': {
                    'title': 'Конкурс научных работ студентов',
                    'slug': 'konkurs-nauchnykh-rabot-studentov',
                    'summary': 'Объявляется ежегодный конкурс научных работ студентов медицинского факультета',
                    'content': '''
                    <p>Медицинский факультет Салымбековского университета объявляет о проведении ежегодного конкурса научных работ студентов.</p>
                    
                    <h3>Номинации</h3>
                    <ul>
                      <li>Фундаментальные медицинские науки</li>
                      <li>Клиническая медицина</li>
                      <li>Общественное здоровье и здравоохранение</li>
                      <li>Инновации в медицине</li>
                    </ul>
                    
                    <h3>Требования к работам</h3>
                    <p>Принимаются научные работы по всем направлениям медицины. Работы должны быть оригинальными и содержать элементы научной новизны.</p>
                    
                    <h3>Награждение</h3>
                    <p>Лучшие работы будут представлены на международной студенческой конференции. Победители получат денежные премии и дипломы.</p>
                    
                    <h3>Подача заявок</h3>
                    <p>Заявки принимаются до 28 февраля 2025 года в научном отделе университета.</p>
                    ''',
                    'author': 'Научный отдел',
                },
                'announcement_data': {
                    'announcement_type': 'competition',
                    'priority': 'medium',
                    'deadline': timezone.now() + timedelta(days=90),
                    'attachment_name': 'research_competition_rules.pdf',
                    'target_students': True,
                    'target_staff': False,
                    'target_faculty': False,
                },
                'tags': ['Студенты', 'Наука']
            }
        ]
        
        for announcement_item in announcements_data:
            tags_names = announcement_item.pop('tags', [])
            news_data = announcement_item['news_data']
            announcement_data = announcement_item['announcement_data']
            
            news, created = News.objects.get_or_create(
                slug=news_data['slug'],
                defaults={
                    **news_data,
                    'category': announcements_category,
                    'published_at': timezone.now() - timedelta(hours=12)
                }
            )
            
            if created:
                # Создаем объявление
                Announcement.objects.get_or_create(
                    news=news,
                    defaults=announcement_data
                )
                
                # Добавляем теги
                for tag_name in tags_names:
                    try:
                        tag = NewsTag.objects.get(name=tag_name)
                        NewsTagRelation.objects.get_or_create(news=news, tag=tag)
                    except NewsTag.DoesNotExist:
                        continue
                
                self.stdout.write(f'Создано объявление: {news.title}')
