from datetime import datetime


class Duty:
    def __init__(self, *args):
        if len(args) == 1:
            (self.id,
             self.m_num,
             self.session_id,
             self.date) = args[0]
            self.date = datetime.combine(self.date, datetime.min.time())
        if len(args) == 3:
            self.id = None
            self.m_num = args[0]
            self.session_id = args[1]
            self.date = args[2]

    def __repr__(self):
        return "{}:{}:{}:{}".format(self.m_num, self.id, self.session_id, self.date)
