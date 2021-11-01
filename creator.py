import sys

# Импортируем из PyQt5.QtWidgets классы для создания приложения и виджета
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.Qt import QFont


# Унаследуем наш класс от простейшего графического примитива QWidget
class Example(QWidget):
    def __init__(self):
        # Надо не забыть вызвать инициализатор базового класса
        super().__init__()
        # В метод initUI() будем выносить всю настройку интерфейса,
        # чтобы не перегружать инициализатор
        self.initUI()

    def initUI(self):
        # Зададим размер и положение нашего виджета,
        self.setGeometry(300, 300, 700, 300)
        # А также его заголовок
        self.setWindowTitle('Создать заметку')

        self.label = QLabel(self)
        self.label.setFont(QFont('Arial', 30))
        self.label.move(int(self.frameGeometry().getRect()[2] / 2.5), int(self.frameGeometry().getRect()[3] / 4))
        self.label.setText("SmartNotes")

        self.btn_create = QPushButton(self)
        self.btn_create.setText("Создать заметку")
        self.btn_create.move(int(self.frameGeometry().getRect()[2] / 2.5), int(self.frameGeometry().getRect()[3] / 2))

        self.btn_remove = QPushButton(self)
        self.btn_remove.setText("Удалить заметку")
        self.btn_remove.move(int(self.frameGeometry().getRect()[2] / 1.8), int(self.frameGeometry().getRect()[3] / 2))


if __name__ == '__main__':
    # Создадим класс приложения PyQT
    app = QApplication(sys.argv)
    # А теперь создадим и покажем пользователю экземпляр
    # нашего виджета класса Example
    ex = Example()
    ex.show()
    # Будем ждать, пока пользователь не завершил исполнение QApplication,
    # а потом завершим и нашу программу
    sys.exit(app.exec())