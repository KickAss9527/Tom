import pymysql.cursors
import pymysql


class MyDB:
    def __init__(self):
        self.connection = pymysql.connect(host='localhost', user='root',password='1234527', db='mydb',use_unicode=True, charset="utf8",cursorclass=pymysql.cursors.DictCursor)
        cursor = self.connection.cursor()

        sqlCreateUSER = """
            CREATE TABLE IF NOT EXISTS USER(
            uid int(11) NOT NULL AUTO_INCREMENT,
            nickName varchar(255) NOT NULL,
            lastUpdate int(11) NOT NULL,
            PRIMARY KEY (uid)
            )"""
        cursor.execute(sqlCreateUSER)

        sqlCreatePOST = """
           CREATE TABLE IF NOT EXISTS POST(
           pid int(11) NOT NULL AUTO_INCREMENT primary key,
           note int(11) NOT NULL,
           link varchar(255) NOT NULL,
           title varchar(255),
           userid int(11) not null,
           FOREIGN KEY kf_userid(userid)
           REFERENCES USER(uid)
           ON DELETE CASCADE
           )"""
        cursor.execute(sqlCreatePOST)

        self.connection.commit()

    def insertPOST(self, link, note, uid, title=None):
        sql = """INSERT INTO POST(link, note, userid, title) VALUES (%s,%s,%s,%s)"""
        self.connection.cursor().execute(sql,(link, note, uid, title))
        self.connection.commit()

    def insert_user(self, userName, lastUpdate):
        sql = """INSERT INTO USER(nickName, lastUpdate) VALUES (%s,%s)"""
        self.connection.cursor().execute(sql, (userName, lastUpdate))
        self.connection.commit()

    def getUidByName(self, name):
        cursor = self.connection.cursor()
        cursor.execute("""SELECT uid FROM USER WHERE nickName=%s LIMIT 1""", name)
        res = cursor.fetchone()
        return res['uid']

    def getNickNameByID(self, uid):
        cursor = self.connection.cursor()
        cursor.execute("""SELECT nickName FROM USER WHERE uid=%s LIMIT 1""", uid)
        res = cursor.fetchone()
        return res['nickName']

    def finish(self):
        self.connection.close()
