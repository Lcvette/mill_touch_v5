#!/usr/bin/env python3
from PyQt5 import QtWidgets
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel

def create_db():
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName(':memory:')
    db.open()
    db.exec('CREATE TABLE test (col text)')
    for i in range(10):
        db.exec('INSERT INTO test VALUES ("Row {}")'.format(i))
    db.commit()
    return db

class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

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
        self.db = create_db()
        self.model = QSqlQueryModel(self)
        self.model.setQuery('SELECT * FROM test')
        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.label, 0, b'text')
        self.mapper.toFirst()

        self.button_left.clicked.connect(self.mapper.toPrevious)
        self.button_right.clicked.connect(self.mapper.toNext)

app = QtWidgets.QApplication([])

w = Widget()
w.show()

app.exec()

