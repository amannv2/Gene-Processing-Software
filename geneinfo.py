# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\ASUS\Desktop\genedisp.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow1(object):

    def setupUi1(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(681, 376)
        MainWindow.setStyleSheet("background-color: rgb(217, 217, 217);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(0, 0, 750, 370))
        self.textEdit.setObjectName("textEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslate_ui(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setGeometry(QtCore.QRect(1173, 370, 750, 370))
        MainWindow.setFixedSize(MainWindow.size())
        MainWindow.setWindowIcon(QtGui.QIcon('images\\icon.png'))
        self.textEdit.setReadOnly(True)
        # self.populate_tb(MainWindow)

    def retranslate_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Gene Information"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow1()
    ui.setupUi1(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
