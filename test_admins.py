#!/usr/bin/env python
"""
Финальный тест всех админок после исправлений
"""
import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_su_m.settings')
django.setup()

from django.contrib import admin
from django.apps import apps

def test_all_admins():
    """Тестируем все админки на наличие ошибок"""
    print("=== ФИНАЛЬНАЯ ПРОВЕРКА ВСЕХ АДМИНОК ===\n")
    
    errors = []
    warnings = []
    successes = []
    
    # Получаем все зарегистрированные админки
    for model, admin_class in admin.site._registry.items():
        app_label = model._meta.app_label
        model_name = model.__name__
        admin_name = admin_class.__class__.__name__
        
        print(f"🔍 Проверяем: {app_label}.{model_name} -> {admin_name}")
        
        try:
            # Проверяем list_display
            if hasattr(admin_class, 'list_display'):
                list_display = admin_class.list_display
                for field in list_display:
                    if isinstance(field, str) and not hasattr(model, field) and not hasattr(admin_class, field):
                        errors.append(f"❌ {app_label}.{model_name}: Поле '{field}' в list_display не существует")
                        continue
                        
            # Проверяем fieldsets
            if hasattr(admin_class, 'fieldsets'):
                fieldsets = admin_class.fieldsets
                for fieldset_name, fieldset_data in fieldsets:
                    fields = fieldset_data.get('fields', [])
                    for field_group in fields:
                        if isinstance(field_group, (list, tuple)):
                            for field in field_group:
                                if not hasattr(model, field) and not hasattr(admin_class, field):
                                    errors.append(f"❌ {app_label}.{model_name}: Поле '{field}' в fieldsets не существует")
                        elif isinstance(field_group, str):
                            if not hasattr(model, field_group) and not hasattr(admin_class, field_group):
                                errors.append(f"❌ {app_label}.{model_name}: Поле '{field_group}' в fieldsets не существует")
            
            # Проверяем readonly_fields
            if hasattr(admin_class, 'readonly_fields'):
                readonly_fields = admin_class.readonly_fields
                for field in readonly_fields:
                    if not hasattr(model, field) and not hasattr(admin_class, field):
                        errors.append(f"❌ {app_label}.{model_name}: Поле '{field}' в readonly_fields не существует")
            
            # Проверяем search_fields
            if hasattr(admin_class, 'search_fields'):
                search_fields = admin_class.search_fields
                for field in search_fields:
                    # Убираем префиксы поиска
                    clean_field = field.replace('__icontains', '').replace('__exact', '').replace('__startswith', '')
                    if not hasattr(model, clean_field):
                        errors.append(f"❌ {app_label}.{model_name}: Поле '{clean_field}' в search_fields не существует")
            
            if not any(error.startswith(f"❌ {app_label}.{model_name}:") for error in errors[-10:]):
                successes.append(f"✅ {app_label}.{model_name}: Админка корректна")
                
        except Exception as e:
            errors.append(f"❌ {app_label}.{model_name}: Ошибка при проверке - {str(e)}")
    
    print("\n" + "="*60)
    print("РЕЗУЛЬТАТЫ ПРОВЕРКИ:")
    print("="*60)
    
    if successes:
        print(f"\n✅ УСПЕШНО ({len(successes)}):")
        for success in successes:
            print(f"   {success}")
    
    if warnings:
        print(f"\n⚠️ ПРЕДУПРЕЖДЕНИЯ ({len(warnings)}):")
        for warning in warnings:
            print(f"   {warning}")
    
    if errors:
        print(f"\n❌ ОШИБКИ ({len(errors)}):")
        for error in errors:
            print(f"   {error}")
    else:
        print(f"\n🎉 ОТЛИЧНО! Все админки работают без ошибок!")
        
    print(f"\nИтого: {len(successes)} успешно, {len(warnings)} предупреждений, {len(errors)} ошибок")

if __name__ == "__main__":
    test_all_admins()
