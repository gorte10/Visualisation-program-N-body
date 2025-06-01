
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.colorchooser import askcolor
import time
import matplotlib
matplotlib.use('TkAgg')  # Указываем бэкенд
from PIL import Image, ImageTk
from matplotlib.colors import LinearSegmentedColormap
import json
import pickle
import re


class TabbedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Plotting Application")
        self.log_q_var = tk.BooleanVar(value=False)
        self.current_filename = None
        self.current_colorbar = None
        self.current_time = None
        self.selected_directory = ""
        self.save_directory = ""
        self.data_loaded_initial = False
        self.data_loaded_fourier = False
        self.data_loaded_radius = False
        self.image_format = tk.StringVar(value='png')  # По умолчанию PNG
        self.x1 = None
        self.y1 = None
        self.y2 = None
        self.y3 = None
        self.y4 = None
        self.y5 = None
        self.y6 = None
        self.y7 = None
        self.y8 = None
        self.y9 = None
        self.y10 = None

        # Данные для Фурье-амплитуд
        self.x2 = None
        self.amp1 = None
        self.amp2 = None
        self.amp3 = None
        self.amp4 = None
        self.amp5 = None
        self.amp6 = None
        self.amp0 = None

        # Данные для pаспределение характеристик на определенном радиусе
        self.x3 = None
        self.r1 = None
        self.r2 = None
        self.r3 = None
        self.r4 = None
        self.r5 = None
        self.r6 = None
        self.r7 = None
        self.r8 = None
        self.r9 = None
        self.r10 = None
        self.r11 = None
        self.r12 = None
        self.r13 = None
        self.r14 = None
        self.r15 = None
        self.r16 = None
        self.r17 = None
        self.r18 = None
        self.r19 = None
        self.r20 = None
        self.r21 = None
        self.r22 = None
        self.r23 = None
        self.r24 = None
        self.r25 = None
        self.r26 = None
        self.r27 = None
        self.r28 = None
        self.r29 = None
        self.r30 = None

        self.current_colorbar = None  # Добавляем для хранения текущего колорбара

        # Загрузка пресетов из файла (если существует)
        self.presets_file = "presets.pkl"
        self.load_presets()

        # Если файла не было, создаем пресеты по умолчанию
        if not hasattr(self, 'presets_initial'):
            self.presets_initial = {
                'Default': self.create_plot_params_initial(),
                'Preset 1': {
                    'x_lim_min': 0.0,
                    'x_lim_max': 10.0,
                    'y_lim_min': 0.0,
                    'y_lim_max': 1.0,
                    # Для начального состояния
                    'thickness': {
                        'q': 2.0,
                        'c_f': 2.0,
                        'c_z': 2.0,
                        'n': 2.0,
                        'Q_c': 2.0,
                        'h': 2.0,
                        'V_c': 2.0,
                        'V_s': 2.0,
                        'c_r': 2.0,
                        'c_z/c_r': 2.0,
                    },
                    'font_size': 12,
                    'title_font_size': 14,
                    'axis_font_size': 12,
                    'legend_font_size': 10,
                    'x_label': "r",
                    'y_label': "Value",
                    'markers': {'q': '', 'c_f': '', 'c_z': '', 'n': '', 'Q_c': '', 'h': '', 'V_c': '', 'V_s': '',
                                'c_r': '',
                                'c_z/c_r': ''},
                    'colors': {'q': 'blue', 'c_f': 'green', 'c_z': 'orange', 'n': 'red', 'Q_c': 'purple', 'h': 'cyan',
                               'V_c': 'magenta', 'V_s': 'brown', 'c_r': 'black', 'c_z/c_r': 'yellow'},
                    'line_styles': {'q': '-', 'c_f': '-', 'c_z': '-', 'n': '-', 'Q_c': '-', 'h': '-', 'V_c': '-',
                                    'V_s': '-', 'c_r': '-', 'c_z/c_r': '-'}
                }
            }

        if not hasattr(self, 'presets_fourier'):
            self.presets_fourier = {
                'Default': self.create_plot_params_fourier(),
                'Preset 1': {
                    'x_lim_min': 0.0,
                    'x_lim_max': 10.0,
                    'y_lim_min': 0.0,
                    'y_lim_max': 1.0,
                    'thickness': 2.0,
                    'font_size': 12,
                    'title_font_size': 14,
                    'axis_font_size': 12,
                    'legend_font_size': 10,
                    'x_label': "t",
                    'y_label': "$A_m$",
                    'markers': {'Amp1': '', 'Amp2': '', 'Amp3': '', 'Amp4': '', 'Amp5': '', 'Amp6': '', 'Amp0': ''},
                    'colors': {'Amp1': 'blue', 'Amp2': 'green', 'Amp3': 'orange', 'Amp4': 'red', 'Amp5': 'purple',
                               'Amp6': 'cyan', 'Amp0': 'magenta'},
                    'line_styles': {'Amp1': '-', 'Amp2': '-', 'Amp3': '-', 'Amp4': '-', 'Amp5': '-', 'Amp6': '-',
                                    'Amp0': '-'}
                }
            }

        if not hasattr(self, 'presets_radius'):
            self.presets_radius = {
                'Default': self.create_plot_params_radius(),
                'Preset 1': {
                    'x_lim_min': 0.0,
                    'x_lim_max': 10.0,
                    'y_lim_min': 0.0,
                    'y_lim_max': 1.0,
                    'thickness': 2.0,
                    'font_size': 12,
                    'title_font_size': 14,
                    'axis_font_size': 12,
                    'x_label': "t",
                    'y_label': "Value",
                    'colors': {f'r{i}': plt.cm.viridis(i / 30) for i in range(1, 31)}
                }
            }

        # Создание меню
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        # Добавление пунктов меню
        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="Выбрать директорию", command=self.select_data_directory)
        file_menu.add_command(label="Выход", command=root.quit)
        self.menu.add_cascade(label="Файл", menu=file_menu)

        save_menu = tk.Menu(self.menu, tearoff=0)
        save_menu.add_command(label="Выбрать директорию для сохранения", command=self.select_save_directory)
        self.menu.add_cascade(label="Сохранить", menu=save_menu)

        # Добавление выпадающего меню для визуализации
        visualization_menu = tk.Menu(self.menu, tearoff=0)
        visualization_menu.add_command(label="Визуализация начального состояния", command=self.show_initial_values_tab)
        visualization_menu.add_command(label="Визуализация Фурье-амплитуд", command=self.show_fourier_amplitude_tab)
        visualization_menu.add_command(label="Распределение характеристик на определенном радиусе",
                                       command=self.show_radius_amplitude_tab)
        visualization_menu.add_command(label="Пакетная визуализация функции",
                                       command=self.show_batch_tab)
        self.menu.add_cascade(label="Визуализация", menu=visualization_menu)

        # Создание панели инструментов
        self.toolbar = tk.Frame(self.root, bg="lightgray")
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.directory_label = tk.Label(self.toolbar, text="Директория, откуда загружаются данные: Нет")
        self.directory_label.pack(side=tk.LEFT, padx=2, pady=2)

        self.save_directory_label = tk.Label(self.toolbar, text="Директория для сохранения графиков: Нет")
        self.save_directory_label.pack(side=tk.LEFT, padx=2, pady=2)

        # Создание вкладок
        self.tab_control = ttk.Notebook(self.root)
        self.initial_tab = ttk.Frame(self.tab_control)
        self.create_initial_graph_tab(self.initial_tab)
        self.tab_control.add(self.initial_tab, text="Визуализация начального состояния")

        self.fourier_tab = ttk.Frame(self.tab_control)
        self.create_fourier_graph_tab(self.fourier_tab)
        self.tab_control.add(self.fourier_tab, text="Визуализация Фурье-амплитуд")

        self.batch_tab = ttk.Frame(self.tab_control)
        self.create_batch_visualization_tab(self.batch_tab)
        self.tab_control.add(self.batch_tab, text="Пакетная визуализация функции")

        self.radius_tab = ttk.Frame(self.tab_control)
        self.create_radius_graph_tab(self.radius_tab)
        self.tab_control.add(self.radius_tab, text="Распределение характеристик на определенном радиусе")
        help_menu = tk.Menu(self.menu, tearoff=0)
        help_menu.add_command(label="Начальное состояние", command=self.show_help_initial)
        help_menu.add_command(label="Фурье-амплитуды", command=self.show_help_fourier)
        help_menu.add_command(label="Распределение по радиусу", command=self.show_help_radius)
        help_menu.add_command(label="Пакетная визуализация", command=self.show_help_batch)
        self.menu.add_cascade(label="Справка", menu=help_menu)
        self.tab_control.pack(fill="both", expand=True)
        self.show_initial_values_tab()

        # Кнопка для сохранения графика
        self.save_button = tk.Button(self.toolbar, text="Сохранить график", command=self.save_plot)
        self.save_button.pack(side=tk.RIGHT, padx=5, pady=5)
        # Параметры графиков по умолчанию для каждой вкладки
        self.plot_params_initial = self.create_plot_params_initial()
        self.plot_params_fourier = self.create_plot_params_fourier()
        self.plot_params_radius = self.create_plot_params_radius()

        # Устанавливаем значения по умолчанию для выбора функций
        self.function_vars_initial['q'].set(True)  # Выбираем 'q' по умолчанию для начального состояния
        self.function_vars_fourier['Amp1'].set(True)  # Выбираем 'Amp1' по умолчанию для Фурье
        self.function_vars_radius['Все радиусы'].set(True)  # Выбираем все радиусы по умолчанию

    def load_presets(self):
        """Загружает пресеты из файла, если он существует"""
        if os.path.exists(self.presets_file):
            try:
                with open(self.presets_file, 'rb') as f:
                    presets = pickle.load(f)
                    self.presets_initial = presets.get('initial', {})
                    self.presets_fourier = presets.get('fourier', {})
                    self.presets_radius = presets.get('radius', {})
            except Exception as e:
                print(f"Ошибка загрузки пресетов: {e}")
                # Создаем пустые словари, если не удалось загрузить
                self.presets_initial = {}
                self.presets_fourier = {}
                self.presets_radius = {}

    def save_presets(self):
        """Сохраняет пресеты в файл"""
        try:
            with open(self.presets_file, 'wb') as f:
                presets = {
                    'initial': self.presets_initial,
                    'fourier': self.presets_fourier,
                    'radius': self.presets_radius
                }
                pickle.dump(presets, f)
        except Exception as e:
            print(f"Ошибка сохранения пресетов: {e}")

    def show_help_initial(self):
        help_window = tk.Toplevel(self.root)
        help_window.title("Справка: Визуализация начального состояния")
        help_window.geometry("999x999")

        help_text = """
        Визуализация начального состояния

        Эта вкладка позволяет визуализировать начальные условия задачи N-тел. 
        Вы можете выбрать одну или несколько функций для отображения на графике.

        Доступные функции:
        - q: Поверхностная плотность
        - c_f: Дисперсия азимутальных скоростей
        - c_z: Дисперсия вертикальных скоростей
        - n: Количество частиц
        - Q_c: Параметр Тоомре
        - h: Толщина диска
        - V_c: Функция V_c
        - V_s: Функция V_s
        - c_r: Дисперсия радиальных скоростей
        - c_z/c_r: Отношение дисперсии вертикальных скоростей к дисперсии радиальных скоростей

        Как использовать:
        1. Сначала необходимо выбрать директорию для загрузки файла, в меню "Файл" -> "Выбрать директорию".
        2. Загрузите файл с данными, нажав кнопку "Загрузить файл".
        3. Выберите функции, которые хотите отобразить на графике, установив соответствующие флажки.
        4. Нажмите кнопку "Обновить график", чтобы построить график с выбранными функциями.
        5. Используйте кнопку "Настройки графика", чтобы настроить внешний вид графика.
        """

        help_text_widget = tk.Text(help_window, wrap=tk.WORD, padx=10, pady=10)
        help_text_widget.insert(tk.END, help_text)
        help_text_widget.config(state=tk.DISABLED)
        help_text_widget.pack(fill=tk.BOTH, expand=True)

    def show_help_fourier(self):
        help_window = tk.Toplevel(self.root)
        help_window.title("Справка: Визуализация Фурье-амплитуд")
        help_window.geometry("999x999")

        help_text = """
        Визуализация Фурье-амплитуд

        Эта вкладка позволяет визуализировать амплитуды Фурье-мод в зависимости от времени.

        Доступные моды:
        - Amp0: Нулевая мода (среднее значение)
        - Amp1: Первая Фурье-мода
        - Amp2: Вторая Фурье-мода
        - Amp3: Третья Фурье-мода
        - Amp4: Четвертая Фурье-мода
        - Amp5: Пятая Фурье-мода
        - Amp6: Шестая Фурье-мода

        Как использовать:
        1. Сначала необходимо выбрать директорию для загрузки файла, в меню "Файл" -> "Выбрать директорию".
        2. Загрузите файл с данными, нажав кнопку "Загрузить файл".
        3. Выберите моды, которые хотите отобразить на графике, установив соответствующие флажки.
        4. Нажмите кнопку "Обновить график", чтобы построить график с выбранными модами.
        5. Используйте кнопку "Настройки графика", чтобы настроить внешний вид графика.
        """

        help_text_widget = tk.Text(help_window, wrap=tk.WORD, padx=10, pady=10)
        help_text_widget.insert(tk.END, help_text)
        help_text_widget.config(state=tk.DISABLED)
        help_text_widget.pack(fill=tk.BOTH, expand=True)

    def show_help_radius(self):
        help_window = tk.Toplevel(self.root)
        help_window.title("Справка: Распределение характеристик по радиусу")
        help_window.geometry("900x700")

        help_text = """
        Распределение характеристик на определенном радиусе

        Эта вкладка позволяет визуализировать распределение характеристик на выбранных радиусах.

        Доступные радиусы: от 1 до 30

        Как использовать:
        1. Сначала необходимо выбрать директорию для загрузки файла, в меню "Файл" -> "Выбрать директорию".
        2. Загрузите файл с данными, нажав кнопку "Загрузить файл".
        3. Выберите радиусы для отображения:
           - Можно ввести конкретные радиусы через запятую (например: 1,5,10)
           - Или указать диапазон радиусов в полях "От" и "До"
           - Или выбрать "Все радиусы" для отображения всех 30 радиусов
        4. Нажмите кнопку "Обновить график", чтобы построить график.
        5. Используйте кнопку "Настройки графика", чтобы настроить внешний вид графика.
        """

        help_text_widget = tk.Text(help_window, wrap=tk.WORD, padx=10, pady=10)
        help_text_widget.insert(tk.END, help_text)
        help_text_widget.config(state=tk.DISABLED)
        help_text_widget.pack(fill=tk.BOTH, expand=True)

    def show_help_batch(self):
        help_window = tk.Toplevel(self.root)
        help_window.title("Справка: Пакетная визуализация")
        help_window.geometry("900x700")

        help_text = """
        Пакетная визуализация функции

        Эта вкладка позволяет визуализировать и сохранять данные в пакетном режиме.

        Возможности:
        - Загрузка отдельных файлов данных
        - Пакетная обработка всех файлов в выбранном временном диапазоне
        - Автоматическое сохранение графиков

        Как использовать:
        1. Выберите директорию с данными в меню "Файл" -> "Выбрать директорию".
        2. Выберите директорию для сохранения в меню "Сохранить" -> "Выбрать директорию для сохранения".
        3. Для обработки одного файла:
           - Нажмите "Загрузить файл" и выберите файл
           - Настройте параметры графика при необходимости
           - Нажмите "Сохранить график"
        4. Для пакетной обработки:
           - Укажите временной диапазон в полях "Начальное время" и "Конечное время"
           - Нажмите "Сохранить все файлы"
           - Прогресс будет отображаться в прогресс-баре
        """

        help_text_widget = tk.Text(help_window, wrap=tk.WORD, padx=10, pady=10)
        help_text_widget.insert(tk.END, help_text)
        help_text_widget.config(state=tk.DISABLED)
        help_text_widget.pack(fill=tk.BOTH, expand=True)

    def apply_preset_initial(self, event=None):
        """Применяет выбранный пресет для вкладки начального состояния"""
        selected_preset = self.preset_var_initial.get()
        if selected_preset in self.presets_initial:
            self.plot_params_initial = self.presets_initial[selected_preset].copy()
            self.update_graph_from_selection_initial()
            messagebox.showinfo("Пресет применен", f"Пресет '{selected_preset}' успешно применен")
        else:
            messagebox.showerror("Ошибка", "Выбранный пресет не найден")

    def save_preset_initial(self):
        """Сохраняет текущие параметры как новый пресет для вкладки начального состояния"""
        # Создаем окно для ввода имени пресета
        preset_name = simpledialog.askstring("Сохранение пресета", "Введите имя нового пресета:")

        if preset_name:
            # Показываем параметры, которые будут сохранены
            params_text = "Параметры, которые будут сохранены:\n\n"
            params_text += f"Толщина линии: {self.plot_params_initial['thickness']}\n"
            params_text += f"Размер шрифта: {self.plot_params_initial['font_size']}\n"
            params_text += f"Размер шрифта заголовка: {self.plot_params_initial['title_font_size']}\n"
            params_text += f"Размер шрифта осей: {self.plot_params_initial['axis_font_size']}\n"
            params_text += f"Размер шрифта легенды: {self.plot_params_initial['legend_font_size']}\n"
            params_text += f"Подпись оси X: {self.plot_params_initial['x_label']}\n"
            params_text += f"Подпись оси Y: {self.plot_params_initial['y_label']}\n\n"
            params_text += "Цвета, маркеры и стили линий для выбранных функций:\n"

            for func, var in self.function_vars_initial.items():
                if var.get():
                    params_text += f"{func}: цвет={self.plot_params_initial['colors'].get(func, 'N/A')}, "
                    params_text += f"маркер={self.plot_params_initial['markers'].get(func, 'N/A')}, "
                    params_text += f"стиль={self.plot_params_initial['line_styles'].get(func, 'N/A')}\n"

            # Показываем подтверждение с параметрами
            confirm = messagebox.askyesno(
                "Подтверждение",
                f"{params_text}\nСохранить пресет '{preset_name}'?",
                icon="question"
            )

            if confirm:
                # Сохраняем текущие параметры как новый пресет
                self.presets_initial[preset_name] = self.plot_params_initial.copy()

                # Обновляем список пресетов в выпадающем меню
                self.preset_menu_initial['values'] = list(self.presets_initial.keys())
                self.preset_var_initial.set(preset_name)

                # Сохраняем пресеты в файл
                self.save_presets()

                messagebox.showinfo("Сохранено", f"Пресет '{preset_name}' успешно сохранен")

    def apply_preset_fourier(self, event=None):
        """Применяет выбранный пресет для вкладки Фурье-амплитуд"""
        selected_preset = self.preset_var_fourier.get()
        if selected_preset in self.presets_fourier:
            self.plot_params_fourier = self.presets_fourier[selected_preset].copy()
            self.update_graph_from_selection_fourier()
            messagebox.showinfo("Пресет применен", f"Пресет '{selected_preset}' успешно применен")
        else:
            messagebox.showerror("Ошибка", "Выбранный пресет не найден")

    def save_preset_fourier(self):
        """Сохраняет текущие параметры как новый пресет для вкладки Фурье-амплитуд"""
        # Создаем окно для ввода имени пресета
        preset_name = simpledialog.askstring("Сохранение пресета", "Введите имя нового пресета:")

        if preset_name:
            # Показываем параметры, которые будут сохранены
            params_text = "Параметры, которые будут сохранены:\n\n"
            params_text += f"Толщина линии: {self.plot_params_fourier['thickness']}\n"
            params_text += f"Размер шрифта: {self.plot_params_fourier['font_size']}\n"
            params_text += f"Размер шрифта заголовка: {self.plot_params_fourier['title_font_size']}\n"
            params_text += f"Размер шрифта осей: {self.plot_params_fourier['axis_font_size']}\n"
            params_text += f"Размер шрифта легенды: {self.plot_params_fourier['legend_font_size']}\n"
            params_text += f"Подпись оси X: {self.plot_params_fourier['x_label']}\n"
            params_text += f"Подпись оси Y: {self.plot_params_fourier['y_label']}\n\n"
            params_text += "Цвета, маркеры и стили линий для выбранных функций:\n"

            for func, var in self.function_vars_fourier.items():
                if var.get():
                    params_text += f"{func}: цвет={self.plot_params_fourier['colors'].get(func, 'N/A')}, "
                    params_text += f"маркер={self.plot_params_fourier['markers'].get(func, 'N/A')}, "
                    params_text += f"стиль={self.plot_params_fourier['line_styles'].get(func, 'N/A')}\n"

            # Показываем подтверждение с параметрами
            confirm = messagebox.askyesno(
                "Подтверждение",
                f"{params_text}\nСохранить пресет '{preset_name}'?",
                icon="question"
            )

            if confirm:
                # Сохраняем текущие параметры как новый пресет
                self.presets_fourier[preset_name] = self.plot_params_fourier.copy()

                # Обновляем список пресетов в выпадающем меню
                self.preset_menu_fourier['values'] = list(self.presets_fourier.keys())
                self.preset_var_fourier.set(preset_name)

                # Сохраняем пресеты в файл
                self.save_presets()

                messagebox.showinfo("Сохранено", f"Пресет '{preset_name}' успешно сохранен")

    def apply_preset_radius(self, event=None):
        """Применяет выбранный пресет для вкладки распределения по радиусу"""
        selected_preset = self.preset_var_radius.get()
        if selected_preset in self.presets_radius:
            self.plot_params_radius = self.presets_radius[selected_preset].copy()
            self.update_graph_from_selection_radius()
            messagebox.showinfo("Пресет применен", f"Пресет '{selected_preset}' успешно применен")
        else:
            messagebox.showerror("Ошибка", "Выбранный пресет не найден")

    def save_preset_radius(self):
        """Сохраняет текущие параметры как новый пресет для вкладки распределения по радиусу"""
        # Создаем окно для ввода имени пресета
        preset_name = simpledialog.askstring("Сохранение пресета", "Введите имя нового пресета:")

        if preset_name:
            # Показываем параметры, которые будут сохранены
            params_text = "Параметры, которые будут сохранены:\n\n"
            params_text += f"Толщина линии: {self.plot_params_radius['thickness']}\n"
            params_text += f"Размер шрифта: {self.plot_params_radius['font_size']}\n"
            params_text += f"Размер шрифта заголовка: {self.plot_params_radius['title_font_size']}\n"
            params_text += f"Размер шрифта осей: {self.plot_params_radius['axis_font_size']}\n"
            params_text += f"Подпись оси X: {self.plot_params_radius['x_label']}\n"
            params_text += f"Подпись оси Y: {self.plot_params_radius['y_label']}\n\n"
            params_text += "Цвета для радиусов:\n"

            # Показываем только первые 5 цветов для примера
            for i in range(1, 6):
                if f'r{i}' in self.plot_params_radius['colors']:
                    params_text += f"r{i}: {self.plot_params_radius['colors'][f'r{i}']}\n"
            if len(self.plot_params_radius['colors']) > 5:
                params_text += f"... и еще {len(self.plot_params_radius['colors']) - 5} радиусов\n"

            # Показываем подтверждение с параметрами
            confirm = messagebox.askyesno(
                "Подтверждение",
                f"{params_text}\nСохранить пресет '{preset_name}'?",
                icon="question"
            )

            if confirm:
                # Сохраняем текущие параметры как новый пресет
                self.presets_radius[preset_name] = self.plot_params_radius.copy()

                # Обновляем список пресетов в выпадающем меню
                self.preset_menu_radius['values'] = list(self.presets_radius.keys())
                self.preset_var_radius.set(preset_name)

                # Сохраняем пресеты в файл
                self.save_presets()

                messagebox.showinfo("Сохранено", f"Пресет '{preset_name}' успешно сохранен")

    def create_plot_params_initial(self):
        return {
            'x_lim_min': 0.0,
            'x_lim_max': None,
            'y_lim_min': 0.0,
            'y_lim_max': None,
            'thickness': 3.0,
            'font_size': 15,
            'title_font_size': 15,  # Размер шрифта заголовка
            'axis_font_size': 12,  # Размер шрифта осей
            'legend_font_size': 10,  # Размер шрифта легенды
            'x_label': "r",
            'y_label': "",
            'markers': {
                'q': '',
                'c_f': '',
                'c_z': '',
                'n': '',
                'Q_c': '',
                'h': '',
                'V_c': '',
                'V_s': '',
                'c_r': '',
                'c_z/c_r': '',
            },
            'colors': {
                'q': 'blue',
                'c_f': 'green',
                'c_z': 'orange',
                'n': 'red',
                'Q_c': 'purple',
                'h': 'cyan',
                'V_c': 'magenta',
                'V_s': 'brown',
                'c_r': 'black',
                'c_z/c_r': 'yellow',
            },
            'line_styles': {  # Добавляем стили линий
                'q': '-',
                'c_f': '-',
                'c_z': '-',
                'n': '-',
                'Q_c': '-',
                'h': '-',
                'V_c': '-',
                'V_s': '-',
                'c_r': '-',
                'c_z/c_r': '-',
            },
        }

    def create_plot_params_fourier(self):
        return {
            'x_lim_min': 0.0,
            'x_lim_max': None,
            'y_lim_min': 0.0,
            'y_lim_max': None,
            'thickness': 3.0,
            'font_size': 15,  # Общий размер шрифта (можно удалить, если не используется)
            'title_font_size': 15,  # Размер шрифта заголовка
            'axis_font_size': 12,  # Размер шрифта осей
            'legend_font_size': 10,  # Размер шрифта легенды
            'x_label': "t",
            'y_label': "",
            'markers': {
                'Amp1': '',
                'Amp2': '',
                'Amp3': '',
                'Amp4': '',
                'Amp5': '',
                'Amp6': '',
                'Amp0': '',
            },
            'colors': {
                'Amp1': 'blue',
                'Amp2': 'green',
                'Amp3': 'orange',
                'Amp4': 'red',
                'Amp5': 'purple',
                'Amp6': 'cyan',
                'Amp0': 'magenta',
            },
            'line_styles': {  # Добавляем стили линий
                'Amp1': '-',
                'Amp2': '-',
                'Amp3': '-',
                'Amp4': '-',
                'Amp5': '-',
                'Amp6': '-',
                'Amp0': '-',
            },
        }

    def create_plot_params_radius(self):
        return {
            'x_lim_min': 0.0,
            'x_lim_max': None,
            'y_lim_min': 0.0,
            'y_lim_max': None,
            'thickness': 3.0,
            'font_size': 15,  # Общий размер шрифта (можно удалить, если не используется)
            'title_font_size': 15,  # Размер шрифта заголовка
            'axis_font_size': 12,  # Размер шрифта осей
            'x_label': "t",
            'y_label': "",
            'colors': {
                'r1': 'black',
                'r2': 'gray',
                'r3': 'firebrick',
                'r4': 'red',
                'r5': 'darksalmon',
                'r6': 'sienna',
                'r7': 'sandybrown',
                'r8': 'gold',
                'r9': 'darkgreen',
                'r10': 'm',
                'r11': 'blue',
                'r12': 'navy',
                'r13': 'c',
                'r14': 'crimson',
                'r15': 'slateblue',
                'r16': 'yellowgreen',
                'r17': 'green',
                'r18': 'r',
                'r19': 'darkmagenta',
                'r20': 'tomato',
                'r21': 'brown',
                'r22': 'orange',
                'r23': 'y',
                'r24': 'aquamarine',
                'r25': 'maroon',
                'r26': 'lime',
                'r27': 'limegreen',
                'r28': 'k',
                'r29': 'b',
                'r30': 'darkred',
            },
        }

    def create_batch_visualization_tab(self, tab):
        # Создаем основной фрейм для разделения на левую и правую части
        main_frame = tk.Frame(tab)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Левый фрейм для настроек и кнопок
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Правый фрейм для графика
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Кнопка для загрузки файла
        load_button = tk.Button(left_frame, text="Загрузить файл", command=self.load_batch_data)
        load_button.pack(pady=10)

        # Поля для ввода диапазона времени
        ttk.Label(left_frame, text="Начальное время:").pack(pady=(10, 0))
        self.start_time_input = tk.Entry(left_frame)
        self.start_time_input.pack(pady=(0, 10))

        ttk.Label(left_frame, text="Конечное время:").pack(pady=(10, 0))
        self.end_time_input = tk.Entry(left_frame)
        self.end_time_input.pack(pady=(0, 10))

        # Метка для отображения расчетного времени текущего файла
        self.current_time_label = tk.Label(left_frame, text="Текущее расчетное время: Нет данных")
        self.current_time_label.pack(pady=(10, 0))

        # Метка для отображения функции
        self.function_label = tk.Label(left_frame, text="Функция: Нет данных")
        self.function_label.pack(pady=(10, 0))

        # Прогресс-бар
        self.progress_bar = ttk.Progressbar(left_frame, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack(pady=(10, 0))

        # Метка для отображения оставшегося времени
        self.remaining_time_label = tk.Label(left_frame, text="Оставшееся время: Нет данных")
        self.remaining_time_label.pack(pady=(10, 0))

        # Кнопка для настройки графика
        self.settings_button_batch = tk.Button(left_frame, text="Настройки графика", command=self.configure_batch_plot)
        self.settings_button_batch.pack(side=tk.BOTTOM, pady=(0, 10))

        # Кнопка для пакетного сохранения
        self.save_all_button = tk.Button(left_frame, text="Сохранить все файлы", command=self.save_all_batch_files)
        self.save_all_button.pack(side=tk.BOTTOM, pady=(0, 10))

        # Создаем график в правой части
        self.batch_fig = plt.Figure(figsize=(8, 8), dpi=200)
        self.batch_ax = self.batch_fig.add_subplot(111)
        self.batch_canvas = FigureCanvasTkAgg(self.batch_fig, right_frame)
        self.batch_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Переменные для хранения данных
        self.batch_x = None
        self.batch_y = None
        self.batch_z = None
        self.batch_plot_params = {
            'x_lim_min': -1,
            'x_lim_max': 1,
            'y_lim_min': -1,
            'y_lim_max': 1,
            'font_size': 10,
            'x_label': "",
            'y_label': "",
            'colorbar': 'gnuplot2',
            'contour_levels': 35,  # Добавляем параметр для количества изолиний
        }


    def create_initial_graph_tab(self, tab):
        functions_frame = ttk.LabelFrame(tab, text="Выбрать функции")
        functions_frame.pack(side=tk.LEFT, padx=10, pady=10, fill="y")

        self.function_vars_initial = {
            'q': tk.BooleanVar(),
            'c_f': tk.BooleanVar(),
            'c_z': tk.BooleanVar(),
            'n': tk.BooleanVar(),
            'Q_c': tk.BooleanVar(),
            'h': tk.BooleanVar(),
            'V_c': tk.BooleanVar(),
            'V_s': tk.BooleanVar(),
            'c_r': tk.BooleanVar(),
            'c_z/c_r': tk.BooleanVar()
        }

        for func, var in self.function_vars_initial.items():
            chk = tk.Checkbutton(functions_frame, text=func, variable=var)
            chk.pack(anchor="w")

        self.update_button_initial = tk.Button(functions_frame, text="Обновить график",
                                               command=self.update_graph_from_selection_initial)
        self.update_button_initial.pack(pady=(10, 0))

        # Перенесли пресеты под кнопку "Обновить график"
        self.preset_var_initial = tk.StringVar(value='Default')
        self.preset_menu_initial = ttk.Combobox(functions_frame, textvariable=self.preset_var_initial,
                                                values=list(self.presets_initial.keys()))
        self.preset_menu_initial.pack(pady=(5, 5))
        self.preset_menu_initial.bind('<<ComboboxSelected>>', self.apply_preset_initial)

        self.save_preset_button_initial = tk.Button(functions_frame, text="Сохранить пресет",
                                                    command=self.save_preset_initial)
        self.save_preset_button_initial.pack(pady=(5, 10))

        load_button = tk.Button(tab, text="Загрузить файл", command=self.load_data_initial)
        load_button.pack(pady=10)
        self.initial_fig = plt.Figure(figsize=(6, 4), dpi=100)
        self.initial_ax = self.initial_fig.add_subplot(111)
        self.initial_canvas = FigureCanvasTkAgg(self.initial_fig, tab)
        self.initial_canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.settings_button_initial = tk.Button(functions_frame, text="Настройки графика",
                                                 command=self.configure_plot_initial)
        self.settings_button_initial.pack(side=tk.BOTTOM, pady=(0, 10))


    def create_fourier_graph_tab(self, tab):
        functions_frame = ttk.LabelFrame(tab, text="Выбрать функции")
        functions_frame.pack(side=tk.LEFT, padx=10, pady=10, fill="y")

        self.function_vars_fourier = {
            'Amp1': tk.BooleanVar(),
            'Amp2': tk.BooleanVar(),
            'Amp3': tk.BooleanVar(),
            'Amp4': tk.BooleanVar(),
            'Amp5': tk.BooleanVar(),
            'Amp6': tk.BooleanVar(),
            'Amp0': tk.BooleanVar()
        }

        function_labels = {
            'Amp1': '1 фурье-мода',
            'Amp2': '2 фурье-мода',
            'Amp3': '3 фурье-мода',
            'Amp4': '4 фурье-мода',
            'Amp5': '5 фурье-мода',
            'Amp6': '6 фурье-мода',
            'Amp0': '0 фурье-мода'
        }

        for func, var in self.function_vars_fourier.items():
            chk = tk.Checkbutton(functions_frame, text=function_labels[func], variable=var)
            chk.pack(anchor="w")

        self.update_button_fourier = tk.Button(functions_frame, text="Обновить график",
                                               command=self.update_graph_from_selection_fourier)
        self.update_button_fourier.pack(pady=(10, 0))

        # Перенесли пресеты под кнопку "Обновить график"
        self.preset_var_fourier = tk.StringVar(value='Default')
        self.preset_menu_fourier = ttk.Combobox(functions_frame, textvariable=self.preset_var_fourier,
                                                values=list(self.presets_fourier.keys()))
        self.preset_menu_fourier.pack(pady=(5, 5))
        self.preset_menu_fourier.bind('<<ComboboxSelected>>', self.apply_preset_fourier)

        self.save_preset_button_fourier = tk.Button(functions_frame, text="Сохранить пресет",
                                                    command=self.save_preset_fourier)
        self.save_preset_button_fourier.pack(pady=(5, 10))

        load_button = tk.Button(tab, text="Загрузить файл", command=self.load_data_fourier)
        load_button.pack(pady=10)

        self.fourier_fig = plt.Figure(figsize=(6, 4), dpi=100)
        self.fourier_ax = self.fourier_fig.add_subplot(111)
        self.fourier_canvas = FigureCanvasTkAgg(self.fourier_fig, tab)
        self.fourier_canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.settings_button_fourier = tk.Button(functions_frame, text="Настройки графика",
                                                 command=self.configure_plot_fourier)
        self.settings_button_fourier.pack(side=tk.BOTTOM, pady=(0, 10))


    def create_radius_graph_tab(self, tab):
        functions_frame = ttk.LabelFrame(tab, text="Выбрать функции")
        functions_frame.pack(side=tk.LEFT, padx=10, pady=10, fill="y")

        self.function_vars_radius = {
            'Все радиусы': tk.BooleanVar(),
        }

        for func, var in self.function_vars_radius.items():
            chk = tk.Checkbutton(functions_frame, text=func, variable=var)
            chk.pack(anchor="w")

        # Поле для ввода радиусов
        ttk.Label(functions_frame, text="Выберите радиусы (например, 1, 2, 3, 30):").pack(pady=(10, 0))
        self.radius_input = tk.Entry(functions_frame)
        self.radius_input.pack(pady=(0, 10))

        # Поля для ввода диапазона радиусов
        ttk.Label(functions_frame, text="Диапазон  (от 1 до 30):").pack(pady=(10, 0))
        ttk.Label(functions_frame, text="От").pack(pady=(0, 5))
        self.radius_min_input = tk.Entry(functions_frame)
        self.radius_min_input.pack(pady=(0, 5))

        ttk.Label(functions_frame, text="До").pack(pady=(0, 5))
        self.radius_max_input = tk.Entry(functions_frame)
        self.radius_max_input.pack(pady=(0, 10))

        self.update_button_radius = tk.Button(functions_frame, text="Обновить график",
                                              command=self.update_graph_from_selection_radius)
        self.update_button_radius.pack(pady=(10, 0))

        # Перенесли пресеты под кнопку "Обновить график"
        self.preset_var_radius = tk.StringVar(value='Default')
        self.preset_menu_radius = ttk.Combobox(functions_frame, textvariable=self.preset_var_radius,
                                               values=list(self.presets_radius.keys()))
        self.preset_menu_radius.pack(pady=(5, 5))
        self.preset_menu_radius.bind('<<ComboboxSelected>>', self.apply_preset_radius)

        self.save_preset_button_radius = tk.Button(functions_frame, text="Сохранить пресет",
                                                   command=self.save_preset_radius)
        self.save_preset_button_radius.pack(pady=(5, 10))

        load_button = tk.Button(tab, text="Загрузить файл", command=self.load_data_radius)
        load_button.pack(pady=10)

        self.radius_fig = plt.Figure(figsize=(6, 4), dpi=100)
        self.radius_ax = self.radius_fig.add_subplot(111)
        self.radius_canvas = FigureCanvasTkAgg(self.radius_fig, tab)
        self.radius_canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.settings_button_radius = tk.Button(functions_frame, text="Настройки графика",
                                                command=self.configure_plot_radius)
        self.settings_button_radius.pack(side=tk.BOTTOM, pady=(0, 10))

    def extract_time_from_filename(self, filename):
        try:
            base = os.path.splitext(filename)[0]

            if base.startswith("dq"):
                remaining = base[2:]
            elif base.startswith("q_"):
                remaining = base[2:]
            else:
                return None

            # Разделение числовой части на компоненты
            parts = re.split(r'[_ ]+', remaining.strip())

            if not parts:
                return 0.0

            # Извлечение целой и дробной частей
            if len(parts) >= 2:
                integer_str, fractional_str = parts[0], parts[1]
            else:
                integer_str = '0'
                fractional_str = parts[0]

            integer_str = integer_str or '0'
            fractional_str = fractional_str or '0'

            # Форматирование дробной части до трех цифр
            fractional_padded = fractional_str.zfill(3)[:3]

            integer = int(integer_str)
            fractional = int(fractional_padded)

            total = integer * 1000 + fractional
            return total / 1000

        except Exception as e:
            print(f"Ошибка при извлечении времени из файла {filename}: {e}")
            return None

    def show_initial_values_tab(self):
        self.tab_control.pack(fill="both", expand=True)
        self.tab_control.select(self.initial_tab)
        self.fourier_tab.pack_forget()  # Скрыть вкладку Фурье
        self.radius_tab.pack_forget()
        self.batch_tab.pack_forget()

    def show_fourier_amplitude_tab(self):
        self.tab_control.pack(fill="both", expand=True)
        self.tab_control.select(self.fourier_tab)
        self.initial_tab.pack_forget()  # Скрыть вкладку начального состояния
        self.radius_tab.pack_forget()
        self.batch_tab.pack_forget()

    def show_radius_amplitude_tab(self):
        self.tab_control.pack(fill="both", expand=True)
        self.tab_control.select(self.radius_tab)
        self.initial_tab.pack_forget()  # Скрыть вкладку начального состояния
        self.fourier_tab.pack_forget()
        self.batch_tab.pack_forget()

    def show_batch_tab(self):
        self.tab_control.pack(fill="both", expand=True)
        self.tab_control.select(self.batch_tab)
        self.initial_tab.pack_forget()  # Скрыть вкладку начального состояния
        self.fourier_tab.pack_forget()
        self.radius_tab.pack_forget()

    def load_data(self, data_type):
        if not self.selected_directory:
            messagebox.showwarning("Warning", "Сначала выберите директорию.")
            return

        filename = filedialog.askopenfilename(
            initialdir=self.selected_directory,
            title="Select Data File",
            filetypes=(("Data files", "*.dat"), ("All files", "*.*"))
        )

        if filename:
            try:
                with open(filename, 'r') as file:
                    lines = file.readlines()[1:]  # Удаляем первую строку
                data = np.loadtxt(lines)
                if data_type == 'initial':
                    self.x1 = data[:, 0]
                    self.y1 = data[:, 1]  # q
                    self.y2 = data[:, 2]  # n
                    self.y3 = data[:, 3]  # V_c
                    self.y4 = data[:, 4]  # V_s
                    self.y5 = data[:, 5]  # c_r
                    self.y6 = data[:, 6]  # c_f
                    self.y7 = data[:, 7]  # c_z
                    self.y8 = data[:, 8]  # h
                    self.y9 = data[:, 9]  # cz/cr
                    self.y10 = data[:, 10]  # Qc
                    self.data_loaded_initial = True
                    self.update_graph_from_selection_initial()

                elif data_type == 'fourier':
                    self.x2 = data[:, 0]
                    self.amp1 = data[:, 2]
                    self.amp2 = data[:, 3]
                    self.amp3 = data[:, 4]
                    self.amp4 = data[:, 5]
                    self.amp5 = data[:, 6]
                    self.amp6 = data[:, 7]
                    self.amp0 = data[:, 1]
                    self.data_loaded_fourier = True
                    self.update_graph_from_selection_fourier()

                elif data_type == 'radius':
                    # Извлекаем характеристику из названия файла
                    base_name = filename.split("/")[-1]  # Получаем только имя файла
                    characteristic = base_name.split("_")[-1].split(".")[0]  # Получаем часть между "_cz(rt)" и ".dat"
                    if characteristic == 'cz(rt)':
                        self.characteristic_display = r'$c_{z}(rt)$'
                        self.plot_params_radius['y_lim_max'] = 0.5
                    elif characteristic == 'cf(rt)':
                        self.characteristic_display = r'$c_{\varphi}(rt)$'
                        self.plot_params_radius['y_lim_max'] = 1.0
                    elif characteristic == 'cr(rt)':
                        self.characteristic_display = r'$c_{r}(rt)$'
                        # Устанавливаем ymax = 1 для функции cr(rt)
                        self.plot_params_radius['y_lim_max'] = 1.0
                    elif characteristic == 'h(rt)':
                        self.characteristic_display = r'$h(rt)$'
                        self.plot_params_radius['y_lim_max'] = 0.07
                    else:
                        self.characteristic_display = characteristic

                        # Загружаем данные
                    data = np.loadtxt(filename)
                    self.x3 = data[:, 0]

                    # Обрабатываем каждый столбец данных (каждый радиус)
                    for i in range(1, 31):
                        column_data = data[:, i]

                        # Если это cr(rt), обрабатываем аномальные значения
                        if characteristic == 'cr(rt)':
                            # Находим индексы аномальных значений (например, больше 10)
                            anomaly_indices = np.where(column_data > 10)[0]

                            # Заменяем аномальные значения на среднее соседних
                            for idx in anomaly_indices:
                                if idx > 0 and idx < len(column_data) - 1:
                                    column_data[idx] = (column_data[idx - 1] + column_data[idx + 1]) / 2
                                elif idx == 0:
                                    column_data[idx] = column_data[idx + 1]
                                else:
                                    column_data[idx] = column_data[idx - 1]

                        # Сохраняем обработанные данные
                        setattr(self, f'r{i}', column_data)
                    self.x3 = data[:, 0]
                    self.r1 = data[:, 1]
                    self.r2 = data[:, 2]
                    self.r3 = data[:, 3]
                    self.r4 = data[:, 4]
                    self.r5 = data[:, 5]
                    self.r6 = data[:, 6]
                    self.r7 = data[:, 7]
                    self.r8 = data[:, 8]
                    self.r9 = data[:, 9]
                    self.r10 = data[:, 10]
                    self.r11 = data[:, 11]
                    self.r12 = data[:, 12]
                    self.r13 = data[:, 13]
                    self.r14 = data[:, 14]
                    self.r15 = data[:, 15]
                    self.r16 = data[:, 16]
                    self.r17 = data[:, 17]
                    self.r18 = data[:, 18]
                    self.r19 = data[:, 19]
                    self.r20 = data[:, 20]
                    self.r21 = data[:, 21]
                    self.r22 = data[:, 22]
                    self.r23 = data[:, 23]
                    self.r24 = data[:, 24]
                    self.r25 = data[:, 25]
                    self.r26 = data[:, 26]
                    self.r27 = data[:, 27]
                    self.r28 = data[:, 28]
                    self.r29 = data[:, 29]
                    self.r30 = data[:, 30]
                    self.data_loaded_radius = True
                    self.update_graph_from_selection_radius()

            except Exception as e:
                messagebox.showerror("Error", f"Could not load data: {e}")

    def load_data_initial(self):
        self.load_data('initial')
        # Если ни одна функция не выбрана, выбираем первую
        if not any(var.get() for var in self.function_vars_initial.values()):
            self.function_vars_initial['q'].set(True)
        self.update_graph_from_selection_initial()

    def load_data_fourier(self):
        self.load_data('fourier')
        # Если ни одна функция не выбрана, выбираем первую
        if not any(var.get() for var in self.function_vars_fourier.values()):
            self.function_vars_fourier['Amp1'].set(True)
        self.update_graph_from_selection_fourier()

    def load_data_radius(self):
        self.load_data('radius')
        # Если ни одна функция не выбрана, выбираем все радиусы
        if not any(var.get() for var in self.function_vars_radius.values()):
            self.function_vars_radius['Все радиусы'].set(True)
        self.update_graph_from_selection_radius()

    def load_batch_data(self):
        filename = filedialog.askopenfilename(
            initialdir=self.selected_directory,
            title="Select Data File",
            filetypes=(("Data files", "*.dat"), ("All files", "*.*"))
        )

        if filename:
            try:
                data = np.loadtxt(filename)
                self.batch_x = data[:, 0]
                self.batch_y = data[:, 1]
                self.batch_z = data[:, 2]

                # Сохраняем имя файла
                self.current_filename = os.path.basename(filename)

                # Извлекаем время из названия файла
                current_time = self.extract_time_from_filename(self.current_filename)
                self.current_time = current_time

                # Обновляем метку с расчетным временем
                if current_time is not None:
                    self.current_time_label.config(text=f"Текущее расчетное время: {current_time:.3f}")
                else:
                    self.current_time_label.config(text="Текущее расчетное время: Нет данных")

                # Определяем функцию по имени файла
                if self.current_filename.startswith('q'):
                    function_name = "q"
                elif self.current_filename.startswith('dq'):
                    function_name = "dq"
                else:
                    function_name = "Неизвестная функция"

                # Обновляем метку с функцией
                self.function_label.config(text=f"Функция: {function_name}")

                # Проверяем данные на наличие NaN или inf
                if np.any(~np.isfinite(self.batch_z)):
                    messagebox.showwarning("Warning",
                                           "Данные содержат нечисловые значения (NaN или inf). Они будут заменены на 0.")
                    self.batch_z[~np.isfinite(self.batch_z)] = 0  # Заменяем NaN и inf на 0

                # Если файл начинается на 'q', предлагаем выбрать, строить ли логарифм
                if self.current_filename.startswith('q'):
                    # Диалоговое окно с выбором
                    build_log = messagebox.askyesno(
                        "Выбор построения",
                        "Файл начинается на 'q'. Построить логарифм для функции q?",
                        icon="question"
                    )

                    if build_log:  # Если пользователь выбрал "Да"
                        # Проверяем, есть ли неположительные значения в данных
                        if np.any(self.batch_z <= 0):
                            # Заменяем неположительные значения на очень маленькое положительное число
                            self.batch_z[self.batch_z <= 0] = 1e-10  # Например, 1e-10
                            messagebox.showwarning("Warning",
                                                   "Данные содержат неположительные значения. Они заменены на 1e-10 для построения логарифма.")

                        # Применяем логарифм
                        self.batch_z = np.log10(self.batch_z)

                        # Проверяем, есть ли NaN или inf в данных после применения логарифма
                        if np.any(~np.isfinite(self.batch_z)):
                            messagebox.showwarning("Warning",
                                                   "После применения логарифма данные содержат нечисловые значения (NaN или inf). Они будут заменены на 0.")
                            self.batch_z[~np.isfinite(self.batch_z)] = 0  # Заменяем NaN и inf на 0

                self.update_batch_plot()

            except Exception as e:
                messagebox.showerror("Error", f"Could not load data: {e}")

    def update_batch_plot(self):
        if self.batch_x is None or self.batch_y is None or self.batch_z is None:
            return

        self.batch_ax.clear()

        # Применяем логарифм, если выбран флажок и файл начинается на 'q'
        if self.log_q_var.get() and self.current_filename and self.current_filename.startswith('q'):
            z_data = np.log10(self.batch_z)
        else:
            z_data = self.batch_z

        contour = self.batch_ax.tricontourf(
            self.batch_x, self.batch_y, z_data,
            self.batch_plot_params['contour_levels'],
            cmap=self.batch_plot_params['colorbar'],
            vmin=self.batch_plot_params.get('colorbar_min'),
            vmax=self.batch_plot_params.get('colorbar_max')
        )
        self.batch_ax.set_aspect('equal')

        # Удаляем старый colorbar, если он существует
        if hasattr(self, 'current_colorbar') and self.current_colorbar is not None:
            self.current_colorbar.remove()
            self.current_colorbar = None  # Сбрасываем ссылку

        # Создаем новый colorbar
        self.current_colorbar = self.batch_fig.colorbar(contour, ax=self.batch_ax)

        # Устанавливаем размер шрифта для колорбара
        self.current_colorbar.ax.tick_params(labelsize=self.batch_plot_params.get('colorbar_font_size', 10))

        # Добавляем заголовок с временем
        if self.current_time is not None:
            self.batch_ax.set_title(f"t = {self.current_time:.3f}",
                                    fontsize=self.batch_plot_params.get('title_font_size', 10))

        # Устанавливаем подписи осей и их размер шрифта
        self.batch_ax.set_xlabel(self.batch_plot_params['x_label'],
                                 fontsize=self.batch_plot_params.get('axis_font_size', 10))
        self.batch_ax.set_ylabel(self.batch_plot_params['y_label'],
                                 fontsize=self.batch_plot_params.get('axis_font_size', 10))

        # Устанавливаем ограничения осей
        if self.batch_plot_params['x_lim_max'] is not None:
            self.batch_ax.set_xlim(self.batch_plot_params['x_lim_min'], self.batch_plot_params['x_lim_max'])
        else:
            self.batch_ax.set_xlim(left=self.batch_plot_params['x_lim_min'])

        if self.batch_plot_params['y_lim_max'] is not None:
            self.batch_ax.set_ylim(self.batch_plot_params['y_lim_min'], self.batch_plot_params['y_lim_max'])
        else:
            self.batch_ax.set_ylim(bottom=self.batch_plot_params['y_lim_min'])

        # Устанавливаем одинаковое количество делений по осям x и y
        self.batch_ax.locator_params(axis='x', nbins=5)  # Устанавливаем количество делений по оси x
        self.batch_ax.locator_params(axis='y', nbins=5)  # Устанавливаем количество делений по оси y

        # Устанавливаем размер шрифта для осей
        self.batch_ax.tick_params(axis='both', labelsize=self.batch_plot_params.get('axis_font_size', 10))

        self.batch_canvas.draw()

    def update_graph_from_selection_initial(self):
        if not self.data_loaded_initial:
            messagebox.showwarning("Warning", "Пожалуйста, загрузите данные перед обновлением графика.")
            return

        self.initial_ax.clear()
        if not any(var.get() for var in self.function_vars_initial.values()):
            self.function_vars_initial['q'].set(True)  # Выбираем 'q' по умолчанию
            messagebox.showinfo("Info", "Автоматически выбрана функция 'q' для отображения")
        thickness = self.plot_params_initial['thickness']
        title_font_size = self.plot_params_initial['title_font_size']
        axis_font_size = self.plot_params_initial['axis_font_size']
        legend_font_size = self.plot_params_initial['legend_font_size']

        selected_functions = []

        if self.function_vars_initial['q'].get():
            color = self.plot_params_initial['colors']['q']
            marker = self.plot_params_initial['markers']['q']
            line_style = self.plot_params_initial['line_styles']['q']
            self.initial_ax.plot(self.x1, self.y1, label='q', color=color, linewidth=thickness,
                                 marker=marker, markersize=thickness * 2, linestyle=line_style)
            selected_functions.append('q')

        if self.function_vars_initial['c_f'].get():
            color = self.plot_params_initial['colors']['c_f']
            marker = self.plot_params_initial['markers']['c_f']
            line_style = self.plot_params_initial['line_styles']['c_f']
            self.initial_ax.plot(self.x1, self.y6, label='$c_f$', color=color, linewidth=thickness,
                                 marker=marker, markersize=thickness * 2, linestyle=line_style)
            selected_functions.append('$c_f$')

        if self.function_vars_initial['c_z'].get():
            color = self.plot_params_initial['colors']['c_z']
            marker = self.plot_params_initial['markers']['c_z']
            line_style = self.plot_params_initial['line_styles']['c_z']
            self.initial_ax.plot(self.x1, self.y7, label='$c_z$', color=color, linewidth=thickness,
                                 marker=marker, markersize=thickness * 2, linestyle=line_style)
            selected_functions.append('$c_z$')

        if self.function_vars_initial['n'].get():
            color = self.plot_params_initial['colors']['n']
            marker = self.plot_params_initial['markers']['n']
            line_style = self.plot_params_initial['line_styles']['n']
            self.initial_ax.plot(self.x1, self.y2, label='n', color=color, linewidth=thickness,
                                 marker=marker, markersize=thickness * 2, linestyle=line_style)
            selected_functions.append('n')

        if self.function_vars_initial['Q_c'].get():
            color = self.plot_params_initial['colors']['Q_c']
            marker = self.plot_params_initial['markers']['Q_c']
            line_style = self.plot_params_initial['line_styles']['Q_c']
            self.initial_ax.plot(self.x1, self.y10, label='$Q_c$', color=color, linewidth=thickness,
                                 marker=marker, markersize=thickness * 2, linestyle=line_style)
            selected_functions.append('$Q_c$')

        if self.function_vars_initial['h'].get():
            color = self.plot_params_initial['colors']['h']
            marker = self.plot_params_initial['markers']['h']
            line_style = self.plot_params_initial['line_styles']['h']
            self.initial_ax.plot(self.x1, self.y8, label='$h$', color=color, linewidth=thickness,
                                 marker=marker, markersize=thickness * 2, linestyle=line_style)
            selected_functions.append('$h$')

        if self.function_vars_initial['V_c'].get():
            color = self.plot_params_initial['colors']['V_c']
            marker = self.plot_params_initial['markers']['V_c']
            line_style = self.plot_params_initial['line_styles']['V_c']
            self.initial_ax.plot(self.x1, self.y3, label='$V_c$', color=color, linewidth=thickness,
                                 marker=marker, markersize=thickness * 2, linestyle=line_style)
            selected_functions.append('$V_c$')

        if self.function_vars_initial['V_s'].get():
            color = self.plot_params_initial['colors']['V_s']
            marker = self.plot_params_initial['markers']['V_s']
            line_style = self.plot_params_initial['line_styles']['V_s']
            self.initial_ax.plot(self.x1, self.y4, label='$V_s$', color=color, linewidth=thickness,
                                 marker=marker, markersize=thickness * 2, linestyle=line_style)
            selected_functions.append('$V_s$')

        if self.function_vars_initial['c_r'].get():
            color = self.plot_params_initial['colors']['c_r']
            marker = self.plot_params_initial['markers']['c_r']
            line_style = self.plot_params_initial['line_styles']['c_r']
            self.initial_ax.plot(self.x1, self.y5, label='$c_r$', color=color, linewidth=thickness,
                                 marker=marker, markersize=thickness * 2, linestyle=line_style)
            selected_functions.append('$c_r$')

        if self.function_vars_initial['c_z/c_r'].get():
            color = self.plot_params_initial['colors']['c_z/c_r']
            marker = self.plot_params_initial['markers']['c_z/c_r']
            line_style = self.plot_params_initial['line_styles']['c_z/c_r']
            self.initial_ax.plot(self.x1, self.y9, label='$c_z/c_r$', color=color, linewidth=thickness,
                                 marker=marker, markersize=thickness * 2, linestyle=line_style)
            selected_functions.append('$c_z/c_r$')

        title = f"Начальные условия: {', '.join(selected_functions)}" if selected_functions else "Начальные условия"
        self.initial_ax.set_title(title, fontsize=title_font_size)

        self.initial_ax.set_xlabel(self.plot_params_initial['x_label'], fontsize=axis_font_size)
        self.initial_ax.set_ylabel(self.plot_params_initial['y_label'], fontsize=axis_font_size)

        if self.plot_params_initial['x_lim_max'] is not None:
            self.initial_ax.set_xlim(self.plot_params_initial['x_lim_min'], self.plot_params_initial['x_lim_max'])
        else:
            self.initial_ax.set_xlim(left=self.plot_params_initial['x_lim_min'])

        if self.plot_params_initial['y_lim_max'] is not None:
            self.initial_ax.set_ylim(self.plot_params_initial['y_lim_min'], self.plot_params_initial['y_lim_max'])
        else:
            self.initial_ax.set_ylim(bottom=self.plot_params_initial['y_lim_min'])

        self.initial_ax.tick_params(axis='both', labelsize=axis_font_size)
        self.initial_ax.legend(fontsize=legend_font_size)

        self.initial_canvas.draw()

    def update_graph_from_selection_fourier(self):
        if not self.data_loaded_fourier:
            messagebox.showwarning("Warning", "Пожалуйста, загрузите данные перед обновлением графика.")
            return

        self.fourier_ax.clear()
        if not any(var.get() for var in self.function_vars_fourier.values()):
            self.function_vars_fourier['Amp1'].set(True)  # Выбираем 'Amp1' по умолчанию
            messagebox.showinfo("Info", "Автоматически выбрана функция 'Amp1' для отображения")
        thickness = self.plot_params_fourier['thickness']
        title_font_size = self.plot_params_fourier['title_font_size']
        axis_font_size = self.plot_params_fourier['axis_font_size']
        legend_font_size = self.plot_params_fourier['legend_font_size']

        selected_functions = []

        if self.function_vars_fourier['Amp1'].get():
            color = self.plot_params_fourier['colors']['Amp1']
            marker = self.plot_params_fourier['markers']['Amp1']
            line_style = self.plot_params_fourier['line_styles']['Amp1']
            self.fourier_ax.plot(self.x2, self.amp1, label='$A_{m}$=1', color=color,
                                 linewidth=thickness,
                                 marker=marker, markersize=thickness * 2, linestyle=line_style)
            selected_functions.append('$A_{m1}$')

        if self.function_vars_fourier['Amp2'].get():
            color = self.plot_params_fourier['colors']['Amp2']
            marker = self.plot_params_fourier['markers']['Amp2']
            line_style = self.plot_params_fourier['line_styles']['Amp2']
            self.fourier_ax.plot(self.x2, self.amp2, label='$A_{m}$=2', color=color,
                                 linewidth=thickness,
                                 marker=marker, markersize=thickness * 2, linestyle=line_style)
            selected_functions.append('$A_{m2}$')

        if self.function_vars_fourier['Amp3'].get():
            color = self.plot_params_fourier['colors']['Amp3']
            marker = self.plot_params_fourier['markers']['Amp3']
            line_style = self.plot_params_fourier['line_styles']['Amp3']
            self.fourier_ax.plot(self.x2, self.amp3, label='$A_{m}$=3', color=color,
                                 linewidth=thickness,
                                 marker=marker, markersize=thickness * 2, linestyle=line_style)
            selected_functions.append('$A_{m3}$')

        if self.function_vars_fourier['Amp4'].get():
            color = self.plot_params_fourier['colors']['Amp4']
            marker = self.plot_params_fourier['markers']['Amp4']
            line_style = self.plot_params_fourier['line_styles']['Amp4']
            self.fourier_ax.plot(self.x2, self.amp4, label='$A_{m}$=4', color=color,
                                 linewidth=thickness,
                                 marker=marker, markersize=thickness * 2, linestyle=line_style)
            selected_functions.append('$A_{m4}$')

        if self.function_vars_fourier['Amp5'].get():
            color = self.plot_params_fourier['colors']['Amp5']
            marker = self.plot_params_fourier['markers']['Amp5']
            line_style = self.plot_params_fourier['line_styles']['Amp5']
            self.fourier_ax.plot(self.x2, self.amp5, label='$A_{m}$=5', color=color,
                                 linewidth=thickness,
                                 marker=marker, markersize=thickness * 2, linestyle=line_style)
            selected_functions.append('$A_{m5}$')

        if self.function_vars_fourier['Amp6'].get():
            color = self.plot_params_fourier['colors']['Amp6']
            marker = self.plot_params_fourier['markers']['Amp6']
            line_style = self.plot_params_fourier['line_styles']['Amp6']
            self.fourier_ax.plot(self.x2, self.amp6, label='$A_{m}$=6', color=color,
                                 linewidth=thickness,
                                 marker=marker, markersize=thickness * 2, linestyle=line_style)
            selected_functions.append('$A_{m6}$')

        if self.function_vars_fourier['Amp0'].get():
            color = self.plot_params_fourier['colors']['Amp0']
            marker = self.plot_params_fourier['markers']['Amp0']
            line_style = self.plot_params_fourier['line_styles']['Amp0']
            self.fourier_ax.plot(self.x2, self.amp0, label='$A_{m}$=0', color=color,
                                 linewidth=thickness,
                                 marker=marker, markersize=thickness * 2, linestyle=line_style)
            selected_functions.append('$A_{m0}$')

        title = f"Усредненные фурье амплитуды в зависимости от времени: {', '.join(selected_functions)}" if selected_functions else "Усредненные фурье амплитуды в зависимости от времени"
        self.fourier_ax.set_title(title, fontsize=title_font_size)

        self.fourier_ax.set_xlabel(self.plot_params_fourier['x_label'], fontsize=axis_font_size)
        self.fourier_ax.set_ylabel(self.plot_params_fourier['y_label'], fontsize=axis_font_size)

        if self.plot_params_fourier['x_lim_max'] is not None:
            self.fourier_ax.set_xlim(self.plot_params_fourier['x_lim_min'], self.plot_params_fourier['x_lim_max'])
        else:
            self.fourier_ax.set_xlim(left=self.plot_params_fourier['x_lim_min'])

        if self.plot_params_fourier['y_lim_max'] is not None:
            self.fourier_ax.set_ylim(self.plot_params_fourier['y_lim_min'], self.plot_params_fourier['y_lim_max'])
        else:
            self.fourier_ax.set_ylim(bottom=self.plot_params_fourier['y_lim_min'])

        self.fourier_ax.tick_params(axis='both', labelsize=axis_font_size)
        self.fourier_ax.legend(fontsize=legend_font_size)

        self.fourier_canvas.draw()

    def update_graph_from_selection_radius(self):
        if not self.data_loaded_radius:
            messagebox.showwarning("Warning", "Пожалуйста, загрузите данные перед обновлением графика.")
            return

        self.radius_ax.clear()
        if not any(var.get() for var in self.function_vars_radius.values()):
            self.function_vars_radius['Все радиусы'].set(True)  # Выбираем все радиусы по умолчанию
            messagebox.showinfo("Info", "Автоматически выбраны все радиусы для отображения")
        thickness = self.plot_params_radius['thickness']
        title_font_size = self.plot_params_radius['title_font_size']
        axis_font_size = self.plot_params_radius['axis_font_size']

        selected_functions = []

        # Получаем диапазон радиусов
        radius_min = self.radius_min_input.get().strip()
        radius_max = self.radius_max_input.get().strip()

        if radius_min and radius_max:
            try:
                radius_min = int(radius_min)
                radius_max = int(radius_max)

                # Проверка на корректность введенных значений
                if radius_min < 1 or radius_max > 30:
                    messagebox.showerror("Ошибка", "Радиусы должны быть в диапазоне от 1 до 30.")
                    return

                if radius_min > radius_max:
                    messagebox.showerror("Ошибка", "Значение минимального радиуса не может быть больше значения максимального радиуса.")
                    return

                selected_radii = list(range(radius_min, radius_max + 1))
            except ValueError:
                messagebox.showerror("Ошибка", "Пожалуйста, введите корректные значения для диапазона радиусов.")
                return
        else:
            # Если диапазон не задан, используем выбранные радиусы
            radius_values = self.radius_input.get().strip()
            if radius_values:
                try:
                    selected_radii = [int(r) for r in radius_values.split(',')]
                    # Проверка на корректность введенных значений
                    for r in selected_radii:
                        if r < 1 or r > 30:
                            messagebox.showerror("Ошибка", "Радиусы должны быть в диапазоне от 1 до 30.")
                            return
                except ValueError:
                    messagebox.showerror("Ошибка", "Пожалуйста, введите корректные номера радиусов.")
                    return
            else:
                selected_radii = []

        # Проверяем, выбрано ли 'Все радиусы'
        if self.function_vars_radius['Все радиусы'].get():
            selected_radii = list(range(1, 31))  # Если выбраны все радиусы

        for radius in selected_radii:
            color = self.plot_params_radius['colors'][f'r{radius}']
            self.radius_ax.plot(self.x3, getattr(self, f'r{radius}'), color=color, linewidth=thickness,
                                label=f'r{radius}')
            selected_functions.append(f'r{radius}')

        title = f"Распределение характеристики {self.characteristic_display} на определенном радиусе:" if self.characteristic_display else "Распределение характеристики на определенном радиусе:"
        self.radius_ax.set_title(title, fontsize=title_font_size)

        # Используем подписи, заданные пользователем
        self.radius_ax.set_xlabel(self.plot_params_radius['x_label'], fontsize=axis_font_size)
        self.radius_ax.set_ylabel(self.plot_params_radius['y_label'], fontsize=axis_font_size)

        # Устанавливаем ограничения осей
        if self.plot_params_radius['x_lim_max'] is not None:
            self.radius_ax.set_xlim(self.plot_params_radius['x_lim_min'], self.plot_params_radius['x_lim_max'])
        else:
            self.radius_ax.set_xlim(left=self.plot_params_radius['x_lim_min'])

        if self.plot_params_radius['y_lim_max'] is not None:
            self.radius_ax.set_ylim(self.plot_params_radius['y_lim_min'], self.plot_params_radius['y_lim_max'])
        else:
            self.radius_ax.set_ylim(bottom=self.plot_params_radius['y_lim_min'])

        self.radius_ax.tick_params(axis='both', labelsize=axis_font_size)

        self.radius_canvas.draw()

    def configure_plot_initial(self):
        configure_window = tk.Toplevel(self.root)
        configure_window.title("Настройки графика начального состояния")
        configure_window.geometry("1300x800")

        # Расположение элементов
        ttk.Label(configure_window, text="Толщина линии:").grid(row=0, column=0, padx=10, pady=5)
        thickness_input = tk.Entry(configure_window)
        thickness_input.insert(0, str(self.plot_params_initial['thickness']))
        thickness_input.grid(row=0, column=1, padx=10, pady=5)

        # Добавляем выпадающие списки для выбора маркеров и стилей линий
        marker_vars = {}
        line_style_vars = {}
        marker_values = ['', 'o', 's', 'd', '^', 'v', '<', '>', 'p', '*', 'x', '+', '|', '_']
        line_style_values = ['-', '--', '-.', ':']
        row_counter = 6  # Счетчик строк для размещения элементов

        ttk.Label(configure_window, text="Ограничение по X:").grid(row=row_counter, column=0, padx=10, pady=5)
        ttk.Label(configure_window, text="От").grid(row=row_counter, column=1, padx=10, pady=5)
        x_lim_min_input = tk.Entry(configure_window)
        x_lim_min_input.insert(0, str(self.plot_params_initial['x_lim_min']))
        x_lim_min_input.grid(row=row_counter, column=2, padx=10, pady=5)

        ttk.Label(configure_window, text="До").grid(row=row_counter, column=3, padx=10, pady=5)
        x_lim_max_input = tk.Entry(configure_window)
        x_lim_max_input.insert(0, str(self.plot_params_initial['x_lim_max']) if self.plot_params_initial[
                                                                                    'x_lim_max'] is not None else "")
        x_lim_max_input.grid(row=row_counter, column=4, padx=10, pady=5)

        row_counter += 1

        ttk.Label(configure_window, text="Ограничение по Y:").grid(row=row_counter, column=0, padx=10, pady=5)
        ttk.Label(configure_window, text="От").grid(row=row_counter, column=1, padx=10, pady=5)
        y_lim_min_input = tk.Entry(configure_window)
        y_lim_min_input.insert(0, str(self.plot_params_initial['y_lim_min']))
        y_lim_min_input.grid(row=row_counter, column=2, padx=10, pady=5)

        ttk.Label(configure_window, text="До").grid(row=row_counter, column=3, padx=10, pady=5)
        y_lim_max_input = tk.Entry(configure_window)
        y_lim_max_input.insert(0, str(self.plot_params_initial['y_lim_max']) if self.plot_params_initial[
                                                                                    'y_lim_max'] is not None else "")
        y_lim_max_input.grid(row=row_counter, column=4, padx=10, pady=5)

        row_counter += 1

        # Размер шрифта заголовка
        ttk.Label(configure_window, text="Размер шрифта заголовка:").grid(row=row_counter, column=0, padx=10, pady=5)
        title_font_size_input = tk.Entry(configure_window)
        title_font_size_input.insert(0, str(self.plot_params_initial['title_font_size']))
        title_font_size_input.grid(row=row_counter, column=1, padx=10, pady=5)

        row_counter += 1

        # Размер шрифта осей
        ttk.Label(configure_window, text="Размер шрифта осей:").grid(row=row_counter, column=0, padx=10, pady=5)
        axis_font_size_input = tk.Entry(configure_window)
        axis_font_size_input.insert(0, str(self.plot_params_initial['axis_font_size']))
        axis_font_size_input.grid(row=row_counter, column=1, padx=10, pady=5)

        row_counter += 1

        # Размер шрифта легенды
        ttk.Label(configure_window, text="Размер шрифта легенды:").grid(row=row_counter, column=0, padx=10, pady=5)
        legend_font_size_input = tk.Entry(configure_window)
        legend_font_size_input.insert(0, str(self.plot_params_initial['legend_font_size']))
        legend_font_size_input.grid(row=row_counter, column=1, padx=10, pady=5)

        row_counter += 1

        # Подписи к осям
        ttk.Label(configure_window, text="Подпись к оси X:").grid(row=row_counter, column=0, padx=10, pady=5)
        x_label_input = tk.Entry(configure_window)
        x_label_input.insert(0, self.plot_params_initial['x_label'])
        x_label_input.grid(row=row_counter, column=1, padx=10, pady=5)

        row_counter += 1

        ttk.Label(configure_window, text="Подпись к оси Y:").grid(row=row_counter, column=0, padx=10, pady=5)
        y_label_input = tk.Entry(configure_window)
        y_label_input.insert(0, self.plot_params_initial['y_label'])
        y_label_input.grid(row=row_counter, column=1, padx=10, pady=5)

        row_counter += 1

        for func, var in self.function_vars_initial.items():
            if var.get():  # Проверяем, выбрана ли функция
                # Проверяем, есть ли ключ в словаре markers
                if func not in self.plot_params_initial['markers']:
                    self.plot_params_initial['markers'][func] = ''  # Устанавливаем значение по умолчанию
                if func not in self.plot_params_initial['line_styles']:
                    self.plot_params_initial['line_styles'][func] = '-'  # Устанавливаем значение по умолчанию

                # Цвет
                ttk.Label(configure_window, text=f"Цвет для {func}:").grid(row=row_counter, column=0, padx=15, pady=5)
                color_button = tk.Button(configure_window, text="Выбрать цвет",
                                         command=lambda f=func: self.choose_color_initial(f))
                color_button.grid(row=row_counter, column=1, padx=10, pady=5)

                # Маркер
                ttk.Label(configure_window, text=f"Маркер для {func}:").grid(row=row_counter, column=2, padx=10, pady=5)
                marker_var = tk.StringVar(value=self.plot_params_initial['markers'].get(func, ''))  # текущий маркер
                marker_vars[func] = marker_var
                markers_menu = ttk.Combobox(configure_window, textvariable=marker_var, values=marker_values)
                markers_menu.grid(row=row_counter, column=3, padx=10, pady=5)

                # Стиль линии
                ttk.Label(configure_window, text=f"Стиль линии для {func}:").grid(row=row_counter, column=4, padx=10,
                                                                                  pady=5)
                line_style_var = tk.StringVar(
                    value=self.plot_params_initial['line_styles'].get(func, '-'))  # текущий стиль линии
                line_style_vars[func] = line_style_var
                line_style_menu = ttk.Combobox(configure_window, textvariable=line_style_var, values=line_style_values)
                line_style_menu.grid(row=row_counter, column=5, padx=10, pady=5)

                row_counter += 1  # Увеличиваем счетчик строк

        def apply_changes():
            try:
                self.plot_params_initial['thickness'] = float(thickness_input.get())
                self.plot_params_initial['x_lim_min'] = float(x_lim_min_input.get())
                self.plot_params_initial['x_lim_max'] = float(x_lim_max_input.get()) if x_lim_max_input.get() else None
                self.plot_params_initial['y_lim_min'] = float(y_lim_min_input.get())
                self.plot_params_initial['y_lim_max'] = float(y_lim_max_input.get()) if y_lim_max_input.get() else None
                self.plot_params_initial['title_font_size'] = int(title_font_size_input.get())
                self.plot_params_initial['axis_font_size'] = int(axis_font_size_input.get())
                self.plot_params_initial['legend_font_size'] = int(legend_font_size_input.get())
                self.plot_params_initial['x_label'] = x_label_input.get()
                self.plot_params_initial['y_label'] = y_label_input.get()

                # Обновляем только те маркеры и стили линий, которые были в интерфейсе
                for func in marker_vars:
                    self.plot_params_initial['markers'][func] = marker_vars[func].get()
                for func in line_style_vars:
                    self.plot_params_initial['line_styles'][func] = line_style_vars[func].get()

                self.update_graph_from_selection_initial()
                configure_window.destroy()
            except ValueError:
                messagebox.showerror("Ошибка", "Введите допустимые числовые значения.")

        # Кнопка применить
        apply_button = tk.Button(configure_window, text="Применить", command=apply_changes)
        apply_button.grid(row=row_counter, columnspan=6, pady=10)

    def choose_color_initial(self, func):
        color = askcolor()[1]
        if color:
            self.plot_params_initial['colors'][func] = color
            self.update_graph_from_selection_initial()

    def configure_plot_fourier(self):
        configure_window = tk.Toplevel(self.root)
        configure_window.title("Настройки графика Фурье-амплитуд")
        configure_window.geometry("1300x800")

        # Расположение элементов
        ttk.Label(configure_window, text="Толщина линии:").grid(row=0, column=0, padx=10, pady=5)
        thickness_input = tk.Entry(configure_window)
        thickness_input.insert(0, str(self.plot_params_fourier['thickness']))
        thickness_input.grid(row=0, column=1, padx=10, pady=5)

        # Добавляем выпадающие списки для выбора маркеров и стилей линий
        marker_vars = {}
        line_style_vars = {}
        marker_values = ['', 'o', 's', 'd', '^', 'v', '<', '>', 'p', '*', 'x', '+', '|', '_']
        line_style_values = ['-', '--', '-.', ':']
        row_counter = 6  # Счетчик строк для размещения элементов

        ttk.Label(configure_window, text="Ограничение по X:").grid(row=row_counter, column=0, padx=10, pady=5)
        ttk.Label(configure_window, text="От").grid(row=row_counter, column=1, padx=10, pady=5)
        x_lim_min_input = tk.Entry(configure_window)
        x_lim_min_input.insert(0, str(self.plot_params_fourier['x_lim_min']))
        x_lim_min_input.grid(row=row_counter, column=2, padx=10, pady=5)

        ttk.Label(configure_window, text="До").grid(row=row_counter, column=3, padx=10, pady=5)
        x_lim_max_input = tk.Entry(configure_window)
        x_lim_max_input.insert(0, str(self.plot_params_fourier['x_lim_max']) if self.plot_params_fourier[
                                                                                    'x_lim_max'] is not None else "")
        x_lim_max_input.grid(row=row_counter, column=4, padx=10, pady=5)

        row_counter += 1

        ttk.Label(configure_window, text="Ограничение по Y:").grid(row=row_counter, column=0, padx=10, pady=5)
        ttk.Label(configure_window, text="От").grid(row=row_counter, column=1, padx=10, pady=5)
        y_lim_min_input = tk.Entry(configure_window)
        y_lim_min_input.insert(0, str(self.plot_params_fourier['y_lim_min']))
        y_lim_min_input.grid(row=row_counter, column=2, padx=10, pady=5)

        ttk.Label(configure_window, text="До").grid(row=row_counter, column=3, padx=10, pady=5)
        y_lim_max_input = tk.Entry(configure_window)
        y_lim_max_input.insert(0, str(self.plot_params_fourier['y_lim_max']) if self.plot_params_fourier[
                                                                                    'y_lim_max'] is not None else "")
        y_lim_max_input.grid(row=row_counter, column=4, padx=10, pady=5)

        row_counter += 1

        # Размер шрифта заголовка
        ttk.Label(configure_window, text="Размер шрифта заголовка:").grid(row=row_counter, column=0, padx=10, pady=5)
        title_font_size_input = tk.Entry(configure_window)
        title_font_size_input.insert(0, str(self.plot_params_fourier['title_font_size']))
        title_font_size_input.grid(row=row_counter, column=1, padx=10, pady=5)

        row_counter += 1

        # Размер шрифта осей
        ttk.Label(configure_window, text="Размер шрифта осей:").grid(row=row_counter, column=0, padx=10, pady=5)
        axis_font_size_input = tk.Entry(configure_window)
        axis_font_size_input.insert(0, str(self.plot_params_fourier['axis_font_size']))
        axis_font_size_input.grid(row=row_counter, column=1, padx=10, pady=5)

        row_counter += 1

        # Размер шрифта легенды
        ttk.Label(configure_window, text="Размер шрифта легенды:").grid(row=row_counter, column=0, padx=10, pady=5)
        legend_font_size_input = tk.Entry(configure_window)
        legend_font_size_input.insert(0, str(self.plot_params_fourier['legend_font_size']))
        legend_font_size_input.grid(row=row_counter, column=1, padx=10, pady=5)

        row_counter += 1

        # Подписи к осям
        ttk.Label(configure_window, text="Подпись к оси X:").grid(row=row_counter, column=0, padx=10, pady=5)
        x_label_input = tk.Entry(configure_window)
        x_label_input.insert(0, self.plot_params_fourier['x_label'])
        x_label_input.grid(row=row_counter, column=1, padx=10, pady=5)

        row_counter += 1

        ttk.Label(configure_window, text="Подпись к оси Y:").grid(row=row_counter, column=0, padx=10, pady=5)
        y_label_input = tk.Entry(configure_window)
        y_label_input.insert(0, self.plot_params_fourier['y_label'])
        y_label_input.grid(row=row_counter, column=1, padx=10, pady=5)

        row_counter += 1

        # Создаем словарь для отображения понятных названий
        function_labels = {
            'Amp1': '1 фурье-моды',
            'Amp2': '2 фурье-моды',
            'Amp3': '3 фурье-моды',
            'Amp4': '4 фурье-моды',
            'Amp5': '5 фурье-моды',
            'Amp6': '6 фурье-моды',
            'Amp0': '0 фурье-моды'
        }

        for func, var in self.function_vars_fourier.items():
            if var.get():  # Проверяем, выбрана ли функция
                # Цвет
                ttk.Label(configure_window, text=f"Цвет для {function_labels[func]}:").grid(row=row_counter, column=0,
                                                                                            padx=15, pady=5)
                color_button = tk.Button(configure_window, text="Выбрать цвет",
                                         command=lambda f=func: self.choose_color_fourier(f))
                color_button.grid(row=row_counter, column=1, padx=10, pady=5)

                # Маркер
                ttk.Label(configure_window, text=f"Маркер для {function_labels[func]}:").grid(row=row_counter, column=2,
                                                                                              padx=10, pady=5)
                marker_var = tk.StringVar(value=self.plot_params_fourier['markers'][func])  # текущий маркер
                marker_vars[func] = marker_var
                markers_menu = ttk.Combobox(configure_window, textvariable=marker_var, values=marker_values)
                markers_menu.grid(row=row_counter, column=3, padx=10, pady=5)

                # Стиль линии
                ttk.Label(configure_window, text=f"Стиль линии для {function_labels[func]}:").grid(row=row_counter,
                                                                                                   column=4, padx=10,
                                                                                                   pady=5)
                line_style_var = tk.StringVar(
                    value=self.plot_params_fourier['line_styles'][func])  # текущий стиль линии
                line_style_vars[func] = line_style_var
                line_style_menu = ttk.Combobox(configure_window, textvariable=line_style_var, values=line_style_values)
                line_style_menu.grid(row=row_counter, column=5, padx=10, pady=5)

                row_counter += 1  # Увеличиваем счетчик строк

        def apply_changes():
            try:
                self.plot_params_fourier['thickness'] = float(thickness_input.get())
                self.plot_params_fourier['x_lim_min'] = float(x_lim_min_input.get())
                self.plot_params_fourier['x_lim_max'] = float(x_lim_max_input.get()) if x_lim_max_input.get() else None
                self.plot_params_fourier['y_lim_min'] = float(y_lim_min_input.get())
                self.plot_params_fourier['y_lim_max'] = float(y_lim_max_input.get()) if y_lim_max_input.get() else None
                self.plot_params_fourier['title_font_size'] = int(title_font_size_input.get())
                self.plot_params_fourier['axis_font_size'] = int(axis_font_size_input.get())
                self.plot_params_fourier['legend_font_size'] = int(legend_font_size_input.get())
                self.plot_params_fourier['x_label'] = x_label_input.get()
                self.plot_params_fourier['y_label'] = y_label_input.get()
                self.plot_params_fourier['markers'] = {func: marker_vars[func].get() for func in marker_vars.keys()}
                self.plot_params_fourier['line_styles'] = {func: line_style_vars[func].get() for func in
                                                           line_style_vars.keys()}
                self.update_graph_from_selection_fourier()
                configure_window.destroy()
            except ValueError:
                messagebox.showerror("Ошибка", "Введите допустимые числовые значения.")

        # Кнопка применить
        apply_button = tk.Button(configure_window, text="Применить", command=apply_changes)
        apply_button.grid(row=row_counter, columnspan=6, pady=10)

    def choose_color_fourier(self, func):
        color = askcolor()[1]
        if color:
            self.plot_params_fourier['colors'][func] = color
            self.update_graph_from_selection_fourier()

    def configure_plot_radius(self):
        configure_window = tk.Toplevel(self.root)
        configure_window.title("Настройки графика Распределения характеристик на определенном радиусе")
        configure_window.geometry("800x800")

        # Расположение элементов
        ttk.Label(configure_window, text="Толщина линии:").grid(row=0, column=0, padx=10, pady=5)
        thickness_input = tk.Entry(configure_window)
        thickness_input.insert(0, str(self.plot_params_radius['thickness']))
        thickness_input.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(configure_window, text="Ограничение по X:").grid(row=1, column=0, padx=10, pady=5)
        ttk.Label(configure_window, text="От").grid(row=1, column=1, padx=10, pady=5)
        x_lim_min_input = tk.Entry(configure_window)
        x_lim_min_input.insert(0, str(self.plot_params_radius['x_lim_min']))
        x_lim_min_input.grid(row=1, column=2, padx=10, pady=5)

        ttk.Label(configure_window, text="До").grid(row=1, column=3, padx=10, pady=5)
        x_lim_max_input = tk.Entry(configure_window)
        x_lim_max_input.insert(0, str(self.plot_params_radius['x_lim_max']) if self.plot_params_radius[
                                                                                   'x_lim_max'] is not None else "")
        x_lim_max_input.grid(row=1, column=4, padx=10, pady=5)

        ttk.Label(configure_window, text="Ограничение по Y:").grid(row=2, column=0, padx=10, pady=5)
        ttk.Label(configure_window, text="От").grid(row=2, column=1, padx=10, pady=5)
        y_lim_min_input = tk.Entry(configure_window)
        y_lim_min_input.insert(0, str(self.plot_params_radius['y_lim_min']))
        y_lim_min_input.grid(row=2, column=2, padx=10, pady=5)

        ttk.Label(configure_window, text="До").grid(row=2, column=3, padx=10, pady=5)
        y_lim_max_input = tk.Entry(configure_window)
        y_lim_max_input.insert(0, str(self.plot_params_radius['y_lim_max']) if self.plot_params_radius[
                                                                                   'y_lim_max'] is not None else "")
        y_lim_max_input.grid(row=2, column=4, padx=10, pady=5)

        # Размер шрифта заголовка
        ttk.Label(configure_window, text="Размер шрифта заголовка:").grid(row=3, column=0, padx=10, pady=5)
        title_font_size_input = tk.Entry(configure_window)
        title_font_size_input.insert(0, str(self.plot_params_radius['title_font_size']))
        title_font_size_input.grid(row=3, column=1, padx=10, pady=5)

        # Размер шрифта осей
        ttk.Label(configure_window, text="Размер шрифта осей:").grid(row=4, column=0, padx=10, pady=5)
        axis_font_size_input = tk.Entry(configure_window)
        axis_font_size_input.insert(0, str(self.plot_params_radius['axis_font_size']))
        axis_font_size_input.grid(row=4, column=1, padx=10, pady=5)

        # Подписи к осям
        ttk.Label(configure_window, text="Подпись к оси X:").grid(row=6, column=0, padx=10, pady=5)
        x_label_input = tk.Entry(configure_window)
        x_label_input.insert(0, self.plot_params_radius['x_label'])
        x_label_input.grid(row=6, column=1, padx=10, pady=5)

        ttk.Label(configure_window, text="Подпись к оси Y:").grid(row=7, column=0, padx=10, pady=5)
        y_label_input = tk.Entry(configure_window)
        y_label_input.insert(0, self.plot_params_radius['y_label'])
        y_label_input.grid(row=7, column=1, padx=10, pady=5)

        # Выбор цветовой схемы
        ttk.Label(configure_window, text="Цветовая схема:").grid(row=8, column=0, padx=10, pady=5)
        color_scheme_var = tk.StringVar(value='default')  # По умолчанию
        color_scheme_menu = ttk.Combobox(configure_window, textvariable=color_scheme_var,
                                         values=['default', 'grayscale', 'rainbow', 'heat', 'cool', 'viridis', 'plasma',
                                                 'inferno', 'magma', 'cividis'])
        color_scheme_menu.grid(row=8, column=1, padx=10, pady=5)

        def apply_changes():
            try:
                self.plot_params_radius['thickness'] = float(thickness_input.get())
                self.plot_params_radius['x_lim_min'] = float(x_lim_min_input.get())
                self.plot_params_radius['x_lim_max'] = float(x_lim_max_input.get()) if x_lim_max_input.get() else None
                self.plot_params_radius['y_lim_min'] = float(y_lim_min_input.get())
                self.plot_params_radius['y_lim_max'] = float(y_lim_max_input.get()) if y_lim_max_input.get() else None
                self.plot_params_radius['title_font_size'] = int(title_font_size_input.get())
                self.plot_params_radius['axis_font_size'] = int(axis_font_size_input.get())
                self.plot_params_radius['x_label'] = x_label_input.get()
                self.plot_params_radius['y_label'] = y_label_input.get()

                # Обновляем цветовую схему
                color_scheme = color_scheme_var.get()
                if color_scheme == 'grayscale':
                    # Создаем кастомную карту серого без белого цвета
                    colors = [(0.2 + 0.6 * (i / 29), 0.2 + 0.6 * (i / 29), 0.2 + 0.6 * (i / 29)) for i in range(30)]
                    grey_cmap = LinearSegmentedColormap.from_list('custom_grey', colors, N=30)
                    self.plot_params_radius['colors'] = {f'r{i}': grey_cmap((i - 1) / 29) for i in range(1, 31)}
                elif color_scheme == 'rainbow':
                    self.plot_params_radius['colors'] = {f'r{i}': plt.cm.rainbow(i / 30) for i in range(1, 31)}
                elif color_scheme == 'heat':
                    self.plot_params_radius['colors'] = {f'r{i}': plt.cm.hot(i / 30) for i in range(1, 31)}
                elif color_scheme == 'cool':
                    self.plot_params_radius['colors'] = {f'r{i}': plt.cm.cool(i / 30) for i in range(1, 31)}
                elif color_scheme == 'viridis':
                    self.plot_params_radius['colors'] = {f'r{i}': plt.cm.viridis(i / 30) for i in range(1, 31)}
                elif color_scheme == 'plasma':
                    self.plot_params_radius['colors'] = {f'r{i}': plt.cm.plasma(i / 30) for i in range(1, 31)}
                elif color_scheme == 'inferno':
                    self.plot_params_radius['colors'] = {f'r{i}': plt.cm.inferno(i / 30) for i in range(1, 31)}
                elif color_scheme == 'cividis':
                    self.plot_params_radius['colors'] = {f'r{i}': plt.cm.cividis(i / 30) for i in range(1, 31)}
                else:
                    # Возвращаем цвета по умолчанию
                    self.plot_params_radius['colors'] = {
                        'r1': 'black', 'r2': 'gray', 'r3': 'firebrick', 'r4': 'red', 'r5': 'darksalmon',
                        'r6': 'sienna', 'r7': 'sandybrown', 'r8': 'gold', 'r9': 'darkgreen', 'r10': 'm',
                        'r11': 'blue', 'r12': 'navy', 'r13': 'c', 'r14': 'crimson', 'r15': 'slateblue',
                        'r16': 'yellowgreen', 'r17': 'green', 'r18': 'r', 'r19': 'darkmagenta', 'r20': 'tomato',
                        'r21': 'brown', 'r22': 'orange', 'r23': 'y', 'r24': 'aquamarine', 'r25': 'maroon',
                        'r26': 'lime', 'r27': 'limegreen', 'r28': 'k', 'r29': 'b', 'r30': 'darkred'
                    }

                self.update_graph_from_selection_radius()
                configure_window.destroy()
            except ValueError:
                messagebox.showerror("Ошибка", "Введите допустимые числовые значения.")

        # Кнопка применить
        apply_button = tk.Button(configure_window, text="Применить", command=apply_changes)
        apply_button.grid(row=9, columnspan=6, pady=10)

    def configure_batch_plot(self):
        configure_window = tk.Toplevel(self.root)
        configure_window.title("Настройки графика")
        configure_window.geometry("800x800")

        # Ограничения по X
        ttk.Label(configure_window, text="Ограничение по X:").grid(row=0, column=0, padx=10, pady=5)
        ttk.Label(configure_window, text="От").grid(row=0, column=1, padx=10, pady=5)
        x_lim_min_input = tk.Entry(configure_window)
        x_lim_min_input.insert(0, str(self.batch_plot_params['x_lim_min']))
        x_lim_min_input.grid(row=0, column=2, padx=10, pady=5)

        ttk.Label(configure_window, text="До").grid(row=0, column=3, padx=10, pady=5)
        x_lim_max_input = tk.Entry(configure_window)
        x_lim_max_input.insert(0, str(self.batch_plot_params['x_lim_max']) if self.batch_plot_params[
                                                                                  'x_lim_max'] is not None else "")
        x_lim_max_input.grid(row=0, column=4, padx=10, pady=5)

        # Ограничения по Y
        ttk.Label(configure_window, text="Ограничение по Y:").grid(row=1, column=0, padx=10, pady=5)
        ttk.Label(configure_window, text="От").grid(row=1, column=1, padx=10, pady=5)
        y_lim_min_input = tk.Entry(configure_window)
        y_lim_min_input.insert(0, str(self.batch_plot_params['y_lim_min']))
        y_lim_min_input.grid(row=1, column=2, padx=10, pady=5)

        ttk.Label(configure_window, text="До").grid(row=1, column=3, padx=10, pady=5)
        y_lim_max_input = tk.Entry(configure_window)
        y_lim_max_input.insert(0, str(self.batch_plot_params['y_lim_max']) if self.batch_plot_params[
                                                                                  'y_lim_max'] is not None else "")
        y_lim_max_input.grid(row=1, column=4, padx=10, pady=5)

        # Добавляем поле для количества изолиний
        ttk.Label(configure_window, text="Количество изолиний:").grid(row=9, column=0, padx=10, pady=5)
        contour_levels_input = tk.Entry(configure_window)
        contour_levels_input.insert(0, str(self.batch_plot_params['contour_levels']))
        contour_levels_input.grid(row=9, column=1, padx=10, pady=5)

        # Минимальное и максимальное значения для колорбара
        ttk.Label(configure_window, text="Min для колорбара:").grid(row=8, column=0, padx=10, pady=5)
        self.colorbar_min_input = tk.Entry(configure_window)
        self.colorbar_min_input.insert(0, str(self.batch_plot_params.get('colorbar_min', -1.5)))
        self.colorbar_min_input.grid(row=8, column=1, padx=10, pady=5)

        ttk.Label(configure_window, text="Max для колорбара:").grid(row=8, column=2, padx=10, pady=5)
        self.colorbar_max_input = tk.Entry(configure_window)
        self.colorbar_max_input.insert(0, str(self.batch_plot_params.get('colorbar_max', 1)))
        self.colorbar_max_input.grid(row=8, column=3, padx=10, pady=5)

        # Размер шрифта для колорбара
        ttk.Label(configure_window, text="Размер шрифта колорбара:").grid(row=4, column=0, padx=10, pady=5)
        colorbar_font_size_input = tk.Entry(configure_window)
        colorbar_font_size_input.insert(0, str(self.batch_plot_params.get('colorbar_font_size', 10)))
        colorbar_font_size_input.grid(row=4, column=1, padx=10, pady=5)

        # Размер шрифта для заголовка
        ttk.Label(configure_window, text="Размер шрифта заголовка:").grid(row=2, column=0, padx=10, pady=5)
        title_font_size_input = tk.Entry(configure_window)
        title_font_size_input.insert(0, str(self.batch_plot_params.get('title_font_size', 10)))
        title_font_size_input.grid(row=2, column=1, padx=10, pady=5)

        # Размер шрифта для осей
        ttk.Label(configure_window, text="Размер шрифта осей:").grid(row=3, column=0, padx=10, pady=5)
        axis_font_size_input = tk.Entry(configure_window)
        axis_font_size_input.insert(0, str(self.batch_plot_params.get('axis_font_size', 10)))
        axis_font_size_input.grid(row=3, column=1, padx=10, pady=5)

        # Подписи осей
        ttk.Label(configure_window, text="Подпись к оси X:").grid(row=5, column=0, padx=10, pady=5)
        x_label_input = tk.Entry(configure_window)
        x_label_input.insert(0, self.batch_plot_params['x_label'])
        x_label_input.grid(row=5, column=1, padx=10, pady=5)

        ttk.Label(configure_window, text="Подпись к оси Y:").grid(row=6, column=0, padx=10, pady=5)
        y_label_input = tk.Entry(configure_window)
        y_label_input.insert(0, self.batch_plot_params['y_label'])
        y_label_input.grid(row=6, column=1, padx=10, pady=5)

        # Цветовая схема
        ttk.Label(configure_window, text="Цветовая схема:").grid(row=7, column=0, padx=10, pady=5)
        colorbar_input = tk.StringVar(value=self.batch_plot_params['colorbar'])
        colorbar_menu = ttk.Combobox(configure_window, textvariable=colorbar_input,
                                     values=['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'gnuplot2'])
        colorbar_menu.grid(row=7, column=1, padx=10, pady=5)

        def apply_changes():
            try:
                self.batch_plot_params['x_lim_min'] = float(x_lim_min_input.get())
                self.batch_plot_params['x_lim_max'] = float(x_lim_max_input.get()) if x_lim_max_input.get() else None
                self.batch_plot_params['y_lim_min'] = float(y_lim_min_input.get())
                self.batch_plot_params['y_lim_max'] = float(y_lim_max_input.get()) if y_lim_max_input.get() else None

                # Получаем значения для колорбара
                self.batch_plot_params['colorbar_min'] = float(self.colorbar_min_input.get())
                self.batch_plot_params['colorbar_max'] = float(self.colorbar_max_input.get())

                # Получаем размеры шрифтов
                self.batch_plot_params['title_font_size'] = int(title_font_size_input.get())
                self.batch_plot_params['axis_font_size'] = int(axis_font_size_input.get())
                self.batch_plot_params['colorbar_font_size'] = int(colorbar_font_size_input.get())

                self.batch_plot_params['x_label'] = x_label_input.get()
                self.batch_plot_params['y_label'] = y_label_input.get()
                self.batch_plot_params['colorbar'] = colorbar_input.get()
                self.batch_plot_params['contour_levels'] = int(contour_levels_input.get())
                self.update_batch_plot()
                configure_window.destroy()
            except ValueError:
                messagebox.showerror("Ошибка", "Введите допустимые числовые значения.")

        apply_button = tk.Button(configure_window, text="Применить", command=apply_changes)
        apply_button.grid(row=9, columnspan=5, pady=10)

    def select_data_directory(self):
        self.selected_directory = filedialog.askdirectory(title="Выбрать директорию с данными")
        if self.selected_directory:
            self.directory_label.config(text=f"Директория данных: {self.selected_directory}")

    def select_save_directory(self):
        self.save_directory = filedialog.askdirectory(title="Выбрать директорию для сохранения графиков")
        if self.save_directory:
            self.save_directory_label.config(text=f"Директория для сохранения: {self.save_directory}")

    def save_plot(self):
        if not self.save_directory:
            messagebox.showwarning("Warning", "Сначала выберите директорию для сохранения.")
            return

        # Создаем окно для выбора параметров сохранения
        save_window = tk.Toplevel(self.root)
        save_window.title("Параметры сохранения")

        # Выбор формата изображения
        ttk.Label(save_window, text="Формат изображения:").grid(row=0, column=0, padx=10, pady=5)
        format_var = tk.StringVar(value=self.image_format.get())
        formats = ['png', 'jpg', 'jpeg', 'tiff', 'svg', 'pdf', 'eps']
        format_menu = ttk.Combobox(save_window, textvariable=format_var, values=formats)
        format_menu.grid(row=0, column=1, padx=10, pady=5)

        # Выбор DPI (разрешения)
        ttk.Label(save_window, text="Разрешение (DPI):").grid(row=1, column=0, padx=10, pady=5)
        dpi_var = tk.StringVar(value="200")  # Значение по умолчанию
        dpi_input = tk.Entry(save_window, textvariable=dpi_var)
        dpi_input.grid(row=1, column=1, padx=10, pady=5)

        # Имя файла
        ttk.Label(save_window, text="Имя файла:").grid(row=2, column=0, padx=10, pady=5)
        filename_var = tk.StringVar()

        # Генерируем имя файла по умолчанию в зависимости от вкладки
        current_tab_index = self.tab_control.index("current")
        if current_tab_index == 0:  # Вкладка начального состояния
            selected_functions = [func for func, var in self.function_vars_initial.items() if var.get()]
            if selected_functions:
                tab_name = "Initial"
                base_name = []
                if 'c_z/c_r' in selected_functions:
                    base_name.append('cz')
                    base_name.append('cr')
                base_name += [func for func in selected_functions if func not in ['c_z/c_r']]
                default_name = f"{tab_name}_" + "__".join(base_name)
                filename_var.set(default_name)
        elif current_tab_index == 1:  # Вкладка Fourier
            selected_functions = [func for func, var in self.function_vars_fourier.items() if var.get()]
            if selected_functions:
                tab_name = "Fourier"
                default_name = f"{tab_name}_" + "_".join(selected_functions)
                filename_var.set(default_name)
        elif current_tab_index == 2:  # Вкладка пакетной обработки
            if hasattr(self, 'current_filename') and self.current_filename:
                base_name = os.path.splitext(self.current_filename)[0]
                filename_var.set(base_name)
        elif current_tab_index == 3:  # Вкладка радиусов
            if self.data_loaded_radius:
                tab_name = "Radius"
                characteristic_suffix = self.characteristic_display.replace(r'$c_{z}(rt)$', 'cz').replace(
                    r'$c_{\varphi}(rt)$', 'cf').replace(r'$c_{r}(rt)$', 'cr').replace(r'$h(rt)$', 'h')
                default_name = f"{tab_name}_{characteristic_suffix}"
                filename_var.set(default_name)

        filename_entry = tk.Entry(save_window, textvariable=filename_var)
        filename_entry.grid(row=2, column=1, padx=10, pady=5)

        def save_with_params():
            self.image_format.set(format_var.get())
            try:
                dpi = int(dpi_var.get())
                if dpi <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Ошибка", "Разрешение должно быть положительным целым числом.")
                return

            filename = filename_var.get().strip()
            if not filename:
                messagebox.showerror("Ошибка", "Введите имя файла.")
                return

            file_path = os.path.join(self.save_directory, f"{filename}.{format_var.get()}")

            try:
                if current_tab_index == 0:
                    self.initial_fig.savefig(file_path, format=format_var.get(), dpi=dpi)
                elif current_tab_index == 1:
                    self.fourier_fig.savefig(file_path, format=format_var.get(), dpi=dpi)
                elif current_tab_index == 2:
                    if self.batch_x is None or self.batch_y is None or self.batch_z is None:
                        messagebox.showwarning("Warning", "Нет данных для сохранения.")
                        return
                    self.batch_fig.savefig(file_path, format=format_var.get(), dpi=dpi)
                elif current_tab_index == 3:
                    self.radius_fig.savefig(file_path, format=format_var.get(), dpi=dpi)

                messagebox.showinfo("Success", f"График успешно сохранен как {filename}.{format_var.get()}!")
                save_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Не удалось сохранить график: {e}")

        save_button = tk.Button(save_window, text="Сохранить", command=save_with_params)
        save_button.grid(row=3, column=0, columnspan=2, pady=10)

        cancel_button = tk.Button(save_window, text="Отмена", command=save_window.destroy)
        cancel_button.grid(row=4, column=0, columnspan=2, pady=5)

    def save_all_batch_files(self):
        if not self.save_directory:
            messagebox.showwarning("Warning", "Сначала выберите директорию для сохранения.")
            return

        if not self.selected_directory:
            messagebox.showwarning("Warning", "Сначала выберите директорию с данными.")
            return

        # Создаем окно для выбора параметров сохранения
        save_window = tk.Toplevel(self.root)
        save_window.title("Параметры пакетного сохранения")

        # Выбор формата изображения
        ttk.Label(save_window, text="Формат изображения:").grid(row=0, column=0, padx=10, pady=5)
        format_var = tk.StringVar(value=self.image_format.get())
        formats = ['png', 'jpg', 'jpeg', 'tiff', 'svg', 'pdf', 'eps']
        format_menu = ttk.Combobox(save_window, textvariable=format_var, values=formats)
        format_menu.grid(row=0, column=1, padx=10, pady=5)

        # Выбор DPI (разрешения)
        ttk.Label(save_window, text="Разрешение (DPI):").grid(row=1, column=0, padx=10, pady=5)
        dpi_var = tk.StringVar(value="200")  # Значение по умолчанию
        dpi_input = tk.Entry(save_window, textvariable=dpi_var)
        dpi_input.grid(row=1, column=1, padx=10, pady=5)

        def save_with_params():
            self.image_format.set(format_var.get())
            try:
                dpi = int(dpi_var.get())
                if dpi <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Ошибка", "Разрешение должно быть положительным целым числом.")
                return

            save_window.destroy()
            self._save_all_batch_files_impl(dpi)

        save_button = tk.Button(save_window, text="Сохранить", command=save_with_params)
        save_button.grid(row=2, column=0, columnspan=2, pady=10)

        cancel_button = tk.Button(save_window, text="Отмена", command=save_window.destroy)
        cancel_button.grid(row=3, column=0, columnspan=2, pady=5)

    def _save_all_batch_files_impl(self, dpi=200):
        try:
            start_time = float(self.start_time_input.get())
            end_time = float(self.end_time_input.get())
        except ValueError:
            messagebox.showerror("Error", "Введите корректные значения времени.")
            return

        if start_time > end_time:
            messagebox.showerror("Error", "Начальное время должно быть меньше или равно конечному.")
            return

        # Собираем все подходящие файлы
        valid_files = []
        for f in os.listdir(self.selected_directory):
            if not f.endswith(".dat"):
                continue

            # Определяем тип файла
            if f.startswith("dq"):
                func_type = "dq"
            elif f.startswith("q_"):
                func_type = "q"
            else:
                continue  # Пропускаем неизвестные форматы

            # Извлекаем время
            file_time = self.extract_time_from_filename(f)
            if file_time is None or not (start_time <= file_time <= end_time):
                continue

            valid_files.append((f, func_type, file_time))

        if not valid_files:
            messagebox.showwarning("Warning", "Нет файлов в указанном временном диапазоне.")
            return

        # Первый проход: вычисление глобальных min и max для колорбара
        global_min = None
        global_max = None
        for filename, func_type, file_time in valid_files:
            full_path = os.path.join(self.selected_directory, filename)
            data = np.loadtxt(full_path)
            z = data[:, 2]

            if func_type == "q":
                z = np.where(z <= 0, 1e-10, z)
                z = np.log10(z)

            current_min = np.nanmin(z)
            current_max = np.nanmax(z)

            global_min = current_min if global_min is None else min(global_min, current_min)
            global_max = current_max if global_max is None else max(global_max, current_max)

        # Проверка, что значения найдены
        if global_min is None or global_max is None:
            messagebox.showerror("Error", "Нет данных для построения графиков")
            return

        # Создаем фиксированные уровни и метки
        num_levels = self.batch_plot_params.get('contour_levels', 35)
        contour_levels = np.linspace(global_min, global_max, num_levels)

        num_ticks = self.batch_plot_params.get('colorbar_ticks_num', 5)
        colorbar_ticks = np.linspace(global_min, global_max, num_ticks)

        precision = self.batch_plot_params.get('colorbar_precision', 2)
        tick_labels = [f"{tick:.{precision}f}" for tick in colorbar_ticks]

        # Настройка прогресс-бара
        self.progress_bar["maximum"] = len(valid_files)
        self.progress_bar["value"] = 0
        start_processing_time = time.time()

        for i, (filename, func_type, file_time) in enumerate(valid_files):
            try:
                # Загрузка данных
                full_path = os.path.join(self.selected_directory, filename)
                data = np.loadtxt(full_path)
                x = data[:, 0]
                y = data[:, 1]
                z = data[:, 2]

                # Применяем логарифм только для q
                if func_type == "q":
                    z = np.where(z <= 0, 1e-10, z)
                    z = np.log10(z)

                # Создаем график
                fig = plt.Figure(figsize=(8, 8), dpi=dpi)
                ax = fig.add_subplot(111)
                contour = ax.tricontourf(
                    x, y, z,
                    levels=contour_levels,
                    cmap=self.batch_plot_params['colorbar'],
                    vmin=global_min,
                    vmax=global_max
                )
                ax.set_aspect("equal")

                # Добавляем цветовую шкалу
                cbar = fig.colorbar(contour, ax=ax, ticks=colorbar_ticks)
                cbar.ax.set_yticklabels(tick_labels)
                cbar.ax.tick_params(labelsize=self.batch_plot_params.get('colorbar_font_size', 10))

                # Заголовок с временем
                ax.set_title(
                    f"t = {file_time:.3f}",
                    fontsize=self.batch_plot_params.get('title_font_size', 12)
                )

                # Сохраняем файл
                output_name = f"{func_type}_{file_time:.3f}.{self.image_format.get()}"
                output_path = os.path.join(self.save_directory, output_name)
                fig.savefig(output_path, bbox_inches="tight", dpi=dpi)
                plt.close(fig)

                # Обновляем прогресс
                self.progress_bar["value"] = i + 1
                self.root.update_idletasks()

                # Расчет оставшегося времени
                elapsed = time.time() - start_processing_time
                avg_time = elapsed / (i + 1)
                remaining = avg_time * (len(valid_files) - i - 1)
                self.remaining_time_label.config(text=f"Осталось: {remaining:.1f} сек")

            except Exception as e:
                messagebox.showerror("Ошибка", f"Файл {filename}: {str(e)}")
                continue

        messagebox.showinfo("Готово", f"Сохранено файлов: {len(valid_files)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TabbedApp(root)
    root.mainloop()
