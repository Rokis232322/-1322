"""
Точка входа в приложение Генератор паролей.
Запускает графический интерфейс.
"""

import tkinter as tk
from ui import PasswordGeneratorApp


def main():
    """Запуск основного окна приложения."""
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
