import sys
import sqlite3
from win32api import GetSystemMetrics
import random
# Импортируем из PyQt5.QtWidgets классы для создания приложения и виджета
from PyQt5.QtWidgets import QApplication, QWidget


# Унаследуем наш класс от простейшего графического примитива QWidget
class Note(QWidget):
    def __init__(self, title, text, pic, author):
        self.title = title
        self.text = text
        self.pic = pic
        self.author = author
        # Надо не забыть вызвать инициализатор базового класса
        super().__init__()
        # В метод initUI() будем выносить всю настройку интерфейса,
        # чтобы не перегружать инициализатор
        self.initUI()

    def initUI(self):
        # Зададим размер и положение нашего виджета,
        self.setGeometry(random.randint(0, GetSystemMetrics(0) - 300), random.randint(0, GetSystemMetrics(1) - 300),
                         300, 300)
        self.setFixedSize(300, 300)
        # А также его заголовок
        self.setWindowTitle(self.title)


if __name__ == '__main__':
    # Список со всеми заметками
    notes = list()
    # Создадим класс приложения PyQT
    app = QApplication(sys.argv)
    # Подключение к БД
    con = sqlite3.connect("notes.db")
    # Создание курсора
    cur = con.cursor()
    # Выполнение запроса и получение всех результатов
    result = cur.execute("""SELECT note_title FROM notes""").fetchall()
    # Запись заметок в список
    for elem in result:
        notes.append(Note(elem[0], None, None, None))
    # Закрытие подключения
    con.close()
    # Вывод всех заметок на экран
    for note in notes:
        note.show()
    # Будем ждать, пока пользователь не завершил исполнение QApplication,
    # а потом завершим и нашу программу
    sys.exit(app.exec())
