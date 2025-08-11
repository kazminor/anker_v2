def init_database(self):
        """Инициализация подключения к PostgreSQL и создание таблиц, если их нет"""
        try:
            # Настройки подключения к PostgreSQL
            self.db_config = {
                "host": "localhost",
                "database": "mining_support",
                "user": "postgres",
                "password": "postgres",
                "port": "5432"
            }
            
            # Подключение к БД
            self.conn = psycopg2.connect(**self.db_config)
            self.cursor = self.conn.cursor()
            
            # Создаём таблицу для хранения данных, если её ещё нет
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS mining_data (
                    id SERIAL PRIMARY KEY,
                    mine_name VARCHAR(100),
                    width FLOAT,
                    height FLOAT,
                    depth FLOAT,
                    section_shape VARCHAR(50),
                    location VARCHAR(100),
                    other_workings VARCHAR(100),
                    roof_type VARCHAR(20),
                    rc FLOAT,
                    humidity FLOAT,
                    fracture FLOAT,
                    custom_params JSONB,
                    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Создаём таблицу для пользовательских параметров
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS custom_parameters (
                    id SERIAL PRIMARY KEY,
                    param_name VARCHAR(100) UNIQUE,
                    param_type VARCHAR(20),
                    default_value VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            self.conn.commit()
            
        except psycopg2.Error as e:
            QMessageBox.critical(self, "Ошибка БД", f"Не удалось подключиться к базе данных: {e}")
            # Если не удалось подключиться к БД, работаем без неё
            self.conn = None
            self.cursor = None
            
    def setup_mine_info_page(self):
        """Настройка страницы с информацией о выработке"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Заголовок
        header = QLabel("Информация о выработке")
        header.setStyleSheet("font-size: 18px; font-weight: bold; color: #0078d4; padding-bottom: 10px;")
        layout.addWidget(header)
        
        # Создаем форму для ввода данных
        form_group = QGroupBox()
        form_layout = QFormLayout(form_group)
        form_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        form_layout.setSpacing(15)
        
        # Параметры
        params = [
            ("Шахта", "text", "Казахстанская"),
            ("Ширина выработки (м)", "text", "6"),
            ("Высота выработки (м)", "text", "10"),
            ("Глубина выработки (м)", "text", "300"),
            ("Форма сечения", "combo", ["Арочная", "Прямоугольная"]),
            ("Расположение выработки", "combo", ["Монтажная камера", "Бремсберг", "Штрек"])
        ]
        
        for param_name, input_type, default in params:
            label = QLabel(param_name + ":")
            label.setStyleSheet("font-weight: bold;")
            
            if input_type == "text":
                input_widget = QLineEdit(default)
            else:
                input_widget = QComboBox()
                input_widget.addItems(default)
            
            self.inputs[param_name] = input_widget
            form_layout.addRow(label, input_widget)
        
        layout.addWidget(form_group)
        
        # Кнопка для перехода к следующему разделу
        next_button = QPushButton("Далее >")
        next_button.clicked.connect(lambda: self.nav_list.setCurrentRow(1))
        next_button.setStyleSheet("font-weight: bold;")
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(next_button)
        layout.addLayout(button_layout)
        
        # Добавляем пространство внизу
        layout.addStretch(1)
        
        # Добавляем страницу в стекированный виджет
        self.stacked_widget.addWidget(page)
    
    def setup_roof_params_page(self):
        """Настройка страницы с параметрами кровли"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Заголовок
        header = QLabel("Параметры кровли")
        header.setStyleSheet("font-size: 18px; font-weight: bold; color: #0078d4; padding-bottom: 10px;")
        layout.addWidget(header)
        
        # Создаем форму для ввода данных
        form_group = QGroupBox()
        form_layout = QFormLayout(form_group)
        form_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        form_layout.setSpacing(15)
        
        # Параметры
        params = [
            ("Тип кровли по обрушаемости", "combo", ["1 тип", "2 тип", "3 тип"]),
            ("Сопротивление кровли (Rc, МПа)", "text", "45"),
            ("Трещиноватость (м)", "text", "0.5")
        ]
        
        for param_name, input_type, default in params:
            label = QLabel(param_name + ":")
            label.setStyleSheet("font-weight: bold;")
            
            if input_type == "text":
                input_widget = QLineEdit(default)
            else:
                input_widget = QComboBox()
                input_widget.addItems(default)
            
            self.inputs[param_name] = input_widget
            form_layout.addRow(label, input_widget)
        
        layout.addWidget(form_group)
        
        # Кнопки для навигации
        prev_button = QPushButton("< Назад")
        prev_button.clicked.connect(lambda: self.nav_list.setCurrentRow(0))
        next_button = QPushButton("Далее >")
        next_button.clicked.connect(lambda: self.nav_list.setCurrentRow(2))
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(prev_button)
        button_layout.addStretch()
        button_layout.addWidget(next_button)
        layout.addLayout(button_layout)
        
        # Добавляем пространство внизу
        layout.addStretch(1)
        
        # Добавляем страницу в стекированный виджет
        self.stacked_widget.addWidget(page)
    
    def setup_additional_params_page(self):
        """Настройка страницы с дополнительными параметрами"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Заголовок
        header = QLabel("Дополнительные параметры")
        header.setStyleSheet("font-size: 18px; font-weight: bold; color: #0078d4; padding-bottom: 10px;")
        layout.addWidget(header)
        
        # Создаем форму для ввода данных
        form_group = QGroupBox()
        form_layout = QFormLayout(form_group)
        form_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        form_layout.setSpacing(15)
        
        # Параметры
        params = [
            ("Коэффициент влажности", "text", "0.47"),
            ("Воздействие других выработок", "combo", ["Одиночная", "Сопряжение с пересечением", "Примыкающая"])
        ]
        
        for param_name, input_type, default in params:
            label = QLabel(param_name + ":")
            label.setStyleSheet("font-weight: bold;")
            
            if input_type == "text":
                input_widget = QLineEdit(default)
            else:
                input_widget = QComboBox()
                input_widget.addItems(default)
            
            self.inputs[param_name] = input_widget
            form_layout.addRow(label, input_widget)
        
        layout.addWidget(form_group)
        
        # Область для пользовательских параметров
        custom_header = QLabel("Пользовательские параметры:")
        custom_header.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 15px;")
        layout.addWidget(custom_header)
        
        # Область прокрутки для пользовательских параметров
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.NoFrame)
        
        # Виджет для пользовательских параметров
        self.custom_params_widget = QWidget()
        self.custom_params_layout = QFormLayout(self.custom_params_widget)
        self.custom_params_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.custom_params_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.custom_params_layout.setSpacing(15)
        
        # Загрузка пользовательских параметров из БД
        self.load_custom_parameters()
        
        scroll_area.setWidget(self.custom_params_widget)
        layout.addWidget(scroll_area)
        
        # Кнопки для навигации
        prev_button = QPushButton("< Назад")
        prev_button.clicked.connect(lambda: self.nav_list.setCurrentRow(1))
        next_button = QPushButton("Перейти к расчетам >")
        next_button.clicked.connect(lambda: self.nav_list.setCurrentRow(3))
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(prev_button)
        button_layout.addStretch()
        button_layout.addWidget(next_button)
        layout.addLayout(button_layout)
        
        # Добавляем страницу в стекированный виджет
        self.stacked_widget.addWidget(page)

    def load_custom_parameters(self):
        """Загрузка пользовательских параметров из БД"""
        if self.conn is None:
            return
            
        try:
            # Очищаем layout с пользовательскими параметрами
            while self.custom_params_layout.count() > 0:
                item = self.custom_params_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            
            # Загружаем параметры из БД
            self.cursor.execute("SELECT param_name, param_type, default_value FROM custom_parameters ORDER BY param_name")
            custom_params = self.cursor.fetchall()
            
            # Если нет пользовательских параметров, показываем сообщение
            if not custom_params:
                label = QLabel("Нет добавленных пользовательских параметров. Добавьте их в разделе 'Параметры пользователя'.")
                label.setStyleSheet("color: #777;")
                label.setWordWrap(True)
                self.custom_params_layout.addRow(label)
                return
                
            # Добавляем параметры в форму
            for param_name, param_type, default_value in custom_params:
                label = QLabel(param_name + ":")
                label.setStyleSheet("font-weight: bold;")
                
                if param_type == "text":
                    input_widget = QLineEdit(default_value)
                else:
                    input_widget = QComboBox()
                    # Разделяем значения по запятой, если это список
                    values = default_value.split(",")
                    input_widget.addItems(values)
                
                self.custom_params[param_name] = input_widget
                self.custom_params_layout.addRow(label, input_widget)
                
        except (psycopg2.Error, Exception) as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить пользовательские параметры: {e}")
    
    def setup_calculation_page(self):
        """Настройка страницы с расчетами и результатами"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Заголовок
        header = QLabel("Расчет и результаты")
        header.setStyleSheet("font-size: 18px; font-weight: bold; color: #0078d4; padding-bottom: 10px;")
        layout.addWidget(header)
        
        # Кнопки для расчёта
        button_group = QGroupBox("Выберите метод расчета:")
        button_layout = QHBoxLayout(button_group)
        button_layout.setSpacing(15)
        
        self.rule_button = QPushButton("Рассчитать по правилам")
        self.rf_button = QPushButton("Рассчитать с Random Forest")
        self.nn_button = QPushButton("Рассчитать с нейронной сетью")
        
        self.rule_button.clicked.connect(self.start_calculation_rules)
        self.rf_button.clicked.connect(self.start_calculation_rf)
        self.nn_button.clicked.connect(self.start_calculation_nn)
        
        button_layout.addWidget(self.rule_button)
        button_layout.addWidget(self.rf_button)
        button_layout.addWidget(self.nn_button)
        
        layout.addWidget(button_group)
        
        # Кнопка для сохранения результатов в БД
        save_layout = QHBoxLayout()
        self.save_button = QPushButton("Сохранить результаты в базу данных")
        self.save_button.setStyleSheet("background-color: #28a745; color: white;")
        self.save_button.clicked.connect(self.save_data_to_db)
        self.save_button.setEnabled(False)  # Изначально отключена, пока нет результатов
        save_layout.addStretch()
        save_layout.addWidget(self.save_button)
        layout.addLayout(save_layout)
        
        # Прогресс-бар для отображения процесса загрузки
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)  # Скрыт по умолчанию
        layout.addWidget(self.progress_bar)
        
        # Область для результатов
        result_group = QGroupBox("Результаты расчета:")
        result_layout = QVBoxLayout(result_group)
        
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        result_layout.addWidget(self.result_text)
        
        layout.addWidget(result_group)
        
        # Кнопка для навигации назад
        prev_button = QPushButton("< Назад")
        prev_button.clicked.connect(lambda: self.nav_list.setCurrentRow(2))
        
        back_layout = QHBoxLayout()
        back_layout.addWidget(prev_button)
        back_layout.addStretch()
        layout.addLayout(back_layout)
        
        # Добавляем страницу в стекированный виджет
        self.stacked_widget.addWidget(page)
        
    def setup_database_page(self):
        """Настройка страницы для просмотра базы данных"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Заголовок
        header = QLabel("База данных")
        header.setStyleSheet("font-size: 18px; font-weight: bold; color: #0078d4; padding-bottom: 10px;")
        layout.addWidget(header)
        
        # Кнопка обновления данных
        refresh_layout = QHBoxLayout()
        refresh_button = QPushButton("Обновить данные")
        refresh_button.clicked.connect(self.load_data_from_db)
        refresh_layout.addWidget(refresh_button)
        refresh_layout.addStretch()
        layout.addLayout(refresh_layout)
        
        # Таблица для отображения данных
        self.data_table = QTableWidget()
        self.data_table.setAlternatingRowColors(True)
        self.data_table.setEditTriggers(QTableWidget.NoEditTriggers)  # Только чтение
        self.data_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.data_table.setStyleSheet(
            "QTableWidget {border: 1px solid #dcdcdc; selection-background-color: #e6f2fa;}"
            "QHeaderView::section {background-color: #f0f2f5; padding: 6px; border: 1px solid #dcdcdc;}"
        )
        
        layout.addWidget(self.data_table)
        
        # Загружаем данные при первом открытии
        self.load_data_from_db()
        
        # Добавляем страницу в стекированный виджет
        self.stacked_widget.addWidget(page)
        
    def load_data_from_db(self):
        """Загрузка данных из БД в таблицу"""
        if self.conn is None:
            QMessageBox.warning(self, "Отсутствует подключение", "Нет подключения к базе данных")
            return
            
        try:
            # Получаем данные из БД
            self.cursor.execute("""
                SELECT id, mine_name, width, height, depth, section_shape, 
                       location, other_workings, roof_type, rc, humidity, 
                       fracture, date_added
                FROM mining_data
                ORDER BY date_added DESC
            """)
            data = self.cursor.fetchall()
            
            # Настраиваем таблицу
            columns = ["ID", "Шахта", "Ширина", "Высота", "Глубина", "Форма", 
                      "Расположение", "Другие выработки", "Тип кровли", "Rc", 
                      "Влажность", "Трещиноватость", "Дата добавления"]
            self.data_table.setColumnCount(len(columns))
            self.data_table.setHorizontalHeaderLabels(columns)
            self.data_table.setRowCount(len(data))
            
            # Заполняем таблицу данными
            for row_idx, row_data in enumerate(data):
                for col_idx, value in enumerate(row_data):
                    if value is not None:
                        item = QTableWidgetItem(str(value))
                        self.data_table.setItem(row_idx, col_idx, item)
            
            # Настраиваем ширину колонок
            header = self.data_table.horizontalHeader()
            for i in range(len(columns)):
                header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
            
        except psycopg2.Error as e:
            QMessageBox.critical(self, "Ошибка БД", f"Не удалось загрузить данные: {e}")
    
    def setup_user_params_page(self):
        """Настройка страницы для добавления пользовательских параметров"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Заголовок
        header = QLabel("Параметры пользователя")
        header.setStyleSheet("font-size: 18px; font-weight: bold; color: #0078d4; padding-bottom: 10px;")
        layout.addWidget(header)
        
        # Группа для добавления нового параметра
        new_param_group = QGroupBox("Добавить новый параметр")
        param_layout = QFormLayout(new_param_group)
        
        # Поля для нового параметра
        self.new_param_name = QLineEdit()
        self.new_param_type = QComboBox()
        self.new_param_type.addItems(["text", "combo"])
        self.new_param_default = QLineEdit()
        
        param_layout.addRow("Название параметра:", self.new_param_name)
        param_layout.addRow("Тип параметра:", self.new_param_type)
        param_layout.addRow("Значение по умолчанию:", self.new_param_default)
        
        # Описание для combo-box
        note_label = QLabel("Примечание: для типа 'combo' укажите варианты через запятую, например:import sys


    def setup_user_params_page(self):
    """Настройка страницы для добавления пользовательских параметров"""
    page = QWidget()
    layout = QVBoxLayout(page)
    
    # Заголовок
    header = QLabel("Параметры пользователя")
    header.setStyleSheet("font-size: 18px; font-weight: bold; color: #0078d4; padding-bottom: 10px;")
    layout.addWidget(header)
    
    # Группа для добавления нового параметра
    new_param_group = QGroupBox("Добавить новый параметр")
    param_layout = QFormLayout(new_param_group)
    
    # Поля для нового параметра
    self.new_param_name = QLineEdit()
    self.new_param_type = QComboBox()
    self.new_param_type.addItems(["text", "combo"])
    self.new_param_default = QLineEdit()
    
    param_layout.addRow("Название параметра:", self.new_param_name)
    param_layout.addRow("Тип параметра:", self.new_param_type)
    param_layout.addRow("Значение по умолчанию:", self.new_param_default)
    
    # Описание для combo-box
    note_label = QLabel("Примечание: для типа 'combo' укажите варианты через запятую, например: 'Вариант 1,Вариант 2,Вариант 3'")
    note_label.setWordWrap(True)
    note_label.setStyleSheet("color: #777; font-style: italic;")
    param_layout.addRow(note_label)
    
    layout.addWidget(new_param_group)
    
    # Кнопка для добавления параметра
    add_button = QPushButton("Добавить параметр")
    add_button.clicked.connect(self.add_custom_parameter)
    add_button.setStyleSheet("background-color: #28a745; color: white;")
    layout.addWidget(add_button)
    
    # Таблица существующих параметров
    table_group = QGroupBox("Существующие параметры")
    table_layout = QVBoxLayout(table_group)
    
    self.params_table = QTableWidget()
    self.params_table.setColumnCount(4)
    self.params_table.setHorizontalHeaderLabels(["ID", "Название", "Тип", "Значение по умолчанию"])
    self.params_table.setAlternatingRowColors(True)
    self.params_table.setSelectionBehavior(QTableWidget.SelectRows)
    self.params_table.setEditTriggers(QTableWidget.NoEditTriggers)
    self.params_table.setStyleSheet(
        "QTableWidget {border: 1px solid #dcdcdc; selection-background-color: #e6f2fa;}"
        "QHeaderView::section {background-color: #f0f2f5; padding: 6px; border: 1px solid #dcdcdc;}"
    )
    
    table_layout.addWidget(self.params_table)
    
    # Кнопки для управления параметрами
    button_layout = QHBoxLayout()
    refresh_button = QPushButton("Обновить список")
    refresh_button.clicked.connect(self.load_custom_parameter_list)
    delete_button = QPushButton("Удалить выбранный")
    delete_button.clicked.connect(self.delete_custom_parameter)
    delete_button.setStyleSheet("background-color: #dc3545; color: white;")
    
    button_layout.addWidget(refresh_button)
    button_layout.addWidget(delete_button)
    table_layout.addLayout(button_layout)
    
    layout.addWidget(table_group)
    
    # Загружаем список параметров при открытии страницы
    self.load_custom_parameter_list()
    
    # Добавляем страницу в стекированный виджет
    self.stacked_widget.addWidget(page)

def add_custom_parameter(self):
    """Добавление нового пользовательского параметра в БД"""
    if self.conn is None:
        QMessageBox.warning(self, "Отсутствует подключение", "Нет подключения к базе данных")
        return
        
    param_name = self.new_param_name.text().strip()
    param_type = self.new_param_type.currentText()
    default_value = self.new_param_default.text().strip()
    
    # Проверка заполнения полей
    if not param_name:
        QMessageBox.warning(self, "Ошибка", "Введите название параметра")
        return
        
    if not default_value:
        QMessageBox.warning(self, "Ошибка", "Введите значение по умолчанию")
        return
    
    try:
        # Проверка на уникальность имени параметра
        self.cursor.execute("SELECT 1 FROM custom_parameters WHERE param_name = %s", (param_name,))
        if self.cursor.fetchone():
            QMessageBox.warning(self, "Ошибка", f"Параметр с названием '{param_name}' уже существует")
            return
            
        # Добавление параметра в БД
        self.cursor.execute(
            "INSERT INTO custom_parameters (param_name, param_type, default_value) VALUES (%s, %s, %s)",
            (param_name, param_type, default_value)
        )
        self.conn.commit()
        
        # Очищаем поля ввода
        self.new_param_name.clear()
        self.new_param_default.clear()
        
        # Обновляем список параметров
        self.load_custom_parameter_list()
        
        QMessageBox.information(self, "Успех", f"Параметр '{param_name}' успешно добавлен")
        
    except psycopg2.Error as e:
        QMessageBox.critical(self, "Ошибка БД", f"Не удалось добавить параметр: {e}")

def load_custom_parameter_list(self):
    """Загрузка списка пользовательских параметров в таблицу"""
    if self.conn is None:
        return
        
    try:
        # Получаем данные из БД
        self.cursor.execute("SELECT id, param_name, param_type, default_value FROM custom_parameters ORDER BY param_name")
        params = self.cursor.fetchall()
        
        # Настраиваем таблицу
        self.params_table.setRowCount(len(params))
        
        # Заполняем таблицу данными
        for row_idx, (param_id, param_name, param_type, default_value) in enumerate(params):
            self.params_table.setItem(row_idx, 0, QTableWidgetItem(str(param_id)))
            self.params_table.setItem(row_idx, 1, QTableWidgetItem(param_name))
            self.params_table.setItem(row_idx, 2, QTableWidgetItem(param_type))
            self.params_table.setItem(row_idx, 3, QTableWidgetItem(default_value))
        
        # Настраиваем ширину колонок
        header = self.params_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        
    except psycopg2.Error as e:
        QMessageBox.critical(self, "Ошибка БД", f"Не удалось загрузить параметры: {e}")

def delete_custom_parameter(self):
    """Удаление выбранного пользовательского параметра"""
    if self.conn is None:
        QMessageBox.warning(self, "Отсутствует подключение", "Нет подключения к базе данных")
        return
        
    # Получаем выбранную строку
    selected_rows = self.params_table.selectedItems()
    if not selected_rows:
        QMessageBox.warning(self, "Предупреждение", "Выберите параметр для удаления")
        return
        
    # Получаем ID выбранного параметра
    selected_row = selected_rows[0].row()
    param_id = self.params_table.item(selected_row, 0).text()
    param_name = self.params_table.item(selected_row, 1).text()
    
    # Подтверждение удаления
    reply = QMessageBox.question(
        self,
        "Подтверждение",
        f"Вы уверены, что хотите удалить параметр '{param_name}'?",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )
    
    if reply == QMessageBox.Yes:
        try:
            # Удаление из БД
            self.cursor.execute("DELETE FROM custom_parameters WHERE id = %s", (param_id,))
            self.conn.commit()
            
            # Обновление таблицы
            self.load_custom_parameter_list()
            
            QMessageBox.information(self, "Успех", f"Параметр '{param_name}' успешно удален")
            
        except psycopg2.Error as e:
            QMessageBox.critical(self, "Ошибка БД", f"Не удалось удалить параметр: {e}")

def save_data_to_db(self):
    """Сохранение результатов расчета в базу данных"""
    if self.conn is None:
        QMessageBox.warning(self, "Отсутствует подключение", "Нет подключения к базе данных")
        return
    
    # Проверяем, что расчет был выполнен
    if self.result_text.toPlainText() == "" or "Выполняется расчет..." in self.result_text.toPlainText():
        QMessageBox.warning(self, "Предупреждение", "Сначала выполните расчет")
        return
    
    try:
        # Получаем все введенные данные
        mine_name = self.inputs["Шахта"].text()
        width = float(self.inputs["Ширина выработки (м)"].text())
        height = float(self.inputs["Высота выработки (м)"].text())
        depth = float(self.inputs["Глубина выработки (м)"].text())
        section_shape = self.inputs["Форма сечения"].currentText()
        location = self.inputs["Расположение выработки"].currentText()
        roof_type = self.inputs["Тип кровли по обрушаемости"].currentText()
        rc = float(self.inputs["Сопротивление кровли (Rc, МПа)"].text())
        humidity = float(self.inputs["Коэффициент влажности"].text())
        fracture = float(self.inputs["Трещиноватость (м)"].text())
        other_workings = self.inputs["Воздействие других выработок"].currentText()
        
        # Подготавливаем пользовательские параметры в формате JSON
        custom_params = {}
        for name, widget in self.custom_params.items():
            if isinstance(widget, QLineEdit):
                custom_params[name] = widget.text()
            elif isinstance(widget, QComboBox):
                custom_params[name] = widget.currentText()
        
        # Сохраняем в БД
        self.cursor.execute("""
            INSERT INTO mining_data (
                mine_name, width, height, depth, section_shape, location, 
                other_workings, roof_type, rc, humidity, fracture, custom_params
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (mine_name, width, height, depth, section_shape, location, 
             other_workings, roof_type, rc, humidity, fracture, 
             psycopg2.extras.Json(custom_params) if custom_params else None))
        
        self.conn.commit()
        QMessageBox.information(self, "Успех", "Данные успешно сохранены в базу данных")
        
    except (ValueError, psycopg2.Error) as e:
        QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить данные: {e}")

def export_results(self):
    """Экспорт результатов расчета в текстовый файл"""
    # Проверяем, что расчет был выполнен
    if self.result_text.toPlainText() == "" or "Выполняется расчет..." in self.result_text.toPlainText():
        QMessageBox.warning(self, "Предупреждение", "Сначала выполните расчет")
        return
        
    # Получаем путь для сохранения файла
    file_path, _ = QFileDialog.getSaveFileName(
        self, 
        "Сохранить результаты", 
        f"результаты_расчета_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt",
        "Текстовые файлы (*.txt);;Все файлы (*)"
    )
    
    if not file_path:
        return
        
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            # Записываем входные параметры
            file.write("===== ЭКСПЕРТНАЯ СИСТЕМА ДЛЯ АНКЕРНОГО КРЕПЛЕНИЯ =====\n\n")
            file.write(f"Дата и время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            file.write("--- ВХОДНЫЕ ПАРАМЕТРЫ ---\n")
            file.write(f"Шахта: {self.inputs['Шахта'].text()}\n")
            file.write(f"Ширина выработки: {self.inputs['Ширина выработки (м)'].text()} м\n")
            file.write(f"Высота выработки: {self.inputs['Высота выработки (м)'].text()} м\n")
            file.write(f"Глубина выработки: {self.inputs['Глубина выработки (м)'].text()} м\n")
            file.write(f"Форма сечения: {self.inputs['Форма сечения'].currentText()}\n")
            file.write(f"Расположение выработки: {self.inputs['Расположение выработки'].currentText()}\n")
            file.write(f"Тип кровли: {self.inputs['Тип кровли по обрушаемости'].currentText()}\n")
            file.write(f"Сопротивление кровли: {self.inputs['Сопротивление кровли (Rc, МПа)'].text()} МПа\n")
            file.write(f"Коэффициент влажности: {self.inputs['Коэффициент влажности'].text()}\n")
            file.write(f"Трещиноватость: {self.inputs['Трещиноватость (м)'].text()} м\n")
            file.write(f"Воздействие других выработок: {self.inputs['Воздействие других выработок'].currentText()}\n\n")
            
            # Если есть пользовательские параметры, добавляем их
            if self.custom_params:
                file.write("--- ПОЛЬЗОВАТЕЛЬСКИЕ ПАРАМЕТРЫ ---\n")
                for name, widget in self.custom_params.items():
                    if isinstance(widget, QLineEdit):
                        file.write(f"{name}: {widget.text()}\n")
                    elif isinstance(widget, QComboBox):
                        file.write(f"{name}: {widget.currentText()}\n")
                file.write("\n")
            
            # Записываем результаты
            file.write("--- РЕЗУЛЬТАТЫ РАСЧЕТА ---\n")
            # Убираем HTML-теги из результатов
            plain_result = self.result_text.toPlainText()
            file.write(plain_result)
        
        QMessageBox.information(self, "Успех", f"Результаты сохранены в файл:\n{file_path}")
        
    except Exception as e:
        QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить результаты: {e}")

# Модифицируем setup_calculation_page для добавления кнопки экспорта
def setup_calculation_page(self):
    """Настройка страницы с расчетами и результатами"""
    page = QWidget()
    layout = QVBoxLayout(page)
    
    # Заголовок
    header = QLabel("Расчет и результаты")
    header.setStyleSheet("font-size: 18px; font-weight: bold; color: #0078d4; padding-bottom: 10px;")
    layout.addWidget(header)
    
    # Кнопки для расчёта
    button_group = QGroupBox("Выберите метод расчета:")
    button_layout = QHBoxLayout(button_group)
    button_layout.setSpacing(15)
    
    self.rule_button = QPushButton("Рассчитать по правилам")
    self.rf_button = QPushButton("Рассчитать с Random Forest")
    self.nn_button = QPushButton("Рассчитать с нейронной сетью")
    
    self.rule_button.clicked.connect(self.start_calculation_rules)
    self.rf_button.clicked.connect(self.start_calculation_rf)
    self.nn_button.clicked.connect(self.start_calculation_nn)
    
    button_layout.addWidget(self.rule_button)
    button_layout.addWidget(self.rf_button)
    button_layout.addWidget(self.nn_button)
    
    layout.addWidget(button_group)
    
    # Кнопки для сохранения и экспорта результатов
    save_layout = QHBoxLayout()
    self.save_button = QPushButton("Сохранить результаты в базу данных")
    self.save_button.setStyleSheet("background-color: #28a745; color: white;")
    self.save_button.clicked.connect(self.save_data_to_db)
    self.save_button.setEnabled(False)  # Изначально отключена, пока нет результатов
    
    self.export_button = QPushButton("Экспорт результатов в файл")
    self.export_button.setStyleSheet("background-color: #17a2b8; color: white;")
    self.export_button.clicked.connect(self.export_results)
    self.export_button.setEnabled(False)  # Изначально отключена, пока нет результатов
    
    save_layout.addStretch()
    save_layout.addWidget(self.save_button)
    save_layout.addWidget(self.export_button)
    layout.addLayout(save_layout)
    
    # Прогресс-бар для отображения процесса загрузки
    self.progress_bar = QProgressBar()
    self.progress_bar.setRange(0, 100)
    self.progress_bar.setValue(0)
    self.progress_bar.setVisible(False)  # Скрыт по умолчанию
    layout.addWidget(self.progress_bar)
    
    # Область для результатов
    result_group = QGroupBox("Результаты расчета:")
    result_layout = QVBoxLayout(result_group)
    
    self.result_text = QTextEdit()
    self.result_text.setReadOnly(True)
    result_layout.addWidget(self.result_text)
    
    layout.addWidget(result_group)
    
    # Кнопка для навигации назад
    prev_button = QPushButton("< Назад")
    prev_button.clicked.connect(lambda: self.nav_list.setCurrentRow(2))
    
    back_layout = QHBoxLayout()
    back_layout.addWidget(prev_button)
    back_layout.addStretch()
    layout.addLayout(back_layout)
    
    # Добавляем страницу в стекированный виджет
    self.stacked_widget.addWidget(page)

# Модифицируем функции finish_calculation для активации кнопок сохранения и экспорта
def finish_calculation(self, result_text):
    # Завершаем расчет, устанавливаем результат и скрываем прогресс-бар
    self.progress_bar.setValue(100)
    self.result_text.setHtml(result_text)
    
    # Снова включаем кнопки
    self.rule_button.setEnabled(True)
    self.rf_button.setEnabled(True)
    self.nn_button.setEnabled(True)
    
    # Активируем кнопки сохранения и экспорта
    self.save_button.setEnabled(True)
    self.export_button.setEnabled(True)
    
    # Скрываем прогресс-бар через небольшую задержку
    QTimer.singleShot(1000, lambda: self.progress_bar.setVisible(False))

# Для полной поддержки JSONB в PostgreSQL добавим импорт
def init_database(self):
    """Инициализация подключения к PostgreSQL и создание таблиц, если их нет"""
    try:
        # Импорт дополнительных модулей для PostgreSQL
        import psycopg2.extras
        
        # Настройки подключения к PostgreSQL
        self.db_config = {
            "host": "localhost",
            "database": "mining_support",
            "user": "postgres",
            "password": "postgres",
            "port": "5432"
        }
        
        # Подключение к БД
        self.conn = psycopg2.connect(**self.db_config)
        self.cursor = self.conn.cursor()
        
        # Создаём таблицу для хранения данных, если её ещё нет
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS mining_data (
                id SERIAL PRIMARY KEY,
                mine_name VARCHAR(100),
                width FLOAT,
                height FLOAT,
                depth FLOAT,
                section_shape VARCHAR(50),
                location VARCHAR(100),
                other_workings VARCHAR(100),
                roof_type VARCHAR(20),
                rc FLOAT,
                humidity FLOAT,
                fracture FLOAT,
                custom_params JSONB,
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Создаём таблицу для пользовательских параметров
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS custom_parameters (
                id SERIAL PRIMARY KEY,
                param_name VARCHAR(100) UNIQUE,
                param_type VARCHAR(20),
                default_value VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.conn.commit()
        
    except psycopg2.Error as e:
        QMessageBox.critical(self, "Ошибка БД", f"Не удалось подключиться к базе данных: {e}")
        # Если не удалось подключиться к БД, работаем без неё
        self.conn = None
        self.cursor = None

# Добавляем в класс метод для импорта/экспорта настроек проекта
def export_project_settings(self):
    """Экспорт текущих настроек проекта в JSON-файл"""
    file_path, _ = QFileDialog.getSaveFileName(
        self, 
        "Экспорт настроек проекта", 
        f"проект_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json",
        "JSON-файлы (*.json);;Все файлы (*)"
    )
    
    if not file_path:
        return
        
    try:
        # Собираем все настройки в словарь
        settings = {
            "mine_info": {
                "mine_name": self.inputs["Шахта"].text(),
                "width": self.inputs["Ширина выработки (м)"].text(),
                "height": self.inputs["Высота выработки (м)"].text(),
                "depth": self.inputs["Глубина выработки (м)"].text(),
                "section_shape": self.inputs["Форма сечения"].currentText(),
                "location": self.inputs["Расположение выработки"].currentText()
            },
            "roof_params": {
                "roof_type": self.inputs["Тип кровли по обрушаемости"].currentText(),
                "rc": self.inputs["Сопротивление кровли (Rc, МПа)"].text(),
                "fracture": self.inputs["Трещиноватость (м)"].text()
            },
            "additional_params": {
                "humidity": self.inputs["Коэффициент влажности"].text(),
                "other_workings": self.inputs["Воздействие других выработок"].currentText()
            },
            "custom_params": {}
        }
        
        # Добавляем пользовательские параметры
        for name, widget in self.custom_params.items():
            if isinstance(widget, QLineEdit):
                settings["custom_params"][name] = widget.text()
            elif isinstance(widget, QComboBox):
                settings["custom_params"][name] = widget.currentText()
        
        # Сохраняем в файл
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(settings, file, ensure_ascii=False, indent=4)
            
        QMessageBox.information(self, "Успех", f"Настройки проекта сохранены в файл:\n{file_path}")
        
    except Exception as e:
        QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить настройки проекта: {e}")

def import_project_settings(self):
    """Импорт настроек проекта из JSON-файла"""
    file_path, _ = QFileDialog.getOpenFileName(
        self, 
        "Импорт настроек проекта", 
        "",
        "JSON-файлы (*.json);;Все файлы (*)"
    )
    
    if not file_path:
        return
        
    try:
        # Загружаем настройки из файла
        with open(file_path, 'r', encoding='utf-8') as file:
            settings = json.load(file)
        
        # Применяем настройки к интерфейсу
        # Mine info
        if "mine_info" in settings:
            mine_info = settings["mine_info"]
            self.inputs["Шахта"].setText(mine_info.get("mine_name", ""))
            self.inputs["Ширина выработки (м)"].setText(mine_info.get("width", ""))
            self.inputs["Высота выработки (м)"].setText(mine_info.get("height", ""))
            self.inputs["Глубина выработки (м)"].setText(mine_info.get("depth", ""))
            
            if "section_shape" in mine_info:
                index = self.inputs["Форма сечения"].findText(mine_info["section_shape"])
                if index >= 0:
                    self.inputs["Форма сечения"].setCurrentIndex(index)
                    
            if "location" in mine_info:
                index = self.inputs["Расположение выработки"].findText(mine_info["location"])
                if index >= 0:
                    self.inputs["Расположение выработки"].setCurrentIndex(index)
        
        # Roof params
        if "roof_params" in settings:
            roof_params = settings["roof_params"]
            
            if "roof_type" in roof_params:
                index = self.inputs["Тип кровли по обрушаемости"].findText(roof_params["roof_type"])
                if index >= 0:
                    self.inputs["Тип кровли по обрушаемости"].setCurrentIndex(index)
                    
            self.inputs["Сопротивление кровли (Rc, МПа)"].setText(roof_params.get("rc", ""))
            self.inputs["Трещиноватость (м)"].setText(roof_params.get("fracture", ""))
        
        # Additional params
        if "additional_params" in settings:
            add_params = settings["additional_params"]
            self.inputs["Коэффициент влажности"].setText(add_params.get("humidity", ""))
            
            if "other_workings" in add_params:
                index = self.inputs["Воздействие других выработок"].findText(add_params["other