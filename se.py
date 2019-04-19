import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject


# noinspection PyTypeChecker,PyPep8Naming
class UiMainWindow(QObject):

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(421, 618)

        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)

        MainWindow.setFont(font)
        MainWindow.setMouseTracking(False)
        MainWindow.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: rgb(217, 217, 217);")
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow.setWindowIcon(QtGui.QIcon('images\\icon.png'))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # logo
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(0, 4, 111, 111))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap("images\\logo.png"))
        self.logo.setScaledContents(True)
        self.logo.setObjectName("logo")

        # header label
        self.title_label = QtWidgets.QLabel(self.centralwidget)
        self.title_label.setGeometry(QtCore.QRect(116, 14, 301, 31))
        self.title_label.setStyleSheet("font: 28pt \"Exan\";\ncolor: rgb(31, 78, 121);")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setObjectName("title_label")

        # header label
        self.seasgn_label = QtWidgets.QLabel(self.centralwidget)
        self.seasgn_label.setGeometry(QtCore.QRect(120, 54, 301, 51))
        self.seasgn_label.setStyleSheet("font: 75 28pt \"Yu Gothic UI\";\ncolor: rgb(31, 78, 121);")
        self.seasgn_label.setAlignment(QtCore.Qt.AlignCenter)
        self.seasgn_label.setObjectName("seasgn_label")

        # gene_seq label
        self.gseq_label = QtWidgets.QLabel(self.centralwidget)
        self.gseq_label.setGeometry(QtCore.QRect(-10, 220, 201, 31))
        self.gseq_label.setStyleSheet("font: 75 16pt \"Calibri\";")
        self.gseq_label.setScaledContents(False)
        self.gseq_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.gseq_label.setObjectName("gseq_label")

        # gene_list label
        self.glist_label = QtWidgets.QLabel(self.centralwidget)
        self.glist_label.setGeometry(QtCore.QRect(0, 290, 191, 31))
        self.glist_label.setStyleSheet("font: 75 16pt \"Calibri\";")
        self.glist_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.glist_label.setObjectName("glist_label")

        # browse GeneSeq File
        self.gseq_btn = QtWidgets.QPushButton(self.centralwidget)
        self.gseq_btn.setGeometry(QtCore.QRect(230, 220, 141, 31))
        self.gseq_btn.setStyleSheet("background-color: rgb(165, 165, 165);\nfont: 25 12pt \"Calibri\";")
        self.gseq_btn.setDefault(False)
        self.gseq_btn.setFlat(False)
        self.gseq_btn.setObjectName("gseq_btn")

        # browse GeneList File
        self.glist_btn = QtWidgets.QPushButton(self.centralwidget)
        self.glist_btn.setGeometry(QtCore.QRect(230, 290, 141, 31))
        self.glist_btn.setStyleSheet("background-color: rgb(165, 165, 165);\nfont: 25 12pt \"Calibri\";")
        self.glist_btn.setFlat(False)
        self.glist_btn.setObjectName("glist_btn")

        # upload GeneSeq to DB
        self.upload_btn = QtWidgets.QPushButton(self.centralwidget)
        self.upload_btn.setGeometry(QtCore.QRect(60, 400, 141, 31))
        self.upload_btn.setStyleSheet("background-color: rgb(165, 165, 165);\nfont: 25 12pt \"Calibri\";")
        self.upload_btn.setFlat(False)
        self.upload_btn.setObjectName("upload_btn")

        # update db with the contents of GeneList file
        self.merge_btn = QtWidgets.QPushButton(self.centralwidget)
        self.merge_btn.setGeometry(QtCore.QRect(220, 400, 141, 31))
        self.merge_btn.setStyleSheet("background-color: rgb(165, 165, 165);\nfont: 25 12pt \"Calibri\";")
        self.merge_btn.setFlat(False)
        self.merge_btn.setObjectName("merge_btn")

        # button to search sidebar
        self.search_btn = QtWidgets.QPushButton(self.centralwidget)
        self.search_btn.setGeometry(QtCore.QRect(401, 125, 21, 199))
        self.search_btn.setStyleSheet("background-color: rgb(190, 190, 190);\nfont: 12pt \"Candara Light\";")
        self.search_btn.setFlat(True)
        self.search_btn.setObjectName("search")

        # button to display sidebar
        self.show = QtWidgets.QPushButton(self.centralwidget)
        self.show.setGeometry(QtCore.QRect(401, 327, 21, 200))
        self.show.setStyleSheet("background-color: rgb(190, 190, 190);\nfont: 12pt \"Candara Light\";")
        self.show.setFlat(True)
        self.show.setObjectName("show")

        # line_1 after header
        self.line_1 = QtWidgets.QFrame(self.centralwidget)
        self.line_1.setGeometry(QtCore.QRect(0, 108, 421, 31))
        self.line_1.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_1.setLineWidth(2)
        self.line_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_1.setObjectName("line_1")

        # bottom line_1
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(0, 510, 421, 31))
        self.line_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_2.setLineWidth(2)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setObjectName("line_2")

        # line b/w search and show button
        self.button_mid_line = QtWidgets.QFrame(self.centralwidget)
        self.button_mid_line.setGeometry(QtCore.QRect(400, 310, 21, 31))
        self.button_mid_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.button_mid_line.setLineWidth(1)
        self.button_mid_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.button_mid_line.setObjectName("button_mid")

        # line beside show button
        self.show_left_line = QtWidgets.QFrame(self.centralwidget)
        self.show_left_line.setGeometry(QtCore.QRect(390, 127, 20, 395))
        self.show_left_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.show_left_line.setLineWidth(1)
        self.show_left_line.setFrameShape(QtWidgets.QFrame.VLine)
        self.show_left_line.setObjectName("show_left_line")

        # please wait label
        self.verify_label = QtWidgets.QLabel(self.centralwidget)
        self.verify_label.setGeometry(QtCore.QRect(1, 538, 421, 41))
        self.verify_label.setStyleSheet("font: 75 16pt \"Calibri\";")
        self.verify_label.setScaledContents(False)
        self.verify_label.setAlignment(QtCore.Qt.AlignCenter)
        self.verify_label.setObjectName("verify_label")

        # loading gif
        self.loading = QLabel(MainWindow)
        self.movie = QtGui.QMovie("images\\loading.gif")
        self.loading.setMovie(self.movie)
        self.loading.setGeometry(QtCore.QRect(180, 570, 51, 51))

        # resize it to fit in a label
        rect = self.loading.geometry()
        size = QtCore.QSize(min(rect.width(), rect.height()), min(rect.width(), rect.height()))
        self.movie.setScaledSize(size)

        # order is important
        self.line_2.raise_()
        self.line_1.raise_()
        self.verify_label.raise_()
        self.show_left_line.raise_()
        self.button_mid_line.raise_()
        self.logo.raise_()
        self.title_label.raise_()
        self.seasgn_label.raise_()
        self.gseq_label.raise_()
        self.glist_label.raise_()
        self.gseq_btn.raise_()
        self.glist_btn.raise_()
        self.upload_btn.raise_()
        self.merge_btn.raise_()
        self.show.raise_()
        self.search_btn.raise_()

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslate_ui(MainWindow)

        # make it non-resizable
        MainWindow.setFixedSize(MainWindow.size())

    def retranslate_ui(self, mw):
        _translate = QtCore.QCoreApplication.translate
        mw.setWindowTitle(_translate("MainWindow", "BNA"))
        self.title_label.setText(_translate("MainWindow", "BNA"))
        self.seasgn_label.setText(_translate("MainWindow", "SE Assignment"))
        self.gseq_label.setText(_translate("MainWindow", "GeneSequence File:"))
        self.glist_label.setText(_translate("MainWindow", "GeneList File:"))
        self.gseq_btn.setText(_translate("MainWindow", "Upload"))
        self.glist_btn.setText(_translate("MainWindow", "Upload"))
        self.upload_btn.setText(_translate("MainWindow", "Upload to DB"))
        self.merge_btn.setText(_translate("MainWindow", "Merge Both Files"))
        self.verify_label.setText(_translate("MainWindow", "Please Wait"))
        # self.show.setText(_translate("MainWindow", ">>"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
