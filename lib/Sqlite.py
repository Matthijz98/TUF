################
# Sqlite Class #
################
class Sqlite:

    # import sqlite libary
    import sqlite3
    from datetime import date, datetime

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
                       'user_name text, '
                       'password text) ')
        # make case_assignments table
        self.c.execute('CREATE TABLE IF NOT EXISTS case_assignments(assiment_id integer primary key AUTOINCREMENT, '
                       'user_id integer NOT NULL, '
                       'case_id integer, '
                       'FOREIGN KEY (user_id) REFERENCES users(user_id), '
                       'FOREIGN KEY (case_id) REFERENCES cases(case_id))')
        # make cases table
        self.c.execute('CREATE TABLE IF NOT EXISTS cases(case_id integer PRIMARY KEY AUTOINCREMENT, '
                       'case_number integer, '
                       'case_title varchar, '
                       'case_note varchar, '
                       'case_created timestamp)')
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
        self.c.execute('CREATE TABLE IF NOT EXISTS files ('
                       'file_id integer PRIMARY KEY AUTOINCREMENT,'
                       'partition_id blob,'
                       'file_md5 text,'
                       'file_sha256 text,'
                       'file_sha1 text,'
                       'title varchar,'
                       'date_created datetime,'
                       'date_last_modified datetime,'
                       'file_path varchar,'
                       'size integer,'
                       'extention varchar,'
                       'file_type integer)')
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

    # check the database if it hase the right tabels
    def check_database(self):
        return

    # make a new logitem in the database
    def set_logitem(self, values):
        self.c.executemany('INSERT INTO logs (evidence_id, session_id, case_id, date_time, title, details) VALUES (?, ?, ?, ?, ?, ? )', values["evidence_id"], values["session_id"], values["case_id"], values["date_time"] ,values["title"] ,values["details"])
        return

    # get all the logitem details
    def get_logitem_details(self, logId):
        self.c.execute("SELECT * FROM logs WHERE logId = '%lodId'" % logId)
        return self.c.fetchall()

    # get all log logitems that meet the arguments
    def get_logitems(self, args):
        self.c.execute("SELECT * FROM logs")
        return self.c.fetchall()

    # make a new case in the database
    def set_case(self, values):
        self.c.execute('INSERT INTO cases(case_number, case_title, case_note, case_created) VALUES (?, ?, ?, ?)', (values['number'], values['title'], values['note'], self.datetime.now()))
        self.conn.commit()
        return

    # get all the details from a case where the
    def get_case(self, case_id):
        self.c.execute("SELECT * FROM cases WHERE case_id='%s'" % case_id)
        return self.c.fetchone()

    # get all cases that meet the arguments
    def get_cases(self):
        self.c.execute("SELECT * FROM cases")
        return self.c.fetchall()

    # make a new evidence item in the database
    def set_evidence_item(self, values):
        self.c.executemany('INSERT INTO evidences (evidence_code, case_id, title, type) values(?, ?, ?, ?)', values["evidence_code"], values["case_id"], values["title"], values["type"])
        return

    # get al the details from a evidence item
    def get_evidence_item_details(self, evidence_id):
        self.c.execute("SELECT * FROM evidences WHERE evidence_id='%evidence_id'" % evidence_id)
        return self.c.fetchall()

    # get all evidence items that meet the args
    def get_evidence_items(self, args):
        self.c.execute("SELECT * FROM evidences" )
        return self.c.fetchall()

    # make a new file in the databse
    def set_files(self, values):
        self.c.executemany('INSERT INTO files (partition_id, file_md5, file_sha256, file_sha1, title, date_created, date_last_modified, file_path, size, extention, file_type) '
                           'VALUES (? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,?)', (values))
        self.conn.commit()

    # get all files that meet the arguments
    def get_files(self):
        self.execute('SELECT fields FROM files')
        return self.c.fetchall()

    # make a new user in the databse
    def set_user(self, values):
        self.c.execute('INSERT INTO users(user_name, password) VALUES(?, ?)', (values))
        self.conn.commit()

    # check if the user password is correct
    def check_user(self, username, password):
        self.c.execute("SELECT * FROM users WHERE users.user_name = '%s'" % username)
        result = self.c.fetchone()
        if result is None:
            print("geen asjdf")
            return False
        if result is not None:
            print("meer dan 0")
            if password == self.c.fetchone()[2]:
                return True
            else:
                return False

    def check_exist(self, username):
        self.c.execute("SELECT user_name FROM users WHERE users.user_name = '%s'" % username)
        result = self.c.fetchone()
        return result[0]

    # update the password from a user only if the old password is correct
    def update_password(self, old_password, new_password, username):
        # fist check if the old password is correct
        if self.check_user(username, old_password) is True:
            self.c.execute("UPDATE users SET password = %password WHERE users.user_id = '%s'" % new_password)
            return True
            self.conn.commit
        else:
            return False

    # get all users without the passwords of cource ;)
    def get_users(self):
        self.c.execute('SELECT user_name FROM users ')
        return self.c.fetchall()

    def assing_user_to_case(self, user_id, case_id):
        self.c.execute("INSERT INTO case_assinment")
