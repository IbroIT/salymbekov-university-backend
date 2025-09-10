#!/usr/bin/env python
"""
Скрипт для проверки всех админок на наличие проблемных полей
"""
import os
import re
from pathlib import Path

def check_admin_files():
    """Проверяем все admin.py файлы"""
    print("=== ПРОВЕРКА ВСЕХ АДМИНОК ===\n")
    
    # Находим все admin.py файлы
    admin_files = list(Path('.').glob('*/admin.py'))
    
    issues = []
    
    for admin_file in admin_files:
        print(f"📁 Файл: {admin_file}")
        
        try:
            content = admin_file.read_text(encoding='utf-8')
            
            # Ищем поля с _ky (должно быть _kg)
            ky_fields = re.findall(r'[\'\"]([a-zA-Z_]*_ky)[\'\"]', content)
            if ky_fields:
                issues.append((str(admin_file), 'ky_fields', ky_fields))
                print(f"   ❌ Найдены поля с _ky: {ky_fields}")
            
            # Ищем методы preview без readonly_fields
            preview_methods = re.findall(r'def ([a-zA-Z_]*_preview)\(', content)
            has_readonly = 'readonly_fields' in content
            
            if preview_methods and not has_readonly:
                issues.append((str(admin_file), 'missing_readonly', preview_methods))
                print(f"   ⚠️ Методы preview без readonly_fields: {preview_methods}")
            elif preview_methods and has_readonly:
                print(f"   ✅ Методы preview с readonly_fields: {preview_methods}")
            
            # Ищем потенциально несуществующие поля в fieldsets
            fieldset_matches = re.findall(r'\'fields\':\s*\([^)]*\)', content)
            for match in fieldset_matches:
                # Простая проверка на наличие подозрительных полей
                if '_ky' in match:
                    print(f"   ❌ Подозрительные поля в fieldsets: {match}")
            
            if not ky_fields and not (preview_methods and not has_readonly):
                print(f"   ✅ Админка выглядит корректно")
                
        except Exception as e:
            print(f"   ❌ Ошибка при чтении файла: {e}")
            
        print()
    
    print("\n=== СВОДКА ПРОБЛЕМ ===")
    if not issues:
        print("✅ Проблем не найдено!")
    else:
        for file_path, issue_type, details in issues:
            if issue_type == 'ky_fields':
                print(f"❌ {file_path}: Поля с _ky вместо _kg: {details}")
            elif issue_type == 'missing_readonly':
                print(f"⚠️ {file_path}: Методы preview без readonly_fields: {details}")

if __name__ == "__main__":
    check_admin_files()
