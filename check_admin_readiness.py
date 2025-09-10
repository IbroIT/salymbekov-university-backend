#!/usr/bin/env python
"""
Проверка доступности админки и готовности к CRUD операциям
Этот скрипт поможет убедиться, что все готово для ручного тестирования
"""
import os
import django
import requests
from datetime import datetime

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_su_m.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.admin import site
from django.conf import settings

class AdminReadinessCheck:
    """Проверка готовности админки к ручному тестированию"""
    
    def __init__(self):
        self.server_url = "http://127.0.0.1:8000"
        self.admin_url = f"{self.server_url}/admin/"
        self.results = []
    
    def check_server_running(self):
        """Проверка, запущен ли сервер"""
        print("🌐 Проверяем, запущен ли Django сервер...")
        try:
            response = requests.get(self.server_url, timeout=5)
            if response.status_code in [200, 404]:  # 404 тоже OK, главное что сервер отвечает
                print("   ✅ Django сервер запущен и отвечает")
                return True
            else:
                print(f"   ❌ Сервер отвечает с кодом {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("   ❌ Сервер не запущен или недоступен")
            print("   💡 Запустите: python manage.py runserver")
            return False
        except Exception as e:
            print(f"   ❌ Ошибка при проверке сервера: {e}")
            return False
    
    def check_admin_accessibility(self):
        """Проверка доступности админки"""
        print("\n🔑 Проверяем доступность админки...")
        try:
            response = requests.get(self.admin_url, timeout=5)
            if response.status_code == 200:
                print("   ✅ Админка доступна по адресу /admin/")
                return True
            elif response.status_code == 302:
                print("   ✅ Админка перенаправляет на страницу входа (это нормально)")
                return True
            else:
                print(f"   ❌ Админка недоступна (код: {response.status_code})")
                return False
        except Exception as e:
            print(f"   ❌ Ошибка при проверке админки: {e}")
            return False
    
    def check_superuser_exists(self):
        """Проверка существования суперпользователя"""
        print("\n👤 Проверяем наличие суперпользователя...")
        try:
            superusers = User.objects.filter(is_superuser=True)
            if superusers.exists():
                usernames = [user.username for user in superusers]
                print(f"   ✅ Найдено {len(usernames)} суперпользователей: {', '.join(usernames)}")
                return True, usernames
            else:
                print("   ❌ Суперпользователи не найдены")
                print("   💡 Создайте: python manage.py createsuperuser")
                return False, []
        except Exception as e:
            print(f"   ❌ Ошибка при проверке пользователей: {e}")
            return False, []
    
    def check_registered_models(self):
        """Проверка зарегистрированных моделей в админке"""
        print("\n📋 Проверяем зарегистрированные модели...")
        try:
            registered_models = []
            for model, admin_class in site._registry.items():
                app_label = model._meta.app_label
                model_name = model._meta.model_name
                if app_label not in ['auth', 'admin', 'sessions', 'contenttypes']:
                    registered_models.append(f"{app_label}.{model_name}")
            
            print(f"   ✅ Зарегистрировано {len(registered_models)} кастомных моделей:")
            for model in sorted(registered_models):
                print(f"      • {model}")
            return True, registered_models
        except Exception as e:
            print(f"   ❌ Ошибка при проверке моделей: {e}")
            return False, []
    
    def check_static_files(self):
        """Проверка статических файлов для админки"""
        print("\n🎨 Проверяем кастомные стили...")
        try:
            css_file = os.path.join(settings.BASE_DIR, 'static', 'admin', 'css', 'custom_admin.css')
            if os.path.exists(css_file):
                print("   ✅ Кастомный CSS файл найден")
                with open(css_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if '#3b82f6' in content:  # Наш синий цвет
                        print("   ✅ Синий дизайн присутствует в CSS")
                        return True
                    else:
                        print("   ⚠️ CSS файл есть, но синий дизайн не найден")
                        return False
            else:
                print("   ❌ Кастомный CSS файл не найден")
                return False
        except Exception as e:
            print(f"   ❌ Ошибка при проверке CSS: {e}")
            return False
    
    def generate_test_instructions(self):
        """Генерация инструкций для ручного тестирования"""
        print("\n📝 Генерируем инструкции для тестирования...")
        
        instructions = f"""
🎯 ГОТОВО К РУЧНОМУ ТЕСТИРОВАНИЮ!

🌐 Адрес админки: {self.admin_url}

🔑 Для входа используйте одного из суперпользователей:
   (логин и пароль, которые вы создавали ранее)

📋 Рекомендуемый план тестирования:

1. 🏗️ CREATE (Создание):
   • Создайте баннер в разделе Banner → Banners
   • Создайте отдел в разделе Careers → Departments
   • Создайте новость в разделе News → News

2. 👀 READ (Просмотр):
   • Посмотрите списки всех созданных объектов
   • Откройте детальные страницы для редактирования

3. ✏️ UPDATE (Обновление):
   • Отредактируйте созданные объекты
   • Сохраните изменения

4. 🗑️ DELETE (Удаление):
   • Удалите тестовые объекты
   • Используйте как массовое удаление, так и единичное

💡 TIPS:
• Обратите внимание на синий дизайн
• Проверьте многоязычные поля (ru/kg/en)
• Попробуйте поиск и фильтры
• Загрузите изображения для проверки превью

⚠️ Если что-то не работает:
• Обновите страницу
• Проверьте консоль браузера на ошибки
• Убедитесь, что сервер все еще запущен
"""
        print(instructions)
        
        # Сохраняем инструкции в файл
        with open('MANUAL_TEST_INSTRUCTIONS.txt', 'w', encoding='utf-8') as f:
            f.write(instructions)
        print("   ✅ Инструкции сохранены в MANUAL_TEST_INSTRUCTIONS.txt")
    
    def run_check(self):
        """Запуск всех проверок"""
        print("🚀 ПРОВЕРКА ГОТОВНОСТИ DJANGO АДМИНКИ К РУЧНОМУ ТЕСТИРОВАНИЮ")
        print("=" * 70)
        print(f"🕒 Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        checks = [
            ("Сервер запущен", self.check_server_running),
            ("Админка доступна", self.check_admin_accessibility),
            ("Суперпользователь существует", lambda: self.check_superuser_exists()[0]),
            ("Модели зарегистрированы", lambda: self.check_registered_models()[0]),
            ("CSS стили подключены", self.check_static_files)
        ]
        
        passed_checks = 0
        for check_name, check_func in checks:
            if check_func():
                passed_checks += 1
        
        print(f"\n📊 РЕЗУЛЬТАТ: {passed_checks}/{len(checks)} проверок пройдено")
        
        if passed_checks == len(checks):
            print("\n🎉 ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ!")
            print("🚀 Админка полностью готова к ручному тестированию CRUD операций!")
            self.generate_test_instructions()
        elif passed_checks >= 3:
            print("\n👍 Базовые проверки пройдены, можно тестировать")
            print("⚠️ Но есть проблемы, которые стоит исправить")
            self.generate_test_instructions()
        else:
            print("\n❌ Слишком много проблем для корректного тестирования")
            print("🔧 Исправьте ошибки и запустите проверку снова")

if __name__ == "__main__":
    checker = AdminReadinessCheck()
    checker.run_check()
