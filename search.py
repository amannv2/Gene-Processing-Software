# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\ASUS\Desktop\genedispv2.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow2(object):
    def setupUi2(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(681, 376)
        MainWindow.setStyleSheet("background-color: rgb(217, 217, 217);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(0, 130, 746, 220))
        self.textEdit.setStyleSheet("font: 75 12pt \"Calibri\";")
        self.textEdit.setObjectName("textEdit")

        self.doubleSpinBox1 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox1.setGeometry(QtCore.QRect(367, 18, 62, 23))
        self.doubleSpinBox1.setObjectName("doubleSpinBox1")

        self.doubleSpinBox2 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox2.setGeometry(QtCore.QRect(484, 18, 62, 23))
        self.doubleSpinBox2.setObjectName("doubleSpinBox2")

        self.search_btn = QtWidgets.QPushButton(self.centralwidget)
        self.search_btn.setGeometry(QtCore.QRect(560, 19, 101, 91))
        self.search_btn.setStyleSheet("background-color: rgb(165, 165, 165);\n"
                                      "font: 25 14pt \"Calibri\";")
        self.search_btn.setDefault(False)
        self.search_btn.setFlat(False)
        self.search_btn.setObjectName("search_btn")

        self.nc_val_radio_btn = QtWidgets.QRadioButton(self.centralwidget)
        self.nc_val_radio_btn.setGeometry(QtCore.QRect(27, 19, 531, 17))
        self.nc_val_radio_btn.setStyleSheet("font: 75 16pt \"Calibri\";")
        self.nc_val_radio_btn.setObjectName("nc_val_radio_btn")

        self.infected_radio_btn = QtWidgets.QRadioButton(self.centralwidget)
        self.infected_radio_btn.setGeometry(QtCore.QRect(28, 50, 331, 31))
        self.infected_radio_btn.setStyleSheet("font: 75 16pt \"Calibri\";")
        self.infected_radio_btn.setObjectName("infected_radio_btn")

        self.nc_val_radio_btn.raise_()
        self.textEdit.raise_()
        self.doubleSpinBox1.raise_()
        self.doubleSpinBox2.raise_()
        self.search_btn.raise_()
        self.infected_radio_btn.raise_()

        MainWindow.setGeometry(QtCore.QRect(1173, 370, 750, 370))
        MainWindow.setFixedSize(MainWindow.size())
        MainWindow.setWindowIcon(QtGui.QIcon('images\\icon.png'))
        self.textEdit.setReadOnly(True)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Search"))
        self.search_btn.setText(_translate("MainWindow", "Search"))
        self.nc_val_radio_btn.setText(_translate("MainWindow", "Show records with Nc value between                and"))
        self.infected_radio_btn.setText(_translate("MainWindow", "Show all infected gene records"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow2()
    ui.setupUi2(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
