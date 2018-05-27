from datetime import datetime
from dateutil.relativedelta import relativedelta
from doorduty.duty import Duty
from operator import attrgetter


class Member:
    def __init__(self, row, duties, exclusions):
        (self.m_num,
         self.sal,
         self.first_name,
         self.second_name,
         self.type,
         self.join_date,
         self.renew_date,
         self.renewed) = row
        self.my_duties = [
            duty for duty in duties
            if (duty.m_num == self.m_num)
        ]
        self.my_exclusions = [
            exclusion for exclusion in exclusions
            if (exclusion.m_num == self.m_num)
        ]
        if self.join_date:
            self.join_date = datetime.strptime(self.join_date, '%d/%m/%Y')
        if self.renew_date:
            #print (f"{self.m_num} : {self.renew_date}")
            self.renew_date = datetime.strptime(self.renew_date, '%d/%m/%Y')
        self.num_duties = self.num_duties_in_last_18_months()
        self.avg_num_duties = self.avg_num_duties_in_last_18_months()

    def renewed_in_last_18_months(self, duty_date):
        if self.renew_date and self.renewed == 1:
            return self.renew_date > \
                   (duty_date - relativedelta(months=18))
        return False

    def more_than_6_duties_in_last_year(self,duty_date):
        count = 0
        for duty in self.my_duties:
            if duty.date > (duty_date - relativedelta(years=1)):
                count += 1
        return count >= 6

    def new_joiner(self, duty_date):
        if self.join_date:
            return self.join_date > \
                   (duty_date - relativedelta(days=60))

    def num_duties_in_last_18_months(self, duty_date=datetime.now()):
        count = 0
        for duty in self.my_duties:
            if duty.date > (duty_date - relativedelta(months=18)):
                count += 1
        return count

    def avg_num_duties_in_last_18_months(self, duty_date=datetime.now()):
        count = 0
        for duty in self.my_duties:
            if duty.date > (duty_date - relativedelta(months=18)):
                count += 1
        if self.renew_date and self.renew_date > (duty_date - relativedelta(months=18)):
            return count/(duty_date - self.renew_date).days
        else:
            return count/(18*30)

    def excempt_from_duties(self):
        excempt_types = ["Lifeguard", "Swimming Teacher", "Student Teacher", "Family Junior", "Junior"]
        if self.type in excempt_types:
            return True
        if self.first_name == "Iris" and self.second_name == "Gosling (Mrs)":
            return True
        return False

    def can_i_do_this_session(self, session_id):
        for ex in self.my_exclusions:
            if ex.type == 'S':
                return str(session_id) not in ex.session

    def can_i_do_this_date(self, session_date):
        for ex in self.my_exclusions:
            if ex.type == 'D':
                if ex.start_date <= session_date <= ex.end_date:
                    return False
        return True

    def add_duty(self, m_num, session_id, duty_date):
        self.my_duties.append(Duty(m_num, session_id, duty_date))
        self.num_duties = self.num_duties_in_last_18_months(duty_date)
        self.avg_num_duties = self.avg_num_duties_in_last_18_months(duty_date)

    def more_than_50_days_since_last_duty(self, duty_date):
        if len(self.my_duties) == 0:
            return True

        sorted_duties = sorted(self.my_duties, key=attrgetter('date'))
        if sorted_duties[-1].date < (duty_date - relativedelta(days=50)):
            return True
        else:
            return False

    # def __repr__(self):
    #     return "{}:{}:{}:{}:{}:{}:{}:{}".format(self.m_num,
    #                                          self.first_name,
    #                                          self.second_name,
    #                                          self.type,
    #                                          self.join_date.strftime("%d/%m/%Y"),
    #                                          self.renew_date.strftime("%d/%m/%Y"),
    #                                          self.num_duties,
    #                                          self.avg_num_duties)

    def __repr__(self):
        return "{} {}".format(self.first_name,self.second_name)


