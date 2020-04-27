

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QStatusBar
import qtmodern.windows
from db import Database
from AddBloodBank import Ui_AddBloodBank
from AddDonation import Ui_AddDonation
from AddPatient import Ui_AddPatient
from AddDonor import Ui_AddDonor
from ViewPatient import Ui_ViewPatient
from UseBlood import Ui_UseBlood


db = Database()
donationHeaderUnused = ['Donor', 'Blood Bank', 'Blood Type', 'Donation Date']
donationHeaderUsed = ['Donor', 'Donation Date', 'Recipient', 'Blood Type']
donorHeader = ['Name', 'Address', 'Contact Number', 'Date of Birth']
bloodbankHeader = ['Name', 'Address', 'Contact Number', 'Blood Types']
patientHeader = ['Name', 'Blood Type', 'Contact Number', 'Last Admitted']


class Ui_MainWindow(object):
  def populateTable(self, res):
    self.mainTable.setRowCount(0)
    for x, row in enumerate(res):
      self.mainTable.insertRow(x)
      for y, col in enumerate(row):
        if len(row) == 4:
          self.mainTable.setItem(x, y, QtWidgets.QTableWidgetItem(str(col)))
        elif len(row) == 5:
          if y != 0:
            self.mainTable.setItem(x, y - 1, QtWidgets.QTableWidgetItem(str(col)))

  def getPatient(self):
    self.patient = db.getPatient()

  def getDonation(self):
    self.donation = db.getDonation(1)
  

  def search(self):
    if self.radShowUnused.isChecked():
      self.res = db.lookFor(self.searchBar.text(), self.filterBox.currentText(), self.optionTools.currentText(), 1)
    else:
      self.res = db.lookFor(self.searchBar.text(), self.filterBox.currentText(), self.optionTools.currentText(), 0)
    self.populateTable(self.res)

  def filter(self):
    self.searchBar.setText('')
    test = self.filterBox.currentText()
    if test == 'Donation':
      if self.radShowUnused.isChecked():
        self.mainTable.setHorizontalHeaderLabels(donationHeaderUnused)
        self.optionTools.setItemText(0, "by Donor")
        self.optionTools.setItemText(1, "by Blood Bank")
        self.optionTools.setItemText(2, "by Blood Type")
        self.optionTools.setItemText(3, "by Donation Date")
        self.populateTable(db.getDonation(1))
        self.useBlood.setVisible(True)
      else:
        self.mainTable.setHorizontalHeaderLabels(donationHeaderUsed)
        self.optionTools.setItemText(0, "by Donor")
        self.optionTools.setItemText(1, "by Donation Date")
        self.optionTools.setItemText(2, "by Recipient")
        self.optionTools.setItemText(3, "by Blood Type")
        self.populateTable(db.getDonation(0))
        self.useBlood.setVisible(False)
      self.viewPatient.setVisible(False)
      self.radShowUnused.setVisible(True)
      self.radShowUsed.setVisible(True)

    if test == 'Donor':
      self.optionTools.setItemText(0, "by Name")
      self.optionTools.setItemText(1, "by Address")
      self.optionTools.setItemText(2, "by Contact Number")
      self.optionTools.setItemText(3, "by Birthdate")
      self.mainTable.setHorizontalHeaderLabels(donorHeader)
      self.populateTable(db.getDonor())
      self.viewPatient.setVisible(False)
      self.radShowUnused.setVisible(False)
      self.radShowUsed.setVisible(False)
      self.useBlood.setVisible(False)

    if test == 'Blood Bank':
      self.optionTools.setItemText(0, "by Name")
      self.optionTools.setItemText(1, "by Address")
      self.optionTools.setItemText(2, "by Contact Number")
      self.optionTools.setItemText(3, "by Blood Types")
      self.mainTable.setHorizontalHeaderLabels(bloodbankHeader)
      self.populateTable(db.getBloodbank())
      self.viewPatient.setVisible(False)
      self.radShowUnused.setVisible(False)
      self.radShowUsed.setVisible(False)
      self.useBlood.setVisible(False)

    if test == 'Patient':
      self.optionTools.setItemText(0, "by Name")
      self.optionTools.setItemText(1, "by Blood Type")
      self.optionTools.setItemText(2, "by Contact Number")
      self.optionTools.setItemText(3, "by Admission Date")
      self.mainTable.setHorizontalHeaderLabels(patientHeader)
      self.populateTable(db.getPatient())
      self.viewPatient.setVisible(True)
      self.radShowUnused.setVisible(False)
      self.radShowUsed.setVisible(False)
      self.useBlood.setVisible(False)

  def patientInfo(self):
    try:
      self.getPatient()
      self.patientViewDialog = QtWidgets.QDialog()
      self.patientViewer = Ui_ViewPatient()
      self.styleModal(self.patientViewDialog, self.patientViewer, 2)
      return self.patientViewDialog
    except Exception as e:
      pass

  def styleModal(self, Dialog, ui_Dialog, check):
    if check == 1:
      ui_Dialog.setupUi(Dialog, db, self.ui_DonationDialog)
    elif check == 0:
      ui_Dialog.setupUi(Dialog, db)
    elif check == 2:
      ui_Dialog.setupUi(Dialog, self.patient[self.mainTable.currentRow()][0], self.patient[self.mainTable.currentRow()][1], db)
    elif check == 3:
      self.getDonation()
      ui_Dialog.setupUi(Dialog, db, self.donation[self.mainTable.currentRow()])
    self.modernDialog = qtmodern.windows.ModernWindow(Dialog, self.centralwidget)
    self.modernDialog.setWindowModality(QtCore.Qt.ApplicationModal)
    qr = self.modernDialog.frameGeometry()
    cp = QtWidgets.QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.modernDialog.move(qr.topLeft())
    self.modernDialog.show()
    return

  def useBloodNow(self, check=3):
    try:
      self.useBloodDialog = QtWidgets.QDialog()
      self.ui_useBloodDialog = Ui_UseBlood()
      self.styleModal(self.useBloodDialog, self.ui_useBloodDialog, check)
      if self.useBloodDialog.exec_() == self.useBloodDialog.Accepted:
        self.filter()
        return self.useBloodDialog
    except Exception as e:
      pass

  def newPatient(self, check=0):
    self.newPatientDialog = QtWidgets.QDialog()
    self.ui_newPatientDialog = Ui_AddPatient()
    self.styleModal(self.newPatientDialog, self.ui_newPatientDialog, check)
    if self.newPatientDialog.exec_() == self.newPatientDialog.Accepted:
      self.filter()
      return self.newPatientDialog
  
  def newDonor(self, check = 0):
    self.newDonorDialog = QtWidgets.QDialog()
    self.ui_newDonorDialog = Ui_AddDonor()
    self.styleModal(self.newDonorDialog, self.ui_newDonorDialog, check)
    if self.newDonorDialog.exec_() == self.newDonorDialog.Accepted:
      self.filter()
      return self.newDonorDialog


  def newBloodBank(self, check = 0):
    self.newBloodBankDialog = QtWidgets.QDialog()
    self.ui_newBloodBankDialog = Ui_AddBloodBank()
    self.styleModal(self.newBloodBankDialog, self.ui_newBloodBankDialog, check)
    if self.newBloodBankDialog.exec_() == self.newBloodBankDialog.Accepted:
      self.filter()
      return self.newBloodBankDialog

  def newDonation(self):
    self.newDonationDialog = QtWidgets.QDialog()
    self.ui_DonationDialog = Ui_AddDonation()
    self.styleModal(self.newDonationDialog, self.ui_DonationDialog, 0)
    self.ui_DonationDialog.newRecipient.clicked.connect(lambda: self.newPatient(1))
    self.ui_DonationDialog.newBloodBank.clicked.connect(lambda: self.newBloodBank(1))
    self.ui_DonationDialog.newDonor.clicked.connect(lambda: self.newDonor(1))
    if self.newDonationDialog.exec_() == self.newDonationDialog.Accepted:
      self.filter()
      # return self.newDonationDialog
      

  def setupUi(self, MainWindow):
    MainWindow.setObjectName("MainWindow")
    MainWindow.resize(630, 420)
    MainWindow.setMaximumHeight(420)
    MainWindow.setMaximumWidth(630)
    MainWindow.setMinimumSize(QtCore.QSize(630, 420))
    MainWindow.setMaximumSize(QtCore.QSize(630, 420))
    MainWindow.setBaseSize(QtCore.QSize(630, 420))

    self.centralwidget = QtWidgets.QWidget(MainWindow)
    self.centralwidget.setObjectName("centralwidget")

    self.mainTable = QtWidgets.QTableWidget(self.centralwidget)
    self.mainTable.setGeometry(QtCore.QRect(20, 70, 460, 300))
    self.mainTable.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
    self.mainTable.setRowCount(50)
    self.mainTable.setAlternatingRowColors(True)
    self.mainTable.setColumnCount(4)
    self.mainTable.horizontalHeader().setDefaultSectionSize(111)
    self.mainTable.horizontalHeader().setMinimumSectionSize(111)
    self.mainTable.verticalHeader().setMinimumSectionSize(30)
    self.mainTable.verticalHeader().setMaximumSectionSize(30)
    self.mainTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
    self.mainTable.setObjectName("mainTable")

    self.addPatient = QtWidgets.QPushButton(self.centralwidget)
    self.addPatient.setGeometry(QtCore.QRect(500, 210, 100, 30))
    self.addPatient.setObjectName("addPatient")
    self.addPatient.clicked.connect(self.newPatient)

    self.addBBank = QtWidgets.QPushButton(self.centralwidget)
    self.addBBank.setGeometry(QtCore.QRect(500, 150, 100, 30))
    self.addBBank.setObjectName("addBBank")
    self.addBBank.clicked.connect(self.newBloodBank)

    self.addDonation = QtWidgets.QPushButton(self.centralwidget)
    self.addDonation.setGeometry(QtCore.QRect(500, 90, 100, 30))
    self.addDonation.setObjectName("addDonation")
    self.addDonation.clicked.connect(self.newDonation)

    self.viewPatient = QtWidgets.QPushButton(self.centralwidget)
    self.viewPatient.setGeometry(QtCore.QRect(500, 270, 100, 30))
    self.viewPatient.setObjectName("viewPatient")
    self.viewPatient.setVisible(False)
    self.viewPatient.clicked.connect(self.patientInfo)

    self.useBlood = QtWidgets.QPushButton(self.centralwidget)
    self.useBlood.setGeometry(QtCore.QRect(500, 270, 100, 30))
    self.useBlood.setObjectName("useBlood")
    self.useBlood.setVisible(False)
    self.useBlood.clicked.connect(lambda: self.useBloodNow(3))

    self.filterBox = QtWidgets.QComboBox(self.centralwidget)
    self.filterBox.setGeometry(QtCore.QRect(20, 40, 161, 25))
    self.filterBox.setMaxVisibleItems(4)
    self.filterBox.setObjectName("filterBox")
    self.filterBox.addItem("")
    self.filterBox.addItem("")
    self.filterBox.addItem("")
    self.filterBox.addItem("")
    self.filterBox.currentTextChanged.connect(self.filter)

    self.optionTools = QtWidgets.QComboBox(self.centralwidget)
    self.optionTools.setGeometry(QtCore.QRect(360, 40, 120, 25))
    self.optionTools.setObjectName("optionTools")
    self.optionTools.addItem("")
    self.optionTools.addItem("")
    self.optionTools.addItem("")
    self.optionTools.addItem("")
    self.optionTools.currentTextChanged.connect(self.search)

    self.searchBar = QtWidgets.QLineEdit(self.centralwidget)
    self.searchBar.setGeometry(QtCore.QRect(220, 40, 131, 25))
    self.searchBar.setPlaceholderText("Search...")
    self.searchBar.setObjectName("searchBar")
    self.searchBar.textChanged.connect(self.search)

    self.radShowUsed = QtWidgets.QRadioButton(self.centralwidget)
    self.radShowUsed.setGeometry(QtCore.QRect(400, 380, 85, 17))
    self.radShowUsed.setObjectName("radShowUsed")
    self.radShowUsed.clicked.connect(self.filter)
    self.radShowUsed.setVisible(True)

    self.radShowUnused = QtWidgets.QRadioButton(self.centralwidget)
    self.radShowUnused.setGeometry(QtCore.QRect(290, 380, 85, 17))
    self.radShowUnused.setObjectName("radShowUnused")
    self.radShowUnused.setChecked(True)
    self.radShowUnused.clicked.connect(self.filter)
    self.radShowUnused.setVisible(True)

    MainWindow.setCentralWidget(self.centralwidget)

    self.statusbar = QtWidgets.QStatusBar(MainWindow)
    self.statusbar.setObjectName("statusbar")
    MainWindow.setStatusBar(self.statusbar)

    self.retranslateUi(MainWindow)
    QtCore.QMetaObject.connectSlotsByName(MainWindow)

    self.res = list()
    self.patient = list()
    self.donation = list()

  def retranslateUi(self, MainWindow):
    _translate = QtCore.QCoreApplication.translate
    MainWindow.setWindowTitle(_translate("MainWindow", "Blood Bank Management System"))
    self.addPatient.setText(_translate("MainWindow", "Add Patient"))
    self.addBBank.setText(_translate("MainWindow", "Add Blood Bank"))
    self.addDonation.setText(_translate("MainWindow", "Add Donation"))

    self.viewPatient.setText(_translate("MainWindow", "Patient History"))
    self.useBlood.setText(_translate("MainWindow", "Use Blood"))

    self.filterBox.setItemText(0, _translate("MainWindow", "Donation"))
    self.filterBox.setItemText(1, _translate("MainWindow", "Donor"))
    self.filterBox.setItemText(2, _translate("MainWindow", "Blood Bank"))
    self.filterBox.setItemText(3, _translate("MainWindow", "Patient"))

    self.radShowUsed.setText(_translate("MainWindow", "Show Used"))
    self.radShowUnused.setText(_translate("MainWindow", "Show Unused"))
