# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\MB2705851\OneDrive - Surbana Jurong Private Limited\1_Coding\GitHub\brandtosaurus\traffic_manual_count_ETL\manualcount.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(532, 544)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(420, 510, 101, 31))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        self.typeComboBox = QtWidgets.QComboBox(Dialog)
        self.typeComboBox.setGeometry(QtCore.QRect(20, 30, 500, 22))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.typeComboBox.sizePolicy().hasHeightForWidth())
        self.typeComboBox.setSizePolicy(sizePolicy)
        self.typeComboBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.typeComboBox.setEditable(False)
        self.typeComboBox.setDuplicatesEnabled(False)
        self.typeComboBox.setFrame(False)
        self.typeComboBox.setObjectName("typeComboBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 10, 361, 21))
        self.label.setObjectName("label")
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(10, 470, 511, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName("progressBar")
        self.chooseDirectory = QtWidgets.QToolButton(Dialog)
        self.chooseDirectory.setGeometry(QtCore.QRect(470, 90, 51, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chooseDirectory.sizePolicy().hasHeightForWidth())
        self.chooseDirectory.setSizePolicy(sizePolicy)
        self.chooseDirectory.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.chooseDirectory.setObjectName("chooseDirectory")
        self.textBar = QtWidgets.QLineEdit(Dialog)
        self.textBar.setEnabled(True)
        self.textBar.setGeometry(QtCore.QRect(20, 90, 450, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.textBar.sizePolicy().hasHeightForWidth())
        self.textBar.setSizePolicy(sizePolicy)
        self.textBar.setMinimumSize(QtCore.QSize(321, 0))
        self.textBar.setAutoFillBackground(False)
        self.textBar.setDragEnabled(True)
        self.textBar.setReadOnly(True)
        self.textBar.setObjectName("textBar")
        self.tchTrustImageExample = QtWidgets.QLabel(Dialog)
        self.tchTrustImageExample.setGeometry(QtCore.QRect(30, 140, 201, 291))
        self.tchTrustImageExample.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.tchTrustImageExample.setOpenExternalLinks(True)
        self.tchTrustImageExample.setObjectName("tchTrustImageExample")
        self.simpleImportExample = QtWidgets.QLabel(Dialog)
        self.simpleImportExample.setGeometry(QtCore.QRect(280, 140, 201, 291))
        self.simpleImportExample.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.simpleImportExample.setOpenExternalLinks(True)
        self.simpleImportExample.setObjectName("simpleImportExample")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 361, 21))
        self.label_2.setObjectName("label_2")
        self.runButton = QtWidgets.QPushButton(Dialog)
        self.runButton.setGeometry(QtCore.QRect(330, 510, 93, 28))
        self.runButton.setObjectName("runButton")
        self.exportToCSV = QtWidgets.QCheckBox(Dialog)
        self.exportToCSV.setGeometry(QtCore.QRect(10, 510, 101, 20))
        self.exportToCSV.setObjectName("exportToCSV")
        self.exportToSQL = QtWidgets.QCheckBox(Dialog)
        self.exportToSQL.setGeometry(QtCore.QRect(140, 510, 171, 20))
        self.exportToSQL.setObjectName("exportToSQL")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Choose Manual Count Type"))
        self.chooseDirectory.setText(_translate("Dialog", "..."))
        self.tchTrustImageExample.setText(_translate("Dialog", "<html><head/><body><p><img src=\":/image/tcstrust_example.png\"/></p></body></html>"))
        self.simpleImportExample.setText(_translate("Dialog", "<html><head/><body><p><img src=\":/image/simpleImport_example.png\"/></p></body></html>"))
        self.label_2.setText(_translate("Dialog", "Choose a Folder (not a file)"))
        self.runButton.setText(_translate("Dialog", "Run"))
        self.exportToCSV.setText(_translate("Dialog", "Export to CSV"))
        self.exportToSQL.setText(_translate("Dialog", "Export to PostgreSQL"))
import images_rc
