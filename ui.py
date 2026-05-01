"""
Модуль графического интерфейса приложения.
Реализован на tkinter. Содержит класс PasswordGeneratorApp.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from generator import generate_password
from validator import validate_password_settings, validate_password_name
from storage import add_password_entry, load_passwords


class PasswordGeneratorApp:
    """Основной класс графического приложения Генератора паролей."""

    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных паролей")
        self.root.geometry("650x550")
        self.root.resizable(False, False)

        # Переменные интерфейса
        self.length_var = tk.IntVar(value=12)
        self.upper_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.special_var = tk.BooleanVar(value=True)
        self.name_var = tk.StringVar()
        self.generated_password = tk.StringVar()

        self._setup_ui()
        self._refresh_password_list()

    # ----------------------------------------------------------------
    # Построение интерфейса
    # ----------------------------------------------------------------
    def _setup_ui(self):
        """Создаёт все элементы интерфейса."""
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Блок настроек ---
        settings_frame = ttk.LabelFrame(main_frame, text="Настройки генерации", padding=10)
        settings_frame.pack(fill=tk.X, pady=(0, 10))

        # Длина пароля
        row0 = ttk.Frame(settings_frame)
        row0.pack(fill=tk.X, pady=3)
        ttk.Label(row0, text="Длина пароля (6–128):").pack(side=tk.LEFT)
        length_spin = ttk.Spinbox(row0, from_=6, to=128, textvariable=self.length_var, width=8)
        length_spin.pack(side=tk.LEFT, padx=10)

        # Флаги символов
        flags_frame = ttk.Frame(settings_frame)
        flags_frame.pack(fill=tk.X, pady=3)
        ttk.Checkbutton(flags_frame, text="Заглавные буквы", variable=self.upper_var).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(flags_frame, text="Цифры", variable=self.digits_var).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(flags_frame, text="Спецсимволы", variable=self.special_var).pack(side=tk.LEFT, padx=5)

        # Кнопка генерации
        btn_gen = ttk.Button(settings_frame, text="Сгенерировать пароль", command=self._on_generate)
        btn_gen.pack(pady=8)

        # --- Блок вывода пароля ---
        output_frame = ttk.LabelFrame(main_frame, text="Сгенерированный пароль", padding=10)
        output_frame.pack(fill=tk.X, pady=(0, 10))

        self.password_display = ttk.Entry(output_frame, textvariable=self.generated_password,
                                          font=("Courier", 14), justify=tk.CENTER, state="readonly")
        self.password_display.pack(fill=tk.X, ipady=4)

        # --- Блок сохранения ---
        save_frame = ttk.LabelFrame(main_frame, text="Сохранить пароль", padding=10)
        save_frame.pack(fill=tk.X, pady=(0, 10))

        save_row = ttk.Frame(save_frame)
        save_row.pack(fill=tk.X)
        ttk.Label(save_row, text="Имя записи:").pack(side=tk.LEFT)
        ttk.Entry(save_row, textvariable=self.name_var, width=40).pack(side=tk.LEFT, padx=10)
        ttk.Button(save_row, text="Сохранить", command=self._on_save).pack(side=tk.LEFT)

        # --- Блок истории ---
        history_frame = ttk.LabelFrame(main_frame, text="Сохранённые пароли", padding=10)
        history_frame.pack(fill=tk.BOTH, expand=True)

        # Таблица
        columns = ("name", "password", "created")
        self.tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=8)
        self.tree.heading("name", text="Имя")
        self.tree.heading("password", text="Пароль")
        self.tree.heading("created", text="Дата создания")
        self.tree.column("name", width=200)
        self.tree.column("password", width=250)
        self.tree.column("created", width=150)

        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # ----------------------------------------------------------------
    # Логика действий
    # ----------------------------------------------------------------
    def _on_generate(self):
        """Обработчик кнопки генерации пароля."""
        settings = {
            'length': self.length_var.get(),
            'use_uppercase': self.upper_var.get(),
            'use_digits': self.digits_var.get(),
            'use_special': self.special_var.get()
        }

        errors = validate_password_settings(settings)
        if errors:
            messagebox.showerror("Ошибка настроек", "\n".join(errors))
            return

        try:
            password = generate_password(**settings)
            self.generated_password.set(password)
        except Exception as e:
            messagebox.showerror("Ошибка генерации", str(e))

    def _on_save(self):
        """Обработчик кнопки сохранения пароля."""
        password = self.generated_password.get()
        if not password:
            messagebox.showwarning("Нет пароля", "Сначала сгенерируйте пароль.")
            return

        name = self.name_var.get()
        name_error = validate_password_name(name)
        if name_error:
            messagebox.showerror("Ошибка имени", name_error)
            return

        settings = {
            'length': self.length_var.get(),
            'use_uppercase': self.upper_var.get(),
            'use_digits': self.digits_var.get(),
            'use_special': self.special_var.get()
        }

        add_password_entry(name, password, settings)
        self._refresh_password_list()
        self.name_var.set("")
        messagebox.showinfo("Успешно", f"Пароль '{name}' сохранён.")

    def _refresh_password_list(self):
        """Обновляет таблицу с сохранёнными паролями."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        entries = load_passwords()
        for entry in entries:
            self.tree.insert("", tk.END, values=(entry.get("name", ""),
                                                 entry.get("password", ""),
                                                 entry.get("created_at", "")))
