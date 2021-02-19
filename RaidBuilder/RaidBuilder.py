"""
@author: Ashley Tufo
"""
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from os import path
from PyQt5 import QtGui
from Query import Query

import sqlite3


class RBWindow(QMainWindow):

    def __init__(self):
        super(RBWindow, self).__init__()
        QMainWindow.__init__(self)
        uic.loadUi('main.ui', self)
        self.HandleButtons()
        self.FillLists()
        today = QtCore.QDate.currentDate()
        self.signup_date_edit.setDate(today)

    def FillLists(self):
        newQuery = Query()
        signups = newQuery.getSignup()
        resList = []
        for row_number, row_data in enumerate(signups):
            resList.append(row_data[0])
        self.signup_cmbo.addItems(reversed(resList))
        self.existing_combo.addItems(reversed(resList))

    def HandleButtons(self):
        self.load_btn.clicked.connect(self.GET_DATA)
        self.create_new_btn.clicked.connect(self.CREATE_NEW)
        self.update_exist_btn.clicked.connect(self.UPDATE_EXISTING)
        self.reset_signup_btn.clicked.connect(self.RESET_SIGNUP)
        self.save_signup_btn.clicked.connect(self.SAVE_SIGNUP)

    def CREATE_NEW(self):
        self.create_new_btn.setDisabled(True)
        self.update_exist_btn.setDisabled(True)

        self.existing_combo.setDisabled(True)
        self.existing_combo.setCurrentIndex(0)

        self.signup_name_edit.setEnabled(True)
        self.signup_date_edit.setEnabled(True)
        self.signup_time_edit.setEnabled(True)

        self.signup_txt_edit.setEnabled(True)

        self.reset_signup_btn.setEnabled(True)
        self.save_signup_btn.setEnabled(True)

    def UPDATE_EXISTING(self):
        self.create_new_btn.setDisabled(True)
        self.update_exist_btn.setDisabled(True)
        
        self.existing_combo.setDisabled(True)

        self.signup_name_edit.setDisabled(True)
        self.signup_date_edit.setEnabled(True)
        self.signup_time_edit.setEnabled(True)
        
        self.signup_txt_edit.setEnabled(True)

        self.reset_signup_btn.setEnabled(True)
        self.save_signup_btn.setEnabled(True)

        slctSignup = self.existing_combo.currentText()
        newQuery = Query()
        result = newQuery.getSignupText(slctSignup)        

        for row_number, row_data in enumerate(result):
            row_data = str(row_data).replace("('", "").replace("',)", "").replace("\\u200e", "")
            rowList = row_data.split("\\r\\n")
            print(rowList)
            for item in rowList:
                self.signup_txt_edit.appendPlainText(item)
    
    def RESET_SIGNUP(self):
        self.create_new_btn.setEnabled(True)
        self.update_exist_btn.setEnabled(True)
        
        self.existing_combo.setEnabled(True)
        self.existing_combo.setCurrentIndex(0)

        self.signup_name_edit.setDisabled(True)
        self.signup_name_edit.clear()

        self.signup_date_edit.setDisabled(True)
        today = QtCore.QDate.currentDate()
        self.signup_date_edit.setDate(today)

        self.signup_time_edit.setDisabled(True)
        self.signup_time_edit.setTime(QtCore.QTime(21, 00, 00))

        self.signup_txt_edit.setDisabled(True)
        self.signup_txt_edit.clear()

        self.reset_signup_btn.setDisabled(True)
        self.save_signup_btn.setDisabled(True)

    def SAVE_SIGNUP():
        pass
    def addAbLaTeBen(self, role, signee, stat):
        if stat == "Absent":
            self.signup_list_absent.addItem(signee)
        elif stat == "Tentative":
            self.signup_list_tentative.addItem(signee)
        elif stat == "Late":
            self.signup_list_late.addItem(signee)
        elif stat == "Bench":
            self.signup_list_bench.addItem(signee)
        else:
            self.signup_list_other.addItem(signee)
        
    def addToList(self, role, signee, stat):
        if role == "Tank":
            signee.setBackground(QtGui.QColor('#C79C6E'))
            signee.setIcon(QtGui.QIcon('icons/tank.png'))
            if stat in ("Absent", "Late", "Tentative", "Bench"):
                self.addAbLaTeBen(role, signee, stat)
            else:
                self.signup_list_tanks.addItem(signee)
        elif role == "BearTank":
            signee.setBackground(QtGui.QColor('#FF7D0A'))
            signee.setIcon(QtGui.QIcon('icons/bear.png'))
            if stat in ("Absent", "Late", "Tentative", "Bench"):
                self.addAbLaTeBen(role, signee, stat)
            else:
                self.signup_list_tanks.addItem(signee)
        elif role == "Hunter":
            signee.setBackground(QtGui.QColor('#abd473'))
            signee.setIcon(QtGui.QIcon('icons/hunter.png'))
            if stat in ("Absent", "Late", "Tentative", "Bench"):
                self.addAbLaTeBen(role, signee, stat)
            else:
                self.signup_list_hunters.addItem(signee)
        elif role == "RestoDruid":
            signee.setBackground(QtGui.QColor('#ffa14e'))
            signee.setIcon(QtGui.QIcon('icons/restoDruid.png'))
            if stat in ("Absent", "Late", "Tentative", "Bench"):
                self.addAbLaTeBen(role, signee, stat)
            else:
                self.signup_list_druids.addItem(signee)
        elif role == "Warrior":
            signee.setBackground(QtGui.QColor('#e9c49d'))
            signee.setIcon(QtGui.QIcon('icons/warrior.png'))
            if stat in ("Absent", "Late", "Tentative", "Bench"):
                self.addAbLaTeBen(role, signee, stat)
            else:
                self.signup_list_warriors.addItem(signee)
        elif role == "Mage":
            signee.setBackground(QtGui.QColor('#40c7eb'))
            signee.setIcon(QtGui.QIcon('icons/mage.png'))
            if stat in ("Absent", "Late", "Tentative", "Bench"):
                self.addAbLaTeBen(role, signee, stat)
            else:
                self.signup_list_mages.addItem(signee)
        elif role == "RestoShaman":
            signee.setBackground(QtGui.QColor('#0070de'))
            signee.setIcon(QtGui.QIcon('icons/restoSham.png'))
            if stat in ("Absent", "Late", "Tentative", "Bench"):
                self.addAbLaTeBen(role, signee, stat)
            else:
                self.signup_list_shamans.addItem(signee)
        elif role == "EnhShaman":
            signee.setBackground(QtGui.QColor('#338de5'))
            signee.setIcon(QtGui.QIcon('icons/enhSham.png'))
            if stat in ("Absent", "Late", "Tentative", "Bench"):
                self.addAbLaTeBen(role, signee, stat)
            else:
                self.signup_list_shamans.addItem(signee)
        elif role == "ElemShaman":
            signee.setBackground(QtGui.QColor('#66a9eb'))
            signee.setIcon(QtGui.QIcon('icons/eleSham.png'))
            if stat in ("Absent", "Late", "Tentative", "Bench"):
                self.addAbLaTeBen(role, signee, stat)
            else:
                self.signup_list_shamans.addItem(signee)
        elif role == "Rogue":
            signee.setBackground(QtGui.QColor('#fff569'))
            signee.setIcon(QtGui.QIcon('icons/rogue.png'))
            if stat in ("Absent", "Late", "Tentative", "Bench"):
                self.addAbLaTeBen(role, signee, stat)
            else:
                self.signup_list_rogues.addItem(signee)
        elif role == "Warlock":
            signee.setBackground(QtGui.QColor('#8787ed'))
            signee.setIcon(QtGui.QIcon('icons/warlock.png'))
            if stat in ("Absent", "Late", "Tentative", "Bench"):
                self.addAbLaTeBen(role, signee, stat)
            else:
                self.signup_list_warlocks.addItem(signee)
        elif role == "ShadowPriest":
            signee.setBackground(QtGui.QColor('#c8ccdf'))
            signee.setIcon(QtGui.QIcon('icons/shadow.png'))
            if stat in ("Absent", "Late", "Tentative", "Bench"):
                self.addAbLaTeBen(role, signee, stat)
            else:
                self.signup_list_priests.addItem(signee)
        elif role == "Priest":
            signee.setBackground(QtGui.QColor('#eaeaea'))
            signee.setIcon(QtGui.QIcon('icons/priest.png'))
            if stat in ("Absent", "Late", "Tentative", "Bench"):
                self.addAbLaTeBen(role, signee, stat)
            else:
                self.signup_list_priests.addItem(signee)
        elif role == "FeralDruid":
            signee.setBackground(QtGui.QColor('#ffb471'))
            signee.setIcon(QtGui.QIcon('icons/feral.png'))
            if stat in ("Absent", "Late", "Tentative", "Bench"):
                self.addAbLaTeBen(role, signee, stat)
            else:
                self.signup_list_druids.addItem(signee)
        elif role == "HolyPaladin":
            signee.setBackground(QtGui.QColor('#e99bbd'))
            
            if stat in ("Absent", "Late", "Tentative", "Bench"):
                self.addAbLaTeBen(role, signee, stat)
            else:
                self.signup_list_other.addItem(signee)
        elif role == "RetribPaladin":
            signee.setBackground(QtGui.QColor('#eeb4ce'))

            if stat in ("Absent", "Late", "Tentative", "Bench"):
                self.addAbLaTeBen(role, signee, stat)
            else:
                self.signup_list_other.addItem(signee)
        elif role == "ProtPaladin":
            signee.setBackground(QtGui.QColor('#E382AD'))

            if stat in ("Absent", "Late", "Tentative", "Bench"):
                self.addAbLaTeBen(role, signee, stat)
            else:
                self.signup_list_other.addItem(signee)
        else:
            signee.setForeground(QtGui.QColor('#9199BE'))

            if stat in ("Absent", "Late", "Tentative", "Bench"):
                self.addAbLaTeBen(role, signee, stat)
            else:
                self.signup_list_other.addItem(signee)
        return

    def GET_DATA(self):
        #Connect to Sqlite3 database and fill GUI table with data
        # db = sqlite3.connect('raidbuilder.db')
        # cursor = db.cursor()
        # slctSignup = (slctSignup)
        # command = """ SELECT Role, Discord_Name, Status FROM rb_signees WHERE Signup_ID = (SELECT ID from rb_signups WHERE Signup_Name = '{}'); """.format(slctSignup)
        # result = cursor.execute(command)
        # self.signup_list_tanks.setRowCount(0)
        slctSignup = self.signup_cmbo.currentText()
        newQuery = Query()
        result = newQuery.getSignee(slctSignup)

        self.signup_list_absent.clear()
        self.signup_list_bench.clear()
        self.signup_list_druids.clear()
        self.signup_list_hunters.clear()
        self.signup_list_late.clear()
        self.signup_list_mages.clear()
        self.signup_list_other.clear()
        self.signup_list_priests.clear()
        self.signup_list_rogues.clear()
        self.signup_list_shamans.clear()
        self.signup_list_tanks.clear()
        self.signup_list_tentative.clear()
        self.signup_list_warlocks.clear()
        self.signup_list_warriors.clear()

        for row_number, row_data in enumerate(result):
            role = row_data[0]
            player = row_data[1]
            stat = row_data[2]
            item = QListWidgetItem(player)

            self.addToList(role, item, stat)
