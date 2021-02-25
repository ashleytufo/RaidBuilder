from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QTableWidget
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5 import QtCore


a = QListWidgetItem("test")

a.setBackground(QtGui.QColor('#C79C6E'))
# a.setIcon(QtGui.QIcon('icons/tank.png'))

b = QListWidgetItem("test")

b.setBackground(QtGui.QColor('#C79C6E'))
# b.setIcon(QtGui.QIcon('icons/tank.png'))

if a.text() == b.text() and a.background() == b.background():
    print("yay!")