import os
import sys
import threading
from importlib import reload
from concurrent import futures

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMessageBox, QFileDialog

import functions
from se import UiMainWindow
from geneinfo import Ui_MainWindow1
from search import Ui_MainWindow2


# TODO
# 1) add comments
# 2) close search/show window if another is open - DONE
# 3) Which genes are infected?


# main class that displays main window and calls sidebar
class MainGui(UiMainWindow):

    # for show sidebar
    sw = None
    side_bar = None
    is_show_all_open = 0
    side_bar_data = ""

    # for search bar
    sb = None
    search_bar = None
    is_search_open = 0

    def __init__(self):
        super().__init__()
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow1()
        self.installEventFilter(self)

        self.check = QIcon('images\\check.png')
        self.cross = QIcon('images\\cross.png')
        self.view = QIcon('images\\view.png')
        self.hide = QIcon('images\\hide.png')
        self.find = QIcon('images\\search.png')

        self.gene_seq_file = ''
        self.gene_list_file = ''

    def setupUi(self, mw):
        super().setupUi(mw)

        self.show.setIcon(self.view)
        self.search_btn.setIcon(self.find)

        self.search_btn.clicked.connect(self.open_search)
        self.show.clicked.connect(self.open_side_bar)

        self.glist_btn.clicked.connect(self.open_gene_list)
        self.gseq_btn.clicked.connect(self.open_gene_seq_file)

        self.merge_btn.clicked.connect(self.merge_data)
        self.upload_btn.clicked.connect(self.upload_to_db)

        # to check if upload.txt exists:
        # if YES then enable sidebar button
        # else turn it off
        try:
            with open(os.path.expanduser("~\\Desktop\\upload.txt"), "r") as fp:
                pass
            functions.format_data()

        except FileNotFoundError:
            self.show.setDisabled(True)

        self.verify_label.hide()
        self.upload_btn.setDisabled(True)
        self.merge_btn.setDisabled(True)

        # TODO
        # perform some task before quiting
        # not working
        finish = QAction("Quit", self)
        finish.triggered.connect(self.closeEvent)

    # this function opens OPEN File Dialog to take GeneSeq file as input and it:
    # verifies it, and creates intermediate files
    def open_gene_seq_file(self):
        self.verify_label.hide()

        options = QFileDialog.Options()
        result, _ = QFileDialog.getOpenFileName(None, "Select GeneSequence File", os.path.expanduser("~\\Desktop"),
                                                "All Files (*);;Text Files (*. txt)", options=options)

        # if file is not selected
        if not result:
            return

        # store filename for future references
        self.gene_seq_file = result

        # if selected file is invalid
        extension = str(result).split('.')
        if extension[1] != "txt":
            QMessageBox.critical(None, 'Error', 'Please choose a text(.txt) file', QMessageBox.Ok)
            self.gseq_btn.setText('Invalid File!')
            self.gseq_btn.setIcon(self.cross)
            return

        # else
        file_name = extension[0].split('/')
        self.gseq_btn.setText(file_name[len(file_name) - 1][:9] + ".txt")
        self.gseq_btn.setIcon(self.check)
        functions.show_loading(self)

        gene_data = os.path.expanduser("~\\Desktop\\gene_data.txt")

        # process the gene data
        flag = functions.process_gene_seq(result, gene_data)

        if flag == 1:
            button_reply = QMessageBox.question(None, 'Message', "Fasta File validation completed. No errors "
                                                                 "were 'found.\nDo you want to open File "
                                                                 "Location?", QMessageBox.Yes | QMessageBox.No,
                                                QMessageBox.No)
            if button_reply == QMessageBox.Yes:
                os.startfile(gene_data)

            functions.calc_agtc()

            self.show.setEnabled(True)
            self.upload_btn.setEnabled(True)
        else:
            QMessageBox.critical(None, 'ERROR', "File validation completed. File format is not correct!\nLine: "
                                 + str(flag - 1), QMessageBox.Ok, QMessageBox.Ok)

            os.remove(gene_data)
            # self.gseq_btn.setText("Upload")
            self.gseq_btn.setText('Invalid File!')
            self.gseq_btn.setIcon(self.cross)

        functions.stop_loading(self)
        self.verify_label.hide()

    pass

    # this function opens OPEN File Dialog to take GeneList file as input and it:
    def open_gene_list(self):
        self.verify_label.hide()

        options = QFileDialog.Options()
        result, _ = QFileDialog.getOpenFileName(None, "Select GeneList File", os.path.expanduser("~\\Desktop"),
                                                "All Files (*);;Text Files (*. txt)", options=options)

        # if file is not selected
        if not result:
            return

        # if selected file is invalid
        extension = str(result).split('.')
        if extension[1] != "txt":
            QMessageBox.critical(None, 'Error', 'Please choose a text(.txt) file', QMessageBox.Ok, QMessageBox.Ok)
            return

        # print(result)

        # else

        # store filename for future references
        self.gene_list_file = result
        file_name = extension[0].split('/')
        self.glist_btn.setText(file_name[len(file_name) - 1][:9] + ".txt")

        self.merge_btn.setEnabled(True)
        self.verify_label.hide()

        pass

    # merge both file contents based on some common fields
    def merge_data(self):

        functions.show_loading(self)
        thread1 = threading.Thread(target=functions.process_merge_data, args=(self.gene_list_file, self,))
        thread1.start()
        # thread1.join()
        return
        pass

    # finally, upload the file into the database
    def upload_to_db(self):

        fp = open(os.path.expanduser("~\\Desktop\\upload.txt"), 'r')
        if not fp:
            QMessageBox.critical(None, 'ERROR', "Please upload GeneSequence.txt again", QMessageBox.Ok, QMessageBox.Ok)
            return

        functions.show_loading(self)

        fp.readline()

        # import cx_Oracle
        # from db import con, cur
        try:
            import db
            db = reload(db)
        except cx_Oracle.DatabaseError:
            QMessageBox.critical(None, 'ERROR', "Something went wrong! Could not connect to the database",
                                 QMessageBox.Ok, QMessageBox.Ok)
            return

        import threading
        thread1 = threading.Thread(target=functions.process_upload_to_db, args=(fp, db.con, db.cur,))
        thread1.start()

        thread2 = threading.Thread(target=self.dummy, args=(thread1,))
        thread2.start()

    # displays how many records have been uploaded to the database
    def dummy(self, thread1):
        thread1.join()

        from functions import q
        flag = q.get()

        if flag == -1:
            self.verify_label.setText('Duplicate entries! Only ' + str(q.get()) + ' records were added.')

        else:
            self.verify_label.setText('All records were added successfully | ' + str(q.get()))

        functions.stop_loading(self)
        self.upload_btn.setDisabled(True)
        return
        pass

    def closeEvent(self, event):
        print('Exiting........................')
        close = QMessageBox.question(None,
                                     "QUIT",
                                     "Sure?",
                                     QMessageBox.Yes | QMessageBox.No)
        if close == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def open_side_bar(self):
        self.verify_label.hide()
        if not self.is_show_all_open:
            self.side_bar = QtWidgets.QMainWindow()
            self.sw = OpenSideBar(self.side_bar)
            self.side_bar.show()
            # self.show.setText('<<')
            self.show.setIcon(self.hide)
            self.is_show_all_open = 1

            if self.is_search_open:
                self.is_search_open = 0
                self.search_bar.close()

        else:
            self.is_show_all_open = 0
            self.side_bar.close()
            # self.show.setText('>>')
            self.show.setIcon(self.view)
    
    def open_search(self):
        self.verify_label.hide()
        if not self.is_search_open:
            self.search_bar = QtWidgets.QMainWindow()
            self.sb = SearchMenu(self.search_bar)
            self.search_bar.show()
            self.is_search_open = 1

            if self.is_show_all_open:
                self.is_show_all_open = 0
                self.side_bar.close()

        else:
            self.is_search_open = 0
            self.search_bar.close()


# geneinfo.py functionality
class OpenSideBar(Ui_MainWindow1):
    def __init__(self, side_bar):
        Ui_MainWindow1.__init__(self)
        self.setupUi1(side_bar)

    def setupUi1(self, mw):
        super().setupUi1(mw)

        try:
            with open(os.path.expanduser("~\\Desktop\\upload.txt"), 'r') as fp:
                pass

        except FileNotFoundError:
            QMessageBox.information(MainWindow, 'Error', 'Make sure upload.txt is on desktop',
                                    QMessageBox.Ok, QMessageBox.Ok)
            return

        functions.populate_tb(self)


# search bar
class SearchMenu(Ui_MainWindow2):
    def __init__(self, side_bar):
        Ui_MainWindow2.__init__(self)
        self.s_icon = QIcon('images\\search.png')
        self.setupUi2(side_bar)

    def setupUi2(self, mw):
        super().setupUi2(mw)

        self.search_btn.setIcon(self.s_icon)
        self.search_btn.clicked.connect(self.find)

        self.doubleSpinBox1.setSingleStep(0.1)
        self.doubleSpinBox2.setSingleStep(0.1)

    def find(self):
        checked = 0
        st = ''
        res = []

        if self.nc_val_radio_btn.isChecked():
            self.first = self.doubleSpinBox1.value()
            self.last = self.doubleSpinBox2.value()

            if self.first > self.last:
                self.textEdit.setText('Invalid search parameters')
                return

            st = "select * from GENOME_DATA where " \
                 "nc >= '" + str(self.first) + "' and nc <= '" + str(self.last) + "' order by serial"
            checked = 1

        if self.infected_radio_btn.isChecked():
            # self.textEdit.setText('infected')
            st = "select * from GENOME_DATA where location = '-' order by serial"
            checked = 1

        if checked == 1:
            res = functions.fetch_results(st)
            functions.display_search_results(self, res)
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MainGui()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
