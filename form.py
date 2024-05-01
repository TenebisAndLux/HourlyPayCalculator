import sys

from PyQt5.QtWidgets import QApplication

from ui import Form

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Form()
    window.show()
    sys.exit(app.exec_())
