from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QTextEdit, QProgressBar, QGridLayout, QGroupBox, QScrollArea, QWidget
from PyQt5.QtCore import Qt
import json

def load_json_data(file_path="ui/structure.json"):
    """Загружает данные из JSON файла."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Ошибка загрузки JSON: {e}")
        return {}

def setup_tab1(tab, inputs):
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    container = QWidget()
    layout = QVBoxLayout(container)
    layout.setSpacing(15)
    layout.setContentsMargins(20, 20, 20, 20)
    
    # Mining-technical parameters group
    group = QGroupBox("Горно-технические параметры")
    group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 16px; padding: 10px; border: 1px solid #ccc; border-radius: 8px; }")
    group_layout = QGridLayout()
    group_layout.setSpacing(10)
    
    params = [
        ("Шахта", "text", "Казахстанская"),
        ("Выработка", "text", "Штрек №1"),
        ("Ширина выработки, м", "text", "6"),
        ("Высота выработки, м", "text", "10"),
        ("Глубина выработки, м", "text", "300"),
        ("Форма поперечного сечения", "combo", ["Арочная", "Прямоугольная", "Трапециевидная"]),
        ("Расположение выработки", "combo", ["Монтажная камера", "Бремсберг", "Штрек"]),
        ("Воздействие других выработок", "combo", ["Одиночная", "Сопряжение с пересечением", "Примыкающая"]),
        ("Влияние других смежных выработок на расстоянии, м", "text", "10"),
        ("Ширина взаимовлияющей выработки, м", "text", "5"),
        ("Вид выработки и условия ее поддержания", "text", "Анкерное крепление"),
        ("Тип кровли по обрушаемости", "combo", ["1 тип", "2 тип", "3 тип"]),
        ("Охрана целиком, его ширина, м", "text", "2"),
        ("Коэффициент концентрации напряжений в боках (Кв)", "text", "1.5")
    ]
    
    for i, (param_name, input_type, default) in enumerate(params):
        label = QLabel(param_name + ":")
        label.setStyleSheet("font-size: 14px; color: #333; font-weight: bold;")
        label.setFixedWidth(300)
        if input_type == "text":
            input_widget = QLineEdit(default)
            input_widget.setStyleSheet("padding: 8px; border-radius: 4px; border: 1px solid #ccc;")
        else:
            input_widget = QComboBox()
            input_widget.addItems(default)
            input_widget.setStyleSheet("padding: 8px; border-radius: 4px; border: 1px solid #ccc;")
        inputs[param_name] = input_widget
        group_layout.addWidget(label, i, 0)
        group_layout.addWidget(input_widget, i, 1)
    
    group.setLayout(group_layout)
    layout.addWidget(group)
    layout.addStretch(1)
    
    scroll.setWidget(container)
    tab_layout = QVBoxLayout(tab)
    tab_layout.addWidget(scroll)

def setup_tab2(tab, inputs):
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    container = QWidget()
    layout = QVBoxLayout(container)
    layout.setSpacing(15)
    layout.setContentsMargins(20, 20, 20, 20)
    
    # Mining-geological characteristics group (multiple layers)
    for layer in range(1, 6):
        group = QGroupBox(f"{layer} Слой в кровле")
        group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 16px; padding: 10px; border: 1px solid #ccc; border-radius: 8px; }")
        group_layout = QGridLayout()
        group_layout.setSpacing(10)
        
        params = [
            (f"Сопротивление, МПа", "text", "45"),
            (f"Мощность, м", "text", "1.5"),
            (f"Коэффициент влажности", "text", "0.47"),
            (f"Угол внутреннего трения, Град.", "text", "30"),
            (f"Объемный вес, кН/м³", "text", "25"),
            (f"Номер слоя по порядку", "text", str(layer))
        ]
        
        for i, (param_name, input_type, default) in enumerate(params):
            full_param_name = f"{layer} Слой: {param_name}"
            label = QLabel(param_name + ":")
            label.setStyleSheet("font-size: 14px; color: #333; font-weight: bold;")
            label.setFixedWidth(300)
            input_widget = QLineEdit(default)
            input_widget.setStyleSheet("padding: 8px; border-radius: 4px; border: 1px solid #ccc;")
            inputs[full_param_name] = input_widget
            group_layout.addWidget(label, i, 0)
            group_layout.addWidget(input_widget, i, 1)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
    
    layout.addStretch(1)
    
    scroll.setWidget(container)
    tab_layout = QVBoxLayout(tab)
    tab_layout.addWidget(scroll)

def setup_tab3(tab, inputs):
    layout = QVBoxLayout(tab)
    layout.setSpacing(15)
    layout.setContentsMargins(20, 20, 20, 20)
    
    # Additional parameters group
    group = QGroupBox("Дополнительные параметры")
    group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 16px; padding: 10px; border: 1px solid #ccc; border-radius: 8px; }")
    group_layout = QGridLayout()
    group_layout.setSpacing(10)
    
    params = [
        ("Трещиноватость, м", "text", "0.5"),
        ("Дополнительный коэффициент безопасности", "text", "1.2")
    ]
    
    for i, (param_name, input_type, default) in enumerate(params):
        label = QLabel(param_name + ":")
        label.setStyleSheet("font-size: 14px; color: #333; font-weight: bold;")
        label.setFixedWidth(300)
        input_widget = QLineEdit(default)
        input_widget.setStyleSheet("padding: 8px; border-radius: 4px; border: 1px solid #ccc;")
        inputs[param_name] = input_widget
        group_layout.addWidget(label, i, 0)
        group_layout.addWidget(input_widget, i, 1)
    
    group.setLayout(group_layout)
    layout.addWidget(group)
    layout.addStretch(1)

def setup_tab4(tab, window):
    layout = QVBoxLayout(tab)
    layout.setSpacing(15)
    layout.setContentsMargins(20, 20, 20, 20)
    
    # Calculation buttons
    button_layout = QHBoxLayout()
    button_layout.setSpacing(10)
    window.rule_button = QPushButton("Рассчитать по правилам")
    window.rf_button = QPushButton("Рассчитать с Random Forest")
    window.nn_button = QPushButton("Рассчитать с нейронной сетью")
    for btn in [window.rule_button, window.rf_button, window.nn_button]:
        btn.setStyleSheet("""
            QPushButton { 
                background-color: #2196F3; 
                color: white; 
                padding: 12px; 
                border-radius: 6px; 
                font-size: 16px; 
            }
            QPushButton:hover { background-color: #1976D2; }
        """)
    window.rule_button.clicked.connect(window.start_calculation_rules)
    window.rf_button.clicked.connect(window.start_calculation_rf)
    window.nn_button.clicked.connect(window.start_calculation_nn)
    button_layout.addWidget(window.rule_button)
    button_layout.addWidget(window.rf_button)
    button_layout.addWidget(window.nn_button)
    layout.addLayout(button_layout)
    
    # Progress bar
    window.progress_bar = QProgressBar()
    window.progress_bar.setRange(0, 100)
    window.progress_bar.setValue(0)
    window.progress_bar.setVisible(False)
    window.progress_bar.setStyleSheet("""
        QProgressBar {
            border: 1px solid #ccc;
            border-radius: 5px;
            text-align: center;
            height: 25px;
        }
        QProgressBar::chunk {
            background-color: #2196F3;
            border-radius: 3px;
        }
    """)
    layout.addWidget(window.progress_bar)
    
    # Results
    window.result_label = QLabel("Результаты расчета:")
    window.result_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 15px; color: #333;")
    layout.addWidget(window.result_label)
    
    window.result_text = QTextEdit()
    window.result_text.setReadOnly(True)
    window.result_text.setStyleSheet("font-size: 14px; border: 1px solid #ccc; border-radius: 4px; padding: 10px;")
    layout.addWidget(window.result_text)
    layout.addStretch(1)

def setup_custom_panel(tab, window):
    layout = QVBoxLayout(tab)
    layout.setSpacing(15)
    layout.setContentsMargins(20, 20, 20, 20)
    
    # Form for adding custom parameters
    group = QGroupBox("Добавление пользовательских параметров")
    group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 16px; padding: 10px; border: 1px solid #ccc; border-radius: 8px; }")
    form_layout = QGridLayout()
    form_layout.setSpacing(10)
    
    window.custom_param_name = QLineEdit()
    window.custom_param_name.setPlaceholderText("Название параметра")
    window.custom_param_name.setStyleSheet("padding: 8px; border-radius: 4px; border: 1px solid #ccc;")
    form_layout.addWidget(QLabel("Название:"), 0, 0)
    form_layout.addWidget(window.custom_param_name, 0, 1)
    
    window.custom_param_type = QComboBox()
    window.custom_param_type.addItems(["Числовой", "Текстовый", "Список"])
    window.custom_param_type.setStyleSheet("padding: 8px; border-radius: 4px; border: 1px solid #ccc;")
    form_layout.addWidget(QLabel("Тип:"), 1, 0)
    form_layout.addWidget(window.custom_param_type, 1, 1)
    
    window.custom_param_default = QLineEdit()
    window.custom_param_default.setPlaceholderText("Значение по умолчанию или список (через запятую)")
    window.custom_param_default.setStyleSheet("padding: 8px; border-radius: 4px; border: 1px solid #ccc;")
    form_layout.addWidget(QLabel("Значение:"), 2, 0)
    form_layout.addWidget(window.custom_param_default, 2, 1)
    
    add_button = QPushButton("Добавить параметр")
    add_button.setStyleSheet("""
        QPushButton { 
            background-color: #4CAF50; 
            color: white; 
            padding: 12px; 
            border-radius: 6px; 
            font-size: 16px; 
        }
        QPushButton:hover { background-color: #45a049; }
    """)
    add_button.clicked.connect(window.add_custom_parameter)
    form_layout.addWidget(add_button, 3, 0, 1, 2)
    
    group.setLayout(form_layout)
    layout.addWidget(group)
    
    # Area to display custom parameters
    window.custom_params_layout = QGridLayout()
    window.custom_params_layout.setSpacing(10)
    layout.addLayout(window.custom_params_layout)
    
    layout.addStretch(1)

def setup_chat_tab(tab, window):
    layout = QVBoxLayout(tab)
    layout.setSpacing(15)
    layout.setContentsMargins(20, 20, 20, 20)
    
    # Chat display
    window.chat_display = QTextEdit()
    window.chat_display.setReadOnly(True)
    window.chat_display.setStyleSheet("""
        QTextEdit {
            font-size: 14px;
            border: 1px solid #ccc;
            border-radius: 4px;
            padding: 10px;
            background-color: #fff;
        }
    """)
    layout.addWidget(window.chat_display)
    
    # Input and send button
    input_layout = QHBoxLayout()
    window.chat_input = QLineEdit()
    window.chat_input.setPlaceholderText("Введите сообщение...")
    window.chat_input.setStyleSheet("""
        QLineEdit {
            padding: 8px;
            border-radius: 4px;
            border: 1px solid #ccc;
            font-size: 14px;
        }
    """)
    input_layout.addWidget(window.chat_input)
    
    window.chat_send_button = QPushButton("Отправить")
    window.chat_send_button.setStyleSheet("""
        QPushButton { 
            background-color: #2196F3; 
            color: white; 
            padding: 12px; 
            border-radius: 6px; 
            font-size: 16px; 
        }
        QPushButton:hover { background-color: #1976D2; }
    """)
    window.chat_send_button.clicked.connect(window.send_chat_message)
    input_layout.addWidget(window.chat_send_button)
    
    layout.addLayout(input_layout)
    layout.addStretch(1)

def setup_json_data_tab(tab, window):
    layout = QVBoxLayout(tab)
    layout.setSpacing(15)
    layout.setContentsMargins(20, 20, 20, 20)
    
    # Загрузка JSON данных
    json_data = load_json_data()

    # Выпадающий список для выбора шахты
    window.mine_selector = QComboBox()
    window.mine_selector.setStyleSheet("padding: 8px; border-radius: 4px; border: 1px solid #ccc;")
    mines = [(uuid, data["description"]) for uuid, data in json_data.get("mines", {}).items()]
    window.mine_selector.addItem("Выберите шахту", "")
    for uuid, description in mines:
        window.mine_selector.addItem(description, uuid)
    layout.addWidget(QLabel("Шахта:"))
    layout.addWidget(window.mine_selector)

    # Выпадающий список для выбора выработки
    window.production_selector = QComboBox()
    window.production_selector.setStyleSheet("padding: 8px; border-radius: 4px; border: 1px solid #ccc;")
    window.production_selector.addItem("Выберите выработку", "")
    layout.addWidget(QLabel("Выработка:"))
    layout.addWidget(window.production_selector)

    # Область для отображения данных
    window.json_data_display = QTextEdit()
    window.json_data_display.setReadOnly(True)
    window.json_data_display.setMinimumHeight(600)  # Увеличиваем минимальную высоту
    window.json_data_display.setMinimumWidth(800)
    window.json_data_display.setStyleSheet("""
        QTextEdit {
            font-size: 14px;
            border: 1px solid #ccc;
            border-radius: 4px;
            padding: 10px;
            background-color: #fff;
        }
    """)
    layout.addWidget(window.json_data_display)
    layout.addStretch(1)

    # Обработчик выбора шахты
    def update_productions(mine_uuid):
        window.production_selector.clear()
        window.production_selector.addItem("Выберите выработку", "")
        window.json_data_display.clear()
        if mine_uuid and mine_uuid in json_data.get("mines", {}):
            productions = json_data["mines"][mine_uuid]["productions"]
            for prod_uuid, prod_data in productions.items():
                window.production_selector.addItem(prod_data["name"], prod_uuid)

    # Обработчик выбора выработки
    def update_data_display(production_uuid):
        window.json_data_display.clear()
        if not production_uuid:
            return
        mine_uuid = window.mine_selector.itemData(window.mine_selector.currentIndex())
        if mine_uuid in json_data.get("mines", {}):
            prod_data = json_data["mines"][mine_uuid]["productions"].get(production_uuid, {})
            html = "<h2>Параметры выработки:</h2>"
            html += f"<p><b>Название:</b> {prod_data.get('name', '')}</p>"
            html += f"<p><b>Ширина, м:</b> {prod_data.get('width', '')}</p>"
            html += f"<p><b>Высота, м:</b> {prod_data.get('height', '')}</p>"
            html += f"<p><b>Глубина, м:</b> {prod_data.get('depth', '')}</p>"
            html += f"<p><b>Форма поперечного сечения:</b> {['Арочная', 'Прямоугольная', 'Трапециевидная'][prod_data.get('crossSectionShapeIndex', 0)]}</p>"
            html += f"<p><b>Расположение выработки:</b> {['Монтажная камера', 'Бремсберг', 'Штрек'][prod_data.get('locationProductionIndex', 0)]}</p>"
            html += f"<p><b>Воздействие других выработок:</b> {['Одиночная', 'Сопряжение с пересечением', 'Примыкающая'][prod_data.get('impactsOtherProductionIndex', 0)]}</p>"
            html += f"<p><b>Влияние смежных выработок, м:</b> {prod_data.get('influenceAdjacentProduction', '')}</p>"
            html += f"<p><b>Ширина взаимовлияющей выработки, м:</b> {prod_data.get('widthInterdependentProduction', '')}</p>"
            html += f"<p><b>Тип кровли по обрушаемости:</b> {['1 тип', '2 тип', '3 тип'][prod_data.get('typeRoofIndex', 0)]}</p>"
            html += f"<p><b>Охрана целиком, м:</b> {prod_data.get('wholeGuard', '')}</p>"
            html += f"<p><b>Коэффициент концентрации напряжений:</b> {prod_data.get('ratioConcentration', '')}</p>"
            html += "<h3>Слои кровли:</h3>"
            for layer in prod_data.get("layers", []):
                html += f"<p><b>Слой {layer.get('number', '')} ({layer.get('name', '')}):</b> Мощность: {layer.get('power', '')} м, Сопротивление: {layer.get('resistance', '')} МПа, Коэффициент влажности: {layer.get('koefWet', '')}</p>"
            html += "<h3>Слои боков:</h3>"
            for layer in prod_data.get("layersSide", []):
                html += f"<p><b>Слой {layer.get('number', '')} ({layer.get('name', '')}):</b> Мощность: {layer.get('power', '')} м, Сопротивление: {layer.get('resistance', '')} МПа, Коэффициент влажности: {layer.get('koefWet', '')}</p>"
            window.json_data_display.setHtml(html)

    window.mine_selector.currentIndexChanged.connect(lambda: update_productions(window.mine_selector.itemData(window.mine_selector.currentIndex())))
    window.production_selector.currentIndexChanged.connect(lambda: update_data_display(window.production_selector.itemData(window.production_selector.currentIndex())))