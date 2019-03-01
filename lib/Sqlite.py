#######################
# Sqlite Class        #
# Matthijs Zondervan  #
# s1106533            #
#######################

class Sqlite:

    # import sqlite libary
    import sqlite3
    # import datetime to get the date and time from the system
    from datetime import datetime
    # import csv to save a csv file
    import csv
    # import hashlib to hash the passwords
    import hashlib

    # make all class atributes
    # the path to save the database this can be set using the constructor
    path = ''
    # the filename of the database this can be set using the constructor
    filename = ''
    # the salt that is used to make the passwords better
    salt = 'D&2WxXKqs2f0ZHY1*2#kQV37$8jG8hSxCk@QPwJ1YmdM!5aCAlF1sJqUopg2kf39'

    # the constructor function to set all the atributes
    def __init__(self, path='', filename='database'):
        self.path = path
        self.filename = filename
        # make a conn object to the database
        self.conn = self.sqlite3.connect(self.path + '/' + self.filename+'.db')
        # make te cursor objects
        self.c = self.conn.cursor()
        self.setup_database()

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
                       'case_id integer NULL,'
                       'date_time text,'
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
                       'partition_offset integer,'
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
        # log the creation of the database to the new database

    #############################
    # all log related functions
    #############################

    # make a new log item in the database
    def log_item(self, case_id=None, user_id=None, evidence_id=None, session_id=None, title=None, details=None):
        # get the current date and time
        date_time = self.datetime.now()
        # build and run the insert query
        self.c.execute('INSERT INTO logs(case_id, user_id, evidence_id, session_id, title, details, date_time) '
                       'VALUES(?, ?, ? ,? ,?, ?, ?)',
                       (case_id, user_id, evidence_id, session_id, title, details, date_time))
        # save the changes made
        self.conn.commit()

    # save all log items to a csv file
    def log2csv(self):
        self.log_item(title="Log export to csv started", details="logs are exported to csv file")
        # get all log items
        logs = self.get_log_items()
        with open('log.csv', 'w') as f:
            # make a csv writer
            writer = self.csv.writer(f)
            # write all rows to the csv file
            writer.writerow(['log id', 'case_id', 'user_id', 'evidence_id', 'session_id', 'date time', 'title', 'details'])
            writer.writerows(logs)
        self.log_item(title="Log export done")

    # get all log logitems that meet the arguments
    def get_log_items(self):
        # build and run the select query
        self.c.execute("SELECT * FROM logs")
        # return all the date
        return self.c.fetchall()

    def get_log(self, log_id):
        # build and run the selct query
        self.c.execute("SELECT * FROM logs WHERE log_id = ?", log_id)

    #############################
    # all case related functions
    #############################

    # make a new case in the database
    def set_case(self, values):
        # build and run the insert query
        self.c.execute('INSERT INTO cases(case_number, case_title, case_note, created_at) VALUES (?, ?, ?, ?)', (values['number'], values['title'], values['note'], self.datetime.now()))
        # save the changes made
        self.conn.commit()
        # log the insert
        self.log_item(case_id=values['number'], title="new cases created", details="case number:" + values['number'] + " title:" + values['title'] + " note: "+values['note']+"")
        return

    # get all the details from a case where the
    def get_case(self, case_id):
        # build and run the select query
        self.c.execute("SELECT * FROM cases WHERE case_id='%s'" % case_id)
        # return all the data
        return self.c.fetchone()

    # get all cases that meet the arguments
    def get_cases(self):
        # build and run the select query
        self.c.execute("SELECT * FROM cases")
        # save the results to "result"
        result = self.c.fetchall()
        # check if there are no results
        if len(result) == 0:
            # return a array so the gui does not crashes
            return [(None, None, None, None, None)]
        else:
            # if there are results just return the results
            return result

    ######################################
    # all evidence item related functions
    ######################################

    # make a new evidence item in the database
    def set_evidence_item(self, values):
        # build and run the insert query
        self.c.executemany('INSERT INTO evidences (evicence_code, case_id, title, type) values(?, ?, ?, ?)',
                           values["evidence_code"], values["case_id"], values["title"], values["type"])
        # save the changes made
        self.conn.commit()
        # log the insert
        self.log_item(case_id=values['case_id'],  title="new evidence item created",
                      details="code:"+values['evidence_code']+"")

    # get al the details from a evidence item
    def get_evidence_item_details(self, evidence_id):
        # build and run the select query
        self.c.execute("SELECT * FROM evidences WHERE evidence_id='%evidence_id'" % evidence_id)
        # return all the data
        return self.c.fetchall()

    # get all evidence items that meet the args
    def get_evidence_items(self):
        # build and run the select query
        self.c.execute("SELECT * FROM evidences")
        # return all the data
        return self.c.fetchall()

    #############################
    # all file related functions
    #############################

    # make a new file in the databse
    def set_files(self, values):
        # build and run the insert query
        self.c.executemany('INSERT INTO files (partition_id, file_md5, file_sha256, file_sha1, title, date_created, date_last_modified, file_path, size, extention, file_type) '
                           'VALUES (? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,?)', (values))
        # log the creation of the files
        self.log_item(title="new files are created", details="a new file has been created")
        # save the changes made
        self.conn.commit()

    def set_file(self, partition_id = None, file_parrent = None, file_md5 = None, file_sha256 = None, file_sha1 = None, title = None, date_created = None, date_last_modified = None, file_path = None, size = None, extention = None, file_type = None, partition_offset=None):
        self.c.execute('INSERT INTO files (partition_id, file_parrent, file_md5, file_sha256, file_sha1, title, date_created, date_last_modified, file_path, size, extention, file_type, partition_offset) '
                           'VALUES (? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,?, ?, ?)', (partition_id, file_parrent, file_md5, file_sha256, file_sha1, title, date_created, date_last_modified, file_path, size, extention, file_type, partition_offset))
        # save the changes made
        self.conn.commit()
        # log to creation of the file
        self.log_item(title="new file has been made", details="filename: " + title + "sha1: " + file_sha1)

    # get all files
    def get_files(self):
        self.c.execute('SELECT * FROM files')
        # return all the data
        return self.c.fetchall()

    def get_file_name(self, file_id):
        self.c.execute("SELECT title FROM files WHERE files.file_id == '%s'" % file_id)
        return self.c.fetchall()

    def get_file_path(self, file_id):
        self.c.execute("SELECT file_path FROM files WHERE files.file_id == '%s'" % file_id)
        return self.c.fetchall()

    def get_file_hash(self, file_id):
        self.c.execute("SELECT file_md5, file_sha256, file_sha1 FROM files WHERE files.file_id == '%s'" % file_id)
        return self.c.fetchall()

    def get_file_size(self, file_id):
        self.c.execute("SELECT size FROM files WHERE files.file_id == '%s'" % file_id)
        return self.c.fetchone()

    def get_partition_offset(self, file_id):
        self.c.execute("SELECT partition_offset FROM files WHERE files.file_id == '%s'" % file_id)
        return self.c.fetchone()

    def get_parent_key(self, name):
        self.c.execute("SELECT file_id FROM files WHERE files.title == '%s'" % name)
        return self.c.fetchone()

    ##############################
    # all user related functions
    ##############################

    # make a new usser in the databse
    def set_user(self, username, password):
        # get the current data and time
        date_time = self.datetime.now()
        # hash the password + salt and save as hexdigets
        hash_password = self.hashlib.sha1(self.salt.encode('utf-8') + password.encode('utf-8')).hexdigest()
        # build and run the insert query
        self.c.execute('INSERT INTO users(user_name, password, created_at) VALUES(?, ?, ?)', (username, hash_password, date_time))
        # save the changes made
        self.conn.commit()
        # log the creation of the new user
        self.log_item(title="new user created", details="username:"+username+" password:"+hash_password+"")

    # check if the user password is correct
    def check_user(self, username, password):
        # build and run the select query to find the username with given
        self.c.execute("SELECT * FROM users WHERE users.user_name = '%s'" % username)
        # save the results to "results"
        result = self.c.fetchone()

        # check if the results are none
        if result is None:
            # return false because no user is found
            self.log_item(user_id=self.get_user_id(username), title="user false login", details="user name: " + username + " tryed to log in but the user name is not found")
            return False
        if result is not None:
            # check if the hash form the password given is the same as the password hash in the database
            if self.hashlib.sha1(self.salt.encode('utf-8') + password.encode('utf-8')).hexdigest() == result[2]:
                # return true if the passwords match
                self.log_item(user_id=int(self.get_user_id(username)), title="user login",
                              details="user name: " + str(username))
                return True
            else:
                # return false if the passwords do not match
                self.log_item(user_id=self.get_user_id(username), title="user false login",
                              details="user name: " + username + " tryed to login but the password was not correct")
                return False

    def get_user_id(self, username):
        self.c.execute("SELECT user_id FROM users WHERE user_id = '%s'" % username)
        return self.c.fetchone()[0]

    # update the password from a user only if the old password is correct
    def update_password(self, old_password, new_password, username):
        # fist check if the old password is correct
        if self.check_user(username, old_password) is True:
            # build and run the update query and update the password using the username
            self.c.execute("UPDATE users SET password = %s WHERE users.user_name = '%s'" % new_password % username)
            self.log_item(user_id=self.get_user_id(username), title=username + " updated his password")
            # save the changes made
            self.conn.commit
            # return true if the query worked
            return True
        else:
            # if the old password is not correct return false
            self.log_item(user_id=self.get_user_id(username), title=username + " tryed updated his password",
                          details="old password was not correct")
            return False

    # get all users without the passwords of cource ;)
    def get_users(self):
        # build and run the select query
        self.c.execute('SELECT user_name FROM users ')
        # save the changes made
        return self.c.fetchall()

    # assing a user to a case
    def assing_user_to_case(self, user_id, case_id):
        # build and run the insert query
        self.c.execute("INSERT INTO case_assinment(user_id, case_id) VALUES(?, ?)", (user_id, case_id))
        # save the changes made
        self.conn.commit()
        # log the assingment
        self.log_item(title="new case assingment created",
                      details="user" + user_id + " has granted access to " + case_id + "")

    # check if user exists
    def check_username(self, username):
        # build and run the select query
        self.c.execute("SELECT user_name FROM users WHERE user_name = '%s'" % username)
        # save the result to "result"
        result = self.c.fetchone()
        # check if there are any result if none the username does not exist yet
        if result is None:
            # return false because the username does not exist yet
            return False
        if result is not None:
            return True
            # return true because there is already a user with the username
        else:
            return False

    #################################
    # All bookmark related functions
    #################################

    # make a new bookmark
    def set_bookmark(self, file_id, title, description, created_at):
        # build and run the insert query
        self.c.execute("INSERT INTO bookmarks(file_id, title, description, created_at) VALUES(?,?,?,?)", file_id, title, description, created_at)
        # save the changes made
        self.conn.commit()

        self.log_item(title="new bookmark for " + self.get_file_name(file_id), file_id=file_id,
                      details="title: " + title + " description " + description)
    # get all bookmarks form a case
    def get_case_bookmarks(self, case_id):
        # build and run the select query
        self.c.execute("SELECT * FROM bookmarks WHERE case_id ='%s'" % case_id)
        # return all the data
        return self.c.execute()