import sys
import getpass
import sqlite3
import requests
from PIL import Image
import shutil
import os
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QDialog, QPlainTextEdit, \
    QMainWindow, QHBoxLayout, QTableWidgetItem
from PyQt5.QtWidgets import QVBoxLayout, QBoxLayout, QDesktopWidget, QInputDialog, QLineEdit, QMessageBox, \
    QAction, QTableWidget
from PyQt5.Qt import Qt, QFont
from win32api import GetSystemMetrics
import random

# Константы
SERVER_IP = "http://192.168.1.159:5000"  # IP запущенного сервера с рейтингом
# Названия столбцов таблицы
LABELS = ["Предпросмотр", "Удаление", "ID", "Заголовок", "Текст", "Картинка", "Автор"]
# Названия столбцов базы данных
SQL_LABELS = ["", "", "", "noteTitle", "noteText", "notePic", "noteAuthor"]


# Функция для центрирования окна по экрану устройства
def center(self):
    qr = self.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())


# Унаследуем наш класс от простейшего графического примитива QWidget
class SmartNotes(QWidget):
    def __init__(self):
        super().__init__()
        self.initui()

    def initui(self):
        self.setGeometry(0, 0, 700, 300)
        center(self)

        self.pixmap = QPixmap("logo.png")
        self.image = QLabel(self)

        # CSS-код для красивых градиентных кнопок
        self.setStyleSheet("""
                QPushButton {
                        font: 75 10pt "Microsoft YaHei UI";
                        font-weight: bold;
                        color: rgb(255, 255, 255);
                        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, 
                        y2:0, stop:0 rgb(255, 136, 0), stop:1 rgb(250, 200, 0));
                        border-style: solid;
                        border-radius:10px;
                }
                QPushButton:hover {
                            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, 
                            y2:0, stop:0 rgb(255, 170, 0), stop:1 rgb(250, 200, 0));
                        }
                        """)

        # Настройка окна и создание виджетов
        self.setWindowTitle("SmartNotes")
        self.setWindowIcon(QIcon('icon.png'))
        self.setMinimumSize(700, 300)

        self.btn_new = QPushButton("Новая заметка")
        self.btn_new.setMinimumSize(200, 35)
        self.btn_new.setFont(QFont("Arial", 15))
        self.btn_new.clicked.connect(self.new_note)

        self.btn_del = QPushButton("Изменить заметки")
        self.btn_del.setMinimumSize(200, 35)
        self.btn_del.setFont(QFont("Arial", 15))
        self.btn_del.clicked.connect(self.edit_note)

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
        self.box_label.addWidget(self.image)

        self.setLayout(self.box_box)
        self.image.setPixmap(self.pixmap)

    def new_note(self):
        # Вызов окна создания новых заметок
        self.note = CreateNote()
        self.note.exec()

    def edit_note(self):
        # Вызов окна изменения и удаления заметок
        self.note = EditNote()
        self.note.exec()


# Класс виджета, отвечающего за создание заметок
class CreateNote(QDialog):
    def __init__(self):
        super().__init__()
        self.path = ""
        self.initui()

    def initui(self):
        self.setGeometry(0, 0, 500, 300)
        center(self)

        # Настройка окна и создание виджетов
        self.setWindowTitle("SmartNotes – Новая заметка")
        self.setWindowIcon(QIcon('icon.png'))
        self.setMinimumSize(500, 300)

        self.title_lable = QLabel(self)
        self.title_lable.setText("Заголовок заметки:")

        self.title_edit = QLineEdit(self)
        self.title_edit.setPlaceholderText("Не забыть!")

        self.text_lable = QLabel(self)
        self.text_lable.setText("Текст заметки:")

        self.text_edit = QPlainTextEdit(self)
        self.text_edit. \
            setPlaceholderText("1) Покормить рыбок\n2) Сделать домашнее задание")

        self.pic_lable = QLabel(self)
        self.pic_lable.setText("Картинка в заметке:")

        self.pic_button = QPushButton(self)
        self.pic_button.setText("Выбрать картинку")
        self.pic_button.clicked.connect(self.picture)

        self.author_lable = QLabel(self)
        self.author_lable.setText("Автор заметки:")

        self.author_edit = QLineEdit(self)
        self.author_edit.setPlaceholderText(getpass.getuser())

        self.btn_ready = QPushButton(self)
        self.btn_ready.setText("Готово!")
        self.btn_ready.clicked.connect(self.ready)

        self.box = QVBoxLayout(self)
        self.box.addWidget(self.title_lable)
        self.box.addWidget(self.title_edit)
        self.box.addWidget(self.text_lable)
        self.box.addWidget(self.text_edit)
        self.box.addWidget(self.pic_lable)
        self.box.addWidget(self.pic_button)
        self.box.addWidget(self.author_lable)
        self.box.addWidget(self.author_edit)
        self.box.addWidget(self.btn_ready)

        self.setLayout(self.box)

    def picture(self):
        self.path = QFileDialog.getOpenFileName(self,
                                                'Выбрать картинку', '',
                                                'Картинка (*.png *jpg *jpeg)')[0]

    def ready(self):
        # Проверка на заполнение полей
        if not self.text_edit.toPlainText() or not \
                self.author_edit.text() or not self.author_edit.text():
            self.msg_box = QMessageBox(self)
            self.msg_box.setWindowTitle("Ошибка!")
            self.msg_box.setText("Заполните все поля!")
            self.msg_box.exec()
        else:
            res, okpressed = QInputDialog.getItem(self,
                                                  "SmartNotes – Новая заметка",
                                                  "Выберете действие:",
                                                  ["Предпросмотр", "Создать"], 0, False)
            if okpressed and res == "Предпросмотр":
                self.img = Image.open(self.path)
                h, w = self.img.size
                scale = 250 / h
                self.img = self.img.resize((int(h * scale), int(w * scale)), Image.ANTIALIAS)
                self.img.save(self.path)

                self.newnote = Note(self.title_edit.text(),
                                    self.author_edit.text(), self.text_edit.toPlainText(),
                                    self.path, False)
                self.newnote.exec()
            if okpressed and res == "Создать":
                # Коннект к базе данных для создания заметки
                con = sqlite3.connect("notes.db")
                cur = con.cursor()
                try:
                    if self.path != "":
                        request = cur.execute("SELECT MAX(noteId) from notes").fetchall()
                        if request:
                            shutil.copy(self.path, os.getcwd() + "\\note_pics\\" + str(int(request[0][0]) + 1) + ".png")
                            self.path = "note_pics\\" + str(int(request[0][0]) + 1) + ".png"
                            self.img = Image.open(self.path)
                            h, w = self.img.size
                            scale = 250 / h
                            self.img = self.img.resize((int(h * scale), int(w * scale)), Image.ANTIALIAS)
                            self.img.save(self.path)

                    cur.execute(f'INSERT INTO notes (noteTitle, noteAuthor) '
                                f'VALUES ("{self.title_edit.text()}", '
                                f'"{self.author_edit.text()}")')
                    con.commit()
                    cur.execute(f'INSERT INTO texts (noteId, noteText, notePic) '
                                f'VALUES ((SELECT MAX(noteId) from notes), '
                                f'"{self.text_edit.toPlainText()}", "{self.path}")')
                    con.commit()
                    self.msg_box = QMessageBox(self)
                    self.msg_box.setWindowTitle("Успешно!")
                    self.msg_box.setText("Заметка создана!")
                    self.msg_box.exec()
                except Exception:
                    # Исключение на всякий случай
                    self.msg_box = QMessageBox(self)
                    self.msg_box.setWindowTitle("Ошибка!")
                    self.msg_box.setText("Заметка не создана!")
                    self.msg_box.exec()
                con.close()


# Класс виджета, отвечающего за изменение и удаление заметок
class EditNote(QDialog):
    def __init__(self):
        super().__init__()
        self.initui()

    def initui(self):
        # Настройка окна
        self.setGeometry(0, 0, 600, 300)
        center(self)
        self.setWindowTitle("SmartNotes – Изменить заметки")
        self.setWindowIcon(QIcon('icon.png'))
        self.setMinimumSize(500, 300)

        # CSS-код для красивых градиентных кнопок
        self.setStyleSheet("""
                        QPushButton {
                                font: 75 10pt "Microsoft YaHei UI";
                                font-weight: bold;
                                color: rgb(255, 255, 255);
                                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, 
                                y2:0, stop:0 rgb(255, 136, 0), stop:1 rgb(250, 200, 0));
                                border-style: solid;
                                border-radius:10px;
                        }
                        QPushButton:hover {
                                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, 
                                    y2:0, stop:0 rgb(255, 170, 0), stop:1 rgb(250, 200, 0));
                                }
                                """)

        self.table = QTableWidget(self)
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(LABELS)
        self.update_data()

        self.btn_update = QPushButton(self)
        self.btn_update.setIcon(QIcon("update1.png"))
        self.btn_update.clicked.connect(self.update_data)

        self.box_tools = QHBoxLayout()
        self.box_tools.addWidget(self.btn_update)

        self.box_main = QVBoxLayout()
        self.box_main.addLayout(self.box_tools)
        self.box_main.addWidget(self.table)

        self.setLayout(self.box_main)

    def update_data(self):
        self.table.disconnect()
        # Коннект к базе данных для обновления таблицы
        con = sqlite3.connect("notes.db")
        cur = con.cursor()
        result = cur.execute("""SELECT notes.noteId, notes.noteTitle, 
        texts.noteText, texts.notePic, notes.noteAuthor FROM notes
            JOIN texts ON notes.noteId=texts.noteId WHERE notes.noteId != 0""").fetchall()
        con.close()
        # Словарь, который хранит картинки заметок
        self.pics = dict()
        # Перебирание ячеек базы данных
        for i in range(len(result)):
            self.pics[i] = result[i][3]

        self.table.setRowCount(len(result))

        for i, elem in enumerate(result):
            # Создание кнопки предпросмотра заметки
            self.btn_show = QPushButton(self)
            self.btn_show.setText("Посмотреть " + str(i + 1))
            self.btn_show.clicked.connect(self.showing)

            self.table.setCellWidget(i, 0, self.btn_show)

            # Создание диалогового окна изменения картинки заметки
            self.btn_del = QPushButton(self)
            self.btn_del.setText("Удалить  " + str(i + 1))
            self.btn_del.clicked.connect(self.delete)

            self.table.setCellWidget(i, 1, self.btn_del)
            for j, val in enumerate(elem, 2):
                if j == 5:
                    # Создание диалогового окна изменения картинки заметки
                    btn_edit = QPushButton(self)
                    btn_edit.setText("Изменить " + str(i + 1))
                    btn_edit.clicked.connect(self.picture)

                    self.table.setCellWidget(i, j, btn_edit)
                else:
                    self.table.setItem(i, j, QTableWidgetItem(str(val)))
                    if j == 2:
                        self.table.item(i, j).setFlags(Qt.ItemIsEnabled)
        self.table.resizeColumnsToContents()
        self.table.itemChanged.connect(self.item_changed)

    def item_changed(self, item):
        res, okpressed = QInputDialog.getItem(self,
                                              "SmartNotes – Изменение замток",
                                              "Подтвердите изменение данных", ["Изменить", "Отменить"], 0, False)
        if okpressed and res == "Изменить":
            # Коннект к базе данных для изменения заметок
            con = sqlite3.connect("notes.db")
            cur = con.cursor()
            if item.column() == 3 or item.column() == 6:
                cur.execute(f"UPDATE notes SET {SQL_LABELS[item.column()]} = "
                            f"'{item.text()}' WHERE noteId = {self.table.item(item.row(), 2).text()}")
            else:
                cur.execute(f"UPDATE texts SET {SQL_LABELS[item.column()]} = "
                            f"'{item.text()}' WHERE noteId = {self.table.item(item.row(), 2).text()}")
            con.commit()
            con.close()
        self.update_data()

    def picture(self):
        self.pics[int(self.sender().text().split()[1]) - 1] = \
            QFileDialog.getOpenFileName(self, 'Выбрать картинку', '',
                                        'Картинка (*.png *jpg *jpeg)')[0]
        shutil.copy(self.pics[int(self.sender().text().split()[1]) - 1],
                    os.getcwd() + "\\note_pics\\" + self.table.item(int(self.sender().text().split()[1]) - 1,
                                                                    2).text() + ".png")
        self.pics[int(self.sender().text().split()[1]) - 1] = "note_pics\\" + self.table.item(
            int(self.sender().text().split()[1]) - 1, 2).text() + ".png"

        self.img = Image.open(self.pics[int(self.sender().text().split()[1]) - 1])
        h, w = self.img.size
        scale = 250 / h
        self.img = self.img.resize((int(h * scale), int(w * scale)), Image.ANTIALIAS)
        self.img.save(self.pics[int(self.sender().text().split()[1]) - 1])

        # Коннект к базе данных для изменения картинки
        con = sqlite3.connect("notes.db")
        cur = con.cursor()
        cur.execute(f"UPDATE texts SET notePic = '{self.pics[int(self.sender().text().split()[1]) - 1]}'"
                    f" WHERE noteId = {self.table.item(int(self.sender().text().split()[1]) - 1, 2).text()}")
        con.commit()
        con.close()

    def delete(self):
        descision, okpressed = QInputDialog.getItem(self,
                                                    "SmartNotes – Удаление заметок",
                                                    "Вы действительно хотите удалить заметку?",
                                                    ["Да", "Нет"], 0, False)
        if okpressed and descision == "Да":
            con = sqlite3.connect("notes.db")
            cur = con.cursor()
            cur.execute(
                f"DELETE FROM texts WHERE noteId = {self.table.item(int(self.sender().text().split()[1]) - 1, 2).text()}")
            con.commit()
            cur.execute(
                f"DELETE FROM notes WHERE noteId = {self.table.item(int(self.sender().text().split()[1]) - 1, 2).text()}")
            con.commit()
            con.close()
            try:
                os.remove(os.getcwd() + "\\note_pics\\" + self.table.item(int(self.sender().text().split()[1]) - 1,
                                                                          2).text() + ".png")
            except:
                pass
        self.update_data()

    def showing(self):
        self.newnote = Note(self.table.item(int(self.sender().text().split()[1]) - 1, 3).text(),
                            self.table.item(int(self.sender().text().split()[1]) - 1, 6).text(),
                            self.table.item(int(self.sender().text().split()[1]) - 1, 4).text(),
                            self.pics[int(self.sender().text().split()[1]) - 1],
                            False)
        self.newnote.exec()


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initui()

    def initui(self):
        # Настройка окна и создание виджетов
        self.setGeometry(0, 0, 700, 300)
        center(self)
        self.setWindowTitle("SmartNotes")
        self.setWindowIcon(QIcon('icon.png'))
        self.setMinimumSize(700, 300)

        # Меню-бар для некоторых функций
        self.menubar = self.menuBar()

        self.settingsMenu = self.menubar.addMenu('&Настройки')
        self.run = QAction("Запустить заметки", self)
        self.settingsMenu.addAction(self.run)

        self.rate = QAction("Оцените приложение", self)
        self.settingsMenu.addAction(self.rate)

        self.run.triggered.connect(self.runapp)
        self.rate.triggered.connect(self.rating)

    def rating(self):
        rate, ok = QInputDialog.getInt(self, 'Оцените SmartNotes', 'Введите оценку от 1 до 5', 0, 1, 5)
        if ok:
            # Отправка на сервер оценки пользователя
            req = requests.get(SERVER_IP + "/rateapp?rating=" + str(rate))
            if req.status_code == 200:
                self.msg_box = QMessageBox(self)
                self.msg_box.setWindowTitle("Успешно!")
                self.msg_box.setText("Ваш отзыв был отправлен!")
                self.msg_box.exec()
            else:
                self.msg_box = QMessageBox(self)
                self.msg_box.setWindowTitle("Ошибка!")
                self.msg_box.setText("Отсутствует связь с сервером, попробоуйте позже.")
                self.msg_box.exec()

    def runapp(self):
        self.notes = list()
        # Коннект к базе данных для создания всех заметок
        con = sqlite3.connect("notes.db")
        cur = con.cursor()
        result = cur.execute("""SELECT noteTitle, noteAuthor, noteText, notePic FROM notes 
            JOIN texts ON notes.noteId=texts.noteId WHERE notes.noteId != 0""").fetchall()
        con.close()
        # Запись заметок в список
        for elem in result:
            self.notes.append(Note(elem[0], elem[1], elem[2], elem[3]))
        # Вывод всех заметок на экран
        for self.note in self.notes:
            self.note.show()


# Класс окна заметок
class Note(QDialog):
    def __init__(self, title, author, text, pic, pinned=True):
        self.title = title
        self.text = text
        self.pic = pic
        self.author = author
        self.pinned = pinned
        super().__init__()
        self.initui()

    def initui(self):
        # Настройка окна и создание виджетов
        self.setGeometry(random.randint(0, GetSystemMetrics(0) - 500), random.randint(0, GetSystemMetrics(1) - 500),
                         300, 300)
        self.adjustSize()
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowTitle("SmartNotes – " + self.title)
        self.setWindowFlag(QtCore.Qt.Dialog)
        self.count = 0

        # CSS-код для красивых градиентных кнопок
        self.setStyleSheet("""
                        QPushButton {
                                font: 75 10pt "Microsoft YaHei UI";
                                font-weight: bold;
                                color: rgb(255, 255, 255);
                                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, 
                                y2:0, stop:0 rgb(255, 136, 0), stop:1 rgb(250, 200, 0));
                                border-style: solid;
                                border-radius:10px;
                        }
                        QPushButton:hover {
                                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, 
                                    y2:0, stop:0 rgb(255, 170, 0), stop:1 rgb(250, 200, 0));
                                }
                                """)

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

        if self.pinned:
            self.btn_pin = QPushButton(self)
            self.btn_pin.setText("Закрепить")
            self.btn_pin.clicked.connect(self.pin)
            self.box.addWidget(self.btn_pin)

        self.setLayout(self.box)

    def pin(self):
        if self.count % 2 == 0:
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
            self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.Dialog)
            self.sender().setText("Открепить")
        else:
            self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
            self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.FramelessWindowHint)
            self.setWindowFlags(QtCore.Qt.Dialog)
            self.sender().setText("Закрепить")
        self.count += 1
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainApp()
    notess = SmartNotes()
    ex.setCentralWidget(notess)
    ex.show()
    sys.exit(app.exec())
