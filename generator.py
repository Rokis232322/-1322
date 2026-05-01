"""
Модуль генерации случайных паролей.
Использует библиотеку random для криптографически непредсказуемых (в учебных целях) паролей.
"""

import random
import string


def generate_password(length=12, use_uppercase=True, use_digits=True, use_special=True):
    """
    Генерирует случайный пароль с заданными параметрами.
    Параметры:
        length — длина пароля (по умолчанию 12)
        use_uppercase — включать ли заглавные буквы
        use_digits — включать ли цифры
        use_special — включать ли специальные символы
    Возвращает строку сгенерированного пароля.
    """
    # Базовый пул — строчные латинские буквы
    char_pool = string.ascii_lowercase
    mandatory_chars = [random.choice(string.ascii_lowercase)]

    if use_uppercase:
        char_pool += string.ascii_uppercase
        mandatory_chars.append(random.choice(string.ascii_uppercase))
    if use_digits:
        char_pool += string.digits
        mandatory_chars.append(random.choice(string.digits))
    if use_special:
        special_symbols = "!@#$%^&*()_+-=[]{}|;:',.<>?/`~"
        char_pool += special_symbols
        mandatory_chars.append(random.choice(special_symbols))

    remaining_length = length - len(mandatory_chars)
    if remaining_length < 0:
        raise ValueError("Слишком маленькая длина пароля для выбранных наборов символов")

    # Добавляем случайные символы до нужной длины
    additional_chars = random.choices(char_pool, k=remaining_length)
    password_list = mandatory_chars + additional_chars
    random.shuffle(password_list)

    return ''.join(password_list)
