class Sqlite:

    # import sqlite libary
    import sqlite3

    # make all class atributes
    path = ''
    filename = ''
    conn = ''
    c =''

    # the constructor function to set all the atributes
    def __init__(self, path, filename):
        self.path = path
        self.filename
        # make a conn object to the database
        self.conn = self.sqlite3.connect('database.db')
        self.c = self.conn.cursor()

    def setUpDataBase(self):
        # make user table
        self.c.execute('CREATE TABLE IF NOT EXISTS users(user_id integer primary key AUTOINCREMENT, username text, password text) ')
        # make case_assignment table
        self.c.execute('CREATE TABLE IF NOT EXISTS case_assignment(assiment_id integer primary key AUTOINCREMENT, user_id integer, case_id integer)')
        # make case table
        self.c.execute('CREATE TABLE IF NOT EXISTS cases(case_id integer primary key AUTOINCREMENT, created_date text, title text, description text)')
        # make session table
        self.c.execute('CREATE TABLE IF NOT EXISTS sessions(session_id integer primary key AUTOINCREMENT, user_id integer ,start_time text, end_time text)')
        # make log table
        self.c.execute('CREATE TABLE IF NOT EXISTS logs(log_id integer primary key AUTOINCREMENT, evidence_id integer, session_id integer, case_id integer, date_time text, title text, details text) ')
        # make evidence table
        self.c.execute('CREATE TABLE IF NOT EXISTS evidences(evidence_id integer primary key AUTOINCREMENT, case_id integer, title text, type integer)')
        # make file table
        self.c.execute('CREATE TABLE IF NOT EXISTS files(file_id integer primary key AUTOINCREMENT, evidence_id integer, file_hash_md5 text, hash_md5 text, hash_sha265 text, hash_sha512 text, hash_sha1 text, title text, date_created text, date_last_modified text, file_path text, size text, extention text)  ')
        # make virustotal_report
        self.c.execute('CREATE TABLE IF NOT EXISTS virustotal_reports(scan_id integer primary key AUTOINCREMENT, file_id integer, scan_report none)')
        # make proces table
        self.c.execute('CREATE TABLE IF NOT EXISTS processes(proces_id integer  primary key AUTOINCREMENT, case_id integer, evidence_id integer, name text, PID integer, PPID integer, thds integer, hnds integer, time integer)')
        # commit all changes to the database
        self.conn.commit()
        # close connection to the database

    def checkDataBase(self):
        return
    def setLogItem(self, values):
        c.executemany('INSERT INTO logs (evidence_id, session_id, case_id, date_time, title, details) VALUES (?, ?, ?, ?, ?, ? )', values)
        return
    def getLogItemDetails(seld, logId, title):
        return
    def getLogItems(self, args):
        return
    def setCase(self, values):
        c.executemany('INSERT INTO cases VALUES (?, ?, ?, ?)', values)
        return
    def getCase(self, caseId, fields):
        return
    def getCases(self, args):
        return
    def setEvidenceItem(self, values):
        c.executemany('INSERT INTO evidences values(?, ?, ?, ?)', values)
        return
    def getEvidenceItemDetails(self, evidenceId, fields):
        return
    def getEvidenceItems(self, args):
        return