#!/usr/bin/env python
from PyQt5 import QtWidgets
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel

def open_db():
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('sfc.db')
    db.open()
    return db

class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)

        self.label = QtWidgets.QLabel()
        self.button_left = QtWidgets.QPushButton('<')
        self.button_right = QtWidgets.QPushButton('>')
        blayout = QtWidgets.QHBoxLayout()
        blayout.addWidget(self.button_left)
        blayout.addWidget(self.button_right)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addLayout(blayout)

        self.mapper = QtWidgets.QDataWidgetMapper(self)
        #self.db = create_db()
        self.db = open_db()
        self.model = QSqlQueryModel(self)
        self.model.setQuery('SELECT DISTINCT form FROM threads')
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.label, 0, b'text')
        self.mapper.toFirst()

        self.button_left.clicked.connect(self.mapper.toPrevious)
        self.button_right.clicked.connect(self.mapper.toNext)

app = QtWidgets.QApplication([])

w = Widget()
w.show()

app.exec_()

