from PyQt5.QtWidgets import QApplication
from RaidBuilder import RBWindow
import sys
from PyQt5.QtWidgets import QMessageBox


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)

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
        msg.setInformativeText(newMsg)
        msg.setWindowTitle("Well, fuck!")
        msg.exec_()
