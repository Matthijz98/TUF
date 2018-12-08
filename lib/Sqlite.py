import sqlite3
conn = sqlite3.connect('database.db')
c = conn.cursor()

def setUpDataBase():
    # make user table
    c.execute('CREATE TABLE IF NOT EXISTS users(user_id integer primary key AUTOINCREMENT, username text, password text) ')
    # make case_assignment table
    c.execute('CREATE TABLE IF NOT EXISTS case_assignment(assiment_id integer primary key AUTOINCREMENT, user_id integer, case_id integer)')
    # make case table
    c.execute('CREATE TABLE IF NOT EXISTS cases(case_id integer primary key AUTOINCREMENT, created_date text, title text, description text)')
    # make session table
    c.execute('CREATE TABLE IF NOT EXISTS sessions(session_id integer primary key AUTOINCREMENT, user_id integer ,start_time text, end_time text)')
    # make log table
    c.execute('CREATE TABLE IF NOT EXISTS logs(log_id integer primary key AUTOINCREMENT, evidence_id integer, session_id integer, case_id integer, date_time text, title text, details text) ')
    # make evidence table
    c.execute('CREATE TABLE IF NOT EXISTS evidences(evidence_id integer primary key AUTOINCREMENT, case_id integer, title text, type integer)')
    # make file table
    c.execute('CREATE TABLE IF NOT EXISTS files(file_id integer primary key AUTOINCREMENT, evidence_id integer, file_hash_md5 text, hash_md5 text, hash_sha265 text, hash_sha512 text, hash_sha1 text, title text, date_created text, date_last_modified text, file_path text, size text, extention text)  ')
    # make virustotal_report
    c.execute('CREATE TABLE IF NOT EXISTS virustotal_reports(scan_id integer primary key AUTOINCREMENT, file_id integer, scan_report none)')
    # make proces table
    c.execute('CREATE TABLE IF NOT EXISTS processes(proces_id integer  primary key AUTOINCREMENT, case_id integer, evidence_id integer, name text, PID integer, PPID integer, thds integer, hnds integer, time integer)')
    # commit all changes to the database
    conn.commit()
    # close connection to the database

def checkDataBase():
    return
def setLogItem(values):
    c.executemany('INSERT INTO logs (evidence_id, session_id, case_id, date_time, title, details) VALUES (?, ?, ?, ?, ?, ? )', values)
    return
def getLogItemDetails(logId, title):
    return
def getLogItems(args):
    return
def setCase(values):
    c.executemany('INSERT INTO cases VALUES (?, ?, ?, ?)', values)
    return
def getCase(caseId, fields):
    return
def getCases(args):
    return
def setEvidenceItem(values):
    c.executemany('INSERT INTO evidences values(?, ?, ?, ?)', values)
    return
def getEvidenceItemDetails(evidenceId, fields):
    return
def getEvidenceItems(args):
    return

if __name__ == '__main__':
    setUpDataBase()

    logValues = [(1, 1, 1, '02-07-1988', 'testtitle', 'testdetails')]
    setLogItem(logValues)

    caseValues = [(1, '02-07-1998', 'testTile', 'TestDescription')]
    setCase(caseValues)

    evidenceValues = [(1, 1, 'testTitle', 'TestDescription')]
    setEvidenceItem(evidenceValues)

    conn.close()