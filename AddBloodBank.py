

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import qtmodern.windows


class Ui_AddBloodBank(object):
    def insertBloodBank(self):
        message = str()
        self.sysMsg = QMessageBox()
        name = " ".join([e.capitalize() for e in self.entName.text().split()])
        addr = " ".join([e.capitalize() for e in self.entAddress.text().split()])
        contact = self.entContact.text()
        if name != '' and not name.isdigit() and addr != '' and contact.isdigit() and len(contact) is 10:
            message = 'Blood Bank Added Successfully'
            self.db.addBloodBank(name, contact, addr)
            self.sysMsg.setIcon(QMessageBox.Information)
            self.sysMsg.setText(message)
            self.sysMsg.setFixedSize(200, 160)
            self.sysMsg.setWindowTitle('Success')
        else:
            if name == '':
                message += 'Please fill the name properly using alphabet.\n'
            if not contact.isdigit() or len(contact) != 10:
                message += 'Please fill contact number with 10 digits.\n'
            if addr == '':
                message += 'Please enter proper address.'
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

        if self.parent is not None and name in [e[1] for e in self.db.getBloodBank()]:
            name = " ".join([e.capitalize() for e in self.entName.text().split()])
            self.parent.entBloodBank.setText(name)
            self.parent.fillCompletersB()

    def getName(self):
        return " ".join([e.capitalize() for e in self.entName.text().split()])
       

    def setupUi(self, AddBloodBank, db, parent = None):
        self.db = db
        self.parent = parent

        AddBloodBank.setObjectName("AddBloodBank")
        AddBloodBank.resize(290, 280)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AddBloodBank.sizePolicy().hasHeightForWidth())

        AddBloodBank.setSizePolicy(sizePolicy)
        AddBloodBank.setMinimumSize(QtCore.QSize(290, 280))
        AddBloodBank.setMaximumSize(QtCore.QSize(290, 360))

        self.lblName = QtWidgets.QLabel(AddBloodBank)
        self.lblName.setGeometry(QtCore.QRect(35, 70, 41, 25))
        self.lblName.setObjectName("lblName")

        self.entName = QtWidgets.QLineEdit(AddBloodBank)
        self.entName.setGeometry(QtCore.QRect(40, 90, 215, 25))
        self.entName.setObjectName("entName")

        self.lblAddress = QtWidgets.QLabel(AddBloodBank)
        self.lblAddress.setGeometry(QtCore.QRect(35, 120, 71, 25))
        self.lblAddress.setObjectName("lblAddress")

        self.entAddress = QtWidgets.QLineEdit(AddBloodBank)
        self.entAddress.setGeometry(QtCore.QRect(40, 140, 215, 25))
        self.entAddress.setObjectName("entAddress")

        self.lblContact = QtWidgets.QLabel(AddBloodBank)
        self.lblContact.setGeometry(QtCore.QRect(40, 170, 91, 25))
        self.lblContact.setObjectName("lblContact")

        self.entContact = QtWidgets.QLineEdit(AddBloodBank)
        self.entContact.setGeometry(QtCore.QRect(100, 190, 120, 25))
        self.entContact.setObjectName("entContact")

        self.lblPrefix = QtWidgets.QLabel(AddBloodBank)
        self.lblPrefix.setGeometry(QtCore.QRect(70, 190, 31, 25))
        self.lblPrefix.setObjectName("lblPrefix")

        self.addConfirm = QtWidgets.QPushButton(AddBloodBank)
        self.addConfirm.setGeometry(QtCore.QRect(120, 240, 75, 25))
        self.addConfirm.setObjectName("addConfirm")
        self.addConfirm.clicked.connect(self.insertBloodBank)
        self.addConfirm.clicked.connect(AddBloodBank.accept)

        self.addCancel = QtWidgets.QPushButton(AddBloodBank)
        self.addCancel.setGeometry(QtCore.QRect(200, 240, 75, 25))
        self.addCancel.setObjectName("addCancel")
        self.addCancel.clicked.connect(AddBloodBank.reject)

        self.lblTitle = QtWidgets.QLabel(AddBloodBank)
        self.lblTitle.setGeometry(QtCore.QRect(70, 20, 180, 25))

        font = QtGui.QFont()
        font.setPointSize(11)
        
        self.lblTitle.setFont(font)
        self.lblTitle.setObjectName("lblTitle")

        self.retranslateUi(AddBloodBank)
        QtCore.QMetaObject.connectSlotsByName(AddBloodBank)

    def retranslateUi(self, AddBloodBank):
        _translate = QtCore.QCoreApplication.translate
        AddBloodBank.setWindowTitle(_translate("AddBloodBank", "New Blood Bank"))
        self.lblName.setText(_translate("AddBloodBank", "Name:"))
        self.lblAddress.setText(_translate("AddBloodBank", "Address:"))
        self.lblContact.setText(_translate("AddBloodBank", "Contact Number:"))
        self.lblPrefix.setText(_translate("AddBloodBank", " +63"))
        self.addConfirm.setText(_translate("AddBloodBank", "Confirm"))
        self.addCancel.setText(_translate("AddBloodBank", "Cancel"))
        self.lblTitle.setText(_translate("AddBloodBank", "ADD NEW BLOOD BANK"))
