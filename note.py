import sys
import sqlite3
from PyQt5.QtGui import QPixmap, QFont
from win32api import GetSystemMetrics
import random
from PyQt5.QtWidgets import QApplication, QLabel, QDialog, QVBoxLayout
from PyQt5 import QtGui


# Класс окна заметок
class Note(QDialog):
    def __init__(self, title, author, text, pic, create_time=None, remove_time=None):
        self.title = title
        self.text = text
        self.pic = pic
        self.author = author
        self.create_time = create_time
        self.remove_time = remove_time
        super().__init__()
        self.initui()

    def initui(self):
        # Настройка окна и создание виджетов
        self.setGeometry(random.randint(0, GetSystemMetrics(0) - 300), random.randint(0, GetSystemMetrics(1) - 300),
                         300, 300)
        self.setFixedSize(300, 300)
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setWindowTitle("SmartNotes – " + self.title)

        self.label_title = QLabel(self)
        self.label_title.setText(self.title)
        self.label_title.setFont(QFont("Courier New", 30))

        self.label_text = QLabel(self)
        self.label_text.setText("\n".join(self.text.split("\\n")))

        self.box = QVBoxLayout()
        self.box.addWidget(self.label_title)
        self.box.addWidget(self.label_text)

        if self.pic != "":
            self.label = QLabel(self)
            self.pixmap = QPixmap(self.pic)
            self.label.setPixmap(self.pixmap)
            self.box.addWidget(self.label)

        self.setLayout(self.box)


if __name__ == '__main__':
    notes = list()
    app = QApplication(sys.argv)
    # Подключение к БД
    con = sqlite3.connect("notes.db")
    cur = con.cursor()
    result = cur.execute("""SELECT noteTitle, noteAuthor, noteText, notePic FROM notes 
    JOIN texts ON notes.noteId=texts.noteId WHERE notes.noteId != 0""").fetchall()
    con.close()
    for elem in result:
            notes.append(Note(elem[0], elem[1], elem[2], elem[3]))
    # Вывод всех заметок на экран
    for note in notes:
        note.show()
    sys.exit(app.exec())
