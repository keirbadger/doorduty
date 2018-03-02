from readdata import Data
from datetime import datetime
from datetime import timedelta
from operator import attrgetter


start = datetime(2018, 6, 1)
stop = datetime(2018, 8, 1)

data = Data()

while start < stop:
    start = start + timedelta(days=1)
    for session in data.sessions:
        for member in sorted(data.members, key=attrgetter('num_duties'), reverse=False):
            if start.strftime("%A") == session.day and \
               not member.excempt_from_duties() and \
               member.renewed_in_last_18_months() and \
               not member.new_joiner() and \
               not member.more_than_6_duties_in_last_year() and \
               member.can_i_do_this_session(session.session_id) and \
               member.can_i_do_this_date(start) and \
               member.more_than_30_days_since_last_duty(start):
                member.add_duty(member.m_num, session.session_id, start)
                print ("{},{}".format(start, member))
                break

        # print("{}:{}:{}:{}".format(member.m_num,
        #                            member.first_name,
        #                            member.second_name,
        #                            member.num_duties))
# TESTING #
# for member in data.members:
#     if member.m_num == 23:
#         print (member)
#         for ex in member.my_exclusions:
#             print(ex)
#         print(member.can_i_do_this_session('4'))
#         print(member.can_i_do_this_date(datetime(2021, 10, 1)))
#
# for member in data.members:
#     if member.m_num == 3:
#         print (member)
#         print (member.renewed_in_last_18_months())

#for member in data.members:
#    if member.m_num == 279:
#        print (member)
#        print (member.more_than_30_days_since_last_duty(datetime(2018, 3, 30)))
