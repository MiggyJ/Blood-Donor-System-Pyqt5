

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import qtmodern.windows
import datetime

class Ui_AddDonor(object):

    def newDonor(self):
        self.sysMsg = QMessageBox()
        name = " ".join([e.capitalize() for e in self.entFname.text().split()]) + " " + " ".join([e.capitalize() for e in self.entLname.text().split()])
        address = " ".join([e.capitalize() for e in self.entAddress.text().split()])
        contact = self.entContact.text()
        birth = self.selYear.currentText() + '-' + (str(self.selMonth.currentIndex()) if self.selMonth.currentIndex() > 9 else str("0" + str(self.selMonth.currentIndex()))) + '-' + str(self.selDay.currentText())

        if not name.isdigit() and name != '' and contact.isdigit() and not "Year" in birth and not "Mon" in birth and not "Day" in birth and len(contact) is 10 and address != '' and not address.isnumeric():
            self.db.addDonor(name, address, contact, birth)
            message = 'Donor Added Successfully!'
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
            if "Year" in birth or "Mon" in birth or "Day" in birth:
                message += 'Please put Year, Month and Day of Birthdate.\n'
            if address == '':
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
        
        if name in [e[1] for e in self.db.getDonor()]:
            self.parent.entDonor.setText(name)
            self.parent.fillCompletersD()


    def unlockMonth(self):
        if self.selYear.currentIndex() != 0:
            self.selMonth.setEnabled(True)
            if self.selDay.isEnabled() == True:
                self.unlockDay()
        else:
            self.selMonnth.setEnabled(False)
            self.selDay.setEnabled(False)

    def unlockDay(self):
        if self.selMonth.currentIndex() != 0:
            self.selDay.setEnabled(True)
            if self.selMonth.currentText() in ['Jan', 'Mar', 'May', 'Jul', 'Aug', 'Oct', 'Dec']:
                while self.selDay.count() < 32:
                    self.selDay.addItem("")
                for i in range(1, 32):
                    self.selDay.setItemText(i, str(i))
            if self.selMonth.currentText() in ['Apr', 'Jun', 'Sep', 'Nov']:
                while self.selDay.count() > 31:
                    self.selDay.removeItem(self.selDay.count()-1)
                while self.selDay.count() < 31:
                    self.selDay.addItem("")
                for i in range(1, 31):
                    self.selDay.setItemText(i, str(i))
            if self.selMonth.currentText() == 'Feb':
                if int(self.selYear.currentText()) % 4 == 0:
                    while self.selDay.count() > 30:
                        self.selDay.removeItem(self.selDay.count() - 1)
                    while self.selDay.count() < 30:
                        self.selDay.addItem("")
                    for i in range(1, 30):
                        self.selDay.setItemText(i, str(i))
                elif int(self.selYear.currentText()) % 4 != 0:
                    while self.selDay.count() > 29:
                        self.selDay.removeItem(self.selDay.count()-1)
                    for i in range(1, 30):
                        self.selDay.setItemText(i, str(i))
        else:
            self.selDay.setEnabled(False)

    def setupUi(self, AddDonor, db, parent):
        self.db = db
        self.parent = parent

        AddDonor.setObjectName("AddDonor")
        AddDonor.resize(290, 320)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AddDonor.sizePolicy().hasHeightForWidth())

        AddDonor.setSizePolicy(sizePolicy)
        AddDonor.setMinimumSize(QtCore.QSize(290, 360))
        AddDonor.setMaximumSize(QtCore.QSize(290, 360))

        self.lblFname = QtWidgets.QLabel(AddDonor)
        self.lblFname.setGeometry(QtCore.QRect(50, 80, 71, 25))
        self.lblFname.setObjectName("lblFname")

        self.entFname = QtWidgets.QLineEdit(AddDonor)
        self.entFname.setGeometry(QtCore.QRect(120, 80, 121, 25))
        self.entFname.setObjectName("entFname")

        self.lblLname = QtWidgets.QLabel(AddDonor)
        self.lblLname.setGeometry(QtCore.QRect(50, 120, 71, 25))
        self.lblLname.setObjectName("lblLname")

        self.entLname = QtWidgets.QLineEdit(AddDonor)
        self.entLname.setGeometry(QtCore.QRect(120, 120, 121, 25))
        self.entLname.setObjectName("entLname")

        self.lblAddress = QtWidgets.QLabel(AddDonor)
        self.lblAddress.setGeometry(QtCore.QRect(50, 160, 71, 25))
        self.lblAddress.setObjectName("lblAddress")

        self.entAddress = QtWidgets.QLineEdit(AddDonor)
        self.entAddress.setGeometry(QtCore.QRect(120, 160, 121, 25))
        self.entAddress.setObjectName("entAddress")

        self.lblContact = QtWidgets.QLabel(AddDonor)
        self.lblContact.setGeometry(QtCore.QRect(50, 200, 91, 25))
        self.lblContact.setObjectName("lblContact")

        self.entContact = QtWidgets.QLineEdit(AddDonor)
        self.entContact.setGeometry(QtCore.QRect(100, 220, 121, 25))
        self.entContact.setObjectName("entContact")

        self.lblPrefix = QtWidgets.QLabel(AddDonor)
        self.lblPrefix.setGeometry(QtCore.QRect(70, 220, 31, 25))
        self.lblPrefix.setObjectName("lblPrefix")

        self.lblYear = QtWidgets.QLabel(AddDonor)
        self.lblYear.setGeometry(QtCore.QRect(140, 255, 75, 25))
        self.lblYear.setText('Birthdate:')
        self.lblYear.setObjectName("lblYear")

        self.selYear = QtWidgets.QComboBox(AddDonor)
        self.selYear.setGeometry(QtCore.QRect(50, 280, 69, 22))
        self.selYear.setObjectName("selYear")
        for i in range(41):
            self.selYear.addItem("")
        self.selYear.currentIndexChanged.connect(self.unlockMonth)
        
        self.selMonth = QtWidgets.QComboBox(AddDonor)
        self.selMonth.setGeometry(QtCore.QRect(130, 280, 51, 22))
        self.selMonth.setObjectName("selMonth")
        for i in range(13):
            self.selMonth.addItem("")
        self.selMonth.setEnabled(False)
        self.selMonth.currentIndexChanged.connect(self.unlockDay)

        self.selDay = QtWidgets.QComboBox(AddDonor)
        self.selDay.setGeometry(QtCore.QRect(190, 280, 51, 22))
        self.selDay.setObjectName("selDay")
        for i in range(32):
            self.selDay.addItem("")
        self.selDay.setEnabled(False)

        self.addConfirm = QtWidgets.QPushButton(AddDonor)
        self.addConfirm.setGeometry(QtCore.QRect(120, 310, 75, 25))
        self.addConfirm.setObjectName("addConfirm")
        self.addConfirm.clicked.connect(self.newDonor)
        self.addConfirm.clicked.connect(AddDonor.accept)

        self.addCancel = QtWidgets.QPushButton(AddDonor)
        self.addCancel.setGeometry(QtCore.QRect(200, 310, 75, 25))
        self.addCancel.setObjectName("addCancel")
        self.addCancel.clicked.connect(AddDonor.reject)


        self.lblTitle = QtWidgets.QLabel(AddDonor)
        self.lblTitle.setGeometry(QtCore.QRect(80, 20, 131, 31))

        font = QtGui.QFont()
        font.setPointSize(11)

        self.lblTitle.setFont(font)
        self.lblTitle.setObjectName("lblTitle")

        self.retranslateUi(AddDonor)
        QtCore.QMetaObject.connectSlotsByName(AddDonor)

    def retranslateUi(self, AddDonor):
        _translate = QtCore.QCoreApplication.translate
        AddDonor.setWindowTitle(_translate("AddDonor", "New Donor"))
        self.lblFname.setText(_translate("AddDonor", "First Name: "))
        self.lblLname.setText(_translate("AddDonor", "Last Name: "))
        self.lblAddress.setText(_translate("AddDonor", "Address:"))
        self.lblContact.setText(_translate("AddDonor", "Contact Number:"))
        self.lblPrefix.setText(_translate("AddDonor", " +63"))
        self.addConfirm.setText(_translate("AddDonor", "Confirm"))
        self.addCancel.setText(_translate("AddDonor", "Cancel"))
        self.lblTitle.setText(_translate("AddDonor", "ADD NEW DONOR"))
        self.selDay.setItemText(0, _translate("AddDonor", "Day"))
        self.selYear.setItemText(0, _translate("AddDonor", 'Year'))
        self.selMonth.setItemText(0, _translate("AddDonor", "Mon"))
        self.selMonth.setItemText(1, _translate("AddDonor", "Jan"))
        self.selMonth.setItemText(2, _translate("AddDonor", "Feb"))
        self.selMonth.setItemText(3, _translate("AddDonor", "Mar"))
        self.selMonth.setItemText(4, _translate("AddDonor", "Apr"))
        self.selMonth.setItemText(5, _translate("AddDonor", "May"))
        self.selMonth.setItemText(6, _translate("AddDonor", "Jun"))
        self.selMonth.setItemText(7, _translate("AddDonor", "Jul"))
        self.selMonth.setItemText(8, _translate("AddDonor", "Aug"))
        self.selMonth.setItemText(9, _translate("AddDonor", "Sep"))
        self.selMonth.setItemText(10, _translate("AddDonor", "Oct"))
        self.selMonth.setItemText(11, _translate("AddDonor", "Nov"))
        self.selMonth.setItemText(12, _translate("AddDonor", "Dec"))


        for i in range(1, 40):
            self.selYear.setItemText(i, _translate("AddDonor", str(int(datetime.datetime.now().year) - 20 - i)))
