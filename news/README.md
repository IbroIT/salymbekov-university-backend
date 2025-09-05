# Система управления новостями Салымбековского университета

Это приложение предоставляет полнофункциональную систему управления новостями, событиями и объявлениями для университета.

## Структура проекта

### Backend (Django)
```
news/
├── models.py          # Модели данных
├── serializers.py     # DRF сериализаторы
├── views.py          # API представления
├── urls.py           # URL маршруты
├── admin.py          # Админ панель
└── management/
    └── commands/
        └── create_news_data.py  # Команда для создания тестовых данных
```

### Frontend (React)
```
components/News/
├── News.jsx                # Главная страница новостей
├── NewsDetail.jsx          # Детальный просмотр новости
├── NewsEvents.jsx          # Страница событий
└── NewsAnnouncements.jsx   # Страница объявлений
```

## Модели данных

### News
Основная модель для всех типов контента:
- `title` - Заголовок
- `slug` - URL slug
- `summary` - Краткое описание
- `content` - Полное содержание (HTML)
- `image`/`image_url` - Изображение
- `category` - Категория (news/events/announcements)
- `author` - Автор
- `published_at` - Дата публикации
- `is_published` - Статус публикации
- `is_featured` - Рекомендуемое
- `is_pinned` - Закрепленное
- `views_count` - Счетчик просмотров

### Event
Дополнительные поля для событий:
- `event_date` - Дата события
- `event_time` - Время начала
- `end_time` - Время окончания
- `location` - Место проведения
- `event_category` - Тип события (conference/workshop/etc)
- `status` - Статус (upcoming/past/cancelled)
- `max_participants` - Максимум участников
- `registration_required` - Требует регистрации

### Announcement
Дополнительные поля для объявлений:
- `announcement_type` - Тип (academic/scholarship/etc)
- `priority` - Приоритет (low/medium/high/urgent)
- `deadline` - Крайний срок
- `attachment` - Вложение
- `target_students/staff/faculty` - Целевая аудитория

## API Endpoints

### Новости
```
GET /news/api/news/ - список новостей
GET /news/api/news/{slug}/ - детали новости
GET /news/api/news/featured/ - рекомендуемые
GET /news/api/news/pinned/ - закрепленные
GET /news/api/news/popular/ - популярные
POST /news/api/news/ - создать новость
PUT /news/api/news/{slug}/ - обновить
DELETE /news/api/news/{slug}/ - удалить
```

### События
```
GET /news/api/events/ - список событий
GET /news/api/events/upcoming/ - предстоящие
GET /news/api/events/past/ - прошедшие
GET /news/api/events/this_month/ - события месяца
POST /news/api/events/ - создать событие
```

### Объявления
```
GET /news/api/announcements/ - список объявлений
GET /news/api/announcements/pinned/ - закрепленные
GET /news/api/announcements/urgent/ - срочные
GET /news/api/announcements/for_students/ - для студентов
POST /news/api/announcements/ - создать объявление
```

### Дополнительные
```
GET /news/api/categories/ - категории
GET /news/api/tags/ - теги
GET /news/api/stats/ - статистика
GET /news/api/search/?q={query} - поиск
```

## Установка и настройка

### Backend (Django)

1. Добавьте приложение в `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    # ...
    'news',
    'rest_framework',
    'django_filters',
    'corsheaders',
]
```

2. Настройте CORS для фронтенда:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

3. Добавьте URL в главный `urls.py`:
```python
urlpatterns = [
    # ...
    path('news/', include('news.urls')),
]
```

4. Выполните миграции:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Создайте тестовые данные:
```bash
python manage.py create_news_data
```

6. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

### Frontend (React)

1. Компоненты уже подключены в `App.jsx`
2. Убедитесь что установлен `lucide-react` для иконок
3. API использует `http://localhost:8000` - убедитесь что Django сервер запущен на этом порту

## Использование

### Админ панель
Перейдите на `/admin/` для управления новостями через веб-интерфейс:
- Создание/редактирование новостей, событий, объявлений
- Управление категориями и тегами
- Просмотр статистики просмотров
- Массовые действия (публикация, закрепление и т.д.)

### API для фронтенда
Фронтенд компоненты автоматически загружают данные из Django API.
При недоступности API используются fallback данные.

### Фильтрация и поиск
- Фильтрация по категориям, типам, статусам
- Полнотекстовый поиск по заголовкам и содержимому
- Сортировка по дате, популярности
- Пагинация результатов

## Особенности

### SEO-дружественность
- Использование slug'ов в URL
- Метатеги для социальных сетей
- Структурированные данные

### Производительность
- Оптимизированные запросы с select_related/prefetch_related
- Кеширование популярных запросов
- Ленивая загрузка изображений

### Безопасность
- CORS настройка
- Валидация данных через сериализаторы
- Защита от XSS в HTML контенте
- Ограничения прав доступа

### Интернационализация
- Поддержка нескольких языков в React
- Локализованные форматы дат
- Переводимые интерфейсы

## Расширение функциональности

### Добавление новых типов контента
1. Создайте новую модель наследующую от News
2. Добавьте соответствующий сериализатор
3. Создайте ViewSet для API
4. Обновите фронтенд компоненты

### Добавление полей
1. Обновите модели
2. Создайте и примените миграцию
3. Обновите сериализаторы и админку
4. Обновите фронтенд компоненты

### Интеграция с внешними сервисами
- Email уведомления о новых публикациях
- Интеграция с социальными сетями
- Аналитика просмотров
- RSS/Atom фиды
