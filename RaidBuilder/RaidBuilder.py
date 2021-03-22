"""
@author: Ashley Tufo
"""
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtChart import *

from PyQt5.QtWidgets import (QApplication, QListWidget, QListWidgetItem,
                             QTableWidgetItem, QMainWindow, QLineEdit,
                             QMessageBox, QAbstractItemView,
                             QInputDialog, QFileDialog, QMenu)
from PyQt5.QtGui import (QPixmap, QClipboard, QIcon, QRegion,
                         QImage, QImageWriter, QPainter)
from PyQt5.QtCore import QPoint, QEvent, Qt
from PyQt5.QtChart import QPieSeries, QPieSlice, QChart, QChartView

from Query import Query
from Signups import Signup
from Rosters import Roster

import json
import logging
from os import path
import sys
from datetime import datetime


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', path.dirname(path.abspath(__file__)))
    return path.join(base_path, relative_path)


class RBWindow(QMainWindow):
    pyClassLog = logging.getLogger(__name__)

    def __init__(self):
        super(RBWindow, self).__init__()
        QMainWindow.__init__(self)
        uic.loadUi(resource_path('main.ui'), self)
        self.saved_rosters_list = QListWidget(self.s_roster_frame)
        self.saved_rosters_list.setObjectName(u"saved_rosters_list")
        self.s_roster_menu_grid.addWidget(self.saved_rosters_btn, 0, 0, 1, 1)
        self.s_roster_menu_grid.addWidget(self.saved_rosters_list, 1, 0, 1, 1)

        self.saved_rosters_list.setFixedWidth(150)
        self.import_roster_btn.setFixedWidth(40)
        self.create_new_btn.setFixedWidth(40)
        self.reset_signup_btn.setFixedWidth(40)
        self.save_signup_btn.setFixedWidth(40)
        self.update_existing_btn.setFixedWidth(40)
        self.edit_signup_btn.setFixedWidth(40)
        self.prefill_roster_btn.setFixedWidth(40)
        self.reset_roster_btn.setFixedWidth(40)
        self.save_roster_btn.setFixedWidth(40)
        self.search_btn.setFixedWidth(40)
        self.add_player_btn.setFixedWidth(40)
        self.delete_player_btn.setFixedWidth(40)
        self.edit_player_btn.setFixedWidth(40)
        self.save_player_btn.setFixedWidth(40)
        self.delete_roster_btn.setFixedWidth(40)
        self.export_roster_btn.setFixedWidth(40)
        self.screenshot_roster_btn.setFixedWidth(40)

        self.saved_rosters_list.setAlternatingRowColors(True)
        self.saved_rosters_list.setEditTriggers(QAbstractItemView.
                                                NoEditTriggers)
        self.saved_rosters_list.setWordWrap(True)
        self.saved_rosters_list.setVisible(False)

        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.AllAnimations)

        self.chart.setTitle("Roster Composition")
        self.chart.legend().hide()

        self.charview = QChartView(self.chart)
        self.charview.setGeometry(0, 0, 500, 500)
        self.charview.setRenderHint(QPainter.Antialiasing)
        self.horizontalLayout_7.addWidget(self.charview)
        self.charview.setFixedWidth(350)
        self.charview.setFixedHeight(250)
        self.charview.hide()

        self.saved_signups_list = QListWidget(self.signups_frame)
        self.saved_signups_list.setObjectName(u"saved_signups_list")
        self.signups_grid.addWidget(self.saved_signups_list, 1, 0, 3, 1)
        self.saved_signups_list.setAlternatingRowColors(True)
        self.saved_signups_list.setEditTriggers(QAbstractItemView.
                                                NoEditTriggers)
        self.saved_signups_list.setWordWrap(True)
        self.saved_signups_list.setVisible(False)
        self.saved_signups_list.setFixedWidth(150)

        self.signups_grid.addWidget(self.signup_name_lbl, 0, 2, 1, 3)
        self.signups_grid.addWidget(self.signup_name_edit, 1, 2, 1, 3)
        self.signups_grid.addWidget(self.signup_txt_edit, 2, 2, 1, 6)

        self.players_grid.addWidget(self.players_tbl, 1, 0, 4, 2)

        today = QtCore.QDate.currentDate()
        self.signup_date_edit.setDate(today)
        self.reset_signup_btn.setVisible(False)
        self.save_signup_btn.setVisible(False)
        self.edit_signup_btn.setVisible(False)
        self.update_existing_btn.setVisible(False)
        self.roster_combo.setVisible(False)
        self.prefill_roster_btn.setVisible(False)
        self.pre_rost_radbtn.setVisible(False)
        self.pre_favs_radbtn.setVisible(False)
        self.reset_roster_btn.setVisible(False)
        self.save_roster_btn.setVisible(False)
        self.players_tbl.setColumnHidden(9, True)
        self.players_tbl.setColumnHidden(10, True)
        self.export_roster_btn.setVisible(False)
        self.screenshot_roster_btn.setVisible(False)
        self.delete_roster_btn.setVisible(False)
        self.player_info_box.setVisible(False)
        self.save_player_btn.setVisible(False)
        self.edit_player_btn.setVisible(False)
        self.delete_player_btn.setVisible(False)
        self.add_player_btn.setVisible(False)

        self.s_rosterGrp_list_1.installEventFilter(self)
        self.signup_list_tanks.installEventFilter(self)
        self.signup_list_warriors.installEventFilter(self)
        self.signup_list_rogues.installEventFilter(self)
        self.signup_list_hunters.installEventFilter(self)
        self.signup_list_druids.installEventFilter(self)
        self.signup_list_shamans.installEventFilter(self)
        self.signup_list_mages.installEventFilter(self)
        self.signup_list_warlocks.installEventFilter(self)
        self.signup_list_priests.installEventFilter(self)
        readOnlyStyle = "[readOnly=\"true\"]{color: rgb(136, 136, 136);}"

        self.signup_name_edit.setReadOnly(True)
        self.signup_date_edit.setReadOnly(True)
        self.signup_time_edit.setReadOnly(True)
        self.signup_txt_edit.setReadOnly(True)

        self.signup_name_edit.setStyleSheet(readOnlyStyle)
        self.signup_date_edit.setStyleSheet(readOnlyStyle)
        self.signup_time_edit.setStyleSheet(readOnlyStyle)
        self.signup_txt_edit.setStyleSheet(readOnlyStyle)

        stylesheet = '''
            QMainWindow {background-image: url(icons/RB_Background.png);
                background-repeat: no-repeat;
                background-position: center;
                background-color: rgb(33, 38, 36);}

            QDialog {background-color: rgb(45, 51, 49);
                border-color: rgb(255, 255, 255);}

            QDialog QLineEdit {background-color: rgb(255, 255, 255);
                font: 9pt;
                padding: 2px;}

            QDialog QLabel {color: rgb(145, 153, 190);
                background-color: rgb(45, 51, 49);
                padding: 1px; font: 12pt;}

            QDialog QPushButton {background-color: qlineargradient(
                        spread:pad, x1:1, y1:1, x2:1, y2:0,
                        stop:0.0738636 rgba(108, 114, 142, 255),
                        stop:1 rgba(255, 255, 255, 255));
                color: pallete(light); border-style: inset;
                border-width: 2px; padding: 3px; border-radius: 8px;
                font: 10pt; min-width: 2em; min-height: 1.5em;}

            QDialog QPushButton:hover:pressed {
                background-color: rgb(145, 153, 190);
                border-style: inset;}

            QDialog QPushButton:hover {background-color: qlineargradient(
                    spread:pad, x1:1, y1:1, x2:1, y2:0,
                    stop:0 rgba(195, 206, 255, 255),
                    stop:0.676136 rgba(255, 255, 255, 255));
                border-style: inset;}
            '''

        self.setStyleSheet(stylesheet)
        self.HandleButtons()
        self._fill_players()
        self._fill_rosters()
        self._fill_signups()

    def createIcons(self):
        raidLeadIcon = QPixmap(resource_path(
                    'icons/raidlead.png')).scaledToHeight(25, 1)
        guildieIcon = QPixmap(resource_path(
                    'icons/guildie.png')).scaledToHeight(25, 1)
        buyerIcon = QPixmap(resource_path(
                    'icons/buyer.png')).scaledToHeight(25, 1)
        carryIcon = QPixmap(resource_path(
                    'icons/carry.png')).scaledToHeight(25, 1)
        favoriteIcon = QPixmap(resource_path(
                    'icons/favorite.png')).scaledToHeight(25, 1)
        shitlistIcon = QPixmap(resource_path(
                    'icons/shitlist.png')).scaledToHeight(25, 1)

        r0 = QPixmap(resource_path(
            "icons/no-stars.png")).scaledToHeight(25, 1)
        r1 = QPixmap(resource_path(
            "icons/one-star.png")).scaledToHeight(25, 1)
        r2 = QPixmap(resource_path(
            "icons/two-stars.png")).scaledToHeight(25, 1)
        r3 = QPixmap(resource_path(
            "icons/three-stars.png")).scaledToHeight(25, 1)
        r4 = QPixmap(resource_path(
            "icons/four-stars.png")).scaledToHeight(25, 1)
        r5 = QPixmap(resource_path(
            "icons/five-stars.png")).scaledToHeight(25, 1)
        categoryIcons = [raidLeadIcon, guildieIcon, buyerIcon,
                         carryIcon, favoriteIcon, shitlistIcon]
        ratingIcons = [r0, r1, r2, r3, r4, r5]
        return categoryIcons, ratingIcons

    def parse_player_tbl(self, data, row_num, row_data, column_num, icons):
        categoryIcons = icons[0]
        ratingIcons = icons[1]
        iconHolder = QtWidgets.QLabel()
        tblItem = QTableWidgetItem(str(data))
        tblItem.setTextAlignment(Qt.AlignHCenter)
        tblItem.setTextAlignment(Qt.AlignVCenter)

        if column_num == 2:
            tblItem.setData(Qt.EditRole, data)
            tblItem.setForeground(QtGui.QColor('#2e303e'))
            if data:
                iconHolder = QtWidgets.QLabel()
                tblItem.setTextAlignment(Qt.AlignCenter)
                iconHolder.setAlignment(Qt.AlignCenter)
                iconHolder.setPixmap(categoryIcons[0])
                self.players_tbl.setCellWidget(row_num, column_num, iconHolder)
            else:
                tblItem.setText("")

        elif column_num == 3:
            tblItem.setData(Qt.EditRole, data)
            tblItem.setForeground(QtGui.QColor('#2e303e'))
            if data:
                iconHolder = QtWidgets.QLabel()
                tblItem.setTextAlignment(Qt.AlignCenter)
                iconHolder.setAlignment(Qt.AlignCenter)
                iconHolder.setPixmap(categoryIcons[1])
                self.players_tbl.setCellWidget(row_num, column_num, iconHolder)
            else:
                tblItem.setText("")
        elif column_num == 4:
            tblItem.setData(Qt.EditRole, data)
            tblItem.setForeground(QtGui.QColor('#2e303e'))
            if data:
                iconHolder = QtWidgets.QLabel()
                tblItem.setTextAlignment(Qt.AlignCenter)
                iconHolder.setAlignment(Qt.AlignCenter)
                iconHolder.setPixmap(categoryIcons[2])
                self.players_tbl.setCellWidget(row_num, column_num, iconHolder)
            else:
                tblItem.setText("")
        elif column_num == 5:
            tblItem.setData(Qt.EditRole, data)
            tblItem.setForeground(QtGui.QColor('#2e303e'))
            if data:
                iconHolder = QtWidgets.QLabel()
                tblItem.setTextAlignment(Qt.AlignCenter)
                iconHolder.setAlignment(Qt.AlignCenter)
                iconHolder.setPixmap(categoryIcons[3])
                self.players_tbl.setCellWidget(row_num, column_num, iconHolder)
            else:
                tblItem.setText("")
        elif column_num == 6:
            tblItem.setData(Qt.EditRole, data)
            tblItem.setForeground(QtGui.QColor('#2e303e'))
            if data:
                iconHolder = QtWidgets.QLabel()
                tblItem.setTextAlignment(Qt.AlignCenter)
                iconHolder.setAlignment(Qt.AlignCenter)
                iconHolder.setPixmap(categoryIcons[4])
                self.players_tbl.setCellWidget(row_num, column_num, iconHolder)
            else:
                tblItem.setText("")
        elif column_num == 7:
            tblItem.setData(Qt.EditRole, data)
            tblItem.setForeground(QtGui.QColor('#2e303e'))
            if data:
                iconHolder = QtWidgets.QLabel()
                tblItem.setTextAlignment(Qt.AlignCenter)
                iconHolder.setAlignment(Qt.AlignCenter)
                iconHolder.setPixmap(categoryIcons[5])
                self.players_tbl.setCellWidget(row_num, column_num, iconHolder)
            else:
                tblItem.setText("")
        elif column_num == 10:
            toon = ""
            toonsJson = json.loads(data)
            toonList = []
            if bool(toonsJson):
                for x in toonsJson:
                    toonList.append(x)
            if bool(toonList):
                toon = " or ".join(toonList)

            tblItem.setText(str(toon))

        self.players_tbl.setItem(row_num, column_num, tblItem)
        iconHolder.setStyleSheet("QLabel{background-color: rgba(0,0,0,0%);\
                                padding-left: 5px;\
                                padding-right: 5px;}")
        if column_num == 8:
            tblItem.setText("")
            tblItem.setData(Qt.EditRole, data)
            tblItem.setForeground(QtGui.QColor('#2e303e'))
            rating = QtWidgets.QLabel()
            rating.setText("")
            rating.setStyleSheet("QLabel{background-color: rgba(0,0,0,0%);\
                padding-left: 5px;\
                padding-right: 5px;}")
            if data < 2:
                rating.setPixmap(ratingIcons[0])
            elif data <= 3:
                rating.setPixmap(ratingIcons[1])
            elif data <= 5:
                rating.setPixmap(ratingIcons[2])
            elif data <= 7:
                rating.setPixmap(ratingIcons[3])
            elif data <= 9:
                rating.setPixmap(ratingIcons[4])
            elif data >= 10:
                rating.setPixmap(ratingIcons[5])
            self.players_tbl.setCellWidget(row_num, column_num, rating)

    def _fill_players(self):
        newQuery = Query()
        players = newQuery.getPlayers()
        self.players_tbl.setRowCount(0)

        icons = self.createIcons()

        for row_num, row_data in enumerate(players):
            self.players_tbl.insertRow(row_num)
            for column_num, data in enumerate(row_data):
                self.parse_player_tbl(data, row_num, row_data,
                                      column_num, icons)

        header = self.players_tbl.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(8, QtWidgets.QHeaderView.Stretch)

        header= self.toons_tbl.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

    def _fill_rosters(self):
        self.roster_combo.clear()
        self.saved_rosters_list.clear()
        newQuery = Query()
        rosters = newQuery.getRosters()
        resList = []
        for row_number, row_data in enumerate(rosters):
            rosterName = row_data[0]
            resList.append(rosterName)

        for r in reversed(resList):
            newQuery = Query()
            raid = newQuery.getRosterRaid(r)
            if raid is not None:
                rosterItem = QListWidgetItem(raid[0])
                rosterItem.setToolTip(r)
                self.saved_rosters_list.addItem(rosterItem)

        resList.append('Choose a saved roster...')

        self.roster_combo.addItems(reversed(resList))

    def _fill_signups(self):
        self.signup_cmbo.clear()
        self.saved_signups_list.clear()

        newQuery = Query()
        signups = newQuery.getSignup()
        resList = []
        for row_number, row_data in enumerate(signups):
            resList.append(row_data[0])

        for r in reversed(resList):
            signupsItem = QListWidgetItem(str(r))
            self.saved_signups_list.addItem(signupsItem)

        resList.append('Choose a signup list...')
        self.signup_cmbo.addItems(reversed(resList))
    
    def eventFilter(self, source, event):
        signupsMenu = QMenu()
        actions = [self.action_moveGrp1, self.action_moveGrp2,
                   self.action_moveGrp3, self.action_moveGrp4,
                   self.action_moveGrp5, self.action_moveGrp6,
                   self.action_moveGrp7, self.action_moveGrp8]
        for a in actions:
            signupsMenu.addAction(a)

        sources = [self.signup_list_tanks, self.signup_list_warriors,
                   self.signup_list_rogues, self.signup_list_hunters,
                   self.signup_list_druids, self.signup_list_shamans,
                   self.signup_list_mages, self.signup_list_warlocks,
                   self.signup_list_priests]

        if event.type() == QEvent.ContextMenu and source in sources\
                and source.itemAt(event.pos()) is not None:

            action = signupsMenu.exec_(event.globalPos())
            if action == self.action_moveGrp1:
                item = source.itemAt(event.pos())
                itemRow = source.row(item)
                takenItem = source.takeItem(itemRow)
                self.rosterGrp_list_1.addItem(takenItem)
            elif action == self.action_moveGrp2:
                item = source.itemAt(event.pos())
                itemRow = source.row(item)
                takenItem = source.takeItem(itemRow)
                self.rosterGrp_list_2.addItem(takenItem)
            elif action == self.action_moveGrp3:
                item = source.itemAt(event.pos())
                itemRow = source.row(item)
                takenItem = source.takeItem(itemRow)
                self.rosterGrp_list_3.addItem(takenItem)
            elif action == self.action_moveGrp4:
                item = source.itemAt(event.pos())
                itemRow = source.row(item)
                takenItem = source.takeItem(itemRow)
                self.rosterGrp_list_4.addItem(takenItem)
            elif action == self.action_moveGrp5:
                item = source.itemAt(event.pos())
                itemRow = source.row(item)
                takenItem = source.takeItem(itemRow)
                self.rosterGrp_list_5.addItem(takenItem)
            elif action == self.action_moveGrp6:
                item = source.itemAt(event.pos())
                itemRow = source.row(item)
                takenItem = source.takeItem(itemRow)
                self.rosterGrp_list_6.addItem(takenItem)
            elif action == self.action_moveGrp7:
                item = source.itemAt(event.pos())
                itemRow = source.row(item)
                takenItem = source.takeItem(itemRow)
                self.rosterGrp_list_7.addItem(takenItem)
            elif action == self.action_moveGrp8:
                item = source.itemAt(event.pos())
                itemRow = source.row(item)
                takenItem = source.takeItem(itemRow)
                self.rosterGrp_list_8.addItem(takenItem)
            return True

        return super().eventFilter(source, event)

    def HandleButtons(self):
        self.load_btn.clicked.connect(self.GET_DATA)

        self.create_new_btn.clicked.connect(self.CREATE_NEW)
        self.edit_signup_btn.clicked.connect(self.EDIT_SIGNUP)
        self.update_existing_btn.clicked.connect(self.UPDATE_EXISTING)
        self.reset_signup_btn.clicked.connect(self.RESET_SIGNUP)
        self.save_signup_btn.clicked.connect(self.SAVE_SIGNUP)

        self.save_roster_btn.clicked.connect(self.SAVE_ROSTER)
        self.prefill_roster_btn.clicked.connect(self.PREFILL_ROSTER)

        self.search_edit.returnPressed.connect(self.SEARCH_PLAYERS)
        self.search_btn.clicked.connect(self.SEARCH_PLAYERS)
        self.players_tbl.itemClicked.connect(self.PLAYER_INFO)
        self.save_player_btn.clicked.connect(self.SAVE_PLAYER)
        self.edit_player_btn.clicked.connect(self.EDIT_PLAYER)
        self.delete_player_btn.clicked.connect(self.DELETE_PLAYER)

        self.reset_roster_btn.clicked.connect(self.RESET_ROSTER)
        self.saved_rosters_btn.clicked.connect(self.OPEN_CLOSE_R_LIST)
        self.saved_rosters_list.itemClicked.connect(self.ROSTER_INFO)

        self.saved_signups_btn.clicked.connect(self.OPEN_CLOSE_S_LIST)
        self.saved_signups_list.itemClicked.connect(self.SIGNUP_INFO)

        self.delete_roster_btn.clicked.connect(self.DELETE_ROSTER)
        self.export_roster_btn.clicked.connect(self.EXPORT_ROSTER)
        self.import_roster_btn.clicked.connect(self.IMPORT_ROSTER)

        self.rosterGrp_list_1.clicked.connect(self.FIX_COLOR)
        self.rosterGrp_list_2.clicked.connect(self.FIX_COLOR)
        self.rosterGrp_list_3.clicked.connect(self.FIX_COLOR)
        self.rosterGrp_list_4.clicked.connect(self.FIX_COLOR)
        self.rosterGrp_list_5.clicked.connect(self.FIX_COLOR)
        self.rosterGrp_list_6.clicked.connect(self.FIX_COLOR)
        self.rosterGrp_list_7.clicked.connect(self.FIX_COLOR)
        self.rosterGrp_list_8.clicked.connect(self.FIX_COLOR)
        self.rosterStandby_list_1.clicked.connect(self.FIX_COLOR)
        self.rosterStandby_list_2.clicked.connect(self.FIX_COLOR)
        self.screenshot_roster_btn.clicked.connect(self.SCRNSHOT_ROSTER)

    def ADD_PLAYER(self):
        # TODO: Add ADD PLAYER functionality
        pass

    def SAVE_PLAYER(self):
        # TODO: Add SAVE PLAYER functionality
        pass

    def EDIT_PLAYER(self):
        # TODO: Add EDIT PLAYER functionality
        pass

    def DELETE_PLAYER(self):
        # TODO: Add DELETE PLAYER functionality
        pass

    def FIX_COLOR(self):
        self.rosterGrp_list_1.clearSelection()
        self.rosterGrp_list_2.clearSelection()
        self.rosterGrp_list_3.clearSelection()
        self.rosterGrp_list_4.clearSelection()
        self.rosterGrp_list_5.clearSelection()
        self.rosterGrp_list_6.clearSelection()
        self.rosterGrp_list_7.clearSelection()
        self.rosterGrp_list_8.clearSelection()
        self.rosterStandby_list_1.clearSelection()
        self.rosterStandby_list_2.clearSelection()

    def DELETE_ROSTER(self):
        slctRoster = self.saved_rosters_list.currentItem().toolTip()

        try:
            newQuery = Query()
            newQuery.deleteRoster(slctRoster)

            self.s_rosterGrp_list_1.clear()
            self.s_rosterGrp_list_2.clear()
            self.s_rosterGrp_list_3.clear()
            self.s_rosterGrp_list_4.clear()
            self.s_rosterGrp_list_5.clear()
            self.s_rosterGrp_list_6.clear()
            self.s_rosterGrp_list_7.clear()
            self.s_rosterGrp_list_8.clear()
            self.s_rosterStandby_list_1.clear()
            self.s_rosterStandby_list_2.clear()

            self.export_roster_btn.setVisible(False)
            self.screenshot_roster_btn.setVisible(False)
            self.delete_roster_btn.setVisible(False)

            # self.charview.hide()
            self._fill_rosters()

        except Exception as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            errMsg = "Error: "+str(error)
            msg.setText("Something went wrong")
            self.pyClassLog.error(errMsg)
            msg.setInformativeText(errMsg)
            msg.setWindowTitle("Oops!")
            msg.setWindowIcon(QIcon(
                                resource_path("icons/raidbuilder_icon.ico")))
            msg.exec_()

    def SCRNSHOT_ROSTER(self):
        msg = QMessageBox()
        try:
            now = datetime.now()
            nowString = now.strftime("%m_%d_%Y__T%H-%m")
            widg = self.s_roster_info_frame
            shortName = self.saved_rosters_list.currentItem().text()
            shortName = shortName + nowString + ".png"
            exportFolder = "exportedRosters/{}".format(shortName)

            image = QImage(widg.size(), QImage.Format_ARGB32_Premultiplied)
            painter = QPainter()

            painter.begin(image)
            painter.setRenderHint(QPainter.TextAntialiasing, True)
            widg.render(painter, QPoint(), QRegion(), QWidget.DrawChildren)
            path = resource_path(exportFolder)
            writer = QImageWriter(path)
            writer.write(image)
            painter.end()
            self.pyClassLog.info("Screenshot exported to {}".format(path))
            QApplication.clipboard().setImage(QImage(image),
                                              QClipboard.Clipboard)

            msg.setText("Copied to clipboard!")
            msg.setInformativeText("Roster screenshot has been copied to "\
                                   " clipboard and written to the "\
                                   "exportedRosters folder.")
            msg.setWindowTitle("Screenshot captured")
            msg.setWindowIcon(QIcon(
                              resource_path("icons/raidbuilder_icon.ico")))
            msg.exec_()
        except Exception as error:
            msg.setIcon(QMessageBox.Critical)
            errMsg = "Error: "+str(error)
            msg.setText("Something went wrong")
            self.pyClassLog.error(errMsg)
            msg.setInformativeText(errMsg)
            msg.setWindowTitle("Oops!")
            msg.setWindowIcon(QIcon(
                              resource_path("icons/raidbuilder_icon.ico")))

    def EXPORT_ROSTER(self):
        slctRoster = self.saved_rosters_list.currentItem().toolTip()
        shortName = self.saved_rosters_list.currentItem().text()
        exportFolder = "exportedRosters/{}".format(shortName)
        name = resource_path(exportFolder)
        try:
            saveAs = QFileDialog.getSaveFileName(self, "Save Roster", name,
                                                 "JSON Files (*.json)")[0]
            if len(saveAs.strip()) > 0:
                self.pyClassLog.info(slctRoster +
                                     " to be exported to " + saveAs)
                newQuery = Query()
                roster = newQuery.getRoster(slctRoster)
                rosterDict = json.loads(roster[0])
                rosterJson = json.dumps(rosterDict, indent=4)
                with open(saveAs, 'w') as jFile:
                    jFile.write(rosterJson)
                    self.pyClassLog.info(slctRoster +
                                         " successfully exported to " + saveAs)
            else:
                return

        except Exception as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            errMsg = "Error: "+str(error)
            msg.setText("Something went wrong")
            self.pyClassLog.error(errMsg)
            msg.setInformativeText(errMsg)
            msg.setWindowTitle("Oops!")
            msg.setWindowIcon(QIcon(
                                resource_path("icons/raidbuilder_icon.ico")))
            msg.exec_()

    def IMPORT_ROSTER(self):
        saveAs = QInputDialog()
        rosterName, ok = saveAs.getText(self, 'Input Dialog',
                                        'Save roster as:',
                                        QLineEdit.Normal)
        try:
            if ok and len(rosterName.strip()) > 0:
                fname = QFileDialog.getOpenFileName(self,
                                                    'Import Roster', './',
                                                    "JSON Files (*.json)")[0]
                self.pyClassLog.info(rosterName +
                                     " chosen to be imported to from " + fname)
                if len(fname.strip()) > 0:
                    with open(fname, 'r') as jFile:
                        data = jFile.read()
                        self.pyClassLog.info("Read data from " + fname)
                        dataCheck = json.loads(data)
                        self.pyClassLog.info("Loaded file as JSON")
                        newRoster = Roster(rosterName, data)
                    self._fill_rosters()
                    rosterName = newRoster.getName()
                    raidName = newRoster.getRaid()
                    for x in range(self.saved_rosters_list.count()):
                        raid = self.saved_rosters_list.item(x).text()
                        name = self.saved_rosters_list.item(x).toolTip()
                        if raid == raidName and name == rosterName:
                            self.saved_rosters_list.setCurrentRow(x)
                            self.ROSTER_INFO()
            else:
                return

        except Exception as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            errMsg = "Error: "+str(error)
            msg.setText("Something went wrong")
            self.pyClassLog.error(errMsg)
            msg.setInformativeText(errMsg)
            msg.setWindowTitle("Oops!")
            msg.setWindowIcon(QIcon(
                                resource_path("icons/raidbuilder_icon.ico")))
            msg.exec_()

    def PLAYER_INFO(self):
        self.player_info_box.setVisible(True)
        self.disc_name_edit.setText("")
        self.aliases_edit.setText("")
        self.raid_lead_combo.setCurrentIndex(0)
        self.guildie_combo.setCurrentIndex(0)
        self.buyer_combo.setCurrentIndex(0)
        self.carry_combo.setCurrentIndex(0)
        self.fav_combo.setCurrentIndex(0)
        self.shitlist_combo.setCurrentIndex(0)
        self.toons_tbl.setRowCount(0)

        item = self.players_tbl.currentRow()
        p_id = self.players_tbl.item(item, 0).text()

        try:
            newQuery = Query()
            result = newQuery.getSelectedPlayersInfo(p_id)

            p_name = self.players_tbl.item(item, 1).text()
            p_alias = result[0]
            p_rl = int(result[1])
            p_gld = int(result[2])
            p_buy = int(result[3])
            p_carry = int(result[4])
            p_fav = int(result[5])
            p_shit = int(result[6])

            self.disc_name_edit.setText(p_name)
            self.aliases_edit.setText(p_alias)
            if p_rl:
                self.raid_lead_combo.setCurrentIndex(1)
            if p_gld:
                self.guildie_combo.setCurrentIndex(1)
            if p_buy:
                self.buyer_combo.setCurrentIndex(1)
            if p_carry:
                self.carry_combo.setCurrentIndex(1)
            if p_fav:
                self.fav_combo.setCurrentIndex(1)
            if p_shit:
                self.fav_combo.setCurrentIndex(0)
                self.shitlist_combo.setCurrentIndex(1)

            newQuery = Query()
            result = newQuery.getSelectedPlayersToons(p_id)
            if result[0] is not None:
                toonList = json.loads(result[0])
            else:
                toonList = {}
            for row, toon in enumerate(toonList):
                self.toons_tbl.insertRow(row)
                name = toon
                wClass = toonList[toon]
                tblItem_name = QTableWidgetItem(str(name))
                tblItem_wClass = QTableWidgetItem(str(wClass))
                self.toons_tbl.setItem(row, 0, tblItem_name)
                self.toons_tbl.setItem(row, 1, tblItem_wClass)

            header = self.toons_tbl.horizontalHeader()
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        except Exception as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            errMsg = "Error: "+str(error)
            msg.setText("Something went wrong")
            self.pyClassLog.error(errMsg)
            msg.setInformativeText(errMsg)
            msg.setWindowTitle("Oops!")
            msg.setWindowIcon(QIcon(
                                resource_path("icons/raidbuilder_icon.ico")))
            msg.exec_()

    def SEARCH_PLAYERS(self):
        searchText = self.search_edit.text().strip()
        items = self.players_tbl.findItems(searchText, Qt.MatchContains)
        for i in range(self.players_tbl.rowCount()):
            self.players_tbl.hideRow(i)

        for i in range(len(items)):
            self.players_tbl.showRow(items[i].row())

    def countRoster(self, countJson, role):
        healers = countJson["healers"]
        tanks = countJson["tanks"]
        melee = countJson["melee"]
        ranged = countJson["ranged"]
        rosterNum = countJson["rosterNum"]

        rosterNum += 1
        if role in ("RestoDruid", "RestoShaman", "Priest"):
            healers += 1
        elif role in ("Tank", "BearTank", "ProtPaladin"):
            tanks += 1
        elif role in ("Hunter", "Mage", "Warlock", "ElemShaman",
                      "ShadowPriest"):
            ranged += 1
        elif role in ("Warrior", "Rogue", "FeralDruid", "BalanceDruid",
                      "EnhShaman"):
            melee += 1

        countJson = {"healers": healers, "tanks": tanks, "melee": melee,
                     "ranged": ranged, "rosterNum": rosterNum}
        return countJson

    def ROSTER_INFO(self):
        self.s_rosterGrp_list_1.clear()
        self.s_rosterGrp_list_2.clear()
        self.s_rosterGrp_list_3.clear()
        self.s_rosterGrp_list_4.clear()
        self.s_rosterGrp_list_5.clear()
        self.s_rosterGrp_list_6.clear()
        self.s_rosterGrp_list_7.clear()
        self.s_rosterGrp_list_8.clear()
        self.s_rosterStandby_list_1.clear()
        self.s_rosterStandby_list_2.clear()
        self.export_roster_btn.setVisible(True)
        self.screenshot_roster_btn.setVisible(True)
        self.delete_roster_btn.setVisible(True)
        slctRoster = self.saved_rosters_list.currentItem().toolTip()

        countJson = {"healers": 0, "tanks": 0, "melee": 0, "ranged": 0,
                     "rosterNum": 0}
        try:
            newQuery = Query()
            roster = newQuery.getRoster(slctRoster)
            rosterDict = json.loads(roster[0])
            grp1 = rosterDict["grp1"]
            for item in grp1:
                signee = QListWidgetItem(item)
                role = grp1[item]
                coloredSignee = self.colorMe(role, signee)
                self.s_rosterGrp_list_1.addItem(coloredSignee)
                countJson = self.countRoster(countJson, role)

            grp2 = rosterDict["grp2"]
            for item in grp2:
                signee = QListWidgetItem(item)
                role = grp2[item]
                coloredSignee = self.colorMe(role, signee)
                self.s_rosterGrp_list_2.addItem(coloredSignee)
                countJson = self.countRoster(countJson, role)

            grp3 = rosterDict["grp3"]
            for item in grp3:
                signee = QListWidgetItem(item)
                role = grp3[item]
                coloredSignee = self.colorMe(role, signee)
                self.s_rosterGrp_list_3.addItem(coloredSignee)
                countJson = self.countRoster(countJson, role)

            grp4 = rosterDict["grp4"]
            for item in grp4:
                signee = QListWidgetItem(item)
                role = grp4[item]
                coloredSignee = self.colorMe(role, signee)
                self.s_rosterGrp_list_4.addItem(coloredSignee)
                countJson = self.countRoster(countJson, role)

            grp5 = rosterDict["grp5"]
            for item in grp5:
                signee = QListWidgetItem(item)
                role = grp5[item]
                coloredSignee = self.colorMe(role, signee)
                self.s_rosterGrp_list_5.addItem(coloredSignee)
                countJson = self.countRoster(countJson, role)

            grp6 = rosterDict["grp6"]
            for item in grp6:
                signee = QListWidgetItem(item)
                role = grp6[item]
                coloredSignee = self.colorMe(role, signee)
                self.s_rosterGrp_list_6.addItem(coloredSignee)
                countJson = self.countRoster(countJson, role)

            grp7 = rosterDict["grp7"]
            for item in grp7:
                signee = QListWidgetItem(item)
                role = grp7[item]
                coloredSignee = self.colorMe(role, signee)
                self.s_rosterGrp_list_7.addItem(coloredSignee)
                countJson = self.countRoster(countJson, role)

            grp8 = rosterDict["grp8"]
            for item in grp8:
                signee = QListWidgetItem(item)
                role = grp8[item]
                coloredSignee = self.colorMe(role, signee)
                self.s_rosterGrp_list_8.addItem(coloredSignee)
                countJson = self.countRoster(countJson, role)

            stdby1 = rosterDict["stdby1"]
            for item in stdby1:
                signee = QListWidgetItem(item)
                role = stdby1[item]
                coloredSignee = self.colorMe(role, signee)
                self.s_rosterStandby_list_1.addItem(coloredSignee)

            stdby2 = rosterDict["stdby2"]
            for item in stdby2:
                signee = QListWidgetItem(item)
                role = stdby2[item]
                coloredSignee = self.colorMe(role, signee)
                self.s_rosterStandby_list_2.addItem(coloredSignee)

            self.pieseries = QPieSeries()
            countHealers = countJson["healers"]
            countTanks = countJson["tanks"]
            countMelee = countJson["melee"]
            countRanged = countJson["ranged"]
            self.chart.removeAllSeries()
            self.pieseries.append("Healers ({})".format(countHealers),
                                  countHealers)
            self.pieseries.append("Tanks ({})".format(countTanks),
                                  countTanks)
            self.pieseries.append("Ranged ({})".format(countRanged),
                                  countRanged)
            self.pieseries.append("Melee ({})".format(countMelee),
                                  countMelee)
            for i in self.pieseries.slices():
                i.setLabelVisible()
                i.setLabelPosition(QPieSlice.LabelOutside)
                i.setLabelArmLengthFactor(0.1)
            self.chart.addSeries(self.pieseries)
            self.charview.show()

        except Exception as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            errMsg = "Error: "+str(error)
            msg.setText("Something went wrong")
            self.pyClassLog.error(errMsg)
            msg.setInformativeText(errMsg)
            msg.setWindowTitle("Oops!")
            msg.setWindowIcon(QIcon(
                                resource_path("icons/raidbuilder_icon.ico")))
            msg.exec_()

    def OPEN_CLOSE_R_LIST(self):
        if self.saved_rosters_btn.isChecked():
            self.saved_rosters_list.setVisible(True)
        else:
            self.saved_rosters_list.setVisible(False)

    def OPEN_CLOSE_S_LIST(self):
        if self.saved_signups_btn.isChecked():
            self.saved_signups_list.setVisible(True)
        else:
            self.saved_signups_list.setVisible(False)

    def CREATE_NEW(self):
        self.signup_name_edit.clear()
        self.signup_txt_edit.clear()
        today = QtCore.QDate.currentDate()
        self.signup_date_edit.setDate(today)

        notReadOnlyStyleO = "[readOnly=\"false\"]{color: rgb(0, 0, 0);}"
        notReadOnlyStylePt = "[readOnly=\"false\"]{color: rgb(255, 255, 255);}"
        self.signup_name_edit.setReadOnly(False)
        self.signup_date_edit.setReadOnly(False)
        self.signup_time_edit.setReadOnly(False)
        self.signup_txt_edit.setReadOnly(False)

        self.signup_name_edit.setStyleSheet(notReadOnlyStyleO)
        self.signup_date_edit.setStyleSheet(notReadOnlyStyleO)
        self.signup_time_edit.setStyleSheet(notReadOnlyStyleO)
        self.signup_txt_edit.setStyleSheet(notReadOnlyStylePt)

        self.reset_signup_btn.setVisible(True)
        self.save_signup_btn.setVisible(True)
        self.edit_signup_btn.setVisible(False)
        self.update_existing_btn.setVisible(False)

    def SIGNUP_INFO(self):
        self.signup_name_edit.clear()
        readOnlyStyle = "[readOnly=\"true\"]{color: rgb(136, 136, 136);}"

        self.signup_name_edit.setReadOnly(True)
        self.signup_date_edit.setReadOnly(True)
        self.signup_time_edit.setReadOnly(True)
        self.signup_txt_edit.setReadOnly(True)

        self.signup_name_edit.setStyleSheet(readOnlyStyle)
        self.signup_date_edit.setStyleSheet(readOnlyStyle)
        self.signup_time_edit.setStyleSheet(readOnlyStyle)
        self.signup_txt_edit.setStyleSheet(readOnlyStyle)

        self.reset_signup_btn.setVisible(True)
        self.save_signup_btn.setVisible(False)
        self.edit_signup_btn.setVisible(True)
        self.update_existing_btn.setVisible(False)

        self.signup_txt_edit.clear()

        slctSignup = self.saved_signups_list.currentItem().text()
        self.signup_name_edit.setText(slctSignup)
        newQuery = Query()
        result = newQuery.getSignupText(slctSignup)
        if result is not None:
            for row_number, row_data in enumerate(result):
                row_data = str(row_data).replace("('", "").replace("',)", "")\
                                .replace("\\u200e", "").replace("\\n", "\n")\
                                .replace("\\r", "")
                rowList = row_data.split("\n")
                for item in rowList:
                    self.signup_txt_edit.appendPlainText(item)

        newQuery = Query()
        dateTime = newQuery.getSignupDateTime(slctSignup)
        if dateTime is not None:
            for row_number, row_data in enumerate(dateTime):
                dtformat = "yyyy-MM-dd HH:mm:ss"
                qdateTime = QtCore.QDateTime.fromString(row_data, dtformat)
                self.signup_date_edit.setDate(qdateTime.date())
                self.signup_time_edit.setTime(qdateTime.time())

    def EDIT_SIGNUP(self):
        notReadOnlyStyleO = "[readOnly=\"false\"]{color: rgb(0, 0, 0);}"
        notReadOnlyStylePt = "[readOnly=\"false\"]{color: rgb(255, 255, 255);}"
        self.signup_name_edit.setReadOnly(False)
        self.signup_date_edit.setReadOnly(False)
        self.signup_time_edit.setReadOnly(False)
        self.signup_txt_edit.setReadOnly(False)

        self.signup_name_edit.setStyleSheet(notReadOnlyStyleO)
        self.signup_date_edit.setStyleSheet(notReadOnlyStyleO)
        self.signup_time_edit.setStyleSheet(notReadOnlyStyleO)
        self.signup_txt_edit.setStyleSheet(notReadOnlyStylePt)

        self.reset_signup_btn.setVisible(True)
        self.save_signup_btn.setVisible(False)
        self.edit_signup_btn.setVisible(False)
        self.update_existing_btn.setVisible(True)

    def UPDATE_EXISTING(self):
        try:
            slctSignup = self.saved_signups_list.currentItem().text()
            newQuery = Query()
            ex_signup_id = newQuery.getThisSignup(slctSignup)
            if ex_signup_id is not None:
                newName = self.signup_name_edit.text()
                s_date = self.signup_date_edit.date()
                s_time = self.signup_time_edit.time()
                text = self.signup_txt_edit.toPlainText()

                if len(newName) < 1:
                    raise Exception("Signup not named.")
                elif len(text) < 1:
                    raise Exception("Signups are empty. Please paste the "\
                                    "signups from discord into the text "\
                                    "edit field.")

                signupID = ex_signup_id[0]
                deleteSignees = Query()
                deleteSignees.deleteAllSignees(signupID)
                updateSignup = Signup(newName, s_date, s_time, text, signupID)

                self._fill_signups()
                self.RESET_SIGNUP()
                readOnlyStyle = "[readOnly=\"true\"]{color: rgb(136, 136, 136);}"

                self.signup_name_edit.setReadOnly(True)
                self.signup_date_edit.setReadOnly(True)
                self.signup_time_edit.setReadOnly(True)
                self.signup_txt_edit.setReadOnly(True)

                self.signup_name_edit.setStyleSheet(readOnlyStyle)
                self.signup_date_edit.setStyleSheet(readOnlyStyle)
                self.signup_time_edit.setStyleSheet(readOnlyStyle)
                self.signup_txt_edit.setStyleSheet(readOnlyStyle)

                self.reset_signup_btn.setVisible(False)
                self.save_signup_btn.setVisible(False)
                self.edit_signup_btn.setVisible(False)
                self.update_existing_btn.setVisible(False)

        except Exception as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            errMsg = "Error: "+str(error)
            msg.setText("Something went wrong")
            self.pyClassLog.error(errMsg)
            msg.setInformativeText(errMsg)
            msg.setWindowTitle("Oops!")
            msg.setWindowIcon(QIcon(
                                resource_path("icons/raidbuilder_icon.ico")))
            msg.exec_()

    def RESET_SIGNUP(self):
        readOnlyStyle = "[readOnly=\"true\"]{color: rgb(136, 136, 136);}"
        self.signup_name_edit.setReadOnly(True)
        self.signup_date_edit.setReadOnly(True)
        self.signup_time_edit.setReadOnly(True)
        self.signup_txt_edit.setReadOnly(True)

        self.signup_name_edit.setStyleSheet(readOnlyStyle)
        self.signup_date_edit.setStyleSheet(readOnlyStyle)
        self.signup_time_edit.setStyleSheet(readOnlyStyle)
        self.signup_txt_edit.setStyleSheet(readOnlyStyle)

        self.reset_signup_btn.setVisible(False)
        self.save_signup_btn.setVisible(False)
        self.edit_signup_btn.setVisible(False)
        self.update_existing_btn.setVisible(False)

        self.signup_name_edit.clear()
        today = QtCore.QDate.currentDate()
        self.signup_date_edit.setDate(today)
        self.signup_time_edit.setTime(QtCore.QTime(21, 00, 00))
        self.signup_txt_edit.clear()

    def RESET_ROSTER(self):
        self.roster_combo.setVisible(False)
        self.prefill_roster_btn.setVisible(False)
        self.roster_combo.setDisabled(True)
        self.prefill_roster_btn.setDisabled(True)
        self.reset_roster_btn.setVisible(False)
        self.save_roster_btn.setVisible(False)

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
        self.rosterGrp_list_1.clear()
        self.rosterGrp_list_2.clear()
        self.rosterGrp_list_3.clear()
        self.rosterGrp_list_4.clear()
        self.rosterGrp_list_5.clear()
        self.rosterGrp_list_6.clear()
        self.rosterGrp_list_7.clear()
        self.rosterGrp_list_8.clear()
        self.rosterStandby_list_1.clear()
        self.rosterStandby_list_2.clear()

    def SAVE_SIGNUP(self):
        try:
            name = self.signup_name_edit.text()
            s_date = self.signup_date_edit.date()
            s_time = self.signup_time_edit.time()
            text = self.signup_txt_edit.toPlainText()

            if len(name) < 1:
                raise Exception("Signup not named.")
            elif len(text) < 1:
                raise Exception("Signups are empty. Please paste the "\
                                "signups from discord into the text "\
                                "edit field.")

            newSignup = Signup(name, s_date, s_time, text)
            self._fill_signups()
            self.RESET_SIGNUP()
            readOnlyStyle = "[readOnly=\"true\"]{color: rgb(136, 136, 136);}"
            self.signup_name_edit.setReadOnly(True)
            self.signup_date_edit.setReadOnly(True)
            self.signup_time_edit.setReadOnly(True)
            self.signup_txt_edit.setReadOnly(True)

            self.signup_name_edit.setStyleSheet(readOnlyStyle)
            self.signup_date_edit.setStyleSheet(readOnlyStyle)
            self.signup_time_edit.setStyleSheet(readOnlyStyle)
            self.signup_txt_edit.setStyleSheet(readOnlyStyle)

            self.reset_signup_btn.setVisible(False)
            self.save_signup_btn.setVisible(False)
            self.edit_signup_btn.setVisible(False)
            self.update_existing_btn.setVisible(False)

        except Exception as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            errMsg = "Error: "+str(error)
            msg.setText("Something went wrong")
            self.pyClassLog.error(errMsg)
            msg.setInformativeText(errMsg)
            msg.setWindowTitle("Oops!")
            msg.setWindowIcon(QIcon(
                                resource_path("icons/raidbuilder_icon.ico")))
            msg.exec_()

    def SAVE_ROSTER(self):
        try:
            slctSignup = self.signup_cmbo.currentText()
            saveAs = QInputDialog()
            rosterName, ok = saveAs.getText(self, 'Input Dialog',
                                            'Save roster as:',
                                            QLineEdit.Normal, slctSignup)

            if ok:
                self.roster_combo.setVisible(False)
                self.prefill_roster_btn.setVisible(False)
                self.pre_rost_radbtn.setVisible(False)
                self.pre_favs_radbtn.setVisible(False)
                self.reset_roster_btn.setVisible(True)
                self.save_roster_btn.setVisible(True)
                grp1Dict = {}
                grp1 = self.rosterGrp_list_1
                for x in range(grp1.count()):
                    tagrole = grp1.item(x).data(QtCore.Qt.UserRole)
                    name = grp1.item(x).text()
                    grp1Dict[name] = str(tagrole)

                grp2Dict = {}
                grp2 = self.rosterGrp_list_2
                for x in range(grp2.count()):
                    tagrole = grp2.item(x).data(QtCore.Qt.UserRole)
                    name = grp2.item(x).text()
                    grp2Dict[name] = str(tagrole)

                grp3Dict = {}
                grp3 = self.rosterGrp_list_3
                for x in range(grp3.count()):
                    tagrole = grp3.item(x).data(QtCore.Qt.UserRole)
                    name = grp3.item(x).text()
                    grp3Dict[name] = str(tagrole)

                grp4Dict = {}
                grp4 = self.rosterGrp_list_4
                for x in range(grp4.count()):
                    tagrole = grp4.item(x).data(QtCore.Qt.UserRole)
                    name = grp4.item(x).text()
                    grp4Dict[name] = str(tagrole)

                grp5Dict = {}
                grp5 = self.rosterGrp_list_5
                for x in range(grp5.count()):
                    tagrole = grp5.item(x).data(QtCore.Qt.UserRole)
                    name = grp5.item(x).text()
                    grp5Dict[name] = str(tagrole)

                grp6Dict = {}
                grp6 = self.rosterGrp_list_6
                for x in range(grp6.count()):
                    tagrole = grp6.item(x).data(QtCore.Qt.UserRole)
                    name = grp6.item(x).text()
                    grp6Dict[name] = str(tagrole)

                grp7Dict = {}
                grp7 = self.rosterGrp_list_7
                for x in range(grp7.count()):
                    tagrole = grp7.item(x).data(QtCore.Qt.UserRole)
                    name = grp7.item(x).text()
                    grp7Dict[name] = str(tagrole)

                grp8Dict = {}
                grp8 = self.rosterGrp_list_8
                for x in range(grp8.count()):
                    tagrole = grp8.item(x).data(QtCore.Qt.UserRole)
                    name = grp8.item(x).text()
                    grp8Dict[name] = str(tagrole)

                stdby1Dict = {}
                stdby1 = self.rosterStandby_list_1
                for x in range(stdby1.count()):
                    tagrole = stdby1.item(x).data(QtCore.Qt.UserRole)
                    name = stdby1.item(x).text()
                    stdby1Dict[name] = str(tagrole)

                stdby2Dict = {}
                stdby2 = self.rosterStandby_list_2
                for x in range(stdby2.count()):
                    tagrole = stdby2.item(x).data(QtCore.Qt.UserRole)
                    name = stdby2.item(x).text()
                    stdby2Dict[name] = str(tagrole)

                rosterDict = {"grp1": grp1Dict,
                            "grp2": grp2Dict,
                            "grp3": grp3Dict,
                            "grp4": grp4Dict,
                            "grp5": grp5Dict,
                            "grp6": grp6Dict,
                            "grp7": grp7Dict,
                            "grp8": grp8Dict,
                            "stdby1": stdby1Dict,
                            "stdby2": stdby2Dict}
                other = json.dumps(rosterDict)
                newRoster = Roster(rosterName, other)
                self._fill_rosters()
        except Exception as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            errMsg = "Error: "+str(error)
            msg.setText("Something went wrong")
            self.pyClassLog.error(errMsg)
            msg.setInformativeText(errMsg)
            msg.setWindowTitle("Oops!")
            msg.setWindowIcon(QIcon(
                                resource_path("icons/raidbuilder_icon.ico")))
            msg.exec_()

    def checkOtherWidgs(self, coloredSignee):
        widgs = [self.signup_list_absent,
                 self.signup_list_bench]
        listItem = coloredSignee.text() + " (Not found)"
        for widg in widgs:
            for x in range(widg.count()):
                cRole = coloredSignee.data(QtCore.Qt.UserRole)
                cName = coloredSignee.text()
                iRole = widg.item(x).data(QtCore.Qt.UserRole)
                iName = widg.item(x).text()
                if cName == iName and cRole == iRole:
                    if widg == self.signup_list_absent:
                        listItem = iName + " (Absent)"
                    elif widg == self.signup_list_bench:
                        listItem = iName + " (Bench)"
                    return listItem
                if cName == iName and iRole is None:
                    if widg == self.signup_list_absent:
                        listItem = iName + " (Absent)"
                    elif widg == self.signup_list_bench:
                        listItem = iName + " (Bench)"
                    return listItem
        return listItem

    def checkRoleWidgs(self, coloredSignee):
        widgs = [self.signup_list_druids,
                 self.signup_list_hunters,
                 self.signup_list_mages,
                 self.signup_list_other,
                 self.signup_list_priests,
                 self.signup_list_rogues,
                 self.signup_list_shamans,
                 self.signup_list_tanks,
                 self.signup_list_tentative,
                 self.signup_list_warlocks,
                 self.signup_list_warriors,
                 self.signup_list_late]
        found = False
        for widg in widgs:
            for x in range(widg.count()):
                cRole = coloredSignee.data(QtCore.Qt.UserRole)
                cName = coloredSignee.text()
                iRole = widg.item(x).data(QtCore.Qt.UserRole)
                iName = widg.item(x).text()
                if cName == iName and cRole == iRole:
                    found = True
                    widg.takeItem(x)
                    return found
        return found

    def PREFILL_ROSTER(self):
        try:
            notPrflld = []
            slctRoster = self.roster_combo.currentText()
            if slctRoster != "Choose a saved roster...":
                self.roster_combo.setDisabled(True)
                self.prefill_roster_btn.setDisabled(True)
                newQuery = Query()
                roster = newQuery.getRoster(slctRoster)
                rosterDict = json.loads(roster[0])
                grp1 = rosterDict["grp1"]
                for item in grp1:
                    signee = QListWidgetItem(item)
                    role = grp1[item]
                    coloredSignee = self.colorMe(role, signee)
                    found = self.checkRoleWidgs(coloredSignee)
                    if found:
                        self.rosterGrp_list_1.addItem(coloredSignee)
                    else:
                        listItem = self.checkOtherWidgs(coloredSignee)
                        notPrflld.append("Group 1: "+listItem)

                grp2 = rosterDict["grp2"]
                for item in grp2:
                    signee = QListWidgetItem(item)
                    role = grp2[item]
                    coloredSignee = self.colorMe(role, signee)
                    found = self.checkRoleWidgs(coloredSignee)
                    if found:
                        self.rosterGrp_list_2.addItem(coloredSignee)
                    else:
                        listItem = self.checkOtherWidgs(coloredSignee)
                        notPrflld.append("Group 2: "+listItem)

                grp3 = rosterDict["grp3"]
                for item in grp3:
                    signee = QListWidgetItem(item)
                    role = grp3[item]
                    coloredSignee = self.colorMe(role, signee)
                    found = self.checkRoleWidgs(coloredSignee)
                    if found:
                        self.rosterGrp_list_3.addItem(coloredSignee)
                    else:
                        listItem = self.checkOtherWidgs(coloredSignee)
                        notPrflld.append("Group 3: "+listItem)

                grp4 = rosterDict["grp4"]
                for item in grp4:
                    signee = QListWidgetItem(item)
                    role = grp4[item]
                    coloredSignee = self.colorMe(role, signee)
                    found = self.checkRoleWidgs(coloredSignee)
                    if found:
                        self.rosterGrp_list_4.addItem(coloredSignee)
                    else:
                        listItem = self.checkOtherWidgs(coloredSignee)
                        notPrflld.append("Group 4: "+listItem)

                grp5 = rosterDict["grp5"]
                for item in grp5:
                    signee = QListWidgetItem(item)
                    role = grp5[item]
                    coloredSignee = self.colorMe(role, signee)
                    found = self.checkRoleWidgs(coloredSignee)
                    if found:
                        self.rosterGrp_list_5.addItem(coloredSignee)
                    else:
                        listItem = self.checkOtherWidgs(coloredSignee)
                        notPrflld.append("Group 5: "+listItem)

                grp6 = rosterDict["grp6"]
                for item in grp6:
                    signee = QListWidgetItem(item)
                    role = grp6[item]
                    coloredSignee = self.colorMe(role, signee)
                    found = self.checkRoleWidgs(coloredSignee)
                    if found:
                        self.rosterGrp_list_6.addItem(coloredSignee)
                    else:
                        listItem = self.checkOtherWidgs(coloredSignee)
                        notPrflld.append("Group 6: "+listItem)

                grp7 = rosterDict["grp7"]
                for item in grp7:
                    signee = QListWidgetItem(item)
                    role = grp7[item]
                    coloredSignee = self.colorMe(role, signee)
                    found = self.checkRoleWidgs(coloredSignee)
                    if found:
                        self.rosterGrp_list_7.addItem(coloredSignee)
                    else:
                        listItem = self.checkOtherWidgs(coloredSignee)
                        notPrflld.append("Group 7: "+listItem)

                grp8 = rosterDict["grp8"]
                for item in grp8:
                    signee = QListWidgetItem(item)
                    role = grp8[item]
                    coloredSignee = self.colorMe(role, signee)
                    found = self.checkRoleWidgs(coloredSignee)
                    if found:
                        self.rosterGrp_list_8.addItem(coloredSignee)
                    else:
                        listItem = self.checkOtherWidgs(coloredSignee)
                        notPrflld.append("Group 8: "+listItem)

                stdby1 = rosterDict["stdby1"]
                for item in stdby1:
                    signee = QListWidgetItem(item)
                    role = stdby1[item]
                    coloredSignee = self.colorMe(role, signee)
                    found = self.checkRoleWidgs(coloredSignee)
                    if found:
                        self.rosterStandby_list_1.addItem(coloredSignee)
                    else:
                        listItem = self.checkOtherWidgs(coloredSignee)
                        notPrflld.append("Standby 1: "+listItem)

                stdby2 = rosterDict["stdby2"]
                for item in stdby2:
                    signee = QListWidgetItem(item)
                    role = stdby2[item]
                    coloredSignee = self.colorMe(role, signee)
                    found = self.checkRoleWidgs(coloredSignee)
                    if found:
                        self.rosterStandby_list_2.addItem(coloredSignee)
                    else:
                        listItem = self.checkOtherWidgs(coloredSignee)
                        notPrflld.append("Standby 2: "+listItem)

                if len(notPrflld) >= 1:
                    newMsg = "\n".join(notPrflld)
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Some players could not be prefilled"
                                " because they are either absent,"
                                " benched, signed up as different role,"
                                " or not signed up at all."
                                "\n\nSee details for the list...")
                    msg.setDetailedText(newMsg)
                    msg.setWindowTitle("Players not prefilled")
                    msg.setWindowIcon(QIcon(
                                    resource_path("icons/raidbuilder_icon.ico")))
                    msg.exec_()
        except Exception as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            errMsg = "Error: "+str(error)
            msg.setText("Something went wrong")
            self.pyClassLog.error(errMsg)
            msg.setInformativeText(errMsg)
            msg.setWindowTitle("Oops!")
            msg.setWindowIcon(QIcon(
                                resource_path("icons/raidbuilder_icon.ico")))
            msg.exec_()

    def GET_DATA(self):
        try:
            slctSignup = self.signup_cmbo.currentText()
            msg = QMessageBox()
            if slctSignup == 'Choose a signup list...':
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Signup not found")
                msg.setInformativeText("Looks like you didn't select a signup"
                                       " name from the dropdown")
                msg.setWindowTitle("Oops!")
                msg.setWindowIcon(QIcon(resource_path(
                                    "icons/raidbuilder_icon.ico")))
                msg.exec_()
            else:
                self.roster_combo.setVisible(True)
                self.prefill_roster_btn.setVisible(True)
                self.roster_combo.setEnabled(True)
                self.prefill_roster_btn.setEnabled(True)
                self.reset_roster_btn.setVisible(True)
                self.save_roster_btn.setVisible(True)
                self.save_roster_btn.setEnabled(True)

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
                self.rosterGrp_list_1.clear()
                self.rosterGrp_list_2.clear()
                self.rosterGrp_list_3.clear()
                self.rosterGrp_list_4.clear()
                self.rosterGrp_list_5.clear()
                self.rosterGrp_list_6.clear()
                self.rosterGrp_list_7.clear()
                self.rosterGrp_list_8.clear()
                self.rosterStandby_list_1.clear()
                self.rosterStandby_list_2.clear()

                for row_number, row_data in enumerate(result):
                    role = row_data[0]
                    player = row_data[1]
                    stat = row_data[2]
                    item = QListWidgetItem(player)
                    self.addToList(role, item, stat)
            return
        except Exception as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            errMsg = "Error: "+str(error)
            msg.setText("Something went wrong")
            self.pyClassLog.error(errMsg)
            msg.setInformativeText(errMsg)
            msg.setWindowTitle("Oops!")
            msg.setWindowIcon(QIcon(
                                resource_path("icons/raidbuilder_icon.ico")))
            msg.exec_()

    def setItemToolTip(self, signee, role):
        p_name = signee.text()
        toon = ""
        toonsQuery = Query()
        toons = toonsQuery.getToon(p_name)
        if toons is not None:
            toonsJson = json.loads(toons[0])
            toonList = []
            if bool(toonsJson):
                for x in toonsJson:
                    if toonsJson[x] == role:
                        toonList.append(x)
            if bool(toonList):
                toon = " or ".join(toonList)
        if toon != "":
            signee.setToolTip(str(toon))
        return signee

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

    def colorMe(self, role, signee):
        signee = self.setItemToolTip(signee, role)
        if role == "Tank":
            signee.setBackground(QtGui.QColor('#C79C6E'))
            signee.setIcon(QtGui.QIcon(resource_path('icons/tank.png')))
            signee.setData(QtCore.Qt.UserRole, "Tank")
        elif role == "BearTank":
            signee.setBackground(QtGui.QColor('#FF7D0A'))
            signee.setIcon(QtGui.QIcon(resource_path('icons/bear.png')))
            signee.setData(QtCore.Qt.UserRole, "BearTank")
        elif role == "Hunter":
            signee.setBackground(QtGui.QColor('#abd473'))
            signee.setIcon(QtGui.QIcon(resource_path('icons/hunter.png')))
            signee.setData(QtCore.Qt.UserRole, "Hunter")
        elif role == "RestoDruid":
            signee.setBackground(QtGui.QColor('#ffa14e'))
            signee.setIcon(QtGui.QIcon(resource_path('icons/restoDruid.png')))
            signee.setData(QtCore.Qt.UserRole, "RestoDruid")
        elif role == "Warrior":
            signee.setBackground(QtGui.QColor('#e9c49d'))
            signee.setIcon(QtGui.QIcon(resource_path('icons/warrior.png')))
            signee.setData(QtCore.Qt.UserRole, "Warrior")
        elif role == "Mage":
            signee.setBackground(QtGui.QColor('#40c7eb'))
            signee.setIcon(QtGui.QIcon(resource_path('icons/mage.png')))
            signee.setData(QtCore.Qt.UserRole, "Mage")
        elif role == "RestoShaman":
            signee.setBackground(QtGui.QColor('#0070de'))
            signee.setIcon(QtGui.QIcon(resource_path('icons/restoSham.png')))
            signee.setData(QtCore.Qt.UserRole, "RestoShaman")
        elif role == "EnhShaman":
            signee.setBackground(QtGui.QColor('#338de5'))
            signee.setIcon(QtGui.QIcon(resource_path('icons/enhSham.png')))
            signee.setData(QtCore.Qt.UserRole, "EnhShaman")
        elif role == "ElemShaman":
            signee.setBackground(QtGui.QColor('#66a9eb'))
            signee.setIcon(QtGui.QIcon(resource_path('icons/eleSham.png')))
            signee.setData(QtCore.Qt.UserRole, "ElemShaman")
        elif role == "Rogue":
            signee.setBackground(QtGui.QColor('#fff569'))
            signee.setIcon(QtGui.QIcon(resource_path('icons/rogue.png')))
            signee.setData(QtCore.Qt.UserRole, "Rogue")
        elif role == "Warlock":
            signee.setBackground(QtGui.QColor('#8787ed'))
            signee.setIcon(QtGui.QIcon(resource_path('icons/warlock.png')))
            signee.setData(QtCore.Qt.UserRole, "Warlock")
        elif role == "ShadowPriest":
            signee.setBackground(QtGui.QColor('#c8ccdf'))
            signee.setIcon(QtGui.QIcon(resource_path('icons/shadow.png')))
            signee.setData(QtCore.Qt.UserRole, "ShadowPriest")
        elif role == "Priest":
            signee.setBackground(QtGui.QColor('#eaeaea'))
            signee.setIcon(QtGui.QIcon(resource_path('icons/priest.png')))
            signee.setData(QtCore.Qt.UserRole, "Priest")
        elif role == "FeralDruid":
            signee.setBackground(QtGui.QColor('#ffb471'))
            signee.setIcon(QtGui.QIcon(resource_path('icons/feral.png')))
            signee.setData(QtCore.Qt.UserRole, "FeralDruid")
        elif role == "BalanceDruid":
            signee.setBackground(QtGui.QColor('#ffb471'))
            signee.setIcon(QtGui.QIcon(resource_path('icons/balance.png')))
            signee.setData(QtCore.Qt.UserRole, "BalanceDruid")
        elif role == "HolyPaladin":
            signee.setBackground(QtGui.QColor('#e99bbd'))
            signee.setIcon(QtGui.QIcon(resource_path('icons/holy.png')))
            signee.setData(QtCore.Qt.UserRole, "HolyPaladin")
        elif role == "RetribPaladin":
            signee.setBackground(QtGui.QColor('#eeb4ce'))
            signee.setIcon(QtGui.QIcon(resource_path('icons/retrib.png')))
            signee.setData(QtCore.Qt.UserRole, "RetribPaladin")
        elif role == "ProtPaladin":
            signee.setBackground(QtGui.QColor('#E382AD'))
            signee.setIcon(QtGui.QIcon(resource_path('icons/prot.png')))
            signee.setData(QtCore.Qt.UserRole, "ProtPaladin")
        else:
            signee.setForeground(QtGui.QColor('#9199BE'))
        return signee

    def addToList(self, role, listItem, stat):
        signee = self.colorMe(role, listItem)
        if stat in ("Absent", "Late", "Tentative", "Bench"):
            self.addAbLaTeBen(role, signee, stat)
        elif role == "Tank":
            self.signup_list_tanks.addItem(signee)
        elif role == "BearTank":
            self.signup_list_tanks.addItem(signee)
        elif role == "Hunter":
            self.signup_list_hunters.addItem(signee)
        elif role == "RestoDruid":
            self.signup_list_druids.addItem(signee)
        elif role == "Warrior":
            self.signup_list_warriors.addItem(signee)
        elif role == "Mage":
            self.signup_list_mages.addItem(signee)
        elif role == "RestoShaman":
            self.signup_list_shamans.addItem(signee)
        elif role == "EnhShaman":
            self.signup_list_shamans.addItem(signee)
        elif role == "ElemShaman":
            self.signup_list_shamans.addItem(signee)
        elif role == "Rogue":
            self.signup_list_rogues.addItem(signee)
        elif role == "Warlock":
            self.signup_list_warlocks.addItem(signee)
        elif role == "ShadowPriest":
            self.signup_list_priests.addItem(signee)
        elif role == "Priest":
            self.signup_list_priests.addItem(signee)
        elif role == "FeralDruid":
            self.signup_list_druids.addItem(signee)
        elif role == "BalanceDruid":
            self.signup_list_druids.addItem(signee)
        elif role == "HolyPaladin":
            self.signup_list_other.addItem(signee)
        elif role == "RetribPaladin":
            self.signup_list_other.addItem(signee)
        elif role == "ProtPaladin":
            self.signup_list_tanks.addItem(signee)
        else:
            self.signup_list_other.addItem(signee)
        return
