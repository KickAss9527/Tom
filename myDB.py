import pymysql.cursors
import pymysql


class MyDB:
    def __init__(self):
        self.connection = pymysql.connect(host='localhost', user='root',password='1234527', db='mydb',use_unicode=True, charset="utf8",cursorclass=pymysql.cursors.DictCursor)
        sqlCreate = """
           CREATE TABLE IF NOT EXISTS POST(
           pid int(11) NOT NULL AUTO_INCREMENT,
           note int(11) NOT NULL,
           link varchar(255) NOT NULL,
           title varchar(255),
           userName varchar(255) NOT NULL,
           PRIMARY KEY (pid)
           )"""
        cursor = self.connection.cursor()
        cursor.execute(sqlCreate)
        self.connection.commit()

    def insert(self, link, note, userName, title=None):
        # sql = """INSERT INTO POST(link, note, userName, title) VALUES (%(link)s,%(note)s,%(userName)s,%(title)s)"""
        sql = """INSERT INTO POST(link, note, userName, title) VALUES (%s,%s,%s,%s)"""
        self.connection.cursor().execute(sql,(link, note, userName, title))
        self.connection.commit()
