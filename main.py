# main.py
from PyQt5.QtWidgets import QApplication
import sys
from ui.main_window import MiningSupportApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MiningSupportApp()
    window.show()
    sys.exit(app.exec_())