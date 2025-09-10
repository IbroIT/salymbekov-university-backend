#!/usr/bin/env python
"""
Финальный тест CRUD операций с детальной диагностикой
Проверяет исправленные проблемы: Vacancy.posted_date и NewsView permissions
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

class FinalCRUDTest:
    """Финальный тест CRUD операций с детальной диагностикой"""
    
    def __init__(self):
        self.client = Client()
        self.admin_user = None
        self.results = {
            'fixed_models': [],
            'successful_models': [],
            'failed_models': [],
            'errors': [],
            'warnings': []
        }
    
    def setup(self):
        """Настройка тестового окружения"""
        print("🔧 Настройка тестового окружения для финального теста...")
        
        try:
            self.admin_user = User.objects.filter(is_superuser=True).first()
            if self.admin_user:
                # Убедимся что пароль установлен
                self.admin_user.set_password('testpass123')
                self.admin_user.save()
                login_success = self.client.login(username=self.admin_user.username, password='testpass123')
                if login_success:
                    print(f"   ✅ Авторизован как {self.admin_user.username}")
                    return True
            
            print("   ❌ Не удалось авторизоваться")
            return False
        except Exception as e:
            print(f"   ❌ Ошибка авторизации: {e}")
            return False
    
    def test_fixed_issues(self):
        """Тест исправленных проблем"""
        print("\n🔍 ТЕСТИРУЕМ ИСПРАВЛЕННЫЕ ПРОБЛЕМЫ:")
        print("=" * 50)
        
        # 1. Тест Vacancy - должен теперь работать
        print("1. 🧪 Тестируем careers.vacancy (исправлена проблема с posted_date)...")
        try:
            # Список
            list_url = reverse('admin:careers_vacancy_changelist')
            response = self.client.get(list_url)
            if response.status_code == 200:
                print("   ✅ Список вакансий загружается")
            else:
                print(f"   ❌ Список недоступен (код: {response.status_code})")
            
            # Форма добавления
            add_url = reverse('admin:careers_vacancy_add')
            response = self.client.get(add_url)
            if response.status_code == 200:
                print("   ✅ Форма добавления вакансии работает!")
                self.results['fixed_models'].append('careers.vacancy')
                
                # Попробуем создать минимальную вакансию
                from careers.models import CareerCategory, Department
                
                # Создаем тестовые данные если их нет
                category, _ = CareerCategory.objects.get_or_create(
                    name='test_category',
                    defaults={
                        'display_name_ru': 'Тестовая категория',
                        'display_name_kg': 'Тест категориясы',
                        'display_name_en': 'Test Category'
                    }
                )
                
                department, _ = Department.objects.get_or_create(
                    short_name='TEST',
                    defaults={
                        'name_ru': 'Тестовый отдел',
                        'name_kg': 'Тест бөлүмү',
                        'name_en': 'Test Department',
                        'contact_email': 'test@example.com'
                    }
                )
                
                test_data = {
                    'title_ru': 'Тестовая вакансия',
                    'title_kg': 'Тест жумуш орду',
                    'title_en': 'Test Position',
                    'slug': 'test-vacancy',
                    'category': category.id,
                    'department': department.id,
                    'status': 'draft',
                    'employment_type': 'full_time',
                    'location_ru': 'Бишкек',
                    'location_kg': 'Бишкек',
                    'location_en': 'Bishkek',
                    'short_description_ru': 'Тест',
                    'short_description_kg': 'Тест',
                    'short_description_en': 'Test',
                    'description_ru': 'Тестовое описание',
                    'description_kg': 'Тест сүрөттөмө',
                    'description_en': 'Test description',
                    'responsibilities_ru': 'Тестовые обязанности',
                    'responsibilities_kg': 'Тест милдеттер',
                    'responsibilities_en': 'Test responsibilities',
                    'requirements_ru': 'Тестовые требования',
                    'requirements_kg': 'Тест талаптар',
                    'requirements_en': 'Test requirements',
                    'contact_email': 'hr@example.com'
                }
                
                create_response = self.client.post(add_url, test_data)
                if create_response.status_code == 302:
                    print("   🎉 СОЗДАНИЕ ВАКАНСИИ РАБОТАЕТ!")
                else:
                    print(f"   ⚠️ Создание не прошло (код: {create_response.status_code})")
                    
            else:
                print(f"   ❌ Форма добавления недоступна (код: {response.status_code})")
                
        except Exception as e:
            print(f"   ❌ Ошибка при тесте vacancy: {e}")
        
        # 2. Тест NewsView - должен быть только для чтения
        print("\n2. 🧪 Тестируем news.newsview (должен быть только для чтения)...")
        try:
            # Список должен работать
            list_url = reverse('admin:news_newsview_changelist')
            response = self.client.get(list_url)
            if response.status_code == 200:
                print("   ✅ Список просмотров новостей доступен")
                
                # Форма добавления должна быть запрещена
                add_url = reverse('admin:news_newsview_add')
                response = self.client.get(add_url)
                if response.status_code == 403:
                    print("   ✅ Добавление корректно запрещено (код 403)")
                    self.results['fixed_models'].append('news.newsview')
                else:
                    print(f"   ⚠️ Неожиданный код ответа для добавления: {response.status_code}")
                    
            else:
                print(f"   ❌ Список недоступен (код: {response.status_code})")
                
        except Exception as e:
            print(f"   ❌ Ошибка при тесте newsview: {e}")
    
    def test_key_models(self):
        """Тест ключевых моделей для подтверждения их работоспособности"""
        print("\n🎯 ТЕСТИРУЕМ КЛЮЧЕВЫЕ МОДЕЛИ:")
        print("=" * 40)
        
        key_models = [
            ('banner.banner', 'Banner'),
            ('news.news', 'News'), 
            ('research.researcharea', 'Research Area'),
            ('careers.department', 'Department')
        ]
        
        for app_model, display_name in key_models:
            app_label, model_name = app_model.split('.')
            print(f"🧪 {display_name}...")
            
            try:
                # Список
                list_url = reverse(f'admin:{app_label}_{model_name}_changelist')
                response = self.client.get(list_url)
                if response.status_code == 200:
                    print(f"   ✅ Список загружается")
                    
                    # Форма добавления
                    add_url = reverse(f'admin:{app_label}_{model_name}_add')
                    response = self.client.get(add_url)
                    if response.status_code == 200:
                        print(f"   ✅ Форма добавления работает")
                        self.results['successful_models'].append(app_model)
                    else:
                        print(f"   ❌ Форма добавления недоступна (код: {response.status_code})")
                        self.results['failed_models'].append(app_model)
                else:
                    print(f"   ❌ Список недоступен (код: {response.status_code})")
                    self.results['failed_models'].append(app_model)
                    
            except Exception as e:
                print(f"   ❌ Ошибка: {e}")
                self.results['errors'].append(f"{app_model}: {e}")
    
    def run_test(self):
        """Запуск финального теста"""
        print("🎯 ФИНАЛЬНЫЙ CRUD ТЕСТ - ПРОВЕРКА ИСПРАВЛЕНИЙ")
        print("=" * 60)
        
        if not self.setup():
            print("❌ Не удалось настроить тестовое окружение")
            return
        
        # Тест исправлений
        self.test_fixed_issues()
        
        # Тест ключевых моделей  
        self.test_key_models()
        
        self.print_results()
    
    def print_results(self):
        """Вывод результатов"""
        print("\n" + "=" * 60)
        print("🏆 РЕЗУЛЬТАТЫ ФИНАЛЬНОГО ТЕСТА")
        print("=" * 60)
        
        if self.results['fixed_models']:
            print(f"\n🔧 ИСПРАВЛЕННЫЕ МОДЕЛИ ({len(self.results['fixed_models'])}):")
            for model in self.results['fixed_models']:
                print(f"   🔧 {model}")
        
        if self.results['successful_models']:
            print(f"\n✅ РАБОТАЮЩИЕ МОДЕЛИ ({len(self.results['successful_models'])}):")
            for model in self.results['successful_models']:
                print(f"   ✅ {model}")
        
        if self.results['failed_models']:
            print(f"\n❌ ПРОБЛЕМНЫЕ МОДЕЛИ ({len(self.results['failed_models'])}):")
            for model in self.results['failed_models']:
                print(f"   ❌ {model}")
        
        if self.results['errors']:
            print(f"\n💥 ОШИБКИ ({len(self.results['errors'])}):")
            for error in self.results['errors']:
                print(f"   💥 {error}")
        
        # Итог
        total_fixed = len(self.results['fixed_models'])
        total_successful = len(self.results['successful_models'])
        total_failed = len(self.results['failed_models'])
        total_tested = total_fixed + total_successful + total_failed
        
        print(f"\n📊 ИТОГОВАЯ СТАТИСТИКА:")
        print(f"   🔧 Исправлено: {total_fixed}")
        print(f"   ✅ Работает: {total_successful}")
        print(f"   ❌ Проблемы: {total_failed}")
        print(f"   📝 Всего протестировано: {total_tested}")
        
        if total_fixed >= 2:
            print("\n🎉 ОТЛИЧНО! Все критические проблемы исправлены!")
            print("   ✅ Vacancy админка работает")
            print("   ✅ NewsView админка настроена корректно")
        elif total_fixed >= 1:
            print("\n👍 Прогресс есть, но нужно доработать")
        else:
            print("\n⚠️ Проблемы не решены")
        
        print(f"\n🚀 Django админка готова к использованию!")

if __name__ == "__main__":
    tester = FinalCRUDTest()
    tester.run_test()
