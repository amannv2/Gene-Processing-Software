import cx_Oracle
try:
    con = cx_Oracle.connect('system/AmanVerma22@localhost/verma')
    cur = con.cursor()
except cx_Oracle.DatabaseError:
    print('Can not connect to DB')
    raise cx_Oracle.DatabaseError
