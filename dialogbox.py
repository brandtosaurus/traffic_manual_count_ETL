from PyQt5 import QtCore, QtGui, QtWidgets , uic
import sys

class Ui(QtWidgets.QDialog):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('manualcount.ui', self)

        self.count_type =  

        TYPES =  ['TCS Trust', 'Cumulative Count']
        self.dropdown = self.findChild(QtWidgets.QComboBox, 'comboBox')
        self.dropdown.addItems(TYPES)
        self.dropdown.activated[str].connect(self.onActivated)

        self.show()

    def onActivated(self, text):
        self.count_type.setText(text)

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()