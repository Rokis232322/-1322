"""
Модуль для работы с JSON-хранилищем сохранённых паролей.
Обеспечивает загрузку, сохранение и добавление новых записей.
"""

import json
import os
from datetime import datetime


STORAGE_FILE = "storage.json"


def load_passwords():
    """
    Загружает список сохранённых паролей из JSON-файла.
    Если файл не существует или повреждён, возвращает пустой список.
    """
    if not os.path.exists(STORAGE_FILE):
        return []
    try:
        with open(STORAGE_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, IOError):
        return []


def save_passwords(passwords):
    """
    Сохраняет список паролей в JSON-файл.
    """
    with open(STORAGE_FILE, 'w', encoding='utf-8') as file:
        json.dump(passwords, file, ensure_ascii=False, indent=4)


def add_password_entry(name, password, settings):
    """
    Добавляет новую запись в хранилище.
    Параметры:
        name — имя записи
        password — сгенерированный пароль
        settings — словарь использованных настроек генерации
    """
    entries = load_passwords()
    new_record = {
        "name": name.strip(),
        "password": password,
        "settings": settings,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    entries.append(new_record)
    save_passwords(entries)
