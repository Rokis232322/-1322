"""
Модуль тестирования функциональности приложения.
Покрывает позитивные, негативные и граничные случаи.
"""

import unittest
from validator import validate_password_settings, validate_password_name
from generator import generate_password
from storage import save_passwords, load_passwords, add_password_entry
import os
import json


class TestValidator(unittest.TestCase):
    """Тесты модуля валидации."""

    def test_correct_settings(self):
        """Позитивный тест: корректные настройки."""
        errors = validate_password_settings({
            'length': 12,
            'use_uppercase': True,
            'use_digits': True,
            'use_special': False
        })
        self.assertEqual(errors, [])

    def test_length_too_small(self):
        """Негативный тест: длина меньше 6."""
        errors = validate_password_settings({
            'length': 3,
            'use_uppercase': True,
            'use_digits': True,
            'use_special': True
        })
        self.assertTrue(any("от 6 до 128" in e for e in errors))

    def test_length_boundary(self):
        """Граничный тест: длина ровно 6 и 128."""
        errors_min = validate_password_settings({
            'length': 6,
            'use_uppercase': True,
            'use_digits': False,
            'use_special': False
        })
        self.assertEqual(errors_min, [])

        errors_max = validate_password_settings({
            'length': 128,
            'use_uppercase': True,
            'use_digits': False,
            'use_special': False
        })
        self.assertEqual(errors_max, [])

    def test_no_additional_chars(self):
        """Негативный тест: не выбран ни один дополнительный набор."""
        errors = validate_password_settings({
            'length': 10,
            'use_uppercase': False,
            'use_digits': False,
            'use_special': False
        })
        self.assertTrue(any("хотя бы один" in e for e in errors))

    def test_wrong_types(self):
        """Негативный тест: неверные типы данных."""
        errors = validate_password_settings({
            'length': "twelve",
            'use_uppercase': "yes",
            'use_digits': 1,
            'use_special': None
        })
        self.assertTrue(len(errors) > 0)

    def test_name_valid(self):
        """Позитивный тест имени."""
        self.assertIsNone(validate_password_name("Email"))
        self.assertIsNone(validate_password_name("Пароль от почты"))

    def test_name_empty(self):
        """Негативный тест: пустое имя."""
        self.assertIsNotNone(validate_password_name(""))
        self.assertIsNotNone(validate_password_name("   "))

    def test_name_too_long(self):
        """Граничный тест: слишком длинное имя."""
        long_name = "A" * 51
        self.assertIsNotNone(validate_password_name(long_name))


class TestGenerator(unittest.TestCase):
    """Тесты модуля генерации паролей."""

    def test_default_generation(self):
        """Позитивный тест: генерация с параметрами по умолчанию."""
        pwd = generate_password()
        self.assertEqual(len(pwd), 12)
        self.assertTrue(any(c.isupper() for c in pwd))
        self.assertTrue(any(c.isdigit() for c in pwd))

    def test_length_generation(self):
        """Граничный тест: минимальная и максимальная длина."""
        pwd_short = generate_password(length=6, use_uppercase=False, use_digits=False, use_special=False)
        self.assertEqual(len(pwd_short), 6)

        pwd_long = generate_password(length=64, use_uppercase=True, use_digits=True, use_special=True)
        self.assertEqual(len(pwd_long), 64)

    def test_character_inclusion(self):
        """Позитивный тест: проверка включения нужных символов."""
        pwd = generate_password(length=20, use_uppercase=True, use_digits=True, use_special=True)
        self.assertTrue(any(c.isupper() for c in pwd))
        self.assertTrue(any(c.isdigit() for c in pwd))
        specials = set("!@#$%^&*()_+-=[]{}|;:',.<>?/`~")
        self.assertTrue(any(c in specials for c in pwd))

    def test_no_unwanted_characters(self):
        """Позитивный тест: отсутствие ненужных типов."""
        pwd = generate_password(length=12, use_uppercase=False, use_digits=False, use_special=False)
        self.assertFalse(any(c.isupper() for c in pwd))
        self.assertFalse(any(c.isdigit() for c in pwd))

    def test_generate_many_unique(self):
        """Позитивный тест: множество паролей должны быть разными."""
        passwords = {generate_password(length=16) for _ in range(50)}
        self.assertEqual(len(passwords), 50)


class TestStorage(unittest.TestCase):
    """Тесты модуля работы с JSON-хранилищем."""

    def setUp(self):
        """Подготовка: очистка хранилища перед каждым тестом."""
        if os.path.exists("storage.json"):
            os.remove("storage.json")

    def tearDown(self):
        """Очистка после тестов."""
        if os.path.exists("storage.json"):
            os.remove("storage.json")

    def test_load_empty(self):
        """Тест загрузки при отсутствии файла."""
        self.assertEqual(load_passwords(), [])

    def test_save_and_load(self):
        """Позитивный тест: сохранение и загрузка."""
        test_data = [{"name": "test", "password": "12345"}]
        save_passwords(test_data)
        loaded = load_passwords()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["name"], "test")

    def test_add_entry(self):
        """Позитивный тест: добавление записи."""
        add_password_entry("Email", "abc123", {"length": 6})
        entries = load_passwords()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["name"], "Email")
        self.assertIn("created_at", entries[0])

    def test_add_multiple_entries(self):
        """Тест добавления нескольких записей."""
        for i in range(5):
            add_password_entry(f"Entry_{i}", f"pass_{i}", {})
        entries = load_passwords()
        self.assertEqual(len(entries), 5)


if __name__ == "__main__":
    unittest.main()
