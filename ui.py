from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QLineEdit, QTextEdit, QGridLayout, QHBoxLayout,
                             QVBoxLayout, QFrame, QFileDialog)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from style import stylesheet
from calc import load_data_from_file, save_data_to_file, add_time, calculate_monthly_hours


class Form(QWidget):
    def __init__(self):
        super().__init__()

        self.last_path = "data/work_hours.txt"
        self.initUi()
        self.data = load_data_from_file(self.last_path)

    def initUi(self):
        self.setWindowTitle('HourlyPayCalculator')
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

        self.save_button = QPushButton('Сохранить', self.border_frame)
        self.save_button.clicked.connect(self.save_data)

        self.load_button = QPushButton('Загрузить', self.border_frame)
        self.load_button.clicked.connect(self.load_data)

        self.close_button = QPushButton('X', self.border_frame)
        self.close_button.clicked.connect(self.close)
        self.close_button.setFixedSize(30, 30)
        self.close_button.setStyleSheet("border-radius: 15px; background-color: #579D01;")

        self.minimize_button = QPushButton('-', self.border_frame)
        self.minimize_button.clicked.connect(self.showMinimized)
        self.minimize_button.setFixedSize(30, 30)
        self.minimize_button.setStyleSheet("border-radius: 15px; background-color: #579D01;")

        header_frame = QFrame(self)
        header_frame.setFrameShape(QFrame.NoFrame)
        header_frame.setStyleSheet("border-bottom: 0px;")

        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(5, 2, 5, 2)

        icon = QLabel(header_frame)
        icon.setPixmap(QPixmap('data/gg.png'))
        icon.setStyleSheet("border: 0px;")
        header_layout.addWidget(icon)

        title = QLabel(self.windowTitle(), header_frame)
        title.setStyleSheet("border: 0px;")
        header_layout.addWidget(title, alignment=Qt.AlignCenter)

        button_container = QWidget()
        button_container.setStyleSheet("border: 0px;")
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.addWidget(self.minimize_button)
        button_layout.addWidget(self.close_button)
        button_layout.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(button_container, alignment=Qt.AlignRight)
        header_layout.addWidget(button_container, alignment=Qt.AlignRight)

        layout = QGridLayout(self.border_frame)
        layout.addWidget(self.file_contents, 0, 0, 1, 3)
        layout.addWidget(self.salary_label, 1, 0, 1, 1)
        layout.addWidget(self.salary_input, 1, 1, 1, 1)
        layout.addWidget(self.time_label, 2, 0, 1, 1)
        layout.addWidget(self.time_input, 2, 1, 1, 1)

        button_row3 = QHBoxLayout()
        button_row3.addWidget(self.add_button)
        button_row3.addWidget(self.delete_button)
        layout.addLayout(button_row3, 3, 0, 1, 1)

        layout.addWidget(self.calculate_button, 3, 2, 1, 1)

        button_row4 = QHBoxLayout()
        button_row4.addWidget(self.load_button)
        button_row4.addWidget(self.save_button)
        layout.addLayout(button_row4, 4, 0, 1, 1)

        layout.addWidget(self.clear_button, 4, 2, 1, 1)

        layout.addWidget(self.output_field, 5, 0, 1, 3)

        main_layout = QVBoxLayout()
        main_layout.addWidget(header_frame)
        main_layout.addWidget(self.border_frame)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

    def save_data(self):
        path = QFileDialog.getSaveFileName(self, 'Сохранить файл', self.last_path,
                                           "CSV (*.csv);;Excel (*.xlsx);;Текстовый файл (*.txt)")[0]
        if path:
            self.last_path = path
            save_data_to_file(self.data, path)

    def load_data(self):
        path = QFileDialog.getOpenFileName(self, 'Загрузить файл', self.last_path,
                                           "CSV (*.csv);;Excel (*.xlsx);;Текстовый файл (*.txt)")[0]
        if path:
            self.last_path = path
            self.data = load_data_from_file(path)
            self.update_file_contents()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def update_file_contents(self):
        data = load_data_from_file(self.last_path)
        if data:
            text = '\n'.join(str(value) for value in data)
            self.file_contents.setPlainText(text)
        else:
            self.file_contents.setPlainText('empty')

    def add_time(self):
        time_str = self.time_input.text()
        try:
            add_time(self.data, time_str, self.last_path)
            self.update_file_contents()
            self.output_field.setPlainText("Значение добавлено.")
        except ValueError:
            self.output_field.setPlainText("Неверный формат времени.")

    def delete_time(self):
        if self.data:
            self.data.pop()
            save_data_to_file(self.data, self.last_path)
            self.output_field.setPlainText("Последнее значение удалено.")
            self.update_file_contents()

    def clear_data(self):
        self.data = []
        save_data_to_file(self.data, self.last_path)
        self.output_field.setPlainText("Файл очищен.")
        self.update_file_contents()

    def calculate_data(self):
        if (self.salary_input.text()) == '':
            salary = 625
        else:
            salary = (self.salary_input.text())
        output_text = calculate_monthly_hours(self.data, float(salary))
        self.output_field.setPlainText(output_text)
