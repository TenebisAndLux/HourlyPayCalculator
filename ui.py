from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QLineEdit, QTextEdit, QGridLayout, QHBoxLayout,
                             QVBoxLayout, QFrame)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from style import stylesheet
from calc import load_data_from_file, save_data_to_file, add_time, calculate_monthly_hours


class Form(QWidget):
    def __init__(self):
        super().__init__()

        self.initUi()
        self.data = load_data_from_file()

    def initUi(self):
        self.setWindowTitle('HourlyPayCalculator')
        self.setWindowIcon(QIcon('data/gg.png'))
        self.setStyleSheet(stylesheet)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(400, 740)

        self.border_frame = QFrame(self)
        self.border_frame.setFrameShape(QFrame.StyledPanel)
        self.border_frame.setFrameShadow(QFrame.Raised)
        self.border_frame.setContentsMargins(10, 30, 10, 10)

        self.file_contents = QTextEdit(self.border_frame)
        self.file_contents.setReadOnly(True)
        self.update_file_contents()

        self.salary_label = QLabel('Почасовая зарплата:', self.border_frame)
        self.salary_input = QLineEdit(self.border_frame)
        self.salary_input.setPlaceholderText("625")

        self.time_label = QLabel('Добавляемое значение:', self.border_frame)
        self.time_input = QLineEdit(self.border_frame)

        self.output_field = QTextEdit(self.border_frame)
        self.output_field.setReadOnly(True)

        self.add_button = QPushButton('Добавить', self.border_frame)
        self.add_button.clicked.connect(self.add_time)

        self.delete_button = QPushButton('Удалить', self.border_frame)
        self.delete_button.clicked.connect(self.delete_time)

        self.clear_button = QPushButton('Очистить', self.border_frame)
        self.clear_button.clicked.connect(self.clear_data)

        self.calculate_button = QPushButton('Посчитать', self.border_frame)
        self.calculate_button.clicked.connect(self.calculate_data)

        self.close_button = QPushButton('X', self.border_frame)
        self.close_button.clicked.connect(self.close)
        self.close_button.setFixedSize(30, 30)
        self.close_button.setStyleSheet("border-radius: 15px; background-color: #579D01;")

        self.minimize_button = QPushButton('-', self.border_frame)
        self.minimize_button.clicked.connect(self.showMinimized)
        self.minimize_button.setFixedSize(30, 30)
        self.minimize_button.setStyleSheet("border-radius: 15px; background-color: #579D01;")

        header_layout = QHBoxLayout()
        header_layout.addStretch()

        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(500, 3, 9, 3)
        button_layout.addWidget(self.minimize_button)
        button_layout.addWidget(self.close_button)
        button_layout.setAlignment(Qt.AlignCenter)

        header_layout.addWidget(button_container)

        layout = QGridLayout(self.border_frame)
        layout.addWidget(self.file_contents, 0, 0, 1, 3)
        layout.addWidget(self.salary_label, 1, 0, 1, 1)
        layout.addWidget(self.salary_input, 1, 1, 1, 1)
        layout.addWidget(self.time_label, 2, 0, 1, 1)
        layout.addWidget(self.time_input, 2, 1, 1, 1)
        layout.addWidget(self.add_button, 2, 2, 1, 1)
        layout.addWidget(self.delete_button, 3, 2, 1, 1)
        layout.addWidget(self.clear_button, 4, 2, 1, 1)
        layout.addWidget(self.calculate_button, 5, 2, 1, 1)
        layout.addWidget(self.output_field, 6, 0, 1, 3)

        main_layout = QVBoxLayout()
        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.border_frame)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

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
            self.output_field.setPlainText("Значение добавлено.")
        except ValueError:
            self.output_field.setPlainText("Неверный формат времени.")

    def delete_time(self):
        if self.data:
            self.data.pop()
            save_data_to_file(self.data)
            self.output_field.setPlainText("Последнее значение удалено.")
            self.update_file_contents()

    def clear_data(self):
        self.data = []
        save_data_to_file(self.data)
        self.output_field.setPlainText("Файл очищен.")
        self.update_file_contents()

    def calculate_data(self):
        if (self.salary_input.text()) == '':
            salary = 625
        else:
            salary = (self.salary_input.text())
        output_text = calculate_monthly_hours(self.data, float(salary))
        self.output_field.setPlainText(output_text)
