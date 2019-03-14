import os
import re
import queue
import textwrap
import cx_Oracle
import amino_acids
from importlib import reload


# from PyQt5.QtWidgets import QMessageBox


# processes gene sequence file and write its content in an
# organized manner into a new file, which is then processed by
# calc_agtc()
from PyQt5.QtWidgets import QMessageBox

q = queue.Queue()


def show_loading(self):
    self.verify_label.show()
    self.loading.show()
    self.movie.start()
    self.upload_btn.setDisabled(True)
    self.merge_btn.setDisabled(True)
    self.gseq_btn.setDisabled(True)
    self.glist_btn.setDisabled(True)


def stop_loading(self):
    self.movie.stop()
    self.loading.hide()
    self.verify_label.hide()
    self.gseq_btn.setEnabled(True)
    self.glist_btn.setEnabled(True)
    # self.upload_btn.setEnabled(True)


def process_gene_seq(result, gene_data):
    i = 0
    flag = 0
    count = 1
    buff = ""
    info_line = 0

    # open file and read one line at a time
    with open(result, 'r') as fp:

        nf = open(gene_data, 'w')

        for line in fp:
            i = i + 1
            # check if line is information line
            if line[0] == '>':
                # if information line is repeated
                if info_line == 1:
                    flag = 0
                    break

                # update buffer
                buff = "\n" + str(count) + "\t"
                buff += line[1:].rstrip() + "\t"

                # true case; all OK
                flag = 1
                count += 1
                info_line = 1

            # gene sequence processing
            else:
                info_line = 0
                # check if line contains something
                # other than ATGC
                if bool(re.match('^[ATGC]+$', line)):
                    flag = 1
                    buff += line.rstrip()
                # if something else it found, exit!
                else:
                    flag = 0
                    break

            # write data to new file
            nf.write(buff)
            del buff
            buff = ""

        fp.close()
        nf.close()

    # print(flag)
    if flag:
        i = 0
    else:
        i += 1
    q.put(flag + i)
    return flag + i
    pass


# provides additional data to be uploaded into the db
# but first it writes it into upload.txt
def calc_agtc():
    with open(os.path.expanduser("~\\Desktop\\gene_data.txt"), 'r') as fp:
        # intermediate file generated for uploading to DataBase
        nf = open(os.path.expanduser("~\\Desktop\\upload.txt"), 'w')

        nf.write("S.No.\tInformation Line\tGene Sequence\tLength of Gene Sequence\t Count of A\tCount of T\tCount "
                 "of G\tCount of C\tGC%\n")
        fp.readline()

        for line in fp:

            token = line.split('\t')
            gene_seq = token[len(token) - 1]
            length = len(gene_seq) - 1
            count_a = gene_seq.count('A')
            count_t = gene_seq.count('T')
            count_g = gene_seq.count('G')
            count_c = gene_seq.count('C')

            gc_per = (count_g + count_c) / (count_a + count_t + count_g + count_c)
            gc_per = round(gc_per, 3)

            nf.write(line.rstrip() + "\t" + str(length) + "\t" + str(count_a) + "\t" + str(count_t) + "\t" +
                     str(count_g) + "\t" + str(count_c) + "\t" + str(gc_per) + "\n")

        fp.close()
        nf.close()
    pass


# this function will return the file data in an organized way
# so that it can be uploaded to database
def process_open_gene_list(result):

    pass


# this module uploads data into the database
# --contents of upload.txt--
def process_upload_to_db(fp, con, cur, self):
    # i = 1
    rows = []
    c_flag = 0
    final_loc = ''

    # extract location and add into database
    for line in fp:
        token = line.split('\t')
        # print(token)
        # # print(">" + token[len(token) - 2])
        loc = token[1].split(':')
        loc = loc[len(loc) - 1].split(' ')
        # print(loc)
        # multiple
        if len(loc[0].split(',')) > 1:
            final_loc = '-'
        else:
            if 'c' in loc[0]:
                loc[0] = loc[0][1:]
                c_flag = 1
            loc = loc[0]
            loc = loc.split('-')
            if c_flag:
                start = loc[len(loc) - 1]
                end = loc[0]
            else:
                start = loc[0]
                end = loc[len(loc) - 1]
            final_loc = start + ".." + end
            c_flag = 0
        # print(final_loc)

        # insert the data into the db
        if len(token[2]) > 4000:
            buff_1 = token[2][0:3998]
            buff_2 = token[2][3998:7998]
        else:
            buff_1 = token[2]
            buff_2 = ""

        buff = (buff_1.rstrip()).lstrip() + (buff_2.rstrip()).lstrip()
        amino_seq = calc_amino_acid(buff)

        temp = float(token[8])
        temp = round(temp, 3)

        row = (str(token[0]), str(final_loc), str(token[1]), str(buff_1), str(buff_2), str(token[3]), str(token[4]),
               str(token[5]), str(token[6]), str(token[7]), str(temp), amino_seq)

        rows.append(row)

        del buff_2
        del buff_1

    st = 'insert into GENOME_DATA(serial, location, genome_info, genome_seq_no, genome_seq_no2, length, count_a, ' \
         'count_t, count_g, count_c, gc_percentage, amino_acid) ' \
         'values (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12)'

    # a = se.UiMainWindow()

    try:
        cur.prepare(st)
        cur.executemany(None, rows)

    except cx_Oracle.IntegrityError:
        flag = -1
        print("Duplicate entries")

    except:
        flag = -2

    else:

        flag = 1
        flag = flag + cur.rowcount
        con.commit()
        print("Total Records Uploaded: " + str(flag - 1))

    finally:
        cur.close()
        con.close()

    return flag
    pass


# this function returns equivalent amino acid seq for
# given gene sequence
def calc_amino_acid(gene_seq):
    wrapper = textwrap.TextWrapper(width=3)
    f = wrapper.fill(text=gene_seq)
    my = f.split('\n')
    final = ''

    for term in my:
        if (len(gene_seq)) % 3 == 0:
            final = final + amino_acids.acids[term]

        pass
    final.rstrip()
    return final
    pass


# this module updates data of the database
# adds fields of GeneList.txt into records of database
def process_merge_data(gene_list_file, self):

    try:
        file = open(gene_list_file, 'r').read().split('\n')
    except FileNotFoundError:
        QMessageBox.critical(None, 'Error', 'File not found. Please upload GeneList file first',
                             QMessageBox.Ok, QMessageBox.Ok)
        return

    import db
    db = reload(db)

    rows = []
    st = ''
    for line in file:
        tokens = line.split('\t')
        if len(tokens) == 9:
            # print(tokens[0] +
            # tokens[1] + tokens[2] + tokens[3] + tokens[4] + tokens[5] + tokens[6] + tokens[7] + tokens[8])
            tokens.append(tokens[0])
            tokens.pop(0)
            rows.append(tokens)
            # print(tokens)
            st = 'update GENOME_DATA set strand = :1, len = :2,  pid = :3, gene = :4, synonym1 = :5, code = :6, ' \
                 'cog = :7, product = :8 where location = :9'

            # db.cur.execute(st, {'1': tokens[0], '2': tokens[1], '3': tokens[2], '4': tokens[3], '5': tokens[4],
            #                     '6': tokens[5], '7': tokens[6], '8': tokens[7], '9': tokens[8]})
    try:
        db.cur.prepare(st)
        db.cur.executemany(None, rows)
        db.con.commit()
        print('Done')
    except:
        flag = -1
        print("Update Error")
        return -1
    finally:
        db.cur.close()
        db.con.close()
        stop_loading(self)
    pass


def populate_tb(self, MainWindow):
    buff = ""
    fp = open(os.path.expanduser("~\\Desktop\\upload.txt"), 'r')
    if not fp:
        QMessageBox.information(MainWindow, 'Error', 'Make sure upload.txt is on desktop',
                                QMessageBox.Ok, QMessageBox.Ok)
        fp.close()
        return

    fp.readline()
    buff = '{:30}'.format("S.No.") + '{:^115}'.format("Info Line") + '{:^10}'.format("Length") + \
           '{:^10}'.format("A") + '{:^10}'.format("T") + '{:^10}'.format("G") + \
           '{:^10}'.format("C") + '{:^10}'.format("GC%") + "\n--------------------------------------------------" \
                                                           "----------------------------------------------------" \
                                                           "----------------------------------------------------" \
                                                           "--------------------------\n "

    for line in fp:
        token = line.split('\t')
        buff = "{0}{1}{2}{3}{4}{5}{6}{7}{8}\n--------------------------------------------------------------------" \
               "-------------------------------------------------------------------------------------------------" \
               "---------------".format(buff, '{:10}'.format(token[0]), '{:90}'.format(token[1][:87]),
                                        '{:^12}'.format(token[3]), '{:10}'.format(token[4]),
                                        '{:10}'.format(token[5]), '{:10}'.format(token[6]),
                                        '{:10}'.format(token[7]), '{:10}'.format(token[8]))
        # print(buff)
    self.textEdit.setText(buff)
    del buff
    fp.close()
    pass

def display_error(self):
    QMessageBox.critical(None, 'Error', 'Duplicate Entries are not allowed', QMessageBox.Ok, QMessageBox.Ok)
