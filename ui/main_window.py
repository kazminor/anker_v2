import random
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QComboBox, QPushButton, 
                             QStackedWidget, QListWidget, QListWidgetItem, 
                             QMessageBox, QScrollArea, QFrame, QDialog, QGridLayout, QTextEdit)
from PyQt5.QtCore import QTimer, QSize
from PyQt5.QtGui import QFont
import asyncio
import nest_asyncio
nest_asyncio.apply()

from models.mining_models import MiningModels
from ui.tab_layouts import (setup_tab1, setup_tab2, setup_tab3, setup_tab4, setup_custom_panel, setup_chat_tab, setup_json_data_tab)
from ui.styling import apply_styles
from database.postgres_connector import PostgresConnector
from ui.ai_chat import get_ai_response

class DatabaseConnectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Подключение к базе данных")
        layout = QGridLayout(self)
        
        self.host_input = QLineEdit("localhost")
        self.port_input = QLineEdit("5432")
        self.name_input = QLineEdit("mining_db")
        self.user_input = QLineEdit("postgres")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        
        layout.addWidget(QLabel("Хост:"), 0, 0)
        layout.addWidget(self.host_input, 0, 1)
        layout.addWidget(QLabel("Порт:"), 1, 0)
        layout.addWidget(self.port_input, 1, 1)
        layout.addWidget(QLabel("Имя БД:"), 2, 0)
        layout.addWidget(self.name_input, 2, 1)
        layout.addWidget(QLabel("Пользователь:"), 3, 0)
        layout.addWidget(self.user_input, 3, 1)
        layout.addWidget(QLabel("Пароль:"), 4, 0)
        layout.addWidget(self.password_input, 4, 1)
        
        connect_button = QPushButton("Подключиться")
        connect_button.clicked.connect(self.accept)
        layout.addWidget(connect_button, 5, 0, 1, 2)

class MiningSupportApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Экспертная система для анкерного крепления")
        self.setGeometry(100, 100, 1400, 900)

        self.models = MiningModels()
        self.inputs = {}
        self.custom_params = {}
        self.db = PostgresConnector()

        # Main container
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar_widget = QWidget()
        self.sidebar_widget.setFixedWidth(300)
        sidebar_layout = QVBoxLayout(self.sidebar_widget)
        sidebar_layout.setContentsMargins(15, 15, 15, 15)
        sidebar_layout.setSpacing(10)
        
        # Menu list for sidebar
        self.menu_list = QListWidget()
        self.menu_list.setIconSize(QSize(24, 24))
        self.menu_list.setFont(QFont("Segoe UI", 14))
        self.menu_list.setFrameShape(QFrame.NoFrame)
        self.menu_list.setFixedHeight(500)  # Increased height for 7 items + 2 buttons
        self.menu_list.setStyleSheet("""
            QListWidget::item { 
                padding: 15px; 
                border-radius: 4px; 
                margin-bottom: 5px; 
            }
            QListWidget::item:selected { 
                background-color: #2196F3; 
                color: white; 
            }
        """)
        
        menu_items = [
            ("Горно-технические параметры", "mine"),
            ("Горно-геологические характеристики", "roof"), 
            ("Дополнительные параметры", "settings"),
            ("Пользовательские параметры", "custom"),
            ("Расчет и результаты", "calculate"),
            ("Чат с ИИ", "chat"),
            ("Данные из JSON", "json_data")  # Новая вкладка
        ]
        
        for text, icon_name in menu_items:
            item = QListWidgetItem(text)
            # Uncomment if icons are available
            # item.setIcon(QIcon(f"icons/{icon_name}.png"))
            self.menu_list.addItem(item)
        
        sidebar_layout.addWidget(self.menu_list)
        
        # Database buttons
        self.db_button = QPushButton("Подключиться к БД")
        self.db_button.setStyleSheet("""
            QPushButton { 
                background-color: #2196F3; 
                color: white; 
                padding: 12px; 
                border-radius: 6px; 
                font-size: 15px; 
            }
            QPushButton:hover { background-color: #1976D2; }
        """)
        self.db_button.clicked.connect(self.connect_to_database)
        sidebar_layout.addWidget(self.db_button)
        
        self.add_data_button = QPushButton("Добавить данные в Dataset")
        self.add_data_button.setStyleSheet("""
            QPushButton { 
                background-color: #2196F3; 
                color: white; 
                padding: 12px; 
                border-radius: 6px; 
                font-size: 15px; 
            }
            QPushButton:hover { background-color: #1976D2; }
        """)
        self.add_data_button.clicked.connect(self.add_data_to_dataset)
        self.add_data_button.setEnabled(False)
        sidebar_layout.addWidget(self.add_data_button)
        
        sidebar_layout.addStretch(1)
        
        # Central content area
        self.content_area = QScrollArea()
        self.content_area.setWidgetResizable(True)
        self.content_area.setFrameShape(QFrame.NoFrame)
        
        self.stacked_widget = QStackedWidget()
        self.panel1 = QWidget()
        self.panel2 = QWidget()
        self.panel3 = QWidget()
        self.panel4 = QWidget()
        self.custom_panel = QWidget()
        self.chat_panel = QWidget()
        self.json_data_panel = QWidget()  # Новый виджет для вкладки
        
        self.stacked_widget.addWidget(self.panel1)
        self.stacked_widget.addWidget(self.panel2)
        self.stacked_widget.addWidget(self.panel3)
        self.stacked_widget.addWidget(self.custom_panel)
        self.stacked_widget.addWidget(self.panel4)
        self.stacked_widget.addWidget(self.chat_panel)
        self.stacked_widget.addWidget(self.json_data_panel)  # Добавляем в stacked_widget
        
        self.content_area.setWidget(self.stacked_widget)
        
        main_layout.addWidget(self.sidebar_widget)
        main_layout.addWidget(self.content_area, 1)
        
        # Setup panels
        setup_tab1(self.panel1, self.inputs)
        setup_tab2(self.panel2, self.inputs)
        setup_tab3(self.panel3, self.inputs)
        setup_tab4(self.panel4, self)
        setup_custom_panel(self.custom_panel, self)
        setup_chat_tab(self.chat_panel, self)
        setup_json_data_tab(self.json_data_panel, self)  # Настройка новой вкладки
        
        self.menu_list.currentRowChanged.connect(self.stacked_widget.setCurrentIndex)
        self.menu_list.setCurrentRow(0)
        
        apply_styles(self)

    def get_input_data(self):
        required_fields = [
            "Глубина выработки, м", 
            "Сопротивление, МПа", 
            "Коэффициент влажности", 
            "Трещиноватость, м", 
            "Ширина выработки, м",
            "Расположение выработки",
            "Тип кровли по обрушаемости"
        ]
        
        try:
            data = {}
            for field in required_fields:
                if field in self.inputs:
                    widget = self.inputs[field]
                    if isinstance(widget, QLineEdit):
                        data[field] = float(widget.text()) if widget.text() else 0.0
                    elif isinstance(widget, QComboBox):
                        data[field] = widget.currentText() or "Не выбрано"
            
            custom_params = {}
            for param_name, widget in self.custom_params.items():
                if isinstance(widget, QLineEdit):
                    try:
                        custom_params[param_name] = float(widget.text()) if widget.text() else 0.0
                    except ValueError:
                        custom_params[param_name] = widget.text() or "Не указано"
                elif isinstance(widget, QComboBox):
                    custom_params[param_name] = widget.currentText() or "Не выбрано"
            
            return data, custom_params
        except ValueError:
            self.result_text.setText("Ошибка: Проверьте корректность введённых данных.")
            QMessageBox.warning(self, "Ошибка ввода", "Проверьте корректность числовых данных!")
            return None

    def connect_to_database(self):
        try:
            dialog = DatabaseConnectionDialog(self)
            if dialog.exec_():
                host = dialog.host_input.text()
                port = dialog.port_input.text()
                dbname = dialog.name_input.text()
                user = dialog.user_input.text()
                password = dialog.password_input.text()
                
                if self.db.connect(host, port, dbname, user, password):
                    QMessageBox.information(self, "Успешно", "Подключение к базе данных установлено!")
                    self.add_data_button.setEnabled(True)
                else:
                    QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка подключения: {str(e)}")

    def add_data_to_dataset(self):
        try:
            inputs = self.get_input_data()
            if inputs is None:
                return
                
            data, custom_params = inputs
            
            depth = data.get("Глубина выработки, м", 0)
            rc = data.get("Сопротивление, МПа", 0)
            humidity = data.get("Коэффициент влажности", 0)
            fracture = data.get("Трещиноватость, м", 0)
            width = data.get("Ширина выработки, м", 0)
            location = data.get("Расположение выработки", "")
            roof_type = data.get("Тип кровли по обрушаемости", "")
            
            displacement = self.calculate_displacement(depth, rc, width, location)
            support_type, anchor_step = self.apply_rules(depth, rc, fracture, roof_type)
            
            dataset = {
                "depth": depth,
                "rock_strength": rc,
                "humidity": humidity,
                "fracture": fracture,
                "width": width,
                "location": location,
                "roof_type": roof_type,
                "displacement": displacement,
                "support_type": support_type,
                "anchor_step": anchor_step,
                **custom_params
            }
            
            if self.db.add_dataset(dataset):
                QMessageBox.information(self, "Успешно", "Данные успешно добавлены в dataset!")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось добавить данные в dataset.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении данных: {str(e)}")

    def add_custom_parameter(self):
        param_name = self.custom_param_name.text().strip()
        param_type = self.custom_param_type.currentText()
        param_default = self.custom_param_default.text().strip()
        
        if not param_name:
            QMessageBox.warning(self, "Предупреждение", "Введите название параметра!")
            return
            
        if param_name in self.custom_params:
            QMessageBox.warning(self, "Предупреждение", f"Параметр '{param_name}' уже существует!")
            return
            
        if param_type == "Числовой":
            try:
                float(param_default)  # Validate numeric input
                widget = QLineEdit(param_default)
                widget.setStyleSheet("padding: 8px; border-radius: 4px; border: 1px solid #ccc;")
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Для числового типа введите корректное число!")
                return
        elif param_type == "Текстовый":
            widget = QLineEdit(param_default)
            widget.setStyleSheet("padding: 8px; border-radius: 4px; border: 1px solid #ccc;")
        else:  # Список
            widget = QComboBox()
            widget.setStyleSheet("padding: 8px; border-radius: 4px; border: 1px solid #ccc;")
            values = [v.strip() for v in param_default.split(",") if v.strip()]
            if values:
                widget.addItems(values)
            else:
                widget.addItem("Значение 1")
                
        self.custom_params[param_name] = widget
        
        row = self.custom_params_layout.rowCount()
        label = QLabel(f"{param_name}:")
        label.setStyleSheet("font-size: 14px; color: #333; font-weight: bold;")
        self.custom_params_layout.addWidget(label, row, 0)
        self.custom_params_layout.addWidget(widget, row, 1)
        
        self.custom_param_name.clear()
        self.custom_param_default.clear()

    def send_chat_message(self):
        message = self.chat_input.text().strip()
        if not message:
            return
        
        # Append user message to chat display
        self.chat_display.append(f"<b>Вы:</b> {message}")
        self.chat_input.clear()
        
        # Disable send button during processing
        self.chat_send_button.setEnabled(False)
        
        # Run async AI response in the event loop
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(self.get_ai_response_async(message))
        
        # Append AI response
        self.chat_display.append(f"<b>ИИ:</b> {response}")
        self.chat_send_button.setEnabled(True)

    async def get_ai_response_async(self, message):
        try:
            response = await get_ai_response(message)
            return response
        except Exception as e:
            return f"Ошибка при получении ответа от ИИ: {str(e)}"

    def start_calculation_rules(self):
        self.start_loading_animation()
        QTimer.singleShot(random.randint(1500, 3000), self.calculate_rules)

    def start_calculation_rf(self):
        self.start_loading_animation()
        QTimer.singleShot(random.randint(1500, 3000), self.calculate_rf)

    def start_calculation_nn(self):
        self.start_loading_animation()
        QTimer.singleShot(random.randint(1500, 3000), self.calculate_nn)

    def start_loading_animation(self):
        self.progress_bar.setVisible(True)
        self.result_text.setText("Выполняется расчет...")
        self.progress_bar.setValue(0)
        
        self.rule_button.setEnabled(False)
        self.rf_button.setEnabled(False)
        self.nn_button.setEnabled(False)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.progress_value = 0
        self.timer.start(50)

    def update_progress(self):
        self.progress_value += random.randint(1, 5)
        if self.progress_value >= 100:
            self.progress_value = 100
            self.timer.stop()
        self.progress_bar.setValue(self.progress_value)

    def apply_rules(self, depth, rc, fracture, roof_type):
        support_type = "Одноуровневое"
        anchor_step = 0.8

        if rc < 35 and fracture < 0.3:
            support_type = "Двухуровневое"
            anchor_step = 0.5

        if depth > 500:
            anchor_step *= 0.8

        if roof_type == "3 тип" and rc < 30:
            support_type = "Канатное"

        if depth > 600 and fracture < 0.2:
            support_type = "Комбинированное (анкеры + рамы)"

        return support_type, anchor_step

    def calculate_displacement(self, depth, rc, width, location):
        ut = 30 if depth < 500 else 50
        k1 = 1.0
        k2 = 1 + (width - 5) * 0.25
        k3 = 1.0
        k4 = 1.0 if location != "Монтажная камера" else 1.2
        return ut * k1 * k2 * k3 * k4

    def format_result(self, support_type, rc, displacement, anchor_step, custom_params=None):
        load_per_m2 = rc * 1.5
        result = (
            f"<h2>Результаты расчета:</h2>"
            f"<p><b>Рекомендуемое крепление:</b> {support_type}</p>"
            f"<p><b>Сопротивление кровли (Rc, 0.5B):</b> {rc:.2f} МПа</p>"
            f"<p><b>Сопротивление кровли (Rc, 1.5B):</b> {rc * 1.5:.2f} МПа</p>"
            f"<p><b>Смещение пород кровли:</b> {displacement:.2f} мм</p>"
            f"<p><b>Сопротивление боков (Rc):</b> {rc * 0.8:.2f} МПа</p>"
            f"<p><b>Расчётная нагрузка на 1 м² в боках:</b> {load_per_m2:.2f} кН/м²</p>"
            f"<p><b>Шаг анкеров:</b> {anchor_step:.2f} м</p>"
        )
        
        if custom_params and len(custom_params) > 0:
            result += "<h3>Пользовательские параметры:</h3>"
            for name, value in custom_params.items():
                result += f"<p><b>{name}:</b> {value}</p>"
                
        return result

    def finish_calculation(self, result_text):
        self.progress_bar.setValue(100)
        self.result_text.setHtml(result_text)
        
        self.rule_button.setEnabled(True)
        self.rf_button.setEnabled(True)
        self.nn_button.setEnabled(True)

    def calculate_rules(self):
        inputs = self.get_input_data()
        if inputs is None:
            self.finish_calculation("Ошибка: Проверьте корректность введённых данных.")
            return

        data, custom_params = inputs
        depth = data.get("Глубина выработки, м", 0)
        rc = data.get("Сопротивление, МПа", 0)
        fracture = data.get("Трещиноватость, м", 0)
        width = data.get("Ширина выработки, м", 0)
        location = data.get("Расположение выработки", "")
        roof_type = data.get("Тип кровли по обрушаемости", "")

        support_type, anchor_step = self.apply_rules(depth, rc, fracture, roof_type)
        displacement = self.calculate_displacement(depth, rc, width, location)

        result = self.format_result(support_type, rc, displacement, anchor_step, custom_params)
        self.finish_calculation(result)

    def calculate_rf(self):
        inputs = self.get_input_data()
        if inputs is None:
            self.finish_calculation("Ошибка: Проверьте корректность введённых данных.")
            return

        data, custom_params = inputs
        depth = data.get("Глубина выработки, м", 0)
        rc = data.get("Сопротивление, МПа", 0)
        humidity = data.get("Коэффициент влажности", 0)
        fracture = data.get("Трещиноватость, м", 0)
        width = data.get("Ширина выработки, м", 0)
        location = data.get("Расположение выработки", "")
        roof_type = data.get("Тип кровли по обрушаемости", "")

        displacement = self.models.predict_rf(depth, rc, humidity, width, fracture)
        support_type, anchor_step = self.apply_rules(depth, rc, fracture, roof_type)

        result = self.format_result(support_type, rc, displacement, anchor_step, custom_params)
        self.finish_calculation(result)

    def calculate_nn(self):
        inputs = self.get_input_data()
        if inputs is None:
            self.finish_calculation("Ошибка: Проверьте корректность введённых данных.")
            return

        data, custom_params = inputs
        depth = data.get("Глубина выработки, м", 0)
        rc = data.get("Сопротивление, МПа", 0)
        humidity = data.get("Коэффициент влажности", 0)
        fracture = data.get("Трещиноватость, м", 0)
        width = data.get("Ширина выработки, м", 0)
        location = data.get("Расположение выработки", "")
        roof_type = data.get("Тип кровли по обрушаемости", "")

        displacement = self.models.predict_nn(depth, rc, humidity, width, fracture)
        support_type, anchor_step = self.apply_rules(depth, rc, fracture, roof_type)

        result = self.format_result(support_type, rc, displacement, anchor_step, custom_params)
        self.finish_calculation(result)