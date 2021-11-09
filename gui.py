from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QMessageBox,
    QErrorMessage,
    QFileDialog,
)
from PyQt5 import uic
import sys
import os

import main
import config

TYPES = ["", "Detailed Manual Traffic Count Form", "Basic Format"]


class Ui(QDialog):
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

        self.runButton.clicked.connect(self.start)

        self.buttonBox.rejected.connect(self.exit)

        self.progressBar.setValue(0)

    def activated(self, text):
        if text == "Detailed Manual Traffic Count Form":
            self.tchTrustImageExample.setStyleSheet(
                "background-color: cyan; border: 3px solid red;"
            )
            self.simpleImportExample.setStyleSheet("background-color: rgba(0,0,0,0%)")
        elif text == "Basic Format":
            self.simpleImportExample.setStyleSheet(
                "background-color: cyan; border: 3px solid red;"
            )
            self.tchTrustImageExample.setStyleSheet("background-color: rgba(0,0,0,0%)")
        Ui.type = str(self.typeComboBox.currentText())

    def _open_file_dialog(self):
        path = str(QFileDialog.getExistingDirectory())
        self.textBar.setText("{}".format(path))
        Ui.path = self.textBar.text()

    def exit(self):
        sys.exit(app.exec_())

    def start(self):
        if (Ui.type == "") or (Ui.type == None):
            self.error_dialogue = QErrorMessage()
            self.error_dialogue.showMessage("Please select a type")
        elif (Ui.path == "") or (Ui.path == None):
            self.error_dialogue = QErrorMessage()
            self.error_dialogue.showMessage("Please select a folder")
        else:
            self.thread = External()
            self.thread.countChanged.connect(self.onCountChanged)
            self.thread.start()
            self.runButton.setEnabled(False)
            self.thread.finished.connect(self.show_popup)

    def onCountChanged(self, value):
        self.progressBar.setValue(value)

    def show_popup(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowText("Process")
        msg.setText("Processing Complete")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Open)
        msg.buttonClicked.connect(self.popup_button)

        returnValue = msg.exec()
        if returnValue == QMessageBox.Ok:
            sys.exit()
        else:
            OUTPATH = os.path.realpath(config.OUTPATH)
            os.startfile(OUTPATH)

    # def popup_button(self, i):
    #     if i.text() == "OK":
    #         sys.exit()
    #     else:
    #         sys.exit()


class External(QThread):

    countChanged = pyqtSignal(int)

    def run(self):
        p = main.Count(str(Ui.type), str(Ui.path))
        src = p.getfiles(Ui.path)
        TOTAL = len(src)
        count = 0
        while count < TOTAL:
            for file in src:
                count += 1
                p.execute(file)
                self.countChanged.emit(int(count / TOTAL * 100))
        p.export()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = Ui()
    window.show()
    sys.exit(app.exec_())
