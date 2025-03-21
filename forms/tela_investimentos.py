# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tela_investimentos.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(884, 501)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setMinimumSize(QtCore.QSize(0, 50))
        self.widget.setMaximumSize(QtCore.QSize(16777215, 50))
        self.widget.setStyleSheet("background-color: rgb(172, 172, 172);")
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(15, 5, 15, 5)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setMinimumSize(QtCore.QSize(60, 0))
        self.label_4.setMaximumSize(QtCore.QSize(60, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.line_Num = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_Num.sizePolicy().hasHeightForWidth())
        self.line_Num.setSizePolicy(sizePolicy)
        self.line_Num.setMinimumSize(QtCore.QSize(95, 25))
        self.line_Num.setMaximumSize(QtCore.QSize(95, 25))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.line_Num.setFont(font)
        self.line_Num.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.line_Num.setInputMask("")
        self.line_Num.setText("")
        self.line_Num.setFrame(True)
        self.line_Num.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.line_Num.setAlignment(QtCore.Qt.AlignCenter)
        self.line_Num.setDragEnabled(False)
        self.line_Num.setPlaceholderText("")
        self.line_Num.setObjectName("line_Num")
        self.horizontalLayout.addWidget(self.line_Num)
        self.label_titulo = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_titulo.setFont(font)
        self.label_titulo.setAlignment(QtCore.Qt.AlignCenter)
        self.label_titulo.setObjectName("label_titulo")
        self.horizontalLayout.addWidget(self.label_titulo)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setMinimumSize(QtCore.QSize(70, 0))
        self.label.setMaximumSize(QtCore.QSize(70, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.date_Emissao = QtWidgets.QDateEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.date_Emissao.sizePolicy().hasHeightForWidth())
        self.date_Emissao.setSizePolicy(sizePolicy)
        self.date_Emissao.setMinimumSize(QtCore.QSize(90, 25))
        self.date_Emissao.setMaximumSize(QtCore.QSize(90, 25))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.date_Emissao.setFont(font)
        self.date_Emissao.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.date_Emissao.setObjectName("date_Emissao")
        self.horizontalLayout.addWidget(self.date_Emissao)
        self.verticalLayout.addWidget(self.widget)
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setObjectName("widget_2")
        self.gridLayout = QtWidgets.QGridLayout(self.widget_2)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName("gridLayout")
        self.widget_3 = QtWidgets.QWidget(self.widget_2)
        self.widget_3.setMinimumSize(QtCore.QSize(350, 0))
        self.widget_3.setMaximumSize(QtCore.QSize(350, 16777215))
        self.widget_3.setObjectName("widget_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget_3)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setHorizontalSpacing(0)
        self.gridLayout_2.setVerticalSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.widget_6 = QtWidgets.QWidget(self.widget_3)
        self.widget_6.setMinimumSize(QtCore.QSize(0, 50))
        self.widget_6.setMaximumSize(QtCore.QSize(16777215, 50))
        self.widget_6.setStyleSheet("background-color: rgb(172, 172, 172);")
        self.widget_6.setObjectName("widget_6")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_6)
        self.horizontalLayout_2.setContentsMargins(15, 5, 15, 5)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_Limpar = QtWidgets.QPushButton(self.widget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_Limpar.sizePolicy().hasHeightForWidth())
        self.btn_Limpar.setSizePolicy(sizePolicy)
        self.btn_Limpar.setMinimumSize(QtCore.QSize(90, 30))
        self.btn_Limpar.setMaximumSize(QtCore.QSize(90, 30))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.btn_Limpar.setFont(font)
        self.btn_Limpar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_Limpar.setObjectName("btn_Limpar")
        self.horizontalLayout_2.addWidget(self.btn_Limpar)
        self.label_3 = QtWidgets.QLabel(self.widget_6)
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.btn_Salvar = QtWidgets.QPushButton(self.widget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_Salvar.sizePolicy().hasHeightForWidth())
        self.btn_Salvar.setSizePolicy(sizePolicy)
        self.btn_Salvar.setMinimumSize(QtCore.QSize(90, 30))
        self.btn_Salvar.setMaximumSize(QtCore.QSize(90, 30))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.btn_Salvar.setFont(font)
        self.btn_Salvar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_Salvar.setObjectName("btn_Salvar")
        self.horizontalLayout_2.addWidget(self.btn_Salvar)
        self.gridLayout_2.addWidget(self.widget_6, 1, 0, 1, 1)
        self.widget_5 = QtWidgets.QWidget(self.widget_3)
        self.widget_5.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.widget_5.setStyleSheet("background-color: rgb(172, 172, 172);")
        self.widget_5.setObjectName("widget_5")
        self.formLayout = QtWidgets.QFormLayout(self.widget_5)
        self.formLayout.setContentsMargins(10, 10, 10, 10)
        self.formLayout.setSpacing(10)
        self.formLayout.setObjectName("formLayout")
        self.label_titulo_2 = QtWidgets.QLabel(self.widget_5)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_titulo_2.setFont(font)
        self.label_titulo_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_titulo_2.setObjectName("label_titulo_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.label_titulo_2)
        self.label_16 = QtWidgets.QLabel(self.widget_5)
        self.label_16.setMinimumSize(QtCore.QSize(75, 0))
        self.label_16.setMaximumSize(QtCore.QSize(75, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_16)
        self.combo_Banco = QtWidgets.QComboBox(self.widget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_Banco.sizePolicy().hasHeightForWidth())
        self.combo_Banco.setSizePolicy(sizePolicy)
        self.combo_Banco.setMinimumSize(QtCore.QSize(0, 23))
        self.combo_Banco.setMaximumSize(QtCore.QSize(16777215, 23))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.combo_Banco.setFont(font)
        self.combo_Banco.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.combo_Banco.setObjectName("combo_Banco")
        self.combo_Banco.addItem("")
        self.combo_Banco.setItemText(0, "")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.combo_Banco)
        self.label_10 = QtWidgets.QLabel(self.widget_5)
        self.label_10.setMinimumSize(QtCore.QSize(75, 0))
        self.label_10.setMaximumSize(QtCore.QSize(75, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.combo_Tipo = QtWidgets.QComboBox(self.widget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_Tipo.sizePolicy().hasHeightForWidth())
        self.combo_Tipo.setSizePolicy(sizePolicy)
        self.combo_Tipo.setMinimumSize(QtCore.QSize(0, 23))
        self.combo_Tipo.setMaximumSize(QtCore.QSize(16777215, 23))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.combo_Tipo.setFont(font)
        self.combo_Tipo.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.combo_Tipo.setObjectName("combo_Tipo")
        self.combo_Tipo.addItem("")
        self.combo_Tipo.setItemText(0, "")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.combo_Tipo)
        self.label_15 = QtWidgets.QLabel(self.widget_5)
        self.label_15.setMinimumSize(QtCore.QSize(0, 0))
        self.label_15.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_15)
        self.label_Saldo = QtWidgets.QLabel(self.widget_5)
        self.label_Saldo.setMinimumSize(QtCore.QSize(0, 23))
        self.label_Saldo.setMaximumSize(QtCore.QSize(16777215, 23))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_Saldo.setFont(font)
        self.label_Saldo.setText("")
        self.label_Saldo.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_Saldo.setObjectName("label_Saldo")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.label_Saldo)
        self.label_12 = QtWidgets.QLabel(self.widget_5)
        self.label_12.setMinimumSize(QtCore.QSize(75, 0))
        self.label_12.setMaximumSize(QtCore.QSize(75, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_12)
        self.combo_Categoria = QtWidgets.QComboBox(self.widget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_Categoria.sizePolicy().hasHeightForWidth())
        self.combo_Categoria.setSizePolicy(sizePolicy)
        self.combo_Categoria.setMinimumSize(QtCore.QSize(0, 23))
        self.combo_Categoria.setMaximumSize(QtCore.QSize(16777215, 23))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.combo_Categoria.setFont(font)
        self.combo_Categoria.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.combo_Categoria.setObjectName("combo_Categoria")
        self.combo_Categoria.addItem("")
        self.combo_Categoria.setItemText(0, "")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.combo_Categoria)
        self.label_13 = QtWidgets.QLabel(self.widget_5)
        self.label_13.setMinimumSize(QtCore.QSize(130, 0))
        self.label_13.setMaximumSize(QtCore.QSize(130, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_13)
        self.line_Valor = QtWidgets.QLineEdit(self.widget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_Valor.sizePolicy().hasHeightForWidth())
        self.line_Valor.setSizePolicy(sizePolicy)
        self.line_Valor.setMinimumSize(QtCore.QSize(0, 23))
        self.line_Valor.setMaximumSize(QtCore.QSize(16777215, 23))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.line_Valor.setFont(font)
        self.line_Valor.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.line_Valor.setText("")
        self.line_Valor.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.line_Valor.setObjectName("line_Valor")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.line_Valor)
        self.label_14 = QtWidgets.QLabel(self.widget_5)
        self.label_14.setMinimumSize(QtCore.QSize(75, 0))
        self.label_14.setMaximumSize(QtCore.QSize(75, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_14)
        self.combo_Estab = QtWidgets.QComboBox(self.widget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_Estab.sizePolicy().hasHeightForWidth())
        self.combo_Estab.setSizePolicy(sizePolicy)
        self.combo_Estab.setMinimumSize(QtCore.QSize(0, 23))
        self.combo_Estab.setMaximumSize(QtCore.QSize(16777215, 23))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.combo_Estab.setFont(font)
        self.combo_Estab.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.combo_Estab.setObjectName("combo_Estab")
        self.combo_Estab.addItem("")
        self.combo_Estab.setItemText(0, "")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.combo_Estab)
        self.label_28 = QtWidgets.QLabel(self.widget_5)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_28.setFont(font)
        self.label_28.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_28.setObjectName("label_28")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_28)
        self.plain_Obs = QtWidgets.QPlainTextEdit(self.widget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plain_Obs.sizePolicy().hasHeightForWidth())
        self.plain_Obs.setSizePolicy(sizePolicy)
        self.plain_Obs.setMinimumSize(QtCore.QSize(0, 100))
        self.plain_Obs.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.plain_Obs.setFont(font)
        self.plain_Obs.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.plain_Obs.setObjectName("plain_Obs")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.plain_Obs)
        self.gridLayout_2.addWidget(self.widget_5, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.widget_3, 0, 0, 1, 1)
        self.widget_4 = QtWidgets.QWidget(self.widget_2)
        self.widget_4.setStyleSheet("background-color: rgb(172, 172, 172);")
        self.widget_4.setObjectName("widget_4")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget_4)
        self.gridLayout_3.setContentsMargins(10, 5, 10, 5)
        self.gridLayout_3.setSpacing(5)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_7 = QtWidgets.QLabel(self.widget_4)
        self.label_7.setMinimumSize(QtCore.QSize(0, 0))
        self.label_7.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_7.setText("")
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 0, 2, 1, 2)
        self.label_5 = QtWidgets.QLabel(self.widget_4)
        self.label_5.setMinimumSize(QtCore.QSize(0, 25))
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 3, 0, 1, 4)
        self.label_9 = QtWidgets.QLabel(self.widget_4)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 0, 0, 1, 1)
        self.combo_Consulta_Categoria = QtWidgets.QComboBox(self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_Consulta_Categoria.sizePolicy().hasHeightForWidth())
        self.combo_Consulta_Categoria.setSizePolicy(sizePolicy)
        self.combo_Consulta_Categoria.setMinimumSize(QtCore.QSize(250, 25))
        self.combo_Consulta_Categoria.setMaximumSize(QtCore.QSize(250, 25))
        self.combo_Consulta_Categoria.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.combo_Consulta_Categoria.setObjectName("combo_Consulta_Categoria")
        self.combo_Consulta_Categoria.addItem("")
        self.combo_Consulta_Categoria.setItemText(0, "")
        self.gridLayout_3.addWidget(self.combo_Consulta_Categoria, 0, 1, 1, 1)
        self.table_Lista = QtWidgets.QTableWidget(self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table_Lista.sizePolicy().hasHeightForWidth())
        self.table_Lista.setSizePolicy(sizePolicy)
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
        self.gridLayout_3.addWidget(self.table_Lista, 4, 0, 1, 4)
        self.gridLayout.addWidget(self.widget_4, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.widget_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.combo_Banco, self.combo_Tipo)
        MainWindow.setTabOrder(self.combo_Tipo, self.btn_Salvar)
        MainWindow.setTabOrder(self.btn_Salvar, self.line_Num)
        MainWindow.setTabOrder(self.line_Num, self.btn_Limpar)
        MainWindow.setTabOrder(self.btn_Limpar, self.date_Emissao)
        MainWindow.setTabOrder(self.date_Emissao, self.combo_Consulta_Categoria)
        MainWindow.setTabOrder(self.combo_Consulta_Categoria, self.table_Lista)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Movimentação de Entrada"))
        self.label_4.setText(_translate("MainWindow", "Código:"))
        self.label_titulo.setText(_translate("MainWindow", "Entrada de Investimentos"))
        self.label.setText(_translate("MainWindow", "Emissão:"))
        self.btn_Limpar.setText(_translate("MainWindow", "LIMPAR"))
        self.btn_Salvar.setText(_translate("MainWindow", "SALVAR"))
        self.label_titulo_2.setText(_translate("MainWindow", "Dados para Cadastro"))
        self.label_16.setText(_translate("MainWindow", "Banco:"))
        self.label_10.setText(_translate("MainWindow", "Tipo Conta:"))
        self.label_15.setText(_translate("MainWindow", "Saldo:"))
        self.label_12.setText(_translate("MainWindow", "Categoria:"))
        self.label_13.setText(_translate("MainWindow", "R$:"))
        self.label_14.setText(_translate("MainWindow", "Estabel.:"))
        self.label_28.setText(_translate("MainWindow", "Observação:"))
        self.label_5.setText(_translate("MainWindow", "Lista das Últimas Entradas"))
        self.label_9.setText(_translate("MainWindow", "Categoria:"))
        item = self.table_Lista.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "DATA"))
        item = self.table_Lista.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "BANCO"))
        item = self.table_Lista.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "TIPO CONTA"))
        item = self.table_Lista.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "CATEGORIA"))
        item = self.table_Lista.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "VALOR"))
        item = self.table_Lista.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "ESTABEL."))
        item = self.table_Lista.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "OBS"))
