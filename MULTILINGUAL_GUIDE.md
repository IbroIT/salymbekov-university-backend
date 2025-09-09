# Многоязычная поддержка - Руководство по обновлению API

## Обзор изменений

Мы добавили поддержку трех языков в бэкенд приложения:
- 🇷🇺 **Русский (ru)** - основной язык
- 🇰🇬 **Кыргызский (kg)** - национальный язык  
- 🇺🇸 **Английский (en)** - международный язык

## Изменения в API

### Автоматическая локализация

API теперь автоматически возвращает контент на языке, указанном в заголовке `Accept-Language`. Если перевод для запрашиваемого языка отсутствует, API возвращает русскую версию.

**Пример запроса:**
```http
GET /api/news/
Accept-Language: en

# Возвратит английские тексты, если доступны
```

### Изменения в моделях

#### News (Новости)
- `title` → `title_ru`, `title_kg`, `title_en`
- `summary` → `summary_ru`, `summary_kg`, `summary_en`
- `content` → `content_ru`, `content_kg`, `content_en`
- `author` → `author_ru`, `author_kg`, `author_en`

#### NewsCategory (Категории новостей)
- Добавлены поля: `name_ru`, `name_kg`, `name_en`
- Добавлены поля: `description_ru`, `description_kg`, `description_en`

#### NewsTag (Теги новостей)
- `name` → `name_ru`, `name_kg`, `name_en`

#### Event (События)
- `location` → `location_ru`, `location_kg`, `location_en`

#### Vacancy (Вакансии)
- `title` → `title_ru`, `title_kg`, `title_en`
- `location` → `location_ru`, `location_kg`, `location_en`
- `experience_years` → `experience_years_ru`, `experience_years_kg`, `experience_years_en`
- `education_level` → `education_level_ru`, `education_level_kg`, `education_level_en`
- `short_description` → `short_description_ru`, `short_description_kg`, `short_description_en`
- `description` → `description_ru`, `description_kg`, `description_en`
- `responsibilities` → `responsibilities_ru`, `responsibilities_kg`, `responsibilities_en`
- `requirements` → `requirements_ru`, `requirements_kg`, `requirements_en`
- `conditions` → `conditions_ru`, `conditions_kg`, `conditions_en`

#### CareerCategory & Department
- Аналогичные изменения для поддержки трех языков

## Рекомендации для фронтенда

### 1. Обновление языковых настроек

Убедитесь, что фронтенд отправляет корректный заголовок `Accept-Language`:

```javascript
// Пример для axios
axios.defaults.headers.common['Accept-Language'] = getCurrentLanguage(); // 'ru', 'kg', или 'en'
```

### 2. Настройка i18n

Обновите настройки интернационализации:

```javascript
// i18n.js
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

i18n
  .use(initReactI18next)
  .init({
    lng: 'ru', // язык по умолчанию
    fallbackLng: 'ru',
    
    resources: {
      ru: { translation: { /* русские тексты */ } },
      kg: { translation: { /* кыргызские тексты */ } },
      en: { translation: { /* английские тексты */ } }
    },
    
    interpolation: {
      escapeValue: false,
    },
  });

export default i18n;
```

### 3. Компонент переключения языков

```jsx
// LanguageSwitcher.jsx
import { useTranslation } from 'react-i18next';

const LanguageSwitcher = () => {
  const { i18n } = useTranslation();

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
    // Обновляем заголовок для API запросов
    axios.defaults.headers.common['Accept-Language'] = lng;
  };

  return (
    <div className="language-switcher">
      <button onClick={() => changeLanguage('ru')} 
              className={i18n.language === 'ru' ? 'active' : ''}>
        🇷🇺 Рус
      </button>
      <button onClick={() => changeLanguage('kg')} 
              className={i18n.language === 'kg' ? 'active' : ''}>
        🇰🇬 Кырг
      </button>
      <button onClick={() => changeLanguage('en')} 
              className={i18n.language === 'en' ? 'active' : ''}>
        🇺🇸 Eng
      </button>
    </div>
  );
};
```

### 4. Обновление API сервисов

```javascript
// api/newsService.js
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

// Устанавливаем заголовок Accept-Language из локального хранилища
axios.interceptors.request.use((config) => {
  const language = localStorage.getItem('language') || 'ru';
  config.headers['Accept-Language'] = language;
  return config;
});

export const newsService = {
  getAllNews: () => axios.get(`${API_BASE_URL}/api/news/`),
  getNewsById: (id) => axios.get(`${API_BASE_URL}/api/news/${id}/`),
  // Остальные методы...
};
```

## Тестирование

### Проверьте API endpoints:

```bash
# Русский
curl -H "Accept-Language: ru" http://localhost:8000/api/news/

# Кыргызский  
curl -H "Accept-Language: kg" http://localhost:8000/api/news/

# Английский
curl -H "Accept-Language: en" http://localhost:8000/api/news/
```

## Миграция данных

Существующие данные были автоматически перенесены:
- Русские поля заполнены существующими данными
- Кыргызские и английские поля имеют значения-заглушки "not given"
- **Необходимо вручную заполнить переводы в админ-панели Django**

## Следующие шаги

1. ✅ Обновить модели бэкенда
2. ✅ Применить миграции  
3. ✅ Обновить API сериализаторы
4. ⏳ **Заполнить переводы в админ-панели**
5. ⏳ **Обновить фронтенд для поддержки языков**
6. ⏳ **Протестировать все функции на разных языках**

---

💡 **Совет:** Начните с заполнения ключевого контента (главные новости, важные объявления) на всех языках, а затем постепенно дополняйте остальной контент.
