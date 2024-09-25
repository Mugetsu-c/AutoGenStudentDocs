import sys
import os
sys.path.append(os.getcwd())

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
)
from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtGui import QFont, QIcon
from datetime import datetime
from App.Model.DataAccess import CSVDataHandler
from App.Model.Students import Student
from App.View.Styles import style_sheet
from App.Model.DocumentGenerator import DocumentGenerator
from App.Model.BusinessLogic import get_path_save




class UserInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Приложение для обработки заявок")
        self.setGeometry(100, 100, 1200, 600)  # Устанавливаем размер окна
        self.csv_handler = CSVDataHandler()
        self.students = []
        self.filtered_students = []

        print(os.path)
        
        self.init_ui()
        self.apply_styles()
        # Связываем сигнал изменения ячейки с методом
        self.table.itemChanged.connect(self.on_item_changed)

    def init_ui(self):
        # Главный виджет и макет
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Верхняя панель с кнопками
        button_layout = QHBoxLayout()

        # Кнопка "Обновить базу данных"
        self.update_button = QPushButton("Обновить базу данных")
        self.update_button.clicked.connect(self.update_database)
        button_layout.addWidget(self.update_button)

        # Выбор временного интервала
        self.time_frame_combo = QComboBox()
        self.time_frame_combo.addItems(["24", "48", "72", "178"])
        self.time_frame_combo.setPlaceholderText("Выберите время (часы)")
        button_layout.addWidget(self.time_frame_combo)

        # Кнопка "Загрузить данные"
        self.load_button = QPushButton("Загрузить данные")
        self.load_button.clicked.connect(self.load_data)
        button_layout.addWidget(self.load_button)

        # Кнопка "Генерация"
        self.generate_button = QPushButton("Генерация")
        self.generate_button.clicked.connect(self.generate_documents)
        button_layout.addWidget(self.generate_button)

        main_layout.addLayout(button_layout)

        # Таблица для отображения данных
        self.table = QTableWidget()
        self.table.setColumnCount(11)
        self.table.setHorizontalHeaderLabels([
            'ФИО', 'Группа', 'Курс', 'Форма обучения', 'Основа обучения', 'Дата зачисления', 'Срок обучения', 
            'Приказ зачисления','Куда нужна справка', 'Количество', 'Отметка времени'
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.DoubleClicked)

        main_layout.addWidget(self.table)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def apply_styles(self):
        self.setStyleSheet(style_sheet)

    def update_database(self):
        self.csv_handler.download_csv()
        QMessageBox.information(self, "Обновление базы данных", "База данных успешно обновлена.")

    def load_data(self):
        time_frame = self.time_frame_combo.currentText()
        if not time_frame:
            QMessageBox.warning(self, "Внимание", "Пожалуйста, выберите временной интервал.")
            return

        raw_data = self.csv_handler.load_data(int(time_frame))
        self.students = self.csv_handler.parse_data_to_students(raw_data)
            
        self.display_data()

    def display_data(self):
        self.table.setRowCount(0)
        for student in self.students:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

            self.table.setItem(row_position, 0, QTableWidgetItem(student.full_name))
            self.table.setItem(row_position, 1, QTableWidgetItem(student.group))
            self.table.setItem(row_position, 2, QTableWidgetItem(str(student.course)))
            self.table.setItem(row_position, 3, QTableWidgetItem(student.study_form))
            self.table.setItem(row_position, 4, QTableWidgetItem(student.study_base if student.study_base else ''))
            self.table.setItem(row_position, 5, QTableWidgetItem(str(student.date_of_receipt) if student.date_of_receipt else ''))
            self.table.setItem(row_position, 6, QTableWidgetItem(str(student.study_duration) if student.study_duration else ''))
            self.table.setItem(row_position, 7, QTableWidgetItem(student.order_number if student.order_number else ''))
            self.table.setItem(row_position, 8, QTableWidgetItem(student.destination))
            self.table.setItem(row_position, 9, QTableWidgetItem(str(student.quantity)))
            self.table.setItem(row_position, 10, QTableWidgetItem(student.timestamp.strftime('%d.%m.%Y %H:%M:%S')))

    def generate_documents(self):
        selected_rows = self.table.selectionModel().selectedRows()  # Получаем список выбранных строк
        if not selected_rows:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите студентов для генерации документов.")
            return
        
        selected_students = [self.students[row.row()] for row in selected_rows]  # Собираем данные только выбранных студентов

        if not selected_students:
            QMessageBox.warning(self, "Ошибка", "Нет данных для генерации документов.")
            return
        
        # output_dir = "D:\my_project\AutoStudentDocsApp"
        generator = DocumentGenerator(get_path_save())
        generator.generate_documents(students=selected_students, template_dir=".\\templates\\")
        QMessageBox.information(self, "Генерация документов", "Документы успешно сгенерированы.")
        
    def on_item_changed(self, item):
        row = item.row()
        column = item.column()
        value = item.text()
        student = self.students[row]

        try:
            if column == 0:
                student.full_name = value
            elif column == 1:
                student.group = value
            elif column == 2:
                student.course = int(value)
            elif column == 3:
                student.study_form = value
            elif column == 4:
                student.study_base = value
            elif column == 5:
                student.date_of_receipt = int(value)
            elif column == 6:
                student.study_duration = int(value)
            elif column == 7:
                student.order_number = value
            elif column == 8:
                student.destination = value
            elif column == 9:
                student.quantity = int(value)
            elif column == 10:
                student.timestamp = datetime.strptime(value, '%d.%m.%Y %H:%M:%S')
        except ValueError:
            QMessageBox.warning(self, "Ошибка ввода", "Пожалуйста, введите корректное значение.")
            # Возвращаем прежнее значение
            self.display_data()

    def run(self):
        self.show()

def main():
    app = QApplication(sys.argv)
    ui = UserInterface()
    ui.run()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
