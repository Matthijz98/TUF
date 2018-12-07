import sqlite3
conn = sqlite3.connect('database.db')
c = conn.cursor()

def setUpDataBase:
    # make user table
    c.execute('''CREATE TABLE user(user_id integer primary key, username text, password text) ''')
    # make case_assignment table
    c.execute('''CREATE TABLE case_assignment(assiment_id integer primary key, user_id integer, case_id integer)''')
    # make case table
    c.execute('''CREATE TABLE case(case_id integer primary key, created_dar text, title text, description text)''')
    # make session table
    c.execute('''CREATE TABLE session(session_id integer primary key, user_id integer ,start_time text, end_time text)''')
    # make log table
    c.execute('''CREATE TABLE log(log_id integer primary key, evidence_id integer, session_id integer, case_id integer, date_time text, title text, details text) ''')
    # make evidence table
    c.execute('''CREATE TABLE evidence(case_id integer , eveidence_id integer, title text, type integer)''')
    # make file table
    c.execute('''CREATE TABLE file(file_id integer primary key, evidence_id integer, evidence_id integer, file_hash_md5 text, hash_md5 text, hash_sha265 text, hash_sha512 text, hash_sha1 text, title text, date_created text, date_last_modified text, file_path text, size text, extention text)  ''')
    # make virustotal_report
    c.execute('''CREATE TABLE virustotal_report(scan_id primary key integer, file_id integer, scan_report )''')
    # make proces table
    c.execute('''CREATE TABLE proces(proces_id integer  primary key, case_id integer, evidence_id integer, name text, PID integer, PPID integer, thds integer, hnds integer, time integer)''')

    conn.commit()

    conn.close()

def checkDataBase:

def setLogItem(dateTime, title, details):

def getLogItemDetails(logId, title):

def getLogItems(args[]):

def setCase(caseId, date):

def getCase(caseId, fields):

def getCases(args[]):

def setEvidenseItem(hashes[], file, extention, size, dateTime):

def getEvidenseItemDetails(evidenseId, fields):

def getEvidenseItems(args[]):

def logItem(file, location, tag):