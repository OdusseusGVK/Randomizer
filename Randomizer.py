import tkinter as tk
from tkinter import ttk
import webbrowser
import random
import json
import os
from datetime import datetime
import platform


if platform.system() == 'Windows':
    import winsound

class RandomizerApp:
    SETTINGS_FILE = 'settings.json'
    HISTORY_FILE = 'history.json'

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Рандомайзер")
        self.is_dark_theme = False
        self.current_language = 'ru'
        self.history = []

        self.load_settings()
        self.load_history()

        self.init_texts()
        self.create_about_window()
        self.create_widgets()
        self.set_theme()
        self.apply_saved_title()
        self.root.mainloop()

    # --------------------- Настройки и история ---------------------
    def load_settings(self):
        if os.path.exists(self.SETTINGS_FILE):
            try:
                with open(self.SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                self.is_dark_theme = settings.get('theme', False)
                self.current_language = settings.get('language', 'ru')
                self.saved_title = settings.get('title', None)
            except:
                self.saved_title = None
        else:
            self.saved_title = None

    def save_settings(self):
        settings = {
            'theme': self.is_dark_theme,
            'language': self.current_language,
            'title': self.root.title()
        }
        with open(self.SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f)

    def load_history(self):
        if os.path.exists(self.HISTORY_FILE):
            try:
                with open(self.HISTORY_FILE, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except:
                self.history = []

    def save_history(self):
        with open(self.HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.history, f)

    # --------------------- Тексты ---------------------
    def init_texts(self):
        self.texts = {
            'ru': {
                'program_title': 'Рандомайзер',
                'menu': 'Меню',
                'about': 'О программе',
                'about_text': 'Версия: 2.1\nСоздатель: OdusseusGVK\nСсылка: нажми на кнопку чтобы перейти',
                'theme': 'Тема',
                'switch_theme': 'Переключить тему',
                'mode': 'Выберите режим:',
                'variables': 'Работать с переменными',
                'range': 'Работать с диапазоном',
                'create_fields': 'Создать поля',
                'select': 'Выбрать',
                'reset': 'Сбросить',
                'variable_label': 'Кол-во переменных (от 2):',
                'number_var': 'Переменная',
                'range_label': 'Диапазон чисел:',
                'min': 'Мин:',
                'max': 'Макс:',
                'choose': 'Выбрать',
                'enter_number': 'Введите число от 2',
                'incorrect_input': 'Некорректный ввод',
                'min_less_than_max': 'Мин должен быть меньше Макс',
                'winner': 'Победитель:',
                'number': 'Число:',
                'language': 'Язык',
                'lang_ru': 'RU',
                'lang_en': 'EN',
                'profile_button_text': 'Перейти на профиль',
                'history': 'История',
                'history_title': 'История выбора',
                'clear_history': 'Очистить историю',
                'entered_vars': 'Введенные переменные/диапазоны',
                'time': 'Время',
            },
            'en': {
                'program_title': 'Randomizer',
                'menu': 'Menu',
                'about': 'About',
                'about_text': 'Version: 2.1\nCreator: OdusseusGVK\nLink: click the button to visit',
                'theme': 'Theme',
                'switch_theme': 'Switch Theme',
                'mode': 'Choose mode:',
                'variables': 'Work with variables',
                'range': 'Work with range',
                'create_fields': 'Create fields',
                'select': 'Select',
                'reset': 'Reset',
                'variable_label': 'Number of variables (from 2):',
                'number_var': 'Variable',
                'range_label': 'Number range:',
                'min': 'Min:',
                'max': 'Max:',
                'choose': 'Choose',
                'enter_number': 'Enter a number from 2',
                'incorrect_input': 'Incorrect input',
                'min_less_than_max': 'Min should be less than Max',
                'winner': 'Winner:',
                'number': 'Number:',
                'language': 'Language',
                'lang_ru': 'RU',
                'lang_en': 'EN',
                'profile_button_text': 'Go to profile',
                'history': 'History',
                'history_title': 'Selection History',
                'clear_history': 'Clear History',
                'entered_vars': 'Entered variables/range',
                'time': 'Time',
            }
        }

    def get_text(self, key):
        return self.texts[self.current_language][key]

    # --------------------- Окно "О программе" ---------------------
    def create_about_window(self):
        self.about_win = tk.Toplevel(self.root)
        self.about_win.title(self.get_text('about'))
        self.about_win.protocol("WM_DELETE_WINDOW", self.about_win.withdraw)
        self.about_win.withdraw()

        self.style_about = ttk.Style()
        self.update_about_theme()

        self.about_label = ttk.Label(self.about_win, text=self.get_text('about_text'), style='About.TLabel', justify='left', padding=10)
        self.about_label.pack()

        self.profile_button = ttk.Button(self.about_win, text=self.get_text('profile_button_text'), style='About.TButton', command=lambda: webbrowser.open("https://github.com/OdusseusGVK"))
        self.profile_button.pack()

    # --------------------- Основные виджеты ---------------------
    def create_widgets(self):
        self.create_menu()
        self.create_main_interface()

    def create_menu(self):
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        self.build_menu()

    def build_menu(self):
        self.menubar.delete(0, 'end')
        menu_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=self.get_text('menu'), menu=menu_menu)
        menu_menu.add_command(label=self.get_text('about'), command=self.show_about)

        theme_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=self.get_text('theme'), menu=theme_menu)
        theme_menu.add_command(label=self.get_text('switch_theme'), command=self.toggle_theme_and_save)

        language_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=self.get_text('language'), menu=language_menu)
        language_menu.add_command(label=self.get_text('lang_ru'), command=lambda: self.switch_language('ru'))
        language_menu.add_command(label=self.get_text('lang_en'), command=lambda: self.switch_language('en'))

        # Меню истории
        history_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=self.get_text('history'), menu=history_menu)
        history_menu.add_command(label=self.get_text('history_title'), command=self.show_history)
        history_menu.add_command(label=self.get_text('clear_history'), command=self.clear_history)

    def create_main_interface(self):
        # Основные виджеты
        self.reset_button = ttk.Button(self.root, text=self.get_text('reset'), command=self.reset_all)

        self.mode_var = tk.StringVar(value='variables')
        self.label_mode = ttk.Label(self.root, text=self.get_text('mode'))
        self.label_mode.pack(pady=10)

        self.mode_frame = ttk.Frame(self.root)
        self.mode_frame.pack()

        self.rb_variables = ttk.Radiobutton(self.mode_frame, text=self.get_text('variables'), variable=self.mode_var, value='variables', command=self.show_mode)
        self.rb_range = ttk.Radiobutton(self.mode_frame, text=self.get_text('range'), variable=self.mode_var, value='range', command=self.show_mode)
        self.rb_variables.pack(side='left', padx=10)
        self.rb_range.pack(side='left', padx=10)

        # Создаем секции для переменных и диапазона
        self.vars_frame = ttk.Frame(self.root)
        self.range_frame = ttk.Frame(self.root)

        self.create_variables_section()
        self.create_range_section()

        # Метка для результатов
        self.result_label = ttk.Label(self.root, text="", font=('Arial', 14))
        self.result_label.pack(pady=10)

        self.show_mode()

    def create_variables_section(self):
        # Очистка, если есть
        if hasattr(self, 'vars_entries_container'):
            for widget in self.vars_entries_container.winfo_children():
                widget.destroy()

        self.variable_entries = []

        self.label_vars_count = ttk.Label(self.vars_frame, text=self.get_text('variable_label'))
        self.label_vars_count.grid(row=0, column=0, pady=5, padx=5)

        self.var_count_str = tk.StringVar(value='2')
        self.entry_vars_count = ttk.Entry(self.vars_frame, textvariable=self.var_count_str, width=5)
        self.entry_vars_count.grid(row=0, column=1, pady=5, padx=5)

        self.btn_create_vars = ttk.Button(self.vars_frame, text=self.get_text('create_fields'), command=self.create_variable_entries)
        self.btn_create_vars.grid(row=1, column=0, columnspan=2, pady=5)

        self.vars_entries_container = ttk.Frame(self.vars_frame)
        self.vars_entries_container.grid(row=2, column=0, columnspan=2, pady=10)

        if hasattr(self, 'select_button'):
            self.select_button.destroy()
        self.select_button = ttk.Button(self.vars_frame, text=self.get_text('select'), command=self.select_variable)
        self.select_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.reset_button.pack(pady=5)

    def create_variable_entries(self):
        for widget in self.vars_entries_container.winfo_children():
            widget.destroy()

        self.variable_entries = []

        try:
            count = int(self.var_count_str.get())
            if count < 2:
                raise ValueError
        except:
            self.result_label.config(text=self.get_text('enter_number'))
            return

        for i in range(count):
            label = ttk.Label(self.vars_entries_container, text=f"{self.get_text('number_var')} {i+1}:")
            label.grid(row=i, column=0, sticky='e')
            entry = ttk.Entry(self.vars_entries_container)
            entry.grid(row=i, column=1, pady=2)
            self.variable_entries.append(entry)

        if hasattr(self, 'select_button'):
            self.select_button.destroy()
        self.select_button = ttk.Button(self.vars_frame, text=self.get_text('select'), command=self.select_variable)
        self.select_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.reset_button.pack(pady=5)
        self.adjust_about_window()

    def select_variable(self):
        options = [e.get().strip() for e in self.variable_entries if e.get().strip() != '']
        if not options:
            self.result_label.config(text=self.get_text('enter_number'))
            return
        choice = random.SystemRandom().choice(options)
        self.result_label.config(text=f"{self.get_text('winner')} {choice}")
        # Анимация мигания
        self.animate_winner_text(choice)
        # Звук
        self.play_sound()

        # Запись в историю
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entered_vars = ', '.join(options)
        history_entry = (
            f"{self.get_text('entered_vars')}: {entered_vars} | "
            f"{self.get_text('time')}: {now} | {self.get_text('winner')}: {choice}"
        )
        self.add_to_history(history_entry)
        self.save_history()
        self.reset_button.pack(pady=5)

    def create_range_section(self):
        # Диапазон
        self.label_range = ttk.Label(self.range_frame, text=self.get_text('range_label'))
        self.label_range.grid(row=0, column=0, columnspan=2, pady=5)

        self.label_min = ttk.Label(self.range_frame, text=self.get_text('min'))
        self.label_min.grid(row=1, column=0, sticky='e', padx=5)

        self.label_max = ttk.Label(self.range_frame, text=self.get_text('max'))
        self.label_max.grid(row=2, column=0, sticky='e', padx=5)

        self.min_var = tk.StringVar()
        self.max_var = tk.StringVar()

        ttk.Entry(self.range_frame, textvariable=self.min_var, width=10).grid(row=1, column=1, sticky='w', padx=5)
        ttk.Entry(self.range_frame, textvariable=self.max_var, width=10).grid(row=2, column=1, sticky='w', padx=5)

        self.btn_range_choose = ttk.Button(self.range_frame, text=self.get_text('choose'), command=self.choose_from_range)
        self.btn_range_choose.grid(row=3, column=0, columnspan=2, pady=10)

    def choose_from_range(self):
        try:
            min_val = int(self.min_var.get())
            max_val = int(self.max_var.get())
        except:
            self.result_label.config(text=self.get_text('incorrect_input'))
            return
        if min_val >= max_val:
            self.result_label.config(text=self.get_text('min_less_than_max'))
            return
        choice = random.SystemRandom().randint(min_val, max_val)
        self.result_label.config(text=f"{self.get_text('number')} {choice}")
        # Анимация
        self.animate_winner_text(str(choice))
        # Звук
        self.play_sound()
        # История
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        range_str = (
            f"{self.get_text('range_label')}: {self.get_text('min')} {min_val} "
            f"{self.get_text('max')} {max_val}"
        )
        history_entry = (
            f"{self.get_text('entered_vars')}: {range_str} | "
            f"{self.get_text('time')}: {now} | {self.get_text('number')}: {choice}"
        )
        self.add_to_history(history_entry)
        self.save_history()
        self.reset_button.pack(pady=5)

    def reset_all(self):
        if hasattr(self, 'vars_entries_container'):
            for widget in self.vars_entries_container.winfo_children():
                widget.destroy()
        self.variable_entries = []
        self.var_count_str.set('2')
        self.min_var.set('')
        self.max_var.set('')
        self.result_label.config(text='')
        self.adjust_about_window()

    def show_mode(self):
        self.vars_frame.pack_forget()
        self.range_frame.pack_forget()
        self.reset_button.pack_forget()

        mode = self.mode_var.get()
        if mode == 'variables':
            self.vars_frame.pack(pady=10)
        else:
            self.range_frame.pack(pady=10)

    def add_to_history(self, entry):
        self.history.append(entry)

    def show_history(self):
        if hasattr(self, 'history_window') and self.history_window and tk.Toplevel.winfo_exists(self.history_window):
            self.history_window.focus()
            self.update_history_style()
            return
        self.history_window = tk.Toplevel(self.root)
        self.history_window.title(self.get_text('history_title'))

        bg = "#2e2e2e" if self.is_dark_theme else "#ffffff"
        fg = "#ffffff" if self.is_dark_theme else "#000000"
        self.history_window.configure(bg=bg)

        self.text_widget = tk.Text(self.history_window, width=80, height=20, bg=bg, fg=fg)
        self.text_widget.pack(padx=10, pady=10)

        for item in self.history:
            self.text_widget.insert('end', item + '\n')

        ttk.Button(self.history_window, text=self.get_text('clear_history'), command=self.clear_history).pack(pady=5)

    def update_history_style(self):
        if hasattr(self, 'history_window') and self.history_window and tk.Toplevel.winfo_exists(self.history_window):
            bg = "#2e2e2e" if self.is_dark_theme else "#ffffff"
            fg = "#ffffff" if self.is_dark_theme else "#000000"
            self.history_window.configure(bg=bg)
            if hasattr(self, 'text_widget') and self.text_widget and self.text_widget.winfo_exists():
                self.text_widget.configure(bg=bg, fg=fg)
            for widget in self.history_window.winfo_children():
                if isinstance(widget, ttk.Button):
                    widget.configure(style='TButton')
        else:
            self.history_window = None
            self.text_widget = None

    def clear_history(self):
        self.history.clear()
        self.save_history()
        if hasattr(self, 'history_window') and self.history_window and tk.Toplevel.winfo_exists(self.history_window):
            self.history_window.destroy()
            self.show_history()

    def get_text(self, key):
        return self.texts[self.current_language][key]

    def switch_language(self, lang):
        self.current_language = lang
        self.update_texts()
        self.save_settings()

    def update_texts(self):
        self.build_menu()
        self.label_mode.config(text=self.get_text('mode'))
        self.reset_button.config(text=self.get_text('reset'))
        self.rb_variables.config(text=self.get_text('variables'))
        self.rb_range.config(text=self.get_text('range'))

        if hasattr(self, 'label_vars_count'):
            self.label_vars_count.config(text=self.get_text('variable_label'))
        if hasattr(self, 'btn_create_vars'):
            self.btn_create_vars.config(text=self.get_text('create_fields'))
        if hasattr(self, 'select_button'):
            self.select_button.config(text=self.get_text('select'))

        if hasattr(self, 'label_range'):
            self.label_range.config(text=self.get_text('range_label'))
        if hasattr(self, 'btn_range_choose'):
            self.btn_range_choose.config(text=self.get_text('choose'))
        if hasattr(self, 'label_min'):
            self.label_min.config(text=self.get_text('min'))
        if hasattr(self, 'label_max'):
            self.label_max.config(text=self.get_text('max'))

        self.about_label.config(text=self.get_text('about_text'))
        self.about_win.title(self.get_text('about'))
        self.profile_button.config(text=self.get_text('profile_button_text'))
        self.root.title(self.get_text('program_title'))

        # Обновление меню
        self.build_menu()

    def toggle_theme_and_save(self):
        self.toggle_theme()
        self.save_settings()

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        self.set_theme()

    def set_theme(self):
        bg = "#2e2e2e" if self.is_dark_theme else "#ffffff"
        fg = "#ffffff" if self.is_dark_theme else "#000000"
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('.', background=bg, foreground=fg)
        style.configure('TButton', background=bg, foreground=fg)
        style.configure('TLabel', background=bg, foreground=fg)
        style.configure('TRadiobutton', background=bg, foreground=fg)
        style.configure('TEntry', fieldbackground=bg, foreground=fg)

        self.root.configure(bg=bg)
        self.update_about_theme()
        self.update_history_style()

    def update_about_theme(self):
        bg = "#2e2e2e" if self.is_dark_theme else "#ffffff"
        fg = "#ffffff" if self.is_dark_theme else "#000000"
        self.style_about = ttk.Style()
        self.style_about.configure('About.TLabel', background=bg, foreground=fg)
        self.style_about.configure('About.TButton', background='#444444' if self.is_dark_theme else '#e0e0e0', foreground=fg)
        if hasattr(self, 'about_win') and self.about_win.winfo_exists():
            self.about_win.configure(bg=bg)
            for widget in self.about_win.winfo_children():
                if isinstance(widget, ttk.Label):
                    widget.configure(style='About.TLabel')
                elif isinstance(widget, ttk.Button):
                    widget.configure(style='About.TButton')

    def show_about(self):
        self.about_win.deiconify()

    def apply_saved_title(self):
        # Устанавливаем сохраненное название
        if hasattr(self, 'saved_title') and self.saved_title:
            self.root.title(self.saved_title)
        else:
            self.root.title(self.get_text('program_title'))

    # --------------------- Анимация и звук ---------------------
    def animate_winner_text(self, text):
        # Простая мигающая анимация текста
        def blink(count=0):
            if count >= 6:
                self.result_label.config(text=f"{self.get_text('winner')} {text}")
                return
            current = self.result_label.cget('text')
            if current == f"{self.get_text('winner')} {text}":
                self.result_label.config(text='')
            else:
                self.result_label.config(text=f"{self.get_text('winner')} {text}")
            self.root.after(300, blink, count+1)
        blink()

    def play_sound(self):
        if platform.system() == 'Windows':
            winsound.MessageBeep(winsound.MB_OK)
        else:
            # Для других ОС можно оставить пустым или использовать другие библиотеки
            pass

    def show_about(self):
        self.about_win.deiconify()

    def adjust_about_window(self):
        if hasattr(self, 'about_win') and self.about_win.winfo_exists():
            self.about_win.update_idletasks()
            self.about_win.geometry('')

if __name__ == "__main__":
    app = RandomizerApp()
