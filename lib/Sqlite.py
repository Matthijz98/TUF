class Sqlite:

    # import sqlite libary
    import sqlite3

    # make all class atributes
    path = ''
    filename = ''

    # the constructor function to set all the atributes
    def __init__(self, path='', filename='database'):
        self.path = path
        self.filename = filename
        # make a conn object to the database
        self.conn = self.sqlite3.connect(self.path + '/' + self.filename+'.db')
        self.c = self.conn.cursor()

    def setup_database(self):
        # make users table
        self.c.execute('CREATE TABLE IF NOT EXISTS users(user_id integer primary key AUTOINCREMENT, '
                       'username text, '
                       'password text) ')
        # make case_assignments table
        self.c.execute('CREATE TABLE IF NOT EXISTS case_assignments(assiment_id integer primary key AUTOINCREMENT, '
                       'user_id integer NOT NULL, '
                       'case_id integer, '
                       'FOREIGN KEY (user_id) REFERENCES users(user_id), '
                       'FOREIGN KEY (case_id) REFERENCES cases(case_id))')
        # make cases table
        self.c.execute('CREATE TABLE IF NOT EXISTS cases(case_id integer primary key AUTOINCREMENT, '
                       'created_date text, '
                       'title text, '
                       'description text)')
        # make sessions table
        self.c.execute('CREATE TABLE IF NOT EXISTS sessions(session_id integer primary key AUTOINCREMENT, '
                       'user_id integer,'
                       'start_time text, '
                       'end_time text, '
                       'FOREIGN KEY (user_id) REFERENCES users(user_id)) ')
        # make logs table
        self.c.execute('CREATE TABLE IF NOT EXISTS logs(log_id integer primary key AUTOINCREMENT, '
                       'evidence_id integer, '
                       'session_id integer, '
                       'case_id integer, '
                       'log_type_id INTEGER,date_time text, '
                       'title text, '
                       'details text, '
                       'FOREIGN KEY (evidence_id) REFERENCES evidences(evidence_id), '
                       'FOREIGN KEY (session_id) REFERENCES sessions(session_id), '
                       'FOREIGN KEY (evidence_id) REFERENCES evidences(evidence_id), '
                       'FOREIGN KEY (log_type_id) REFERENCES log_type(log_type_id), '
                       'FOREIGN KEY (case_id) REFERENCES cases(case_id))')
        # make log_types table
        self.c.execute('CREATE TABLE IF NOT EXISTS log_types(log_type_id INTEGER primary key AUTOINCREMENT, '
                       'name text, '
                       'color text)')
        # make evidences table
        self.c.execute('CREATE TABLE IF NOT EXISTS evidences(evidence_id integer primary key AUTOINCREMENT, '
                       'case_id integer, '
                       'title text, '
                       'type integer,'
                       'FOREIGN KEY (case_id) REFERENCES cases(case_id))')
        # make files table
        self.c.execute('CREATE TABLE IF NOT EXISTS files(file_id integer primary key AUTOINCREMENT, '
                       'evidence_id integer, '
                       'file_hash_md5 text, '
                       'hash_md5 text, '
                       'hash_sha265 text, '
                       'hash_sha512 text, '
                       'hash_sha1 text, '
                       'title text, '
                       'date_created text, '
                       'date_last_modified text, '
                       'file_path text, '
                       'size text, '
                       'extention text, '
                       'FOREIGN KEY (evidence_id) REFERENCES evidences(evidence_id))')
        # make virustotal_reports
        self.c.execute('CREATE TABLE IF NOT EXISTS virustotal_reports(scan_id integer primary key AUTOINCREMENT, '
                       'file_id integer, '
                       'scan_report none,'
                       'FOREIGN KEY (file_id) REFERENCES files(file_id))')
        # make processes table
        self.c.execute('CREATE TABLE IF NOT EXISTS processes(proces_id integer primary key AUTOINCREMENT, '
                       'evidence_id integer, '
                       'name text, '
                       'PID integer, '
                       'PPID integer, '
                       'thds integer, '
                       'hnds integer, '
                       'time integer, '
                       'FOREIGN KEY (evidence_id) REFERENCES evidences(evidence_id))')
        # commit all changes to the database
        self.conn.commit()
        # close connection to the database

    def check_database(self):
        return

    def set_logitem(self, values):
        self.c.executemany('INSERT INTO logs (evidence_id, session_id, case_id, date_time, title, details) VALUES (?, ?, ?, ?, ?, ? )', values)
        return

    def get_logitem_details(self, logId):
        self.c.execute("SELECT * FROM logs WHERE logId = '%lodId'" % logId)
        return self.c.fetchall()

    def get_logitems(self, args):
        self.c.execute("SELECT * FROM logs WHERE '%args'" % args)
        return self.c.fetchall()

    def set_case(self, values):
        self.c.executemany('INSERT INTO cases VALUES (?, ?, ?, ?)', values)
        return

    def get_case(self, case_id, fields='*'):
        self.c.execute("SELECT '%fields' WHERE case_id='%caseId'" % fields % case_id)
        return self.c.fetchall()

    def get_cases(self, args):
        self.c.execute("SELECT * FROM cases WHERE '%args'" % args)
        return self.c.fetchall()

    def set_evidence_item(self, values):
        self.c.executemany('INSERT INTO evidences values(?, ?, ?, ?)', values)
        return

    def get_evidence_item_details(self, evidence_id, fields):
        self.c.execute("SELECT * FROM evidences WHERE evidence_id='%evidence_id'" % evidence_id)
        return self.c.fetchall()

    def get_evidence_items(self, args):
        self.c.execute("SELECT * FROM evidences WHERE '%args'" % args)
        return

if __name__ == '__main__':
    Sqlite = Sqlite('C:\Users\mzond\Desktop\DEV\TUF', 'database')
    Sqlite.setup_database()