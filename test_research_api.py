import requests
import json

# Базовый URL API
BASE_URL = "http://127.0.0.1:8000/research/api"

def test_api_endpoints():
    """Тестируем основные API endpoints"""
    
    print("🔬 Тестирование Research API...")
    print("=" * 50)
    
    # Тест 1: Получение областей исследований
    print("1. Тестирование областей исследований...")
    try:
        response = requests.get(f"{BASE_URL}/areas/")
        if response.status_code == 200:
            data = response.json()
            # API возвращает paginated результаты
            if 'results' in data:
                areas = data['results']
            else:
                areas = data
            print(f"   ✅ Получено {len(areas)} областей исследований")
            if areas and len(areas) > 0:
                print(f"   📋 Первая область: {areas[0]['title_ru']}")
        else:
            print(f"   ❌ Ошибка: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Исключение: {e}")
    
    # Тест 2: Получение грантов
    print("\n2. Тестирование грантов...")
    try:
        response = requests.get(f"{BASE_URL}/grants/")
        if response.status_code == 200:
            data = response.json()
            # API возвращает paginated результаты
            if 'results' in data:
                grants = data['results']
            else:
                grants = data
            print(f"   ✅ Получено {len(grants)} грантов")
            if grants and len(grants) > 0:
                print(f"   💰 Первый грант: {grants[0]['title_ru']}")
                print(f"   💵 Сумма: {grants[0]['amount']}")
        else:
            print(f"   ❌ Ошибка: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Исключение: {e}")
    
    # Тест 3: Получение активных грантов
    print("\n3. Тестирование активных грантов...")
    try:
        response = requests.get(f"{BASE_URL}/grants/active/")
        if response.status_code == 200:
            active_grants = response.json()
            # Это не paginated endpoint, возвращает список напрямую
            print(f"   ✅ Получено {len(active_grants)} активных грантов")
        else:
            print(f"   ❌ Ошибка: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Исключение: {e}")
    
    # Тест 4: Получение конференций
    print("\n4. Тестирование конференций...")
    try:
        response = requests.get(f"{BASE_URL}/conferences/")
        if response.status_code == 200:
            data = response.json()
            # API возвращает paginated результаты
            if 'results' in data:
                conferences = data['results']
            else:
                conferences = data
            print(f"   ✅ Получено {len(conferences)} конференций")
            if conferences and len(conferences) > 0:
                print(f"   📅 Первая конференция: {conferences[0]['title_ru']}")
        else:
            print(f"   ❌ Ошибка: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Исключение: {e}")
    
    # Тест 5: Получение публикаций
    print("\n5. Тестирование публикаций...")
    try:
        response = requests.get(f"{BASE_URL}/publications/")
        if response.status_code == 200:
            data = response.json()
            # API возвращает paginated результаты
            if 'results' in data:
                publications = data['results']
            else:
                publications = data
            print(f"   ✅ Получено {len(publications)} публикаций")
            if publications and len(publications) > 0:
                print(f"   📝 Первая публикация: {publications[0]['title_ru']}")
                print(f"   📊 Импакт-фактор: {publications[0].get('impact_factor', 'N/A')}")
        else:
            print(f"   ❌ Ошибка: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Исключение: {e}")
    
    # Тест 6: Статистика
    print("\n6. Тестирование статистики...")
    try:
        response = requests.get(f"{BASE_URL}/stats/")
        if response.status_code == 200:
            stats = response.json()
            print(f"   ✅ Статистика получена:")
            print(f"   📊 Общее количество грантов: {stats.get('total_grants', 0)}")
            print(f"   📊 Активных грантов: {stats.get('active_grants', 0)}")
            print(f"   📊 Общее количество публикаций: {stats.get('total_publications', 0)}")
        else:
            print(f"   ❌ Ошибка: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Исключение: {e}")
    
    # Тест 7: Поиск
    print("\n7. Тестирование поиска...")
    try:
        response = requests.get(f"{BASE_URL}/search/?q=кардио&lang=ru")
        if response.status_code == 200:
            search_results = response.json()
            print(f"   ✅ Поиск выполнен:")
            print(f"   🔍 Найдено грантов: {len(search_results.get('grants', []))}")
            print(f"   🔍 Найдено публикаций: {len(search_results.get('publications', []))}")
            print(f"   🔍 Найдено областей: {len(search_results.get('research_areas', []))}")
        else:
            print(f"   ❌ Ошибка: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Исключение: {e}")
    
    # Тест 8: Подача заявки на грант
    print("\n8. Тестирование подачи заявки на грант...")
    try:
        # Сначала получаем ID первого гранта
        grants_response = requests.get(f"{BASE_URL}/grants/")
        if grants_response.status_code == 200:
            data = grants_response.json()
            if 'results' in data:
                grants = data['results']
            else:
                grants = data
            
            if grants and len(grants) > 0:
                grant_id = grants[0]['id']
                
                application_data = {
                    "grant": grant_id,
                    "project_title": "Тестовый проект по кардиологии",
                    "principal_investigator": "Иванов Тест Тестович",
                    "email": "test@example.com",
                    "phone": "+996555123456",
                    "department": "Кафедра кардиологии",
                    "team_members": "Петров И.И., Сидорова А.А.",
                    "project_description": "Исследование влияния новых препаратов на сердечную деятельность",
                    "budget": 25000,
                    "timeline": 18,
                    "expected_results": "Разработка новых методов лечения"
                }
                
                response = requests.post(f"{BASE_URL}/grant-applications/", json=application_data)
                if response.status_code == 201:
                    result = response.json()
                    print(f"   ✅ Заявка подана успешно!")
                    print(f"   📝 ID заявки: {result.get('application_id')}")
                    print(f"   💬 Сообщение: {result.get('message')}")
                else:
                    print(f"   ❌ Ошибка при подаче заявки: {response.status_code}")
                    print(f"   📄 Ответ: {response.text}")
            else:
                print("   ⚠️  Нет доступных грантов для подачи заявки")
        else:
            print(f"   ❌ Ошибка при получении грантов: {grants_response.status_code}")
    except Exception as e:
        print(f"   ❌ Исключение: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Тестирование завершено!")

if __name__ == "__main__":
    test_api_endpoints()
