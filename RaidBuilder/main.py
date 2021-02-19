from PyQt5.QtWidgets import QApplication
from RaidBuilder import RBWindow
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = RBWindow()
    window.show()
    sys.exit(app.exec_())
