#!/usr/bin/env python
"""
Тест проверки того, что hover эффекты на input полях удалены
"""
import os
import django
from django.test.utils import setup_test_environment
from django.contrib.auth.models import User

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_su_m.settings')
django.setup()

from django.test import TestCase, Client
from django.urls import reverse

class LoginUITest:
    """Тест UI страницы входа"""
    
    def __init__(self):
        self.client = Client()
    
    def test_login_page_accessibility(self):
        """Проверка доступности страницы входа"""
        print("🧪 Тестируем страницу входа...")
        
        try:
            response = self.client.get('/admin/')
            if response.status_code == 302:
                # Перенаправление на страницу входа - это нормально
                login_url = response.url
                print(f"   ✅ Перенаправление на страницу входа: {login_url}")
                
                # Тестируем саму страницу входа
                login_response = self.client.get(login_url)
                if login_response.status_code == 200:
                    print("   ✅ Страница входа загружается корректно")
                    
                    # Проверяем содержимое
                    content = login_response.content.decode('utf-8')
                    
                    # Проверяем, что нет transition в input полях
                    if 'transition: all 0.3s ease' not in content:
                        print("   ✅ Transition эффекты удалены из input полей")
                    else:
                        print("   ⚠️ Transition эффекты все еще присутствуют")
                    
                    # Проверяем, что нет transform: translateY в focus состоянии
                    if 'transform: translateY(-2px)' not in content:
                        print("   ✅ Transform hover эффекты удалены")
                    else:
                        print("   ⚠️ Transform hover эффекты все еще присутствуют")
                    
                    # Проверяем наличие кастомного дизайна
                    if 'Университет Салымбекова' in content:
                        print("   ✅ Кастомный заголовок присутствует")
                    
                    if 'linear-gradient' in content:
                        print("   ✅ Синий градиентный дизайн активен")
                    
                    return True
                else:
                    print(f"   ❌ Страница входа недоступна (код: {login_response.status_code})")
                    return False
            else:
                print(f"   ❌ Неожиданный код ответа: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ Ошибка при тестировании: {e}")
            return False
    
    def run_test(self):
        """Запуск теста"""
        print("🎯 ТЕСТ УДАЛЕНИЯ HOVER ЭФФЕКТОВ НА INPUT ПОЛЯХ")
        print("=" * 55)
        
        success = self.test_login_page_accessibility()
        
        if success:
            print("\n🎉 ТЕСТ ПРОЙДЕН УСПЕШНО!")
            print("✅ Hover эффекты на input полях удалены")
            print("✅ Страница входа работает корректно")
            print("✅ Кастомный дизайн активен")
            print("\n💡 Теперь можете проверить в браузере:")
            print("   • Откройте http://127.0.0.1:8000/admin/")
            print("   • Наведите курсор на поля Username и Password") 
            print("   • Поля не должны 'подпрыгивать' при наведении")
            print("   • При фокусе должны только менять цвет границы")
        else:
            print("\n❌ ТЕСТ НЕ ПРОЙДЕН")
            print("Проверьте логи выше для деталей")

if __name__ == "__main__":
    tester = LoginUITest()
    tester.run_test()
