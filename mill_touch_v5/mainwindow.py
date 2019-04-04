from qtpyvcp.widgets.form_widgets.main_window import VCPMainWindow

# Setup logging
from qtpyvcp.utilities import logger
LOG = logger.getLogger('qtpyvcp.' + __name__)

import sqlite3

import os
current_path = os.path.dirname(os.path.realpath(__file__)) + '/'

from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel
from PyQt5.QtWidgets import QDataWidgetMapper


class MyMainWindow(VCPMainWindow):
    """Main window class for the VCP."""
    def __init__(self, *args, **kwargs):
        super(MyMainWindow, self).__init__(*args, **kwargs)

        self.formNextBtn.clicked.connect(self.formNext)
        self.formPreviousBtn.clicked.connect(self.formPrevious)
        self.classNextBtn.clicked.connect(self.classNext)
        self.classPreviousBtn.clicked.connect(self.classPrevious)
        self.sizeNextBtn.clicked.connect(self.sizeNext)
        self.sizePreviousBtn.clicked.connect(self.sizePrevious)

        if not self.open_db():
            print('Failed to Open Database')

        self.formModelInit()
        #self.sizeModelInit()

    def open_db(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(current_path + 'sfc.db')
        db.open()
        return db

    def formModelInit(self):
        self.formMapper = QDataWidgetMapper(self)
        self.formModel = QSqlQueryModel(self)
        self.formModel.setQuery('SELECT DISTINCT form FROM threads')
        self.formMapper.setModel(self.formModel)
        self.formMapper.addMapping(self.formLbl, 0, b'text')
        self.formMapper.currentIndexChanged.connect(self.formChanged)
        self.formMapper.toLast()
        self.formsLast = self.formMapper.currentIndex()
        self.formMapper.toFirst()
        self.formIndexLbl.setText('{}'.format(self.formMapper.currentIndex()))
        self.classModelInit()

    def formNext(self):
        #print('before {}'.format(self.mapper.currentIndex()))
        if self.formMapper.currentIndex() != self.formsLast:
            self.formMapper.toNext()
        else:
            self.formMapper.toFirst()
        self.formIndexLbl.setText('{}'.format(self.formMapper.currentIndex()))
        #print('after {}'.format(self.mapper.currentIndex()))
        self.classModelInit()

    def formPrevious(self):
        if self.formMapper.currentIndex() != 0:
            self.formMapper.toPrevious()
        else:
            self.formMapper.toLast()
        self.formIndexLbl.setText('{}'.format(self.formMapper.currentIndex()))
        self.classModelInit()

    def formChanged(self):
        # is fired before the change is complete
        pass

    def classModelInit(self):
        print('class update')
        self.classMapper = QDataWidgetMapper(self)
        self.classModel = QSqlQueryModel(self)
        form = self.formLbl.text()
        print(form)
        classSelect = "SELECT DISTINCT class FROM threads WHERE form = '{}'".format(form)
        self.classModel.setQuery(classSelect)
        self.classMapper.setModel(self.classModel)
        self.classMapper.addMapping(self.classLbl, 0, b'text')
        #self.classMapper.currentIndexChanged.connect(self.formChanged)
        self.classMapper.toLast()
        self.classLast = self.classMapper.currentIndex()
        self.classMapper.toFirst()
        self.classIndexLbl.setText('{}'.format(self.classMapper.currentIndex()))
        self.sizeModelInit()

    def classNext(self):
        #print('before {}'.format(self.mapper.currentIndex()))
        if self.classMapper.currentIndex() != self.classLast:
            self.classMapper.toNext()
        else:
            self.classMapper.toFirst()
        self.classIndexLbl.setText('{}'.format(self.classMapper.currentIndex()))
        #print('after {}'.format(self.mapper.currentIndex()))
        self.sizeModelInit(self.sizeMapper.currentIndex())

    def classPrevious(self):
        if self.classMapper.currentIndex() != 0:
            self.classMapper.toPrevious()
        else:
            self.classMapper.toLast()
        self.classIndexLbl.setText('{}'.format(self.classMapper.currentIndex()))
        self.sizeModelInit(self.sizeMapper.currentIndex())


    def sizeModelInit(self, index = 0):
        self.sizeMapper = QDataWidgetMapper(self)
        self.sizeModel = QSqlQueryModel(self)
        form = str(self.formLbl.text())
        fit = self.classLbl.text()
        sizeSelect = "SELECT * FROM threads WHERE form = '{}' AND class = '{}'".format(form, fit)
        self.sizeModel.setQuery(sizeSelect)
        self.sizeMapper.setModel(self.sizeModel)
        self.sizeMapper.addMapping(self.threadLbl, 0, b'text')
        self.sizeMapper.addMapping(self.pitchLbl, 3, b'text')
        self.sizeMapper.addMapping(self.majorDiameterLbl, 4, b'text')
        self.sizeMapper.addMapping(self.maxMajorDiameterLbl, 5, b'text')
        self.sizeMapper.addMapping(self.minMajorDiameterLbl, 6, b'text')
        self.sizeMapper.addMapping(self.pitchDiameterLbl, 7, b'text')
        self.sizeMapper.addMapping(self.maxPitchDiameterLbl, 8, b'text')
        self.sizeMapper.addMapping(self.minPitchDiameterLbl, 9, b'text')
        self.sizeMapper.addMapping(self.minMinorDiameterLbl, 10, b'text')
        self.sizeMapper.currentIndexChanged.connect(self.formChanged)
        self.sizeMapper.toLast()
        self.sizeLast = self.sizeMapper.currentIndex()
        self.sizeMapper.setCurrentIndex(index)
        #self.sizeMapper.toFirst()
        self.sizeIndexLbl.setText('{}'.format(self.sizeMapper.currentIndex()))

    def sizeNext(self):
        #print('before {}'.format(self.mapper.currentIndex()))
        if self.sizeMapper.currentIndex() != self.sizeLast:
            self.sizeMapper.toNext()
        else:
            self.sizeMapper.toFirst()
        self.sizeIndexLbl.setText('{}'.format(self.sizeMapper.currentIndex()))
        #print('after {}'.format(self.mapper.currentIndex()))

    def sizePrevious(self):
        if self.sizeMapper.currentIndex() != 0:
            self.sizeMapper.toPrevious()
        else:
            self.sizeMapper.toLast()
        self.sizeIndexLbl.setText('{}'.format(self.sizeMapper.currentIndex()))

