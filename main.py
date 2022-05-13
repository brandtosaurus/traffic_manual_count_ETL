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
import csv

import pandas as pd

import calcs
import config

TYPES = [
    "",
    "Manual Traffic Counting Sheet",
    "Basic Format",
]


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

        self.exportToSQL.setChecked(False)
        self.exportToCSV.setChecked(False)

        self.exportToSQL.stateChanged.connect(lambda: self.btnstate(self.exportToSQL))
        self.exportToCSV.stateChanged.connect(lambda: self.btnstate(self.exportToCSV))

        # self.exportToSQL.stateChanged.connect(self.checkBoxChangedActionSQL)
        # self.exportToCSV.stateChanged.connect(self.checkBoxChangedActionCSV)

        self.chooseDirectory.clicked.connect(self._open_file_dialog)

        self.runButton.clicked.connect(self.start)

        self.buttonBox.rejected.connect(self.exit)

        self.progressBar.setValue(0)

        self.type = ""
        self.path = ""
        self.csv_export = False
        self.sql_export = False

    # def checkBoxChangedActionSQL(self, state):
    #     if (Qt.Checked == state):
    #         self.sql_export = True
    #     else:
    #         self.sql_export = False

    # def checkBoxChangedActionCSV(self, state):
    #     if (Qt.Checked == state):
    #         self.csv_export = True
    #     else:
    #         self.csv_export = False 

    def btnstate(self, b):
        if b.text() == "Export to CSV":
            if b.isChecked() == True:
                self.csv_export = True
            else:
                self.csv_export = False

        if b.text() == "Export to PostgreSQL":
            if b.isChecked() == True:
                self.sql_export = True
            else:
                self.sql_export = False

    def activated(self, text):
        if text == "Manual Traffic Counting Sheet":
            self.tchTrustImageExample.setStyleSheet(
                "background-color: cyan; border: 3px solid red;"
            )
            self.simpleImportExample.setStyleSheet("background-color: rgba(0,0,0,0%)")
        elif text == "Basic Format":
            self.simpleImportExample.setStyleSheet(
                "background-color: cyan; border: 3px solid red;"
            )
            self.tchTrustImageExample.setStyleSheet("background-color: rgba(0,0,0,0%)")
        self.type = str(self.typeComboBox.currentText())

    def _open_file_dialog(self):
        path = str(QFileDialog.getExistingDirectory())
        self.textBar.setText("{}".format(path))
        self.path = self.textBar.text()

    def exit(self):
        sys.exit(app.exec_())

    def start(self):
        if (self.type == "") or (self.type == None):
            self.error_dialogue = QErrorMessage()
            self.error_dialogue.showMessage("Please select a type")
        elif (self.path == "") or (self.path == None):
            self.error_dialogue = QErrorMessage()
            self.error_dialogue.showMessage("Please select a folder")
        elif (self.csv_export == False) and (self.sql_export == False):
            self.error_dialogue = QErrorMessage()
            self.error_dialogue.showMessage("Please select an export type")
        else:
            self.thread = External(self.type, self.path, self.csv_export, self.sql_export)
            self.thread.countChanged.connect(self.onCountChanged)
            self.thread.start()
            self.runButton.setEnabled(False)
            self.thread.finished.connect(self.show_popup)

    def onCountChanged(self, value):
        self.progressBar.setValue(value)

    def show_popup(self):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setWindowTitle("Process")
        self.msg.setText("Processing Complete")
        self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Open)
        self.msg.buttonClicked.connect(self.popup_button)

        returnValue = self.msg.exec()
        if returnValue == QMessageBox.Ok:
            sys.exit()
        else:
            OUT = os.path.realpath(config.OUTPATH)
            os.startfile(OUT)

    def popup_button(self, i):
        if i.text() == "OK":
            sys.exit()
        elif i.text() == "Open":
            OUT = os.path.realpath(config.OUTPATH)
            os.startfile(OUT)


class External(QThread):
    
    countChanged = pyqtSignal(int)

    def __init__(self, type, path, csv_export, sql_export, parent=None):
        super(QThread, self).__init__()
        self.type = type
        self.path = path
        self.csv_export = csv_export
        self.sql_export = sql_export

    def run(self):
        if not os.path.exists(os.path.expanduser(config.OUTPATH)):
            os.makedirs(os.path.expanduser(config.OUTPATH))

        if not os.path.exists(os.path.expanduser(config.FILES_COMPLETE)):
            with open(
                os.path.expanduser(config.FILES_COMPLETE),
                "w",
            ) as f:
                pass

        fileComplete = os.path.expanduser(config.FILES_COMPLETE)
        try:
            fileComplete = pd.read_csv(fileComplete, header=None, sep="\n")
            fileComplete = fileComplete[0].tolist()
        except Exception:
            fileComplete = []

        print(str(self.type), str(self.path), self.csv_export, self.sql_export)
        p = calcs.Count(str(self.type), str(self.path), self.csv_export, self.sql_export)
        src = p.getfiles(self.path)
        TOTAL = len(src)
        print("number of files: " + str(TOTAL))
        # files = [i for i in src if i not in fileComplete]
        # print("number of files not complete: " + len(files))

        count = 0
        while count < TOTAL:
            for file in src:
                count += 1
                print("busy with: " + file)
                p.execute(file)
                self.countChanged.emit(int(count / TOTAL * 100))

        h = p.header_out_df
        d = p.data_out_df
        print(h)
        print(d)
        p.export()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = Ui()
    window.show()
    sys.exit(app.exec_())
