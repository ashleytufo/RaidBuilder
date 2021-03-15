from PyQt5.QtWidgets import (QApplication, QMessageBox)
from PyQt5.QtGui import QIcon
from RaidBuilder import RBWindow

import resources
import sys
import logging
from os import path
from datetime import datetime


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', path.dirname(path.abspath(__file__)))
    return path.join(base_path, relative_path)


if __name__ == '__main__':
    now = datetime.now()
    nowString = now.strftime("%m_%d_%Y")
    LOG_BRKT_FRMT = " "
    LOG_FORMAT = '%(asctime)s: [%(levelname)s]  '\
                 '%(name)s(%(lineno)d): %(message)s'
    LOG_FILENAME = resource_path("./logs/RaidBuilder_" + nowString + ".log")
    # with open(LOG_FILENAME, 'w') as f:
    #     f.write()
    LOG_APPEND = 'a'
    LOG_DATE_FRMT = '%m-%d %H:%M:%S'
    logging.basicConfig(filename=LOG_FILENAME, filemode=LOG_APPEND,
                        format=LOG_FORMAT, datefmt=LOG_DATE_FRMT,
                        level=logging.INFO)
    pyClassLog = logging.getLogger(__name__)

    try:
        app = QApplication(sys.argv)
        stylesheet = '''
            QMessageBox {background-color: rgb(45, 51, 49);
                border-color: rgb(255, 255, 255);}

            QMessageBox QLabel#qt_msgbox_label {color: rgb(145, 153, 190);
                background-color: rgb(45, 51, 49);
                padding: 1px; font: 12pt;}

            QMessageBox QLabel {color: rgb(145, 153, 190);
                background-color: rgb(45, 51, 49);
                padding: 1px;}

            QMessageBox QPushButton {background-color: qlineargradient(
                        spread:pad, x1:1, y1:1, x2:1, y2:0,
                        stop:0.0738636 rgba(108, 114, 142, 255),
                        stop:1 rgba(255, 255, 255, 255));
                color: pallete(light); border-style: inset;
                border-width: 2px; padding: 3px; border-radius: 8px;
                font: 10pt; min-width: 2em; min-height: 1.5em;}

            QMessageBox QPushButton:hover:pressed {
                background-color: rgb(145, 153, 190);
                border-style: inset;}

            QMessageBox QPushButton:hover {background-color: qlineargradient(
                    spread:pad, x1:1, y1:1, x2:1, y2:0,
                    stop:0 rgba(195, 206, 255, 255),
                    stop:0.676136 rgba(255, 255, 255, 255));
                border-style: inset;}
            '''
        app.setStyleSheet(stylesheet)
        window = RBWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as error:
        newMsg = "Something went wrong and I wasn't built to expect this."\
                 " You can probably just restart and try not to do the same"\
                 " exact thing as before :P\nError: "+str(error)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("You done messed up Ay-Ay-Ron!")
        pyClassLog.error(error)
        msg.setInformativeText(newMsg)
        msg.setWindowTitle("Well, fuck!")
        msg.setWindowIcon(QIcon(
                          resource_path("icons/raidbuilder_icon.ico")))
        msg.exec_()
