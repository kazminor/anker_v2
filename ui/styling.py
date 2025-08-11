# ui/styling.py
from PyQt5.QtWidgets import QStyleFactory

def apply_styles(app):
    app.setStyle(QStyleFactory.create("Fusion"))
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f5f5f5;
        }
        QWidget {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 14px;
            color: #333;
        }
        QPushButton { 
            background-color: #2196F3; 
            color: white; 
            padding: 10px 20px; 
            border-radius: 6px; 
            border: none;
            font-size: 15px;
            font-weight: 500;
        }
        QPushButton:hover { 
            background-color: #1976D2; 
        }
        QPushButton:pressed {
            background-color: #1565C0;
        }
        QLineEdit, QComboBox { 
            border: 1px solid #d0d0d0; 
            padding: 8px; 
            border-radius: 4px; 
            background-color: #fff;
            font-size: 14px;
        }
        QLineEdit:focus, QComboBox:focus {
            border: 1px solid #2196F3;
            outline: none;
        }
        QComboBox::drop-down {
            border: none;
            padding-right: 10px;
        }
        QComboBox::down-arrow {
            image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAFCAYAAAC3pW8lAAAAAXNSR0IArs4c6QAAAERlWElmTU0AKgAAAAgAAYdpAAQAAAABAAAAGgAAAAAAA6ABAAMAAAABAAEAAKACAAQAAAABAAAAPKADAAQAAAABAAAABAAAAADUt6p9AAAACXBIWXMAAAsTAAALEwEAmpwYAAAANklEQVR4nGP4//8/A7mBQQYGBob/Hz9+MPj//+cPqGZmZvr//v0zMDIy8v//Z2BwcPD//48fAACl8xG1vKxryQAAAABJRU5ErkJggg==);
            width: 10px;
            height: 5px;
        }
        QListWidget { 
            border: none; 
            background-color: #ffffff; 
            border-radius: 6px;
            padding: 5px;
        }
        QListWidget::item { 
            padding: 12px; 
            border-radius: 4px;
        }
        QListWidget::item:selected { 
            background-color: #2196F3; 
            color: white; 
        }
        QScrollArea {
            border: none;
            background-color: transparent;
        }
        QTextEdit {
            border: 1px solid #d0d0d0;
            border-radius: 4px;
            padding: 10px;
            background-color: #fff;
        }
        QLabel {
            color: #333;
        }
    """)