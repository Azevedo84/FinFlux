# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tela_rel_cartoes.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(722, 531)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_5 = QtWidgets.QWidget(self.centralwidget)
        self.widget_5.setMinimumSize(QtCore.QSize(0, 40))
        self.widget_5.setMaximumSize(QtCore.QSize(16777215, 40))
        self.widget_5.setStyleSheet("background-color: rgb(172, 172, 172);")
        self.widget_5.setObjectName("widget_5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_5)
        self.horizontalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout.addWidget(self.widget_5)
        self.widget_3 = QtWidgets.QWidget(self.centralwidget)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget_6 = QtWidgets.QWidget(self.widget_3)
        self.widget_6.setStyleSheet("background-color: rgb(172, 172, 172);")
        self.widget_6.setObjectName("widget_6")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_6)
        self.verticalLayout_2.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_5 = QtWidgets.QLabel(self.widget_6)
        self.label_5.setMinimumSize(QtCore.QSize(0, 25))
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.table_C6 = QtWidgets.QTableWidget(self.widget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table_C6.sizePolicy().hasHeightForWidth())
        self.table_C6.setSizePolicy(sizePolicy)
        self.table_C6.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.table_C6.setObjectName("table_C6")
        self.table_C6.setColumnCount(2)
        self.table_C6.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table_C6.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_C6.setHorizontalHeaderItem(1, item)
        self.verticalLayout_2.addWidget(self.table_C6)
        self.horizontalLayout.addWidget(self.widget_6)
        self.widget = QtWidgets.QWidget(self.widget_3)
        self.widget.setStyleSheet("background-color: rgb(172, 172, 172);")
        self.widget.setObjectName("widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setMinimumSize(QtCore.QSize(0, 25))
        self.label_6.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_3.addWidget(self.label_6)
        self.table_XP = QtWidgets.QTableWidget(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table_XP.sizePolicy().hasHeightForWidth())
        self.table_XP.setSizePolicy(sizePolicy)
        self.table_XP.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.table_XP.setObjectName("table_XP")
        self.table_XP.setColumnCount(2)
        self.table_XP.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table_XP.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_XP.setHorizontalHeaderItem(1, item)
        self.verticalLayout_3.addWidget(self.table_XP)
        self.horizontalLayout.addWidget(self.widget)
        self.widget_2 = QtWidgets.QWidget(self.widget_3)
        self.widget_2.setStyleSheet("background-color: rgb(172, 172, 172);")
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_4.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_7 = QtWidgets.QLabel(self.widget_2)
        self.label_7.setMinimumSize(QtCore.QSize(0, 25))
        self.label_7.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_4.addWidget(self.label_7)
        self.table_NU = QtWidgets.QTableWidget(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table_NU.sizePolicy().hasHeightForWidth())
        self.table_NU.setSizePolicy(sizePolicy)
        self.table_NU.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.table_NU.setObjectName("table_NU")
        self.table_NU.setColumnCount(2)
        self.table_NU.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table_NU.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_NU.setHorizontalHeaderItem(1, item)
        self.verticalLayout_4.addWidget(self.table_NU)
        self.horizontalLayout.addWidget(self.widget_2)
        self.widget_7 = QtWidgets.QWidget(self.widget_3)
        self.widget_7.setStyleSheet("background-color: rgb(172, 172, 172);")
        self.widget_7.setObjectName("widget_7")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget_7)
        self.verticalLayout_5.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_8 = QtWidgets.QLabel(self.widget_7)
        self.label_8.setMinimumSize(QtCore.QSize(0, 25))
        self.label_8.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_5.addWidget(self.label_8)
        self.table_Samsung = QtWidgets.QTableWidget(self.widget_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table_Samsung.sizePolicy().hasHeightForWidth())
        self.table_Samsung.setSizePolicy(sizePolicy)
        self.table_Samsung.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.table_Samsung.setObjectName("table_Samsung")
        self.table_Samsung.setColumnCount(2)
        self.table_Samsung.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table_Samsung.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_Samsung.setHorizontalHeaderItem(1, item)
        self.verticalLayout_5.addWidget(self.table_Samsung)
        self.horizontalLayout.addWidget(self.widget_7)
        self.widget_4 = QtWidgets.QWidget(self.widget_3)
        self.widget_4.setStyleSheet("background-color: rgb(172, 172, 172);")
        self.widget_4.setObjectName("widget_4")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.widget_4)
        self.verticalLayout_6.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_9 = QtWidgets.QLabel(self.widget_4)
        self.label_9.setMinimumSize(QtCore.QSize(0, 25))
        self.label_9.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_6.addWidget(self.label_9)
        self.table_Bradesco = QtWidgets.QTableWidget(self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table_Bradesco.sizePolicy().hasHeightForWidth())
        self.table_Bradesco.setSizePolicy(sizePolicy)
        self.table_Bradesco.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.table_Bradesco.setObjectName("table_Bradesco")
        self.table_Bradesco.setColumnCount(2)
        self.table_Bradesco.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table_Bradesco.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_Bradesco.setHorizontalHeaderItem(1, item)
        self.verticalLayout_6.addWidget(self.table_Bradesco)
        self.horizontalLayout.addWidget(self.widget_4)
        self.widget_8 = QtWidgets.QWidget(self.widget_3)
        self.widget_8.setStyleSheet("background-color: rgb(172, 172, 172);")
        self.widget_8.setObjectName("widget_8")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.widget_8)
        self.verticalLayout_7.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_10 = QtWidgets.QLabel(self.widget_8)
        self.label_10.setMinimumSize(QtCore.QSize(0, 25))
        self.label_10.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_7.addWidget(self.label_10)
        self.table_Total = QtWidgets.QTableWidget(self.widget_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table_Total.sizePolicy().hasHeightForWidth())
        self.table_Total.setSizePolicy(sizePolicy)
        self.table_Total.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.table_Total.setObjectName("table_Total")
        self.table_Total.setColumnCount(2)
        self.table_Total.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table_Total.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_Total.setHorizontalHeaderItem(1, item)
        self.verticalLayout_7.addWidget(self.table_Total)
        self.horizontalLayout.addWidget(self.widget_8)
        self.verticalLayout.addWidget(self.widget_3)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Despesas Mensal/Anual"))
        self.label_5.setText(_translate("MainWindow", "C6"))
        item = self.table_C6.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "FATURA"))
        item = self.table_C6.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "VALOR"))
        self.label_6.setText(_translate("MainWindow", "XP"))
        item = self.table_XP.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "FATURA"))
        item = self.table_XP.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "VALOR"))
        self.label_7.setText(_translate("MainWindow", "NUBANK"))
        item = self.table_NU.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "FATURA"))
        item = self.table_NU.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "VALOR"))
        self.label_8.setText(_translate("MainWindow", "SAMSUNG"))
        item = self.table_Samsung.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "FATURA"))
        item = self.table_Samsung.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "VALOR"))
        self.label_9.setText(_translate("MainWindow", "BRADESCO"))
        item = self.table_Bradesco.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "FATURA"))
        item = self.table_Bradesco.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "VALOR"))
        self.label_10.setText(_translate("MainWindow", "Total"))
        item = self.table_Total.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "FATURA"))
        item = self.table_Total.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "VALOR"))
