import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import random

class RandomSelector:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Рандомайзер")

        # Создаем меню-бар
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Добавляем пункт "О программе"
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="О программе", command=self.show_about)
        self.menu_bar.add_cascade(label="Меню", menu=help_menu)

        ttk.Label(self.root, text="Введите количество переменных:").grid(row=0, column=0, pady=5, padx=5)
        self.count_var = tk.StringVar()
        self.count_entry = ttk.Entry(self.root, textvariable=self.count_var, width=5)
        self.count_entry.grid(row=0, column=1, pady=5, padx=5)

        self.btn_confirm = ttk.Button(self.root, text="Создать поля", command=self.create_input_fields)
        self.btn_confirm.grid(row=1, column=0, columnspan=2, pady=5)

        self.entries_frame = ttk.Frame(self.root)
        self.entries_frame.grid(row=2, column=0, columnspan=2, pady=10)

        self.entries = []

        self.result_label = ttk.Label(self.root, text="", font=('Arial', 14))
        self.result_label.grid(row=4, column=0, columnspan=2, pady=10)

        # Кнопка сброса
        self.btn_reset = ttk.Button(self.root, text="Сбросить", command=self.reset_all)
        self.btn_reset.grid(row=5, column=0, columnspan=2, pady=5)

        self.root.mainloop()

    def show_about(self):
        # Открываем окно с информацией о программе
        about_text = (
            "Версия: 1.0\n"
            "Создатель: OdusseusGVK\n"
            "Сайт: "
        )
        # Создаем всплывающее окно
        about_window = tk.Toplevel(self.root)
        about_window.title("О программе")
        about_window.geometry("400x150")
        ttk.Label(about_window, text=about_text, justify='left').pack(pady=10)

        # Создаем ссылку на сайт
        link = ttk.Label(about_window, text="Ссылка", foreground="blue", cursor="hand2")
        link.pack()
        link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/OdusseusGVK"))

    def create_input_fields(self):
        # Очистка предыдущих полей
        for widget in self.entries_frame.winfo_children():
            widget.destroy()
        self.entries.clear()

        count_str = self.count_var.get().strip()
        if not count_str.isdigit():
            self.result_label.config(text="Пожалуйста, введите корректное число переменных.")
            return

        count = int(count_str)
        if count <= 0:
            self.result_label.config(text="Количество переменных должно быть больше нуля.")
            return

        # Создание новых полей
        for i in range(count):
            ttk.Label(self.entries_frame, text=f"Переменная {i+1}:").grid(row=i, column=0, sticky='e')
            entry = ttk.Entry(self.entries_frame)
            entry.grid(row=i, column=1, pady=2)
            self.entries.append(entry)

        # Удаление старой кнопки выбора, если есть
        if hasattr(self, 'btn_choose'):
            self.btn_choose.destroy()

        # Кнопка выбора
        self.btn_choose = ttk.Button(self.root, text="Выбрать случайную", command=self.select_random)
        self.btn_choose.grid(row=3, column=0, columnspan=2, pady=10)

    def select_random(self):
        vars_list = [entry.get().strip() for entry in self.entries if entry.get().strip() != ""]
        if not vars_list:
            self.result_label.config(text="Пожалуйста, введите переменные.")
            return
        secure_rand = random.SystemRandom()
        choice = secure_rand.choice(vars_list)
        self.result_label.config(text=f"Победитель: {choice}")

    def reset_all(self):
        # Очистка всех полей и результата
        for widget in self.entries_frame.winfo_children():
            widget.destroy()
        self.entries.clear()
        self.result_label.config(text="")
        self.count_var.set("")
        # Удаляем кнопку выбора, если есть
        if hasattr(self, 'btn_choose'):
            self.btn_choose.destroy()

if __name__ == "__main__":
    app = RandomSelector()
