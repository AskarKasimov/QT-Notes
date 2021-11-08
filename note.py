import sys
import sqlite3
from win32api import GetSystemMetrics
import random
# Импортируем из PyQt5.QtWidgets классы для создания приложения и виджета
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5 import QtGui


# Унаследуем наш класс от простейшего графического примитива QWidget
class Note(QWidget):
    def __init__(self, title, author, text, pic, create_time=None, remove_time=None):
        self.title = title
        self.text = text
        self.pic = pic
        self.author = author
        self.create_time = create_time
        self.remove_time = remove_time
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
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        # А также его заголовок
        self.setWindowTitle(self.title)

        self.label_text = QLabel(self)
        self.label_text.move(1, 1)
        self.label_text.setText("\n".join(self.text.split("\\n")))


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
    result = cur.execute("""SELECT noteTitle, noteAuthor, noteText, notePic, noteCreateTime, noteRemoveTime FROM notes 
    JOIN texts ON notes.noteId=texts.noteId JOIN times ON notes.noteId=times.noteId""").fetchall()
    # Запись заметок в список
    for elem in result:
        notes.append(Note(elem[0], elem[1], elem[2], elem[3], elem[4], elem[5])) if elem[4] != "NULL" \
            else notes.append(Note(elem[0], elem[1], elem[2], elem[3]))
    # Закрытие подключения
    con.close()
    # Вывод всех заметок на экран
    for note in notes:
        note.show()
    # Будем ждать, пока пользователь не завершил исполнение QApplication,
    # а потом завершим и нашу программу
    sys.exit(app.exec())
