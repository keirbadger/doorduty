import pymysql
from doorduty.member import Member
from doorduty.duty import Duty
from doorduty.exclusion import Exclusion
from doorduty.session import Session
from operator import attrgetter
from doorduty import config


class ReadData:

    def read_duties(self):
        _duties = []
        cursor = self.connection.cursor()
        retrieve = "Select * from duty;"
        cursor.execute(retrieve)
        rows = cursor.fetchall()
        for row in rows:
            #print(row)
            _duties.append(Duty(row))
        self.connection.commit()
        return _duties

    def read_members(self, duties, exclusions):
        _members = []
        cursor = self.connection.cursor()
        retrieve = "Select * from member;"
        cursor.execute(retrieve)
        rows = cursor.fetchall()
        for row in rows:
            _members.append(Member(row, duties, exclusions))
        self.connection.commit()
        return sorted(
            _members,
            key=attrgetter('avg_num_duties'),
            reverse=False)

    def read_exclusions(self):
        _exclusions = []
        cursor = self.connection.cursor()
        retrieve = "Select * from exclusion;"
        cursor.execute(retrieve)
        rows = cursor.fetchall()
        for row in rows:
            _exclusions.append(Exclusion(row))
        self.connection.commit()
        return _exclusions

    def read_sessions(self):
        _sessions = []
        cursor = self.connection.cursor()
        retrieve = "Select * from session;"
        cursor.execute(retrieve)
        rows = cursor.fetchall()
        for row in rows:
            _sessions.append(Session(row))
        self.connection.commit()
        return _sessions

    def all_members(self):
        return self.members

    def all_duties(self):
        return self.duties

    def all_exclusions(self):
        return self.exclusions

    def all_sessions(self):
        return self.sessions

    def __init__(self):
        self.connection = pymysql.connect(
            host="localhost",
            user=config.AS_DB_USER,
            passwd=config.AS_DB_PASS,
            database=config.AS_DB_NAME,
            port=config.AS_DB_PORT)
        self.duties = self.read_duties()
        self.exclusions = self.read_exclusions()
        self.sessions = self.read_sessions()
        self.members = self.read_members(self.duties, self.exclusions)
        self.connection.close()
