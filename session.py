class Session:
    def __init__(self, row):
        (self.session_id,
         self.day,
         self.start_time,
         self.end_time) = row

    def __repr__(self):
        return "{}:{}".format(self.session_id, self.day)
