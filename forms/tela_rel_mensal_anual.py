# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tela_rel_mensal_anual.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(776, 531)
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
        self.label_19 = QtWidgets.QLabel(self.widget_5)
        self.label_19.setMinimumSize(QtCore.QSize(0, 0))
        self.label_19.setMaximumSize(QtCore.QSize(40, 16777215))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_3.addWidget(self.label_19)
        self.combo_Grupo = QtWidgets.QComboBox(self.widget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_Grupo.sizePolicy().hasHeightForWidth())
        self.combo_Grupo.setSizePolicy(sizePolicy)
        self.combo_Grupo.setMinimumSize(QtCore.QSize(0, 0))
        self.combo_Grupo.setMaximumSize(QtCore.QSize(150, 25))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.combo_Grupo.setFont(font)
        self.combo_Grupo.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.combo_Grupo.setObjectName("combo_Grupo")
        self.combo_Grupo.addItem("")
        self.combo_Grupo.setItemText(0, "")
        self.horizontalLayout_3.addWidget(self.combo_Grupo)
        self.label_3 = QtWidgets.QLabel(self.widget_5)
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.label_21 = QtWidgets.QLabel(self.widget_5)
        self.label_21.setMinimumSize(QtCore.QSize(0, 0))
        self.label_21.setMaximumSize(QtCore.QSize(60, 16777215))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_21.setFont(font)
        self.label_21.setObjectName("label_21")
        self.horizontalLayout_3.addWidget(self.label_21)
        self.combo_Classifica = QtWidgets.QComboBox(self.widget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_Classifica.sizePolicy().hasHeightForWidth())
        self.combo_Classifica.setSizePolicy(sizePolicy)
        self.combo_Classifica.setMinimumSize(QtCore.QSize(0, 0))
        self.combo_Classifica.setMaximumSize(QtCore.QSize(120, 23))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.combo_Classifica.setFont(font)
        self.combo_Classifica.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.combo_Classifica.setObjectName("combo_Classifica")
        self.combo_Classifica.addItem("")
        self.combo_Classifica.addItem("")
        self.combo_Classifica.addItem("")
        self.combo_Classifica.addItem("")
        self.combo_Classifica.addItem("")
        self.combo_Classifica.addItem("")
        self.combo_Classifica.addItem("")
        self.horizontalLayout_3.addWidget(self.combo_Classifica)
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
        self.btn_Consulta.setMinimumSize(QtCore.QSize(0, 0))
        self.btn_Consulta.setMaximumSize(QtCore.QSize(70, 30))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.btn_Consulta.setFont(font)
        self.btn_Consulta.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_Consulta.setObjectName("btn_Consulta")
        self.horizontalLayout_3.addWidget(self.btn_Consulta)
        self.verticalLayout.addWidget(self.widget_5)
        self.widget_3 = QtWidgets.QWidget(self.centralwidget)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.widget_9 = QtWidgets.QWidget(self.widget_3)
        self.widget_9.setObjectName("widget_9")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget_9)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.widget_4 = QtWidgets.QWidget(self.widget_9)
        self.widget_4.setMinimumSize(QtCore.QSize(0, 0))
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
        self.table_Lista = QtWidgets.QTableWidget(self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table_Lista.sizePolicy().hasHeightForWidth())
        self.table_Lista.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.table_Lista.setFont(font)
        self.table_Lista.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.table_Lista.setObjectName("table_Lista")
        self.table_Lista.setColumnCount(7)
        self.table_Lista.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table_Lista.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_Lista.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_Lista.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_Lista.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_Lista.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_Lista.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_Lista.setHorizontalHeaderItem(6, item)
        self.verticalLayout_2.addWidget(self.table_Lista)
        self.verticalLayout_4.addWidget(self.widget_4)
        self.widget = QtWidgets.QWidget(self.widget_9)
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
        self.label_Total_Lista = QtWidgets.QLabel(self.widget)
        self.label_Total_Lista.setMaximumSize(QtCore.QSize(100, 25))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_Total_Lista.setFont(font)
        self.label_Total_Lista.setText("")
        self.label_Total_Lista.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Total_Lista.setObjectName("label_Total_Lista")
        self.horizontalLayout.addWidget(self.label_Total_Lista)
        self.verticalLayout_4.addWidget(self.widget)
        self.horizontalLayout_2.addWidget(self.widget_9)
        self.widget_10 = QtWidgets.QWidget(self.widget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_10.sizePolicy().hasHeightForWidth())
        self.widget_10.setSizePolicy(sizePolicy)
        self.widget_10.setMaximumSize(QtCore.QSize(650, 16777215))
        self.widget_10.setObjectName("widget_10")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget_10)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.widget_6 = QtWidgets.QWidget(self.widget_10)
        self.widget_6.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.widget_6.setStyleSheet("background-color: rgb(172, 172, 172);")
        self.widget_6.setObjectName("widget_6")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_6)
        self.verticalLayout_3.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_6 = QtWidgets.QLabel(self.widget_6)
        self.label_6.setMinimumSize(QtCore.QSize(0, 0))
        self.label_6.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_3.addWidget(self.label_6)
        self.widget_grafico = QtWidgets.QWidget(self.widget_6)
        self.widget_grafico.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.widget_grafico.setObjectName("widget_grafico")
        self.verticalLayout_3.addWidget(self.widget_grafico)
        self.verticalLayout_5.addWidget(self.widget_6)
        self.widget_8 = QtWidgets.QWidget(self.widget_10)
        self.widget_8.setMaximumSize(QtCore.QSize(16777215, 35))
        self.widget_8.setStyleSheet("background-color: rgb(172, 172, 172);")
        self.widget_8.setObjectName("widget_8")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget_8)
        self.horizontalLayout_5.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_5.setSpacing(5)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_4 = QtWidgets.QLabel(self.widget_8)
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_5.addWidget(self.label_4)
        self.label_20 = QtWidgets.QLabel(self.widget_8)
        self.label_20.setMinimumSize(QtCore.QSize(0, 0))
        self.label_20.setMaximumSize(QtCore.QSize(35, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_20.setFont(font)
        self.label_20.setAlignment(QtCore.Qt.AlignCenter)
        self.label_20.setObjectName("label_20")
        self.horizontalLayout_5.addWidget(self.label_20)
        self.label_Total_Grafico = QtWidgets.QLabel(self.widget_8)
        self.label_Total_Grafico.setMaximumSize(QtCore.QSize(100, 25))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_Total_Grafico.setFont(font)
        self.label_Total_Grafico.setText("")
        self.label_Total_Grafico.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Total_Grafico.setObjectName("label_Total_Grafico")
        self.horizontalLayout_5.addWidget(self.label_Total_Grafico)
        self.verticalLayout_5.addWidget(self.widget_8)
        self.horizontalLayout_2.addWidget(self.widget_10)
        self.verticalLayout.addWidget(self.widget_3)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Despesas Mensal/Anual"))
        self.label_16.setText(_translate("MainWindow", "Mês:"))
        self.combo_Meses.setItemText(1, _translate("MainWindow", "1 - JANEIRO"))
        self.combo_Meses.setItemText(2, _translate("MainWindow", "2 - FEVEREIRO"))
        self.combo_Meses.setItemText(3, _translate("MainWindow", "3 - MARÇO"))
        self.combo_Meses.setItemText(4, _translate("MainWindow", "4 - ABRIL"))
        self.combo_Meses.setItemText(5, _translate("MainWindow", "5 - MAIO"))
        self.combo_Meses.setItemText(6, _translate("MainWindow", "6 - JUNHO"))
        self.combo_Meses.setItemText(7, _translate("MainWindow", "7 - JULHO"))
        self.combo_Meses.setItemText(8, _translate("MainWindow", "8 - AGOSTO"))
        self.combo_Meses.setItemText(9, _translate("MainWindow", "9 - SETEMBRO"))
        self.combo_Meses.setItemText(10, _translate("MainWindow", "10 - OUTUBRO"))
        self.combo_Meses.setItemText(11, _translate("MainWindow", "11 - NOVEMBRO"))
        self.combo_Meses.setItemText(12, _translate("MainWindow", "12 - DEZEMBRO"))
        self.label_17.setText(_translate("MainWindow", "Ano:"))
        self.label_19.setText(_translate("MainWindow", "Grupo:"))
        self.label_21.setText(_translate("MainWindow", "Classificar:"))
        self.combo_Classifica.setItemText(0, _translate("MainWindow", "DATA"))
        self.combo_Classifica.setItemText(1, _translate("MainWindow", "MAIOR VALOR"))
        self.combo_Classifica.setItemText(2, _translate("MainWindow", "MENOR VALOR"))
        self.combo_Classifica.setItemText(3, _translate("MainWindow", "GRUPO"))
        self.combo_Classifica.setItemText(4, _translate("MainWindow", "CATEGORIA"))
        self.combo_Classifica.setItemText(5, _translate("MainWindow", "ESTABELECIMENTO"))
        self.combo_Classifica.setItemText(6, _translate("MainWindow", "CIDADE"))
        self.btn_Consulta.setText(_translate("MainWindow", "Consultar"))
        self.label_5.setText(_translate("MainWindow", "Lista de Despesas Mensal/Anual"))
        item = self.table_Lista.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "DATA"))
        item = self.table_Lista.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "BANCO"))
        item = self.table_Lista.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "CATEGORIA"))
        item = self.table_Lista.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "SAÍDA"))
        item = self.table_Lista.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "ESTABEL."))
        item = self.table_Lista.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "CIDADE"))
        item = self.table_Lista.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "OBS"))
        self.label_18.setText(_translate("MainWindow", "Total:"))
        self.label_6.setText(_translate("MainWindow", "Gráfico Despesas Total"))
        self.label_20.setText(_translate("MainWindow", "Total:"))
