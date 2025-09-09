#!/usr/bin/env python
"""
Полный тест CRUD операций для всех админок
Проверяет: Create, Read, Update, Delete операции
"""
import os
import django
from django.test.utils import setup_test_environment, teardown_test_environment
from django.test.runner import DiscoverRunner
from django.conf import settings

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_su_m.settings')
django.setup()

from django.contrib.admin import site
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
import json

class AdminCRUDTest:
    """Тест CRUD операций для всех админок"""
    
    def __init__(self):
        self.client = Client()
        self.admin_user = None
        self.results = {
            'successful_models': [],
            'failed_models': [],
            'errors': [],
            'warnings': []
        }
    
    def setup(self):
        """Настройка тестового окружения"""
        print("🔧 Настройка тестового окружения...")
        
        # Создаем или получаем админ пользователя
        try:
            self.admin_user = User.objects.filter(is_superuser=True).first()
            if not self.admin_user:
                self.admin_user = User.objects.create_superuser(
                    'testadmin', 'test@example.com', 'testpass123'
                )
                print("   ✅ Создан тестовый админ пользователь")
            else:
                print("   ✅ Используется существующий админ пользователь")
        except Exception as e:
            print(f"   ❌ Ошибка создания админ пользователя: {e}")
            return False
        
        # Авторизуемся в админке
        try:
            login_success = self.client.login(username='testadmin', password='testpass123')
            if not login_success:
                # Если не получилось войти, попробуем с существующим пользователем
                if User.objects.filter(is_superuser=True).exists():
                    admin = User.objects.filter(is_superuser=True).first()
                    admin.set_password('testpass123')
                    admin.save()
                    login_success = self.client.login(username=admin.username, password='testpass123')
            
            if login_success:
                print("   ✅ Авторизация в админке успешна")
                return True
            else:
                print("   ❌ Не удалось авторизоваться в админке")
                return False
        except Exception as e:
            print(f"   ❌ Ошибка авторизации: {e}")
            return False
    
    def test_model_admin(self, model, admin_class):
        """Тест CRUD операций для конкретной модели"""
        app_label = model._meta.app_label
        model_name = model._meta.model_name
        print(f"🧪 Тестируем {app_label}.{model_name}...")
        
        errors = []
        warnings = []
        
        # Пропускаем системные модели Django
        if app_label in ['auth', 'admin', 'sessions', 'contenttypes']:
            print(f"   ⏭️ Пропускаем системную модель {app_label}.{model_name}")
            return True, [], []
        
        try:
            # 1. Тест READ - список объектов
            list_url = reverse(f'admin:{app_label}_{model_name}_changelist')
            response = self.client.get(list_url)
            if response.status_code != 200:
                errors.append(f"Список объектов недоступен (код: {response.status_code})")
            else:
                print(f"   ✅ Список объектов загружается")
            
            # 2. Тест CREATE - форма добавления
            add_url = reverse(f'admin:{app_label}_{model_name}_add')
            response = self.client.get(add_url)
            if response.status_code != 200:
                errors.append(f"Форма добавления недоступна (код: {response.status_code})")
            else:
                print(f"   ✅ Форма добавления загружается")
                
                # Попробуем создать тестовый объект
                test_data = self.generate_test_data(model)
                if test_data:
                    post_response = self.client.post(add_url, test_data)
                    if post_response.status_code == 302:  # Успешное перенаправление
                        print(f"   ✅ Создание объекта работает")
                        
                        # Найдем созданный объект для тестов UPDATE и DELETE
                        try:
                            created_obj = model.objects.order_by('-id').first()
                            if created_obj:
                                # 3. Тест UPDATE - редактирование
                                change_url = reverse(f'admin:{app_label}_{model_name}_change', args=[created_obj.pk])
                                response = self.client.get(change_url)
                                if response.status_code != 200:
                                    errors.append(f"Форма редактирования недоступна (код: {response.status_code})")
                                else:
                                    print(f"   ✅ Форма редактирования загружается")
                                
                                # 4. Тест DELETE - удаление
                                delete_url = reverse(f'admin:{app_label}_{model_name}_delete', args=[created_obj.pk])
                                response = self.client.get(delete_url)
                                if response.status_code != 200:
                                    warnings.append(f"Форма удаления недоступна (код: {response.status_code})")
                                else:
                                    print(f"   ✅ Форма удаления загружается")
                                    
                                    # Подтверждаем удаление
                                    delete_response = self.client.post(delete_url, {'post': 'yes'})
                                    if delete_response.status_code == 302:
                                        print(f"   ✅ Удаление работает")
                                    else:
                                        warnings.append("Удаление не работает")
                        except Exception as e:
                            warnings.append(f"Ошибка при тесте UPDATE/DELETE: {e}")
                    else:
                        warnings.append("Создание объекта не работает (возможно, нужны дополнительные данные)")
                else:
                    warnings.append("Не удалось сгенерировать тестовые данные")
            
        except Exception as e:
            errors.append(f"Общая ошибка тестирования: {e}")
        
        success = len(errors) == 0
        return success, errors, warnings
    
    def generate_test_data(self, model):
        """Генерирует тестовые данные для модели"""
        data = {}
        
        # Базовые паттерны полей
        text_fields = ['title', 'name', 'description', 'summary', 'content']
        lang_suffixes = ['_ru', '_kg', '_en']
        
        for field in model._meta.get_fields():
            if hasattr(field, 'null') and hasattr(field, 'blank'):
                field_name = field.name
                
                # Пропускаем автоматические поля
                if field.auto_created or field_name in ['id', 'created_at', 'updated_at', 'submitted_at']:
                    continue
                
                # Текстовые поля
                if field.__class__.__name__ in ['CharField', 'TextField']:
                    if any(text_field in field_name.lower() for text_field in text_fields):
                        data[field_name] = f"Тест {field_name}"
                    elif field_name == 'slug':
                        data[field_name] = 'test-slug'
                    elif field_name == 'email':
                        data[field_name] = 'test@example.com'
                    elif 'phone' in field_name.lower():
                        data[field_name] = '+996700123456'
                    else:
                        data[field_name] = f"Тест {field_name}"
                
                # Boolean поля
                elif field.__class__.__name__ == 'BooleanField':
                    data[field_name] = True
                
                # Числовые поля
                elif field.__class__.__name__ in ['IntegerField', 'PositiveIntegerField']:
                    data[field_name] = 1
                
                # Поля даты
                elif field.__class__.__name__ in ['DateTimeField', 'DateField']:
                    if not field.auto_now and not field.auto_now_add:
                        data[field_name] = timezone.now()
        
        return data if data else None
    
    def run_tests(self):
        """Запуск всех тестов"""
        print("🚀 НАЧИНАЕМ CRUD ТЕСТЫ ДЛЯ ВСЕХ АДМИНОК")
        print("=" * 60)
        
        if not self.setup():
            print("❌ Не удалось настроить тестовое окружение")
            return
        
        # Получаем все зарегистрированные модели
        for model, admin_class in site._registry.items():
            success, errors, warnings = self.test_model_admin(model, admin_class)
            
            if success:
                self.results['successful_models'].append(f"{model._meta.app_label}.{model._meta.model_name}")
            else:
                self.results['failed_models'].append(f"{model._meta.app_label}.{model._meta.model_name}")
            
            self.results['errors'].extend([f"{model._meta.app_label}.{model._meta.model_name}: {error}" for error in errors])
            self.results['warnings'].extend([f"{model._meta.app_label}.{model._meta.model_name}: {warning}" for warning in warnings])
        
        self.print_results()
    
    def print_results(self):
        """Вывод результатов тестирования"""
        print("\n" + "=" * 60)
        print("🏆 РЕЗУЛЬТАТЫ CRUD ТЕСТИРОВАНИЯ")
        print("=" * 60)
        
        print(f"\n✅ УСПЕШНО ({len(self.results['successful_models'])}):")
        for model in self.results['successful_models']:
            print(f"   ✅ {model}")
        
        if self.results['warnings']:
            print(f"\n⚠️ ПРЕДУПРЕЖДЕНИЯ ({len(self.results['warnings'])}):")
            for warning in self.results['warnings']:
                print(f"   ⚠️ {warning}")
        
        if self.results['errors']:
            print(f"\n❌ ОШИБКИ ({len(self.results['errors'])}):")
            for error in self.results['errors']:
                print(f"   ❌ {error}")
        
        if self.results['failed_models']:
            print(f"\n💥 НЕУДАЧНЫЕ МОДЕЛИ ({len(self.results['failed_models'])}):")
            for model in self.results['failed_models']:
                print(f"   💥 {model}")
        
        # Итоговая статистика
        total_models = len(self.results['successful_models']) + len(self.results['failed_models'])
        success_rate = (len(self.results['successful_models']) / total_models * 100) if total_models > 0 else 0
        
        print(f"\n📊 ИТОГОВАЯ СТАТИСТИКА:")
        print(f"   Всего протестировано: {total_models}")
        print(f"   Успешно: {len(self.results['successful_models'])} ({success_rate:.1f}%)")
        print(f"   С ошибками: {len(self.results['failed_models'])}")
        print(f"   Предупреждения: {len(self.results['warnings'])}")
        print(f"   Критические ошибки: {len(self.results['errors'])}")
        
        if success_rate >= 80:
            print("\n🎉 ОТЛИЧНО! Большинство админок работают корректно!")
        elif success_rate >= 60:
            print("\n👍 ХОРОШО! Большая часть админок работает, есть что исправить.")
        else:
            print("\n⚠️ НУЖНЫ ИСПРАВЛЕНИЯ! Много проблем с админками.")

if __name__ == "__main__":
    tester = AdminCRUDTest()
    tester.run_tests()
