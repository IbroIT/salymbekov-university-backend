#!/usr/bin/env python
"""
Скрипт для проверки всех моделей и их полей
"""
import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_su_m.settings')
django.setup()

from django.apps import apps

def check_all_models():
    """Проверяем все модели и их поля"""
    print("=== ПРОВЕРКА ВСЕХ МОДЕЛЕЙ И ИХ ПОЛЕЙ ===\n")
    
    # Получаем все приложения
    app_configs = apps.get_app_configs()
    
    for app_config in app_configs:
        # Пропускаем системные приложения Django
        if app_config.name.startswith('django.'):
            continue
            
        print(f"📱 Приложение: {app_config.name}")
        print("-" * 50)
        
        # Получаем все модели приложения
        models = app_config.get_models()
        
        if not models:
            print("   Нет моделей\n")
            continue
            
        for model in models:
            print(f"   📋 Модель: {model.__name__}")
            
            # Получаем все поля модели
            fields = model._meta.get_fields()
            field_names = [field.name for field in fields]
            
            print(f"      Поля: {field_names}")
            
            # Проверяем наличие мультиязычных полей
            lang_fields = {
                'ru': [f for f in field_names if f.endswith('_ru')],
                'kg': [f for f in field_names if f.endswith('_kg')], 
                'ky': [f for f in field_names if f.endswith('_ky')],
                'en': [f for f in field_names if f.endswith('_en')]
            }
            
            for lang, lang_field_list in lang_fields.items():
                if lang_field_list:
                    print(f"      {lang.upper()}: {lang_field_list}")
            
            print()
        
        print()

if __name__ == "__main__":
    check_all_models()
