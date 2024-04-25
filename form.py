import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTextEdit, QGridLayout
from PyQt5.QtCore import Qt

from calc import load_data_from_file, save_data_to_file, add_time, calculate_monthly_hours


class Form(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('data/gg.png'))
        self.setWindowTitle('HourlyPayCalculator')
        resolution = QApplication.primaryScreen().size()

        self.setStyleSheet("""
            QWidget {
                background-color: #1A4B32;
                color: white;
                font-size: 20px;
            }
            QLabel {
                font-size: 20px;
            }
            QLineEdit {
                background-color: #579D01;
                color: white;
                font-size: 20px;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton {
                background-color: #579D01;
                color: white;
                font-size: 20px;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QTextEdit {
                background-color: #579D01;
                color: white;
                font-size: 20px;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
        """)

        width, height = resolution.width(), resolution.height()
        self.setGeometry(int(width / 2.2), int(height / 4), 400, 740)
        self.data = load_data_from_file()
        self.file_contents = QTextEdit()
        self.file_contents.setReadOnly(True)
        self.update_file_contents()

        self.salary_label = QLabel('Почасовая зарплата:')
        self.salary_input = QLineEdit()
        self.salary_input.setPlaceholderText("625")

        self.time_label = QLabel('Добавляемое значение:')
        self.time_input = QLineEdit()

        self.output_field = QTextEdit()
        self.output_field.setReadOnly(True)

        self.add_button = QPushButton('Добавить')
        self.add_button.clicked.connect(self.add_time)

        self.delete_button = QPushButton('Удалить')
        self.delete_button.clicked.connect(self.delete_time)

        self.clear_button = QPushButton('Очистить')
        self.clear_button.clicked.connect(self.clear_data)

        self.calculate_button = QPushButton('Посчитать')
        self.calculate_button.clicked.connect(self.calculate_data)

        layout = QGridLayout()
        layout.addWidget(self.file_contents, 0, 0, 1, 3)
        layout.addWidget(self.salary_label, 1, 0)
        layout.addWidget(self.salary_input, 1, 1)
        layout.addWidget(self.time_label, 2, 0)
        layout.addWidget(self.time_input, 2, 1)
        layout.addWidget(self.add_button, 2, 2)
        layout.addWidget(self.delete_button, 3, 2)
        layout.addWidget(self.clear_button, 4, 2)
        layout.addWidget(self.calculate_button, 5, 2)
        layout.addWidget(self.output_field, 6, 0, 1, 3)
        self.setLayout(layout)

    def update_file_contents(self):
        data = load_data_from_file()
        if data:
            text = '\n'.join(str(value) for value in data)
            self.file_contents.setPlainText(text)
        else:
            self.file_contents.setPlainText('empty')

    def add_time(self):
        time_str = self.time_input.text()
        try:
            add_time(self.data, time_str)
            self.update_file_contents()
            print("Значение добавлено.")
        except ValueError:
            print("Неверный формат времени.")

    def delete_time(self):
        if self.data:
            self.data.pop()
            save_data_to_file(self.data)
            print("Последнее значение удалено.")
            self.update_file_contents()

    def clear_data(self):
        self.data = []
        save_data_to_file(self.data)
        print("Файл очищен.")
        self.update_file_contents()

    def calculate_data(self):
        if (self.salary_input.text()) == '':
            salary = 625
        else:
            salary = (self.salary_input.text())
        output_text = calculate_monthly_hours(self.data, float(salary))
        self.output_field.setPlainText(output_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())

