from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap, QMouseEvent
from PyQt5 import QtWidgets, uic
import sys

TYPES = ["TCS Trust", "Basic Format"]


class Ui(QtWidgets.QDialog):
    def __init__(self):
        super(Ui, self).__init__()

        uic.loadUi("manualcount.ui", self)

        self.typeComboBox.addItems(TYPES)
        self.typeComboBox.activated[str].connect(self.activated)

        self.tchTrustImageExample.setPixmap(QPixmap(r"assets\tcstrust_example.png"))
        self.tchTrustImageExample.mousePressEvent.connect(self.activated)

        self.simpleImportExample.setPixmap(QPixmap(r"assets\simpleImport_example.png"))
        self.simpleImportExample.mousePressEvent.connect(self.activated)

        self.chooseDirectory.clicked.connect(self._open_file_dialog)

    def activated(self, text):
        if self == self.tchTrustImageExample:
            self.type = "TCS Trust"
        elif self == self.simpleImportExample:
            self.type = "Basic Format"

    def _open_file_dialog(self):
        directory = str(QtWidgets.QFileDialog.getExistingDirectory())
        self.textBar.setText("{}".format(directory))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = Ui()
    window.show()
    sys.exit(app.exec_())
