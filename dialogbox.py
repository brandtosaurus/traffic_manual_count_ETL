from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PyQt5 import QtWidgets, uic
import sys
import csv
import os

import main
import config

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
        Ui.type = str(self.typeComboBox.currentText())

    def _open_file_dialog(self):
        path = str(QtWidgets.QFileDialog.getExistingDirectory())
        self.textBar.setText("{}".format(path))
        Ui.path = self.textBar.text()

    def exit(self):
        sys.exit(app.exec_())

    def run(self):
        if (Ui.type == "") or (Ui.type == None):
            self.error_dialogue = QtWidgets.QErrorMessage()
            self.error_dialogue.showMessage("Please select a type")
        elif (Ui.path == "") or (Ui.path == None):
            self.error_dialogue = QtWidgets.QErrorMessage()
            self.error_dialogue.showMessage("Please select a folder")
        else:
            self.calc = External()
            self.calc.countChanged.connect(self.onCountChanged)
            self.calc.start()
            self.runButton.setEnabled(False)

    def onCountChanged(self, value):
        self.progressBar.setValue(value)

    def app_done(self):
        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText("Process")
        self.msg.setInformativeText("Processing Complete")
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.buttonClicked.connect(msgbtn)

    def msgbtn(self):
        sys.exit()


class External(QThread):

    countChanged = pyqtSignal(int)

    def run(self):
        p = main.Count(str(Ui.type), str(Ui.path))
        TOTAL = len(p.src)
        src = p.src
        print(TOTAL)
        count = 0
        while count <= TOTAL:
            # ! DUPLICATE OUTPUTS
            # TODO: Almost works, remove duplicate outputs
            try:
                for file in src:
                    count += 1
                    p.run(file)
                    self.countChanged.emit(int(count / TOTAL * 100))
            except Exception:
                with open(
                    os.path.expanduser(config.PROBLEM_FILES),
                    "a",
                    newline="",
                ) as f:
                    write = csv.writer(f)
                    write.writerows([[file]])
                pass
        header = p.header_out_df.drop_duplicates()
        data = p.data_out_df.drop_duplicates()
        header.to_csv(config.HEADEROUT, mode="a", index=False)
        data.to_csv(config.DATAOUT, mode="a", index=False)
        Ui.app_done()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = Ui()
    window.show()
    sys.exit(app.exec_())
