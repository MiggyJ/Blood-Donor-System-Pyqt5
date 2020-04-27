

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import qtmodern.windows

class Ui_AddPatient(object):
    def insertPatient(self):
        self.sysMsg = QMessageBox()
        name = " ".join([e.capitalize() for e in self.entFname.text().split()]) + " " + " ".join([e.capitalize() for e in self.entLname.text().split()])
        bloodtype = self.selBloodType.currentText()
        contact = self.entContact.text()
        diagnosis = " ".join([e.capitalize() for e in self.entDiagnosis.text().split()])
        if not name.isdigit() and name != '' and contact.isdigit() and  not diagnosis.isdigit() and diagnosis != '' and len(contact) is 10:
            if name not in [e[1] for e in self.db.getPatient()]:
                self.db.addPatient(name, bloodtype, contact)
                self.db.addPatientDisease(diagnosis)
            else: 
                self.db.addPatientDisease(diagnosis, [e[1] for e in self.db.getPatient()].index(name) + 1)
            message = 'Patient Added Successfully!'
            self.sysMsg.setIcon(QMessageBox.Information)
            self.sysMsg.setText(message)
            self.sysMsg.setFixedSize(200, 160)
            self.sysMsg.setWindowTitle('Success')
        else:
            message = str()
            if self.entLname.text() == '' or self.entFname.text() == '':
                message += 'Please fill the name properly.\n'
            if not self.entContact.text().isdigit() or len(contact) != 10:
                message += 'Please fill contact number with 10 digits.\n'
            if self.entDiagnosis.text() == '':
                message += 'Please enter diagnosis.'
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

        if self.parent is not None and name in [e[1] for e in self.db.getPatient()]:
            self.parent.entRecipient.setText(name)
            self.parent.selBloodType.setCurrentText(bloodtype)
            self.parent.selBloodType.setEnabled(False)
            self.parent.fillCompletersP()

    def setupUi(self, AddPatient, db, parent = None):
        self.db = db
        self.parent = parent

        AddPatient.setObjectName("AddPatient")
        AddPatient.resize(290, 330)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AddPatient.sizePolicy().hasHeightForWidth())

        AddPatient.setSizePolicy(sizePolicy)
        AddPatient.setMinimumSize(QtCore.QSize(290, 360))
        AddPatient.setMaximumSize(QtCore.QSize(290, 360))

        self.lblFname = QtWidgets.QLabel(AddPatient)
        self.lblFname.setGeometry(QtCore.QRect(50, 80, 71, 25))
        self.lblFname.setObjectName("lblFname")

        self.entFname = QtWidgets.QLineEdit(AddPatient)
        self.entFname.setGeometry(QtCore.QRect(120, 80, 121, 25))
        self.entFname.setObjectName("entFname")

        self.lblLname = QtWidgets.QLabel(AddPatient)
        self.lblLname.setGeometry(QtCore.QRect(50, 120, 71, 25))
        self.lblLname.setObjectName("lblLname")

        self.entLname = QtWidgets.QLineEdit(AddPatient)
        self.entLname.setGeometry(QtCore.QRect(120, 120, 121, 25))
        self.entLname.setObjectName("entLname")

        self.lblBloodType = QtWidgets.QLabel(AddPatient)
        self.lblBloodType.setGeometry(QtCore.QRect(50, 160, 71, 25))
        self.lblBloodType.setObjectName("lblBloodType")

        self.selBloodType = QtWidgets.QComboBox(AddPatient)
        self.selBloodType.setGeometry(QtCore.QRect(120, 160, 50, 25))
        self.selBloodType.setObjectName("selBloodType")
        self.selBloodType.addItem("")
        self.selBloodType.addItem("")
        self.selBloodType.addItem("")
        self.selBloodType.addItem("")

        self.lblContact = QtWidgets.QLabel(AddPatient)
        self.lblContact.setGeometry(QtCore.QRect(50, 200, 91, 25))
        self.lblContact.setObjectName("lblContact")

        self.entContact = QtWidgets.QLineEdit(AddPatient)
        self.entContact.setGeometry(QtCore.QRect(120, 220, 121, 25))
        self.entContact.setObjectName("entContact")

        self.lblPrefix = QtWidgets.QLabel(AddPatient)
        self.lblPrefix.setGeometry(QtCore.QRect(90, 220, 30, 25))
        self.lblPrefix.setObjectName("lblPrefix")

        self.lblDiagnosis = QtWidgets.QLabel(AddPatient)
        self.lblDiagnosis.setGeometry(QtCore.QRect(50, 260, 71, 25))
        self.lblDiagnosis.setObjectName("lblDiagnosis")

        self.entDiagnosis = QtWidgets.QLineEdit(AddPatient)
        self.entDiagnosis.setGeometry(QtCore.QRect(120, 260, 121, 25))
        self.entDiagnosis.setObjectName("entDiagnosis")

        self.addConfirm = QtWidgets.QPushButton(AddPatient)
        self.addConfirm.setGeometry(QtCore.QRect(120, 320, 75, 25))
        self.addConfirm.setObjectName("addConfirm")
        self.addConfirm.clicked.connect(self.insertPatient)
        self.addConfirm.clicked.connect(AddPatient.accept)

        self.addCancel = QtWidgets.QPushButton(AddPatient)
        self.addCancel.setGeometry(QtCore.QRect(200, 320, 75, 25))
        self.addCancel.setObjectName("addCancel")
        self.addCancel.clicked.connect(AddPatient.reject)

        self.lblTitle = QtWidgets.QLabel(AddPatient)
        self.lblTitle.setGeometry(QtCore.QRect(80, 20, 140, 31))

        font = QtGui.QFont()
        font.setPointSize(11)
        
        self.lblTitle.setFont(font)
        self.lblTitle.setObjectName("lblTitle")

        self.retranslateUi(AddPatient)
        QtCore.QMetaObject.connectSlotsByName(AddPatient)

    def retranslateUi(self, AddPatient):
        _translate = QtCore.QCoreApplication.translate
        AddPatient.setWindowTitle(_translate("AddPatient", "New Patient"))
        self.lblFname.setText(_translate("AddPatient", "First Name: "))
        self.lblLname.setText(_translate("AddPatient", "Last Name: "))
        self.lblBloodType.setText(_translate("AddPatient", "Blood Type:"))
        self.selBloodType.setItemText(0, _translate("AddPatient", "A"))
        self.selBloodType.setItemText(1, _translate("AddPatient", "B"))
        self.selBloodType.setItemText(2, _translate("AddPatient", "AB"))
        self.selBloodType.setItemText(3, _translate("AddPatient", "O"))
        self.lblContact.setText(_translate("AddPatient", "Contact Number:"))
        self.lblPrefix.setText(_translate("AddPatient", " +63"))
        self.lblDiagnosis.setText(_translate("AddPatient", "Diagnosis"))
        self.addConfirm.setText(_translate("AddPatient", "Confirm"))
        self.addCancel.setText(_translate("AddPatient", "Cancel"))
        self.lblTitle.setText(_translate("AddPatient", "ADD NEW PATIENT"))
