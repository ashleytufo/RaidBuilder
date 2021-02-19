"""
@author: Ashley Tufo
"""
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from ui_raidbuilder import Ui_RaidBuilder
import sqlite3

import sys

from os import path
from PyQt5 import uic
# from PyQt5.uic import loadUiType
# from PyQt5.uic import loadUi
# FORM_CLASS = loadUiType(path.join(path.dirname('__file__'), "main.ui"))

class Main(QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        QMainWindow.__init__(self)
        # self.setupUi(self)
        uic.loadUi('main.ui', self)
        self.HandleButtons()

    def HandleButtons(self):
        pass

    # Here is our code

def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
