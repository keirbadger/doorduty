import pymysql
from doorduty import config
from doorduty.duty import Duty


class WriteData:

    duties = []

    def add_duty (self, m_num, session_id, session_date):
        self.duties.append(Duty(m_num, session_id, session_date))

    def write_duties(self):
        cursor = self.connection.cursor()
        # import pydevd
        # pydevd.settrace('192.168.1.234', port=57588, stdoutToServer=True, stderrToServer=True)
        for duty in self.duties:
            sql = f"INSERT INTO duty VALUES (null, {duty.m_num}, {duty.session_id}, '{duty.date}')"
            print(sql)
            cursor.execute(sql)

        cursor.close()

    def close_connection(self):
        self.connection.commit()
        self.connection.close()

    def __init__(self):
        self.connection = pymysql.connect(
            host="localhost",
            user=config.AS_DB_USER,
            passwd=config.AS_DB_PASS,
            database=config.AS_DB_NAME,
            port=config.AS_DB_PORT)
