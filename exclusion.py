from datetime import datetime


class Exclusion:
    def __init__(self, row):
        (self.m_num,
         self.session,
         self.type,
         self.start_date,
         self.end_date) = row
        if self.start_date:
            self.start_date = datetime.combine(self.start_date, datetime.min.time())
        if self.end_date:
            self.end_date = datetime.combine(self.end_date, datetime.min.time())



    def __repr__(self):
        return "{}:{}:{}:{}:{}".format(self.m_num,
                                       self.session,
                                       self.type,
                                       self.start_date,
                                       self.end_date)
