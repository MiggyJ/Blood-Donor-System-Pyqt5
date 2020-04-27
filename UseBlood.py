# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UseBloodBds.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import qtmodern.windows

class Ui_UseBlood(object):
    def checkNew(self):
        name = " ".join([e.capitalize() for e in self.entFname.text().split()]) + " " + " ".join([e.capitalize() for e in self.entLname.text().split()])
        for e in self.patient:
            if name in e:
                self.targetPatient = e
                self.selBloodType.setCurrentText(e[2])
                self.entContact.setText(e[3].split('+63')[1])
                record = self.db.getOnePatient(e[0])
                for f in record:
                    if f[2] == 'No':
                        self.entDiagnosis.setText(f[0])
                        self.selBloodType.setEnabled(False)
                        self.entContact.setEnabled(False)
                        self.entDiagnosis.setEnabled(False)  
                        break;

    def updateDonate(self):
        self.sysMsg = QMessageBox()
        if (self.data[3] != self.selBloodType.currentText()):
            message = 'Incompatible Blood Type'   
            self.sysMsg.setIcon(QMessageBox.Critical)
            self.sysMsg.setText(message)
            self.sysMsg.setFixedSize(200, 160)
            self.sysMsg.setWindowTitle('ERROR')
        else:
            if 'No' in [e[2] for e in self.db.getOnePatient(self.targetPatient[0])]:
                self.db.updateDonation(self.targetPatient[0], self.data[0], self.entDiagnosis.text())
                message = 'Updated Successfully!'
                self.sysMsg.setIcon(QMessageBox.Information)
                self.sysMsg.setText(message)
                self.sysMsg.setFixedSize(200, 160)
                self.sysMsg.setWindowTitle('Success')
            else:
                message = "The patient doesn't need more blood."
                self.sysMsg.setIcon(QMessageBox.Critical)
                self.sysMsg.setText(message)
                self.sysMsg.setFixedSize(200, 160)
                self.sysMsg.setWindowTitle('ERROR')
        self.modernErr = qtmodern.windows.ModernWindow(self.sysMsg)
        self.modernErr.setWindowModality(QtCore.Qt.ApplicationModal)
        qr = self.modernErr.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.modernErr.move(qr.topLeft())
        self.modernErr.show()
        self.sysMsg.exec_()

    def setupUi(self, UseBlood, db, data):
        self.db = db
        self.data = data

        UseBlood.setObjectName("UseBlood")
        UseBlood.resize(290, 360)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(UseBlood.sizePolicy().hasHeightForWidth())

        UseBlood.setSizePolicy(sizePolicy)
        UseBlood.setMinimumSize(QtCore.QSize(290, 360))
        UseBlood.setMaximumSize(QtCore.QSize(290, 360))
        
        self.lblFname = QtWidgets.QLabel(UseBlood)
        self.lblFname.setGeometry(QtCore.QRect(50, 90, 71, 25))
        self.lblFname.setObjectName("lblFname")

        self.entFname = QtWidgets.QLineEdit(UseBlood)
        self.entFname.setGeometry(QtCore.QRect(120, 90, 121, 25))
        self.entFname.setObjectName("entFname")
        self.entFname.textChanged.connect(self.checkNew)

        self.lblLname = QtWidgets.QLabel(UseBlood)
        self.lblLname.setGeometry(QtCore.QRect(50, 130, 71, 25))
        self.lblLname.setObjectName("lblLname")

        self.entLname = QtWidgets.QLineEdit(UseBlood)
        self.entLname.setGeometry(QtCore.QRect(120, 130, 121, 25))
        self.entLname.setObjectName("entLname")
        self.entLname.textChanged.connect(self.checkNew)

        self.lblBloodType = QtWidgets.QLabel(UseBlood)
        self.lblBloodType.setGeometry(QtCore.QRect(50, 170, 71, 25))
        self.lblBloodType.setObjectName("lblBloodType")

        self.selBloodType = QtWidgets.QComboBox(UseBlood)
        self.selBloodType.setGeometry(QtCore.QRect(120, 170, 51, 22))
        self.selBloodType.setObjectName("selBloodType")
        self.selBloodType.setEnabled(False)
        self.selBloodType.addItem("")
        self.selBloodType.addItem("")
        self.selBloodType.addItem("")
        self.selBloodType.addItem("")

        self.lblContact = QtWidgets.QLabel(UseBlood)
        self.lblContact.setGeometry(QtCore.QRect(50, 210, 91, 25))
        self.lblContact.setObjectName("lblContact")

        self.entContact = QtWidgets.QLineEdit(UseBlood)
        self.entContact.setGeometry(QtCore.QRect(100, 230, 121, 25))
        self.entContact.setObjectName("entContact")
        self.entContact.setEnabled(False)

        self.lblDiagnosis = QtWidgets.QLabel(UseBlood)
        self.lblDiagnosis.setGeometry(QtCore.QRect(50, 270, 71, 25))
        self.lblDiagnosis.setObjectName("lblDiagnosis")
        
        self.entDiagnosis = QtWidgets.QLineEdit(UseBlood)
        self.entDiagnosis.setGeometry(QtCore.QRect(120, 270, 121, 25))
        self.entDiagnosis.setObjectName("entDiagnosis")
        self.entDiagnosis.setEnabled(False)

        self.lblPrefix = QtWidgets.QLabel(UseBlood)
        self.lblPrefix.setGeometry(QtCore.QRect(70, 230, 31, 25))
        self.lblPrefix.setObjectName("lblPrefix")

        self.addConfirm = QtWidgets.QPushButton(UseBlood)
        self.addConfirm.setGeometry(QtCore.QRect(120, 320, 75, 25))
        self.addConfirm.setObjectName("addConfirm")
        self.addConfirm.clicked.connect(self.updateDonate)
        self.addConfirm.clicked.connect(UseBlood.accept)

        self.addCancel = QtWidgets.QPushButton(UseBlood)
        self.addCancel.setGeometry(QtCore.QRect(200, 320, 75, 25))
        self.addCancel.setObjectName("addCancel")
        self.addCancel.clicked.connect(UseBlood.reject)

        self.lblTitle = QtWidgets.QLabel(UseBlood)
        self.lblTitle.setGeometry(QtCore.QRect(100, 20, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lblTitle.setFont(font)
        self.lblTitle.setObjectName("lblTitle")

        self.lblTitle_2 = QtWidgets.QLabel(UseBlood)
        self.lblTitle_2.setGeometry(QtCore.QRect(80, 50, 129, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lblTitle_2.setFont(font)
        self.lblTitle_2.setObjectName("lblTitle_2")

        self.retranslateUi(UseBlood)
        QtCore.QMetaObject.connectSlotsByName(UseBlood)

        self.patient = self.db.getPatient()

    def retranslateUi(self, UseBlood):
        _translate = QtCore.QCoreApplication.translate
        UseBlood.setWindowTitle(_translate("UseBlood", "Use Donated Blood"))
        self.lblFname.setText(_translate("UseBlood", "First Name: "))
        self.lblLname.setText(_translate("UseBlood", "Last Name: "))
        self.lblBloodType.setText(_translate("UseBlood", "Blood Type:"))
        self.selBloodType.setItemText(0, _translate("UseBlood", "A"))
        self.selBloodType.setItemText(1, _translate("UseBlood", "B"))
        self.selBloodType.setItemText(2, _translate("UseBlood", "AB"))
        self.selBloodType.setItemText(3, _translate("UseBlood", "O"))
        self.lblContact.setText(_translate("UseBlood", "Contact Number:"))
        self.lblPrefix.setText(_translate("UseBlood", " +63"))
        self.addConfirm.setText(_translate("UseBlood", "Confirm"))
        self.addCancel.setText(_translate("UseBlood", "Cancel"))
        self.lblTitle.setText(_translate("UseBlood", "USE BLOOD"))
        self.lblDiagnosis.setText(_translate("UseBlood", "Diagnosis:"))
        self.lblTitle_2.setText(_translate("UseBlood", "Registered Patient Only"))
