"""
Модуль валидации пользовательского ввода.
Обеспечивает проверку корректности настроек генерации пароля и имени записи.
"""

import re


def validate_password_settings(settings):
    """
    Проверяет словарь настроек генерации пароля.
    Возвращает список строк с описаниями ошибок.
    Если список пуст — данные корректны.
    """
    errors = []

    # Проверка длины
    length = settings.get('length')
    if not isinstance(length, int):
        errors.append("Длина пароля должна быть целым числом.")
    elif not (6 <= length <= 128):
        errors.append("Длина пароля должна быть от 6 до 128 символов.")

    # Проверка булевых флагов
    for key in ['use_uppercase', 'use_digits', 'use_special']:
        value = settings.get(key)
        if not isinstance(value, bool):
            errors.append(f"Параметр '{key}' должен принимать значение True или False.")

    # Хотя бы один дополнительный набор символов
    if not (settings.get('use_uppercase') or settings.get('use_digits') or settings.get('use_special')):
        errors.append("Необходимо выбрать хотя бы один дополнительный тип символов (заглавные, цифры или спецсимволы).")

    return errors


def validate_password_name(name):
    """
    Проверяет имя (название) сохраняемого пароля.
    Возвращает None, если имя корректно, иначе строку с ошибкой.
    """
    if not name or not name.strip():
        return "Имя пароля не может быть пустым."
    if len(name.strip()) > 50:
        return "Имя пароля не должно превышать 50 символов."
    if not re.match(r'^[A-Za-zА-Яа-я0-9 _-]+$', name.strip()):
        return "Имя может содержать только буквы, цифры, пробелы, дефисы и подчёркивания."
    return None
