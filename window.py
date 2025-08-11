import sys
import time
import random
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QComboBox, QPushButton, QTextEdit,
                             QTabWidget, QProgressBar, QMessageBox)
from PyQt5.QtCore import Qt, QTimer
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler

class MiningSupportApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Экспертная система для анкерного крепления")
        self.setGeometry(100, 100, 900, 700)

        self.init_models()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("QTabBar::tab { height: 40px; font-size: 14px; padding: 5px 20px; }")
        
        self.tab1 = QWidget()
        self.tab_widget.addTab(self.tab1, "Информация о выработке")
        
        self.tab2 = QWidget()
        self.tab_widget.addTab(self.tab2, "Параметры кровли")
        
        self.tab3 = QWidget()
        self.tab_widget.addTab(self.tab3, "Дополнительные параметры")
        
        self.tab4 = QWidget()
        self.tab_widget.addTab(self.tab4, "Расчет и результаты")
        
        main_layout.addWidget(self.tab_widget)
        
        self.inputs = {}
        self.setup_tab1()
        self.setup_tab2()
        self.setup_tab3()
        self.setup_tab4()
        
        self.apply_styles()

    def setup_tab1(self):
        layout = QVBoxLayout(self.tab1)
        layout.setSpacing(15)
        
        params = [
            ("Шахта", "text", "Казахстанская"),
            ("Ширина выработки (м)", "text", "6"),
            ("Высота выработки (м)", "text", "10"),
            ("Глубина выработки (м)", "text", "300"),
            ("Форма сечения", "combo", ["Арочная", "Прямоугольная"]),
            ("Расположение выработки", "combo", ["Монтажная камера", "Бремсберг", "Штрек"])
        ]
        
        for param_name, input_type, default in params:
            h_layout = QHBoxLayout()
            h_layout.setSpacing(10)
            label = QLabel(param_name + ":")
            label.setStyleSheet("font-size: 14px; color: #333; font-weight: bold;")
            label.setFixedWidth(250)
            if input_type == "text":
                input_widget = QLineEdit(default)
            else:
                input_widget = QComboBox()
                input_widget.addItems(default)
            self.inputs[param_name] = input_widget
            h_layout.addWidget(label)
            h_layout.addWidget(input_widget)
            layout.addLayout(h_layout)
            
        layout.addStretch(1)

    def setup_tab2(self):
        layout = QVBoxLayout(self.tab2)
        layout.setSpacing(15)
        
        params = [
            ("Тип кровли по обрушаемости", "combo", ["1 тип", "2 тип", "3 тип"]),
            ("Сопротивление кровли (Rc, МПа)", "text", "45"),
            ("Трещиноватость (м)", "text", "0.5")
        ]
        
        for param_name, input_type, default in params:
            h_layout = QHBoxLayout()
            h_layout.setSpacing(10)
            label = QLabel(param_name + ":")
            label.setStyleSheet("font-size: 14px; color: #333; font-weight: bold;")
            label.setFixedWidth(250)
            if input_type == "text":
                input_widget = QLineEdit(default)
            else:
                input_widget = QComboBox()
                input_widget.addItems(default)
            self.inputs[param_name] = input_widget
            h_layout.addWidget(label)
            h_layout.addWidget(input_widget)
            layout.addLayout(h_layout)
            
        layout.addStretch(1)

    def setup_tab3(self):
        layout = QVBoxLayout(self.tab3)
        layout.setSpacing(15)
        
        params = [
            ("Коэффициент влажности", "text", "0.47"),
            ("Воздействие других выработок", "combo", ["Одиночная", "Сопряжение с пересечением", "Примыкающая"])
        ]
        
        for param_name, input_type, default in params:
            h_layout = QHBoxLayout()
            h_layout.setSpacing(10)
            label = QLabel(param_name + ":")
            label.setStyleSheet("font-size: 14px; color: #333; font-weight: bold;")
            label.setFixedWidth(250)
            if input_type == "text":
                input_widget = QLineEdit(default)
            else:
                input_widget = QComboBox()
                input_widget.addItems(default)
            self.inputs[param_name] = input_widget
            h_layout.addWidget(label)
            h_layout.addWidget(input_widget)
            layout.addLayout(h_layout)
            
        layout.addStretch(1)

    def setup_tab4(self):
        layout = QVBoxLayout(self.tab4)
        layout.setSpacing(15)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        self.rule_button = QPushButton("Рассчитать по правилам")
        self.rf_button = QPushButton("Рассчитать с Random Forest")
        self.nn_button = QPushButton("Рассчитать с нейронной сетью")
        self.rule_button.clicked.connect(self.start_calculation_rules)
        self.rf_button.clicked.connect(self.start_calculation_rf)
        self.nn_button.clicked.connect(self.start_calculation_nn)
        button_layout.addWidget(self.rule_button)
        button_layout.addWidget(self.rf_button)
        button_layout.addWidget(self.nn_button)
        layout.addLayout(button_layout)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)  
        layout.addWidget(self.progress_bar)
        
        self.result_label = QLabel("Результаты расчета:")
        self.result_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(self.result_label)
        
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)

    def apply_styles(self):
        style_sheet = """
            QMainWindow {
                background-color: #f0f2f5;
            }
            QWidget {
                background-color: #f0f2f5;
                font-family: 'Arial', sans-serif;
            }
            QLabel {
                color: #333333;
                font-size: 14px;
                font-weight: bold;
            }
            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #dcdcdc;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
                color: #333333;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            QLineEdit:focus {
                border: 1px solid #0078d4;
                box-shadow: 0 0 5px rgba(0,120,212,0.5);
            }
            QComboBox {
                background-color: #ffffff;
                border: 1px solid #dcdcdc;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
                color: #333333;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            QComboBox:hover {
                border: 1px solid #0078d4;
            }
            QComboBox::drop-down {
                width: 20px;
                border-left: 1px solid #dcdcdc;
                border-top-right-radius: 5px;
                border-bottom-right-radius: 5px;
                background-color: #f5f5f5;
            }
            QComboBox QAbstractItemView {
                background-color: #ffffff;
                border: 1px solid #dcdcdc;
                selection-background-color: #0078d4;
                selection-color: #ffffff;
                color: #333333;
                font-size: 14px;
            }
            QPushButton {
                background-color: #0078d4;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }
            QPushButton:hover {
                background-color: #005ea2;
            }
            QPushButton:pressed {
                background-color: #004e8c;
                box-shadow: 0 1px 2px rgba(0,0,0,0.2);
            }
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #dcdcdc;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                color: #333333;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            QTextEdit QScrollBar:vertical {
                background: #f0f2f5;
                width: 12px;
                margin: 0;
                border-radius: 6px;
            }
            QTextEdit QScrollBar::handle:vertical {
                background: #dcdcdc;
                border-radius: 6px;
                min-height: 20px;
            }
            QTextEdit QScrollBar::handle:vertical:hover {
                background: #b0b0b0;
            }
            QTextEdit QScrollBar::add-line:vertical, QTextEdit QScrollBar::sub-line:vertical {
                height: 0;
            }
            QProgressBar {
                border: 1px solid #dcdcdc;
                border-radius: 5px;
                text-align: center;
                background-color: #ffffff;
                height: 25px;
                font-size: 14px;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #0078d4;
                border-radius: 4px;
            }
            QTabWidget::pane {
                border: 1px solid #dcdcdc;
                border-radius: 5px;
                background-color: #ffffff;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            QTabBar::tab {
                background-color: #f0f2f5;
                border: 1px solid #dcdcdc;
                border-bottom: none;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                padding: 8px 16px;
                margin-right: 2px;
                color: #333333;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                border-bottom-color: #ffffff;
                font-weight: bold;
            }
            QTabBar::tab:hover:!selected {
                background-color: #e8e8e8;
            }
        """
        self.setStyleSheet(style_sheet)

    def init_models(self):
        np.random.seed(42)
        n_samples = 100
        X = np.column_stack([
            np.random.uniform(200, 1500, n_samples),  
            np.random.uniform(5, 150, n_samples),     
            np.random.uniform(0.4, 0.9, n_samples),   
            np.random.uniform(1.5, 12, n_samples),    
            np.random.uniform(0.1, 1.0, n_samples)    
        ])
        y = 30 + 0.05 * X[:, 0] - 0.3 * X[:, 1] + 20 * X[:, 2] + 5 * X[:, 3] + 10 * X[:, 4] + np.random.normal(0, 5, n_samples)

        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)

        self.rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.rf_model.fit(X_scaled, y)

        self.nn_model = MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=1000, random_state=42)
        self.nn_model.fit(X_scaled, y)

    def get_input_data(self):
        required_fields = [
            "Глубина выработки (м)", 
            "Сопротивление кровли (Rc, МПа)", 
            "Коэффициент влажности", 
            "Трещиноватость (м)", 
            "Ширина выработки (м)",
            "Расположение выработки",
            "Тип кровли по обрушаемости"
        ]
        
        try:
            depth = float(self.inputs["Глубина выработки (м)"].text())
            rc = float(self.inputs["Сопротивление кровли (Rc, МПа)"].text())
            humidity = float(self.inputs["Коэффициент влажности"].text())
            fracture = float(self.inputs["Трещиноватость (м)"].text())
            width = float(self.inputs["Ширина выработки (м)"].text())
            location = self.inputs["Расположение выработки"].currentText()
            roof_type = self.inputs["Тип кровли по обрушаемости"].currentText()
            return depth, rc, humidity, fracture, width, location, roof_type
        except ValueError:
            self.result_text.setText("Ошибка: Проверьте корректность введённых данных.")
            QMessageBox.warning(self, "Ошибка ввода", "Проверьте корректность числовых данных во всех вкладках!")
            return None

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

    def format_result(self, support_type, rc, displacement, anchor_step):
        load_per_m2 = rc * 1.5  
        return (
            f"<h2>Результаты расчета:</h2>"
            f"<p><b>Рекомендуемое крепление:</b> {support_type}</p>"
            f"<p><b>Сопротивление кровли (Rc, 0.5B):</b> {rc:.2f} МПа</p>"
            f"<p><b>Сопротивление кровли (Rc, 1.5B):</b> {rc * 1.5:.2f} МПа</p>"
            f"<p><b>Смещение пород кровли:</b> {displacement:.2f} мм</p>"
            f"<p><b>Сопротивление боков (Rc):</b> {rc * 0.8:.2f} МПа</p>"
            f"<p><b>Расчётная нагрузка на 1 м² в боках:</b> {load_per_m2:.2f} кН/м²</p>"
            f"<p><b>Шаг анкеров:</b> {anchor_step:.2f} м</p>"
        )

    def finish_calculation(self, result_text):
        self.progress_bar.setValue(100)
        self.result_text.setHtml(result_text)
        
        self.rule_button.setEnabled(True)
        self.rf_button.setEnabled(True)
        self.nn_button.setEnabled(True)
        
        QTimer.singleShot(1000, lambda: self.progress_bar.setVisible(False))

    def calculate_rules(self):
        inputs = self.get_input_data()
        if inputs is None:
            self.finish_calculation("Ошибка: Проверьте корректность введённых данных.")
            return

        depth, rc, humidity, fracture, width, location, roof_type = inputs

        support_type, anchor_step = self.apply_rules(depth, rc, fracture, roof_type)

        displacement = self.calculate_displacement(depth, rc, width, location)

        result = self.format_result(support_type, rc, displacement, anchor_step)
        self.finish_calculation(result)

    def calculate_rf(self):
        inputs = self.get_input_data()
        if inputs is None:
            self.finish_calculation("Ошибка: Проверьте корректность введённых данных.")
            return

        depth, rc, humidity, fracture, width, location, roof_type = inputs

        X = np.array([[depth, rc, humidity, width, fracture]])
        X_scaled = self.scaler.transform(X)

        displacement = self.rf_model.predict(X_scaled)[0]

        support_type, anchor_step = self.apply_rules(depth, rc, fracture, roof_type)

        result = self.format_result(support_type, rc, displacement, anchor_step)
        self.finish_calculation(result)

    def calculate_nn(self):
        inputs = self.get_input_data()
        if inputs is None:
            self.finish_calculation("Ошибка: Проверьте корректность введённых данных.")
            return

        depth, rc, humidity, fracture, width, location, roof_type = inputs

        X = np.array([[depth, rc, humidity, width, fracture]])
        X_scaled = self.scaler.transform(X)

        displacement = self.nn_model.predict(X_scaled)[0]

        support_type, anchor_step = self.apply_rules(depth, rc, fracture, roof_type)

        result = self.format_result(support_type, rc, displacement, anchor_step)
        self.finish_calculation(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MiningSupportApp()
    window.show()
    sys.exit(app.exec_())