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


#TO-DO
# add comments


class MainGui(UiMainWindow):
    # for sidebar
    sw = None
    side_bar = None
    is_open = 0

    def __init__(self):
        super().__init__()
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow1()
        self.installEventFilter(self)

        self.check = QIcon('images\\check.png')
        self.cross = QIcon('images\\cross.png')

        self.gene_seq_file = ''
        self.gene_list_file = ''

    def setupUi(self, mw):
        super().setupUi(mw)

        self.show.clicked.connect(self.open_side_bar)

        self.glist_btn.clicked.connect(self.open_gene_list)
        self.gseq_btn.clicked.connect(self.open_gene_seq_file)

        self.upload_btn.clicked.connect(self.upload_to_db)
        self.merge_btn.clicked.connect(self.merge_data)

        fp = open(os.path.expanduser("~\\Desktop\\upload.txt"), "r")

        if not fp:
            self.show.setDisabled(True)

        self.verify_label.hide()
        self.upload_btn.setDisabled(True)
        self.merge_btn.setDisabled(True)

        # perform some task before quiting
        # not working
        finish = QAction("Quit", self)
        finish.triggered.connect(self.closeEvent)

    def open_gene_seq_file(self):

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
        # print(flag)

        if flag == 1:
            button_reply = QMessageBox.question(None, 'Message', "Fasta File validation completed. No errors "
                                                                 "were 'found.\nDo you want to open File "
                                                                 "Location?", QMessageBox.Yes | QMessageBox.No,
                                                QMessageBox.No)
            if button_reply == QMessageBox.Yes:
                os.startfile(gene_data)

            functions.calc_agtc()

            # self.upload_btn.show()
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

    pass

    def open_gene_list(self):

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

        print(result)

        # else

        # store filename for future references
        self.gene_list_file = result
        file_name = extension[0].split('/')
        self.glist_btn.setText(file_name[len(file_name) - 1][:9] + ".txt")

        self.merge_btn.setEnabled(True)

        pass

    def merge_data(self):

        functions.show_loading(self)
        thread1 = threading.Thread(target=functions.process_merge_data, args=(self .gene_list_file, self,))
        thread1.start()
        # thread1.join()
        return
        pass

    def upload_to_db(self):

        fp = open(os.path.expanduser("~\\Desktop\\upload.txt"), 'r')
        if not fp:
            QMessageBox.critical(None, 'ERROR', "Please upload GeneSequence.txt again", QMessageBox.Ok, QMessageBox.Ok)
            return

        fp.readline()

        # from db import con, cur
        import db
        db = reload(db)
        # import cx_Oracle
        # con = cx_Oracle.connect('system/AmanVerma22@localhost/verma')

        if not db.con:
            QMessageBox.critical(None, 'ERROR', "Something went wrong! Could not connect to the database",
                                 QMessageBox.Ok, QMessageBox.Ok)
            return

        # cur = con.cursor()

        # flag = 0
        # import threading
        # thread1 = threading.Thread(target=functions.process_upload_to_db, args=(fp, db.con, db.cur, self,))
        # thread1.start()

        executor = futures.ThreadPoolExecutor(max_workers=1)
        future = executor.submit(functions.process_upload_to_db, fp, db.con, db.cur, self)
        functions.show_loading(self)
        # print(future.result())
        # flag = functions.process_upload_to_db(fp, con, cur)

        # choice = QMessageBox.question(None, 'Upload GeneList', 'Do you want to upload GeneList.txt while records are'
        #                                                        ' being uploaded to the database?',
        #                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        #
        # if choice == QMessageBox.Yes:
        #     self.open_gene_list()

        # thread1.join()

        flag = future.result()
        if flag == -1:
            QMessageBox.critical(None, 'Database Error',
                                 'Duplicate Entries are not allowed\n\nNone of the records were added.',
                                 QMessageBox.Ok, QMessageBox.Ok)

        elif flag == -2:
            QMessageBox.critical(None, 'Database Error',
                                 'Something went wrong in the database!\nNone of the records were added.',
                                 QMessageBox.Ok, QMessageBox.Ok)
        else:
            QMessageBox.information(None, 'Database Updated',
                                    str(flag - 1) + ' records have been added to the database',
                                    QMessageBox.Ok, QMessageBox.Ok)

        functions.stop_loading(self)
        self.upload_btn.setDisabled(True)
        # return
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

        if not self.is_open:
            self.side_bar = QtWidgets.QMainWindow()
            self.sw = OpenSideBar(self.side_bar)
            self.side_bar.show()
            self.show.setText('<<')
            self.is_open = 1
        else:

            self.is_open = 0
            self.side_bar.close()
            self.show.setText('>>')


# geneinfo.py functionality
class OpenSideBar(Ui_MainWindow1):
    def __init__(self, side_bar):
        Ui_MainWindow1.__init__(self)
        self.setupUi1(side_bar)

    def setupUi1(self, mw):
        super().setupUi1(mw)
        functions.populate_tb(self, mw)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MainGui()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
