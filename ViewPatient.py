

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ViewPatient(object):

    def populateTable(self, res):
        self.chartTable.setRowCount(0)
        for x, row in enumerate(res):
            self.chartTable.insertRow(x)
            for y, col in enumerate(row):
                self.chartTable.setItem(x, y, QtWidgets.QTableWidgetItem(str(col)))
    

    def setupUi(self, ViewPatient, id, name, db):
        self.db = db

        ViewPatient.setObjectName("ViewPatient")
        ViewPatient.resize(600, 420)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ViewPatient.sizePolicy().hasHeightForWidth())

        ViewPatient.setSizePolicy(sizePolicy)
        ViewPatient.setMinimumSize(QtCore.QSize(600, 420))
        ViewPatient.setMaximumSize(QtCore.QSize(600, 420))

        self.chartTable = QtWidgets.QTableWidget(ViewPatient)
        self.chartTable.setGeometry(QtCore.QRect(40, 110, 511, 261))

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chartTable.sizePolicy().hasHeightForWidth())

        self.chartTable.setSizePolicy(sizePolicy)
        self.chartTable.setMinimumSize(QtCore.QSize(351, 0))
        self.chartTable.setObjectName("chartTable")
        self.chartTable.setColumnCount(4)
        self.chartTable.setRowCount(0)

        item = QtWidgets.QTableWidgetItem()
        self.chartTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.chartTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.chartTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.chartTable.setHorizontalHeaderItem(3, item)
        self.chartTable.horizontalHeader().setCascadingSectionResizes(False)
        self.chartTable.horizontalHeader().setDefaultSectionSize(123)
        self.chartTable.horizontalHeader().setMinimumSectionSize(110)

        self.lblPId = QtWidgets.QLabel(ViewPatient)
        self.lblPId.setGeometry(QtCore.QRect(50, 20, 101, 41))

        font = QtGui.QFont()
        font.setPointSize(14)

        self.lblPId.setFont(font)
        self.lblPId.setObjectName("lblPId")
        self.lblPName = QtWidgets.QLabel(ViewPatient)
        self.lblPName.setGeometry(QtCore.QRect(50, 60, 101, 41))

        font = QtGui.QFont()
        font.setPointSize(14)

        self.lblPName.setFont(font)
        self.lblPName.setObjectName("lblPName")
        self.lblConID = QtWidgets.QLabel(ViewPatient)
        self.lblConID.setGeometry(QtCore.QRect(160, 20, 271, 41))
        self.lblConID.setText(str(id))

        font = QtGui.QFont()
        font.setPointSize(14)

        self.lblConID.setFont(font)
        self.lblConID.setObjectName("lblConID")

        self.lbConName = QtWidgets.QLabel(ViewPatient)
        self.lbConName.setGeometry(QtCore.QRect(160, 60, 271, 41))
        self.lbConName.setText(name)

        font = QtGui.QFont()
        font.setPointSize(14)

        self.lbConName.setFont(font)
        self.lbConName.setObjectName("lbConName")

        self.retranslateUi(ViewPatient)
        QtCore.QMetaObject.connectSlotsByName(ViewPatient)

        self.populateTable(self.db.getOnePatient(id))

    def retranslateUi(self, ViewPatient):
        _translate = QtCore.QCoreApplication.translate
        ViewPatient.setWindowTitle(_translate("ViewPatient", "Patient Chart"))
        item = self.chartTable.horizontalHeaderItem(0)
        item.setText(_translate("ViewPatient", "Diagnosis"))
        item = self.chartTable.horizontalHeaderItem(1)
        item.setText(_translate("ViewPatient", "Date Admitted"))
        item = self.chartTable.horizontalHeaderItem(2)
        item.setText(_translate("ViewPatient", "has Received Blood"))
        item = self.chartTable.horizontalHeaderItem(3)
        item.setText(_translate("ViewPatient", "Donor"))
        self.lblPId.setText(_translate("ViewPatient", "Patient ID:"))
        self.lblPName.setText(_translate("ViewPatient", "Name:"))
