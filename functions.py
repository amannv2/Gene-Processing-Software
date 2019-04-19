import os
import re
import queue
import textwrap
import threading

import cx_Oracle
import amino_acids
from importlib import reload

from PyQt5.QtWidgets import QMessageBox

q = queue.Queue()


def show_loading(self):
    self.verify_label.setText('Please Wait')
    self.verify_label.show()
    self.loading.show()
    self.movie.start()
    self.upload_btn.setDisabled(True)
    self.merge_btn.setDisabled(True)
    self.gseq_btn.setDisabled(True)
    self.glist_btn.setDisabled(True)
    self.search_btn.setDisabled(True)
    self.show.setDisabled(True)


def stop_loading(self):
    self.movie.stop()
    self.loading.hide()
    # self.verify_label.hide()
    self.gseq_btn.setEnabled(True)
    self.glist_btn.setEnabled(True)
    self.search_btn.setEnabled(True)
    self.show.setEnabled(True)


# processes gene sequence file and write its content in an
# organized manner into a new file, which is then processed by
# calc_agtc()

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

    # init sidebar content
    thread1 = threading.Thread(target=format_data, args=())
    thread1.start()
    # format_data()
    pass


# this module uploads data into the database
# --contents of upload.txt--
def process_upload_to_db(fp, con, cur):
    # i = 1
    rows = []
    c_flag = 0

    # extract location and add into database
    for line in fp:
        token = line.split('\t')
        loc = token[1].split(':')
        loc = loc[len(loc) - 1].split(' ')

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

        # insert the data into the db
        if len(token[2]) > 4000:
            buff_1 = token[2][0:3998]
            buff_2 = token[2][3998:7998]
        else:
            buff_1 = token[2]
            buff_2 = ""

        buff = (buff_1.rstrip()).lstrip() + (buff_2.rstrip()).lstrip()
        amino_seq = calc_amino_acid(buff)
        # for item in codon_count_list:
        calculate_nc(codon_count_list[len(codon_count_list) - 1])
        nc_value = float(nc_list[len(nc_list) - 1])

        temp = float(token[8])
        temp = round(temp, 3)

        row = (str(token[0]), str(final_loc), str(token[1]), str(buff_1), str(buff_2), str(token[3]), str(token[4]),
               str(token[5]), str(token[6]), str(token[7]), str(temp), amino_seq, float(nc_value))

        rows.append(row)

        del buff_2
        del buff_1

    st = 'insert into GENOME_DATA(serial, location, genome_info, genome_seq_no, genome_seq_no2, length, count_a, ' \
         'count_t, count_g, count_c, gc_percentage, amino_acid, nc) ' \
         'values (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13)'

    try:
        cur.prepare(st)
        cur.executemany(None, rows)

    except cx_Oracle.IntegrityError:
        # flag = -1
        while not q.empty():
            q.get()
        q.put(-1)
        q.put(cur.rowcount)
        print("Duplicate entries")

    else:

        # flag = 1
        # flag = flag + cur.rowcount
        q.put(cur.rowcount)
        con.commit()
        print("Total Records Uploaded: " + str(cur.rowcount))

    finally:
        cur.close()
        con.close()

    # print(*nc_list, sep='\n')

    # return flag
    pass


codon_count_list = []


# this function returns equivalent amino acid seq for
# given gene sequence
# AND
# keeps track of codon count for each gene sequence
def calc_amino_acid(gene_seq):
    codon_count = {
        'TTT': 0, 'TTC': 0, 'TTA': 0, 'TTG': 0,
        'TCT': 0, 'TCC': 0, 'TCA': 0, 'TCG': 0,
        'TAT': 0, 'TAC': 0, 'TAA': 0, 'TAG': 0,
        'TGT': 0, 'TGC': 0, 'TGA': 0, 'TGG': 0,
        'CTT': 0, 'CTC': 0, 'CTA': 0, 'CTG': 0,
        'CCT': 0, 'CCC': 0, 'CCA': 0, 'CCG': 0,
        'CAT': 0, 'CAC': 0, 'CAA': 0, 'CAG': 0,
        'CGT': 0, 'CGC': 0, 'CGA': 0, 'CGG': 0,
        'ATT': 0, 'ATC': 0, 'ATA': 0, 'ATG': 0,
        'ACT': 0, 'ACC': 0, 'ACA': 0, 'ACG': 0,
        'AAT': 0, 'AAC': 0, 'AAA': 0, 'AAG': 0,
        'AGT': 0, 'AGC': 0, 'AGA': 0, 'AGG': 0,
        'GTT': 0, 'GTC': 0, 'GTA': 0, 'GTG': 0,
        'GCT': 0, 'GCC': 0, 'GCA': 0, 'GCG': 0,
        'GAT': 0, 'GAC': 0, 'GAA': 0, 'GAG': 0,
        'GGT': 0, 'GGC': 0, 'GGA': 0, 'GGG': 0
    }

    wrapper = textwrap.TextWrapper(width=3)
    f = wrapper.fill(text=gene_seq)
    my = f.split('\n')
    final = ''

    for term in my:
        if (len(gene_seq)) % 3 == 0:
            final = final + amino_acids.acids[term]

            # increment count for respective gene and add all that info in a list
            codon_count[term] = codon_count[term] + 1
        else:
            final = 'Infected Gene Sequence'

    final.rstrip()

    # delete terminating codons as they
    # are not require in the computations
    del codon_count['TAA']
    del codon_count['TGA']
    del codon_count['TAG']

    # list of dictionaries
    if final == 'Infected Gene Sequence':
        codon_count_list.append(final)
    else:
        codon_count_list.append(codon_count)

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

    try:
        import db
        db = reload(db)
    except cx_Oracle.DatabaseError:
        QMessageBox.critical(None, 'ERROR', "Something went wrong! Could not connect to the database",
                             QMessageBox.Ok, QMessageBox.Ok)
        return

    rows = []
    st = ''
    for line in file:
        tokens = line.split('\t')
        if len(tokens) == 9:
            tokens.append(tokens[0])
            tokens.pop(0)
            rows.append(tokens)
            # print(tokens)
            st = 'update GENOME_DATA set strand = :1, len = :2,  pid = :3, gene = :4, synonym1 = :5, code = :6, ' \
                 'cog = :7, product = :8 where location = :9'
    try:
        db.cur.prepare(st)
        db.cur.executemany(None, rows)
        db.con.commit()
        print('Done')
        # QMessageBox.information(None,
        # 'Message', "Both file contents have been merged.", QMessageBox.Ok, QMessageBox.Ok)

    except AttributeError:
        # flag = -1
        print("Update Error")
        QMessageBox.critical(None, 'ERROR', "Something went wrong! Could not connect to the database",
                             QMessageBox.Ok, QMessageBox.Ok)
        return -1
    finally:
        stop_loading(self)
    db.cur.close()
    db.con.close()
    pass


# acid_count = {
#     'M': {'ATG': 1, 'abc': 0....},
#     'T': {...},
#     ...
#     ..
#     .
# }


nc_list = []


def calculate_nc(item):
    global nc_list

    acid_count = {
        'A': {'GCT': 0, 'GCC': 0, 'GCA': 0, 'GCG': 0, 'TOTAL': 0},
        'C': {'TGT': 0, 'TGC': 0, 'TOTAL': 0},
        'D': {'GAT': 0, 'GAC': 0, 'TOTAL': 0},
        'E': {'GAA': 0, 'GAG': 0, 'TOTAL': 0},
        'F': {'TTT': 0, 'TTC': 0, 'TOTAL': 0},
        'G': {'GGT': 0, 'GGC': 0, 'GGA': 0, 'GGG': 0, 'TOTAL': 0},
        'H': {'CAT': 0, 'CAC': 0, 'TOTAL': 0},
        'I': {'ATT': 0, 'ATC': 0, 'ATA': 0, 'TOTAL': 0},
        'K': {'AAA': 0, 'AAG': 0, 'TOTAL': 0},
        'L': {'TTA': 0, 'TTG': 0, 'CTT': 0, 'CTC': 0, 'CTA': 0, 'CTG': 0, 'TOTAL': 0},
        'M': {'ATG': 0, 'TOTAL': 0},
        'N': {'AAT': 0, 'AAC': 0, 'TOTAL': 0},
        'P': {'CCT': 0, 'CCC': 0, 'CCA': 0, 'CCG': 0, 'TOTAL': 0},
        'Q': {'CAA': 0, 'CAG': 0, 'TOTAL': 0},
        'R': {'CGT': 0, 'CGC': 0, 'CGA': 0, 'CGG': 0, 'AGA': 0, 'AGG': 0, 'TOTAL': 0},
        'S': {'TCT': 0, 'TCC': 0, 'TCA': 0, 'TCG': 0, 'AGT': 0, 'AGC': 0, 'TOTAL': 0},
        'T': {'ACT': 0, 'ACC': 0, 'ACA': 0, 'ACG': 0, 'TOTAL': 0},
        'V': {'GTT': 0, 'GTC': 0, 'GTA': 0, 'GTG': 0, 'TOTAL': 0},
        'W': {'TGG': 0, 'TOTAL': 0},
        'Y': {'TAT': 0, 'TAC': 0, 'TOTAL': 0}
    }

    if item == 'Infected Gene Sequence':
        nc_list.append('0.0')

    else:
        for key in item:
            value = item[key]
            acid = amino_acids.acids[key]
            acid_count[acid][key] = acid_count[acid][key] + value
            # print('->' + str(acid_count[acid][key]))
            acid_count[acid]['TOTAL'] = acid_count[acid]['TOTAL'] + value

        for acid in acid_count:
            for codon in acid_count[acid]:
                if codon != 'TOTAL':
                    try:
                        # pi
                        acid_count[acid][codon] = acid_count[acid][codon] / acid_count[acid]['TOTAL']
                        # pi^2
                        acid_count[acid][codon] = pow(acid_count[acid][codon], 2)
                    except ZeroDivisionError:
                        acid_count[acid][codon] = 0

        nc = 0
        # (summation(pi^2) || Fk) and 1/Fk and Nc
        for acid in acid_count:
            temp = 0
            for codon in acid_count[acid]:
                if codon != 'TOTAL':
                    # add up all the values of an Amino acid
                    temp = temp + acid_count[acid][codon]
            try:
                # Fk
                acid_count[acid]['TOTAL'] = temp
                acid_count[acid]['TOTAL'] = acid_count[acid]['TOTAL']
                # print('Fk: ' + str(acid_count[acid]['TOTAL'] ))

                # 1/Fk
                acid_count[acid]['TOTAL'] = 1 / temp
                # acid_count[acid]['TOTAL'] = round(acid_count[acid]['TOTAL'], 2)
                # print('1/Fk: ' + str(acid_count[acid]['TOTAL']))

                # Nc
                nc = nc + acid_count[acid]['TOTAL']
            except ZeroDivisionError:
                acid_count[acid]['TOTAL'] = 0
        nc = round(nc, 2)
        # print('Nc: ' + str(nc))
        nc_list.append(nc)


buff = ""


def fetch_results(st):

    import db
    db = reload(db)

    result = []

    try:
        db.cur.execute(st)
        for rows in db.cur.fetchall():
            result.append(rows)

    except AttributeError:
        print('Something went wrong on the backend! :(')
        del result
        result.append('Sorry, Something went wrong on the backend! :(')

    finally:
        db.cur.close()
        db.con.close()

        return result
    pass


def display_search_results(self, result):

    total = len(result)

    if total < 1:
        buffer = 'No records satisfy given criteria'

    elif total > 90:
        buffer = 'Too many results. Please narrow down your search.'

    else:

        buffer = 'Total records fetched: ' + str(len(result)) +\
                 '\n-------------------------------------------------------------------------------------------------' \
                 '----------------------------------------------\n'

        for items in result:

            buffer = buffer + '{:38}'.format('Serial') + '{:^10}'.format(':') + str(items[0]) + '\n'
            buffer = buffer + '{:36}'.format('Location') + '{:^10}'.format(':') + str(items[1]) + '\n'
            part1 = str(items[2])[:71]
            part2 = '\n\t\t           ' + str(items[2])[71:]
            buffer = buffer + '{:32}'.format('Genome Info') + '{:^10}'.format(':') + part1 + part2 + '\n'
            buffer = buffer + '{:28}'.format('Length of Genome') + '{:^10}'.format(':') + str(items[10]) + '\n'
            buffer = buffer + '{:35}'.format('Count of A') + '{:^10}'.format(':') + str(items[6]) + '\n'
            buffer = buffer + '{:35}'.format('Count of T') + '{:^10}'.format(':') + str(items[7]) + '\n'
            buffer = buffer + '{:35}'.format('Count of G') + '{:^10}'.format(':') + str(items[8]) + '\n'
            buffer = buffer + '{:35}'.format('Count of C') + '{:^10}'.format(':') + str(items[9]) + '\n'
            buffer = buffer + '{:38}'.format('GC%') + '{:^10}'.format(':') + str(items[10]) + '%' + '\n'
            buffer = buffer + '{:38}'.format('Strand') + '{:^10}'.format(':') + str(items[11]) + '\n'
            buffer = buffer + '{:37}'.format('Length') + '{:^10}'.format(':') + str(items[12]) + '\n'
            buffer = buffer + '{:40}'.format('PID') + '{:^10}'.format(':') + str(items[13]) + '\n'
            buffer = buffer + '{:38}'.format('Gene') + '{:^10}'.format(':') + str(items[14]) + '\n'
            buffer = buffer + '{:35}'.format('Synonym') + '{:^10}'.format(':') + str(items[15]) + '\n'
            buffer = buffer + '{:38}'.format('Code') + '{:^10}'.format(':') + str(items[16]) + '\n'
            buffer = buffer + '{:38}'.format('COG') + '{:^10}'.format(':') + str(items[17]) + '\n'
            buffer = buffer + '{:37}'.format('Product') + '{:^10}'.format(':') + str(items[18]) + '\n'
            buffer = buffer + '{:36}'.format('Nc Value') + '{:^10}'.format(':') + str(items[20]) + '\n'
            buffer = buffer + '{:26}'.format('Amino Acid Sequence') + '{:^10}'.format(':') + str(items[19]) + '\n'

            buffer = buffer + '\n===================================================================================' \
                              '======\n\n'

    self.textEdit.setText(buffer)

    pass


def populate_tb(self):
    self.textEdit.setText(buff)
    pass


def format_data():
    global buff

    fp = open(os.path.expanduser("~\\Desktop\\upload.txt"), 'r')

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
    # del buff
    fp.close()
    pass
