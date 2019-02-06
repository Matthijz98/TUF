#######################
# Sqlite Class        #
# Matthijs Zondervan  #
# s1106533            #
#######################

class Sqlite:

    # import sqlite libary
    import sqlite3
    from datetime import date, datetime
    import csv

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

    ##########################
    # Main database functions
    ##########################

    # set up database function this runs the create query
    def setup_database(self):
        # make users table
        self.c.execute('CREATE TABLE IF NOT EXISTS users(user_id integer primary key AUTOINCREMENT, '
                       'user_name text, '
                       'password text, '
                       'created_at timestamp) ')
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
                       'created_at timestamp)')
        # make sessions table
        self.c.execute('CREATE TABLE IF NOT EXISTS sessions(session_id integer primary key AUTOINCREMENT, '
                       'user_id integer,'
                       'start_time text, '
                       'end_time text, '
                       'FOREIGN KEY (user_id) REFERENCES users(user_id)) ')
        # make logs table
        self.c.execute('CREATE TABLE IF NOT EXISTS logs(log_id integer primary key AUTOINCREMENT, '
                       'evidence_id integer NULL, '
                       'user_id integer NULL,'
                       'session_id integer NULL, '
                       'case_id integer NULL, '
                       'date_time text, '
                       'title text NULL, '
                       'details text NULL, '
                       'FOREIGN KEY (evidence_id) REFERENCES evidences(evidence_id), '
                       'FOREIGN KEY (user_id) REFERENCES users(user_id),'
                       'FOREIGN KEY (session_id) REFERENCES sessions(session_id), '
                       'FOREIGN KEY (evidence_id) REFERENCES evidences(evidence_id), '
                       'FOREIGN KEY (case_id) REFERENCES cases(case_id))')
        # make evidences table
        self.c.execute('CREATE TABLE IF NOT EXISTS evidences(evidence_id integer primary key AUTOINCREMENT, '
                       'case_id integer, '
                       'case_number integer,'
                       'title text, '
                       'type integer,'
                       'FOREIGN KEY (case_id) REFERENCES cases(case_id))')
        # make files table
        self.c.execute('CREATE TABLE IF NOT EXISTS files ('
                       'file_id integer PRIMARY KEY AUTOINCREMENT,'
                       'file_parrent text,'
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
                       'file_type integer,'
                       'FOREIGN KEY (file_parrent) REFERENCES files(file_id))')
        # make virustotal_reports
        self.c.execute('CREATE TABLE IF NOT EXISTS virustotal_reports(scan_id integer primary key AUTOINCREMENT, '
                       'file_id integer, '
                       'scan_report none,'
                       'FOREIGN KEY (file_id) REFERENCES files(file_id))')
        # make bookmark table
        self.c.execute('CREATE TABLE IF NOT EXISTS bookmarks ('
                       'bookmark_id integer PRIMARY KEY AUTOINCREMENT,'
                       'file_id integer,'
                       'tile text,'
                       'description text,'
                       'created_at datetime,'
                       'FOREIGN KEY (file_id) REFERENCES files(file_id))')
        # commit all changes to the database
        self.conn.commit()
        # close connection to the database

    # check the database if it has the right tabels
    def check_database(self):
        return

    #############################
    # all log related functions
    #############################

    # make a new log item in the database
    def log_item(self, case_id='', user_id=None, evidence_id=None, session_id=None, title=None, details=None):
        date_time = self.datetime.now()
        self.c.execute('INSERT INTO logs(case_id, user_id, evidence_id, session_id, title, details, date_time) '
                       'VALUES(?, ?, ? ,? ,?, ?, ?)',
                       (case_id, user_id, evidence_id, session_id, title, details, date_time))
        self.conn.commit()

    # save all log items to a csv file
    def log2csv(self):
        data = self.get_log_items()
        with open('output.csv', 'w') as f:
            writer = self.csv.writer(f)
            writer.writerow(['case_id', 'user_id', 'evidence_id', 'session_id', 'title', 'details', 'date_time'])
            writer.writerows(data)

    # get all log logitems that meet the arguments
    def get_log_items(self):
        self.c.execute("SELECT * FROM logs")
        return self.c.fetchall()

    def get_log(self, log_id):
        self.c.execute("SELECT * FROM logs WHERE log_id = ?", log_id)

    #############################
    # all case related functions
    #############################

    # make a new case in the database
    def set_case(self, values):
        self.c.execute('INSERT INTO cases(case_number, case_title, case_note, created_at) VALUES (?, ?, ?, ?)', (values['number'], values['title'], values['note'], self.datetime.now()))
        self.conn.commit()
        self.log_item(case_id=values['number'], title="new cases created", details="case number:" + values['number'] + " title:" + values['title'] + " note: "+values['note']+"")
        return

    # get all the details from a case where the
    def get_case(self, case_id):
        self.c.execute("SELECT * FROM cases WHERE case_id='%s'" % case_id)
        return self.c.fetchone()

    # get all cases that meet the arguments
    def get_cases(self):
        self.c.execute("SELECT * FROM cases")
        result = self.c.fetchall()
        print(result)
        if len(result) == 0:
            return [(None, None, None, None, None)]
        else:
            return result

    ######################################
    # all evidence item related functions
    ######################################

    # make a new evidence item in the database
    def set_evidence_item(self, values):
        self.c.executemany('INSERT INTO evidences (evicence_code, case_id, title, type) values(?, ?, ?, ?)',
                           values["evidence_code"], values["case_id"], values["title"], values["type"])
        self.conn.commit()
        self.log_item(case_id=values['case_id'],  title="new evidence item created",
                      details="code:"+values['evidence_code']+"")
        return

    # get al the details from a evidence item
    def get_evidence_item_details(self, evidence_id):
        self.c.execute("SELECT * FROM evidences WHERE evidence_id='%evidence_id'" % evidence_id)
        return self.c.fetchall()

    # get all evidence items that meet the args
    def get_evidence_items(self, args):
        self.c.execute("SELECT * FROM evidences" )
        return self.c.fetchall()

    #############################
    # all file related functions
    #############################

    # make a new file in the databse
    def set_files(self, values):
        self.c.executemany('INSERT INTO files (partition_id, file_md5, file_sha256, file_sha1, title, date_created, date_last_modified, file_path, size, extention, file_type) '
                           'VALUES (? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,?)', (values))
        self.conn.commit()

    def set_file(self, partition_id = None, file_parrent = None, file_md5 = None, file_sha256 = None, file_sha1 = None, title = None, date_created = None, date_last_modified = None, file_path = None, size = None, extention = None, file_type = None):
        self.c.execute('INSERT INTO files (partition_id, file_parrent, file_md5, file_sha256, file_sha1, title, date_created, date_last_modified, file_path, size, extention, file_type) '
                           'VALUES (? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,?, ?)', (partition_id, file_parrent, file_md5, file_sha256, file_sha1, title, date_created, date_last_modified, file_path, size, extention, file_type))
        self.conn.commit()

    # get all files that meet the arguments
    def get_files(self):
        self.c.execute('SELECT * FROM files')
        return self.c.fetchall()

    def get_parent_key(self, name):
        self.c.execute("SELECT file_id FROM files WHERE files.title == '%s'" % name)
        return self.c.fetchone()

    ##############################
    # all user related functions
    ##############################

    # make a new user in the databse
    def set_user(self, username, password):
        date_time = self.datetime.now()
        self.c.execute('INSERT INTO users(user_name, password, created_at) VALUES(?, ?, ?)', (username, password, date_time))
        self.conn.commit()
        self.log_item(title="new user created", details="username:"+username+" password:"+password+"")

    # check if the user password is correct
    def check_user(self, username, password):
        self.c.execute("SELECT * FROM users WHERE users.user_name = '%s'" % username)
        result = self.c.fetchone()
        print(result)
        if result is None:
            return False
        if result is not None:
            if password == result[2]:
                return True
            else:
                return False

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

    # assing a user to a case
    def assing_user_to_case(self, user_id, case_id):
        self.c.execute("INSERT INTO case_assinment(user_id, case_id) VALUES(?, ?)", (user_id, case_id))
        self.conn.commit()
        self.log_item(title="new case assingment created",
                      details="user" + user_id + " has granted access to " + case_id + "")

    # check if user exists
    def check_username(self, username):
        self.c.execute("SELECT user_name FROM users WHERE user_name = '%s'" % username)
        result = self.c.fetchone()
        if result is None:
            return False
        if result is not None:
            return True
        else:
            return False

    #################################
    # All bookmark related functions
    #################################

    def set_bookmark(self, file_id, title, description, created_at):
        self.c.execute("INSERT INTO bookmarks(file_id, title, description, created_at) VALUES(?,?,?,?)", file_id, title, description, created_at)

    def get_case_bookmarks(self, case_id):
        self.c.execute("SELECT * FROM bookmarks WHERE case_id ='%s'" %case_id)
        return self.c.executemany()
