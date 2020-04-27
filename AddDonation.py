

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import qtmodern.windows
from db import Database

class Ui_AddDonation(object):

    def fillCompletersD(self):
        self.donors = []
        self.d_id = []
        for e in self.db.getDonor():
            self.donors.append(e[1])
            self.d_id.append(e[0])
        self.dCompleter = QtWidgets.QCompleter(self.donors)
        self.dCompleter.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.entDonor.setCompleter(self.dCompleter)

    def fillCompletersB(self):
        self.bloodbanks = []
        self.bb_id = []
        for e in self.db.getBloodbank():
            self.bloodbanks.append(e[1])
            self.bb_id.append(e[0])
        self.bbCompleter = QtWidgets.QCompleter(self.bloodbanks)
        self.bbCompleter.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.entBloodBank.setCompleter(self.bbCompleter)

    def fillCompletersP(self):
        self.patients = []
        self.p_id = []
        self.bTypes = []
        for e in self.db.getPatient():
            self.patients.append(e[1])
            self.bTypes.append(e[2])
            self.p_id.append(e[0])
        self.pCompleter = QtWidgets.QCompleter(self.patients)
        self.pCompleter.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.entRecipient.setCompleter(self.pCompleter)

    def insertDonation(self):
        message = str()
        self.sysMsg = QMessageBox()
        donor = self.entDonor.text()
        recipient = self.entRecipient.text()
        bloodbank = self.entBloodBank.text()
        blood = self.selBloodType.currentText()
        inDonors = donor in self.donors
        inBloodBank = bloodbank in self.bloodbanks
        inPatient = recipient in self.patients
        if inDonors and inBloodBank and (inPatient or recipient == ''):
            if inPatient:
                donor = self.donors.index(donor)
                bloodbank = self.bloodbanks.index(bloodbank)
                recipient = self.patients.index(recipient)
                if 'No' in [e[2] for e in self.db.getOnePatient(self.p_id[recipient])]:
                    self.db.addDonationWithRecipient(self.d_id[donor], self.bb_id[bloodbank], self.p_id[recipient], blood)
                    message = 'Donation Added Successfully!'                   
                else:
                    message = "The patient doesn't need more blood."
                self.sysMsg.setIcon(QMessageBox.Information)
                self.sysMsg.setText(message)
                self.sysMsg.setFixedSize(200, 160)
                self.sysMsg.setWindowTitle('Success')
            elif recipient == '':
                donor = self.donors.index(donor)
                bloodbank = self.bloodbanks.index(bloodbank)
                self.db.addDonationNoRecipient(self.d_id[donor], self.bb_id[bloodbank], blood)
                message = 'Donation Added Successfully!'
                self.sysMsg.setIcon(QMessageBox.Information)
                self.sysMsg.setText(message)
                self.sysMsg.setFixedSize(200, 160)
                self.sysMsg.setWindowTitle('Success')
        else:
            if donor == '':
                message += 'Please fill-up Donor field.\n'
            elif not inDonors:
                message += 'The donor you entered is not yet registered.\n'
            if bloodbank == '':
                message += 'Please fill up Blood Bank field\n'
            elif not inBloodBank:
                message += 'The bloodbank you entered is not yet registered\n'
            if not inPatient and recipient != '':
                message += 'The patient you entered is not yet registered.'
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



    def useBloodType(self):
        if self.entRecipient.text() in self.patients:
            self.selBloodType.setCurrentText(self.bTypes[self.patients.index(self.entRecipient.text())])
            self.selBloodType.setEnabled(False)
        else:
            self.selBloodType.setEnabled(True)

    def setupUi(self, AddDonation, db):
        self.db = db
        self.bloodbanks, self.donors, self.patients = [], [], []
        
        AddDonation.setObjectName("AddDonation")
        AddDonation.resize(350, 400)

        self.lblDonor = QtWidgets.QLabel(AddDonation)
        self.lblDonor.setGeometry(QtCore.QRect(30, 60, 47, 25))
        self.lblDonor.setObjectName("lblDonor")

        self.entDonor = QtWidgets.QLineEdit(AddDonation)
        self.entDonor.setGeometry(QtCore.QRect(30, 90, 200, 25))
        self.entDonor.setObjectName("entDonor")

        self.newDonor = QtWidgets.QPushButton(AddDonation)
        self.newDonor.setGeometry(QtCore.QRect(244, 90, 90, 25))
        self.newDonor.setObjectName("newDonor")

        self.lblRecipient = QtWidgets.QLabel(AddDonation)
        self.lblRecipient.setGeometry(QtCore.QRect(30, 130, 51, 25))
        self.lblRecipient.setObjectName("lblRecipient")

        self.newRecipient = QtWidgets.QPushButton(AddDonation)
        self.newRecipient.setGeometry(QtCore.QRect(244, 160, 90, 25))
        self.newRecipient.setObjectName("newRecipient")

        self.entRecipient = QtWidgets.QLineEdit(AddDonation)
        self.entRecipient.setGeometry(QtCore.QRect(30, 160, 200, 25))
        self.entRecipient.setObjectName("entRecipient")
        self.entRecipient.textChanged.connect(self.useBloodType)

        self.lblBloodBank = QtWidgets.QLabel(AddDonation)
        self.lblBloodBank.setGeometry(QtCore.QRect(30, 200, 60, 25))
        self.lblBloodBank.setObjectName("lblBloodBank")

        self.newBloodBank = QtWidgets.QPushButton(AddDonation)
        self.newBloodBank.setGeometry(QtCore.QRect(244, 230, 90, 25))
        self.newBloodBank.setObjectName("newBloodBank")

        self.entBloodBank = QtWidgets.QLineEdit(AddDonation)
        self.entBloodBank.setGeometry(QtCore.QRect(30, 230, 200, 25))
        self.entBloodBank.setObjectName("entBloodBank")

        self.lblBloodType = QtWidgets.QLabel(AddDonation)
        self.lblBloodType.setGeometry(QtCore.QRect(100, 280, 70, 25))
        self.lblBloodType.setObjectName("lblBloodType")

        self.selBloodType = QtWidgets.QComboBox(AddDonation)
        self.selBloodType.setGeometry(QtCore.QRect(170, 280, 50, 25))
        self.selBloodType.setObjectName("selBloodType")
        self.selBloodType.addItem("")
        self.selBloodType.addItem("")
        self.selBloodType.addItem("")
        self.selBloodType.addItem("")

        self.btnConfirm = QtWidgets.QPushButton(AddDonation)
        self.btnConfirm.setGeometry(QtCore.QRect(180, 340, 75, 25))
        self.btnConfirm.setObjectName("btnConfirm")
        self.btnConfirm.clicked.connect(self.insertDonation)
        self.btnConfirm.clicked.connect(AddDonation.accept)

        self.btnCancel = QtWidgets.QPushButton(AddDonation)
        self.btnCancel.setGeometry(QtCore.QRect(260, 340, 75, 25))
        self.btnCancel.setObjectName("btnCancel")
        self.btnCancel.clicked.connect(AddDonation.reject)

        self.lblTitle = QtWidgets.QLabel(AddDonation)
        self.lblTitle.setGeometry(QtCore.QRect(110, 20, 131, 41))

        font = QtGui.QFont()
        font.setPointSize(13)
        
        self.lblTitle.setFont(font)
        self.lblTitle.setObjectName("lblTitle")

        self.retranslateUi(AddDonation)
        QtCore.QMetaObject.connectSlotsByName(AddDonation)

        self.fillCompletersD()
        self.fillCompletersB()
        self.fillCompletersP()

    def retranslateUi(self, AddDonation):
        _translate = QtCore.QCoreApplication.translate
        AddDonation.setWindowTitle(_translate("AddDonation", "New Donation"))
        self.lblDonor.setText(_translate("AddDonation", "Donor:"))
        self.newDonor.setText(_translate("AddDonation", "New Donor"))
        self.lblRecipient.setText(_translate("AddDonation", "Recipient:"))
        self.newRecipient.setText(_translate("AddDonation", "New Recipient"))
        self.lblBloodBank.setText(_translate("AddDonation", "Blood Bank:"))
        self.newBloodBank.setText(_translate("AddDonation", "New Blood Bank"))
        self.lblBloodType.setText(_translate("AddDonation", "Blood Type:"))
        self.selBloodType.setItemText(0, _translate("AddDonation", "A"))
        self.selBloodType.setItemText(1, _translate("AddDonation", "B"))
        self.selBloodType.setItemText(2, _translate("AddDonation", "AB"))
        self.selBloodType.setItemText(3, _translate("AddDonation", "O"))
        self.btnConfirm.setText(_translate("AddDonation", "Confirm"))
        self.btnCancel.setText(_translate("AddDonation", "Cancel"))
        self.lblTitle.setText(_translate("AddDonation", "NEW DONATION"))
