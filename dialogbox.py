from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap, QMouseEvent
from PyQt5 import QtWidgets, uic
import sys

TYPES = ["", "TCS Trust", "Basic Format"]


class Ui(QtWidgets.QDialog):
    def __init__(self):
        super(Ui, self).__init__()

        uic.loadUi("manualcount.ui", self)

        self.typeComboBox.addItems(TYPES)
        self.typeComboBox.activated[str].connect(self.activated)

        self.tchTrustImageExample.setOpenExternalLinks(True)
        self.tchTrustImageExample.setPixmap(QPixmap(r"assets\tcstrust_example.png"))
        self.tchTrustImageExample.linkActivated.connect(self.activated)

        self.simpleImportExample.setOpenExternalLinks(True)
        self.simpleImportExample.setPixmap(QPixmap(r"assets\simpleImport_example.png"))
        self.simpleImportExample.linkActivated.connect(self.activated)

        self.chooseDirectory.clicked.connect(self._open_file_dialog)

        self.runButton.clicked.connect(self.run)

        self.buttonBox.rejected.connect(self.exit)

        self.progressBar.setValue(0)

    def activated(self, text):
        if text == "TCS Trust":
            self.tchTrustImageExample.setStyleSheet(
                "background-color: cyan; border: 3px solid red;"
            )
            self.simpleImportExample.setStyleSheet("background-color: rgba(0,0,0,0%)")
        elif text == "Basic Format":
            self.simpleImportExample.setStyleSheet(
                "background-color: cyan; border: 3px solid red;"
            )
            self.tchTrustImageExample.setStyleSheet("background-color: rgba(0,0,0,0%)")

    def _open_file_dialog(self):
        path = str(QtWidgets.QFileDialog.getExistingDirectory())
        self.textBar.setText("{}".format(path))

    def run(self):
        type = str(self.typeComboBox.currentText())
        path = self.textBar.text()
        if (type == "") or (type == None):
            self.error_dialogue = QtWidgets.QErrorMessage()
            self.error_dialogue.showMessage("Please select a type")
        elif (path == "") or (path == None):
            self.error_dialogue = QtWidgets.QErrorMessage()
            self.error_dialogue.showMessage("Please select a folder")
        else:
            print("RUN")

    def exit(self):
        sys.exit(app.exec_())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = Ui()
    window.show()
    sys.exit(app.exec_())
