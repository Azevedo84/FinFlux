# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tela_grafico_mensal.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(795, 552)
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
        self.label_16 = QtWidgets.QLabel(self.widget_5)
        self.label_16.setMinimumSize(QtCore.QSize(0, 0))
        self.label_16.setMaximumSize(QtCore.QSize(30, 16777215))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_16.setFont(font)
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_3.addWidget(self.label_16)
        self.combo_Meses = QtWidgets.QComboBox(self.widget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_Meses.sizePolicy().hasHeightForWidth())
        self.combo_Meses.setSizePolicy(sizePolicy)
        self.combo_Meses.setMinimumSize(QtCore.QSize(0, 0))
        self.combo_Meses.setMaximumSize(QtCore.QSize(130, 25))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.combo_Meses.setFont(font)
        self.combo_Meses.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.combo_Meses.setObjectName("combo_Meses")
        self.combo_Meses.addItem("")
        self.combo_Meses.setItemText(0, "")
        self.combo_Meses.addItem("")
        self.combo_Meses.addItem("")
        self.combo_Meses.addItem("")
        self.combo_Meses.addItem("")
        self.combo_Meses.addItem("")
        self.combo_Meses.addItem("")
        self.combo_Meses.addItem("")
        self.combo_Meses.addItem("")
        self.combo_Meses.addItem("")
        self.combo_Meses.addItem("")
        self.combo_Meses.addItem("")
        self.combo_Meses.addItem("")
        self.combo_Meses.addItem("")
        self.horizontalLayout_3.addWidget(self.combo_Meses)
        self.label_17 = QtWidgets.QLabel(self.widget_5)
        self.label_17.setMinimumSize(QtCore.QSize(0, 0))
        self.label_17.setMaximumSize(QtCore.QSize(30, 16777215))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_17.setFont(font)
        self.label_17.setAlignment(QtCore.Qt.AlignCenter)
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_3.addWidget(self.label_17)
        self.line_Ano = QtWidgets.QLineEdit(self.widget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_Ano.sizePolicy().hasHeightForWidth())
        self.line_Ano.setSizePolicy(sizePolicy)
        self.line_Ano.setMaximumSize(QtCore.QSize(70, 25))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.line_Ano.setFont(font)
        self.line_Ano.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.line_Ano.setText("")
        self.line_Ano.setMaxLength(45)
        self.line_Ano.setAlignment(QtCore.Qt.AlignCenter)
        self.line_Ano.setObjectName("line_Ano")
        self.horizontalLayout_3.addWidget(self.line_Ano)
        self.label = QtWidgets.QLabel(self.widget_5)
        self.label.setText("")
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.btn_Consulta = QtWidgets.QPushButton(self.widget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_Consulta.sizePolicy().hasHeightForWidth())
        self.btn_Consulta.setSizePolicy(sizePolicy)
        self.btn_Consulta.setMinimumSize(QtCore.QSize(90, 30))
        self.btn_Consulta.setMaximumSize(QtCore.QSize(90, 30))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.btn_Consulta.setFont(font)
        self.btn_Consulta.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_Consulta.setObjectName("btn_Consulta")
        self.horizontalLayout_3.addWidget(self.btn_Consulta)
        self.verticalLayout.addWidget(self.widget_5)
        self.widget_4 = QtWidgets.QWidget(self.centralwidget)
        self.widget_4.setStyleSheet("background-color: rgb(172, 172, 172);")
        self.widget_4.setObjectName("widget_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_4)
        self.verticalLayout_2.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_5 = QtWidgets.QLabel(self.widget_4)
        self.label_5.setMinimumSize(QtCore.QSize(0, 0))
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.widget_2 = QtWidgets.QWidget(self.widget_4)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.widget_3 = QtWidgets.QWidget(self.widget_2)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_2.addWidget(self.widget_3)
        self.widget_grafico = QtWidgets.QWidget(self.widget_2)
        self.widget_grafico.setObjectName("widget_grafico")
        self.horizontalLayout_2.addWidget(self.widget_grafico)
        self.verticalLayout_2.addWidget(self.widget_2)
        self.verticalLayout.addWidget(self.widget_4)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setMaximumSize(QtCore.QSize(16777215, 35))
        self.widget.setStyleSheet("background-color: rgb(172, 172, 172);")
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.label_18 = QtWidgets.QLabel(self.widget)
        self.label_18.setMinimumSize(QtCore.QSize(0, 0))
        self.label_18.setMaximumSize(QtCore.QSize(35, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_18.setFont(font)
        self.label_18.setAlignment(QtCore.Qt.AlignCenter)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout.addWidget(self.label_18)
        self.label_Total = QtWidgets.QLabel(self.widget)
        self.label_Total.setMaximumSize(QtCore.QSize(100, 25))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_Total.setFont(font)
        self.label_Total.setText("")
        self.label_Total.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Total.setObjectName("label_Total")
        self.horizontalLayout.addWidget(self.label_Total)
        self.verticalLayout.addWidget(self.widget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Despesas Mensal"))
        self.label_16.setText(_translate("MainWindow", "Mês:"))
        self.combo_Meses.setItemText(1, _translate("MainWindow", "TODOS"))
        self.combo_Meses.setItemText(2, _translate("MainWindow", "1 - JANEIRO"))
        self.combo_Meses.setItemText(3, _translate("MainWindow", "2 - FEVEREIRO"))
        self.combo_Meses.setItemText(4, _translate("MainWindow", "3 - MARÇO"))
        self.combo_Meses.setItemText(5, _translate("MainWindow", "4 - ABRIL"))
        self.combo_Meses.setItemText(6, _translate("MainWindow", "5 - MAIO"))
        self.combo_Meses.setItemText(7, _translate("MainWindow", "6 - JUNHO"))
        self.combo_Meses.setItemText(8, _translate("MainWindow", "7 - JULHO"))
        self.combo_Meses.setItemText(9, _translate("MainWindow", "8 - AGOSTO"))
        self.combo_Meses.setItemText(10, _translate("MainWindow", "9 - SETEMBRO"))
        self.combo_Meses.setItemText(11, _translate("MainWindow", "10 - OUTUBRO"))
        self.combo_Meses.setItemText(12, _translate("MainWindow", "11 - NOVEMBRO"))
        self.combo_Meses.setItemText(13, _translate("MainWindow", "12 - DEZEMBRO"))
        self.label_17.setText(_translate("MainWindow", "Ano:"))
        self.btn_Consulta.setText(_translate("MainWindow", "Consultar"))
        self.label_5.setText(_translate("MainWindow", "Despesas Mensal"))
        self.label_18.setText(_translate("MainWindow", "Total:"))
