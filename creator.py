import sys

# Импортируем из PyQt5.QtWidgets классы для создания приложения и виджета
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QBoxLayout, QDesktopWidget
from PyQt5.Qt import Qt, QFont
from PyQt5 import QtGui


# Унаследуем наш класс от простейшего графического примитива QWidget
class SmartNotes(QWidget):
    def __init__(self):
        # Надо не забыть вызвать инициализатор базового класса
        super().__init__()
        # В метод initUI() будем выносить всю настройку интерфейса,
        # чтобы не перегружать инициализатор
        self.initUI()

    # Функция для центрирования окна по экрану устройства
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):
        self.setGeometry(0, 0, 700, 300)
        self.center()

        # Настройка окна
        self.setWindowTitle("SmartNotes")
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setMinimumSize(700, 300)

        # Создание объектов на экране
        self.btn_new = QPushButton("Новая заметка")
        self.btn_new.setStyleSheet("QPushButton {background-color: rgb(51,122,183); color: White; border-radius: 4px;}"
                                   "QPushButton:pressed {background-color:rgb(31,101,163) ; }")
        self.btn_new.setFont(QFont("Arial", 15))

        self.btn_del = QPushButton("Удалить заметки")
        self.btn_del.setStyleSheet("QPushButton {background-color: rgb(51,122,183); color: White; border-radius: 4px;}"
                                   "QPushButton:pressed {background-color:rgb(31,101,163) ; }")
        self.btn_del.setFont(QFont("Arial", 15))

        self.lable_main = QLabel("SmartNotes")
        self.lable_main.setFont(QFont("Arial", 60))

        # Создание сеток дабы центрировать объекты на экране
        self.box_btn = QBoxLayout(1)
        self.box_btn.addWidget(self.btn_del)
        self.box_btn.addWidget(self.btn_new)
        self.box_btn.setAlignment(Qt.AlignCenter)

        self.box_label = QBoxLayout(1)
        self.box_label.addWidget(self.lable_main)
        self.box_label.setAlignment(Qt.AlignCenter)

        self.box_box = QVBoxLayout()
        self.box_box.addLayout(self.box_label)
        self.box_box.addLayout(self.box_btn)
        self.box_box.setAlignment(Qt.AlignCenter)

        self.setLayout(self.box_box)


if __name__ == '__main__':
    # Создадим класс приложения PyQT
    app = QApplication(sys.argv)
    # А теперь создадим и покажем пользователю экземпляр
    # нашего виджета класса Example
    ex = SmartNotes()
    ex.show()
    # Будем ждать, пока пользователь не завершил исполнение QApplication,
    # а потом завершим и нашу программу
    sys.exit(app.exec())
