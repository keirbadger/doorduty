from doorduty.duty import Duty
from doorduty.readdata import ReadData
from datetime import datetime
from datetime import timedelta
from operator import attrgetter
import sys

from doorduty.writedata import WriteData


def calc_duties():
    start = datetime(2018, 6, 1)
    stop = datetime(2018, 9, 1)
    read_data = ReadData()
    write_data = WriteData()

    while start < stop:
        for session in read_data.sessions:
            for member in sorted(read_data.members, key=attrgetter('avg_num_duties'), reverse=False):
                if start.strftime("%A") == session.day and \
                   not member.excempt_from_duties() and \
                   member.renewed_in_last_18_months(start) and \
                   not member.new_joiner(start) and \
                   not member.more_than_6_duties_in_last_year(start) and \
                   member.can_i_do_this_session(session.session_id) and \
                   member.can_i_do_this_date(start) and \
                   member.more_than_50_days_since_last_duty(start):
                    print("{},{},{},{},{}".format(
                        start.strftime("%d/%m/%Y"),
                        session.day,
                        session.start_time,
                        session.end_time,
                        member))
                    member.add_duty(member.m_num, session.session_id, start)
                    #max DUTYID before running this 12421
                    write_data.add_duty(member.m_num, session.session_id, start)
                    break
        start = start + timedelta(days=1)

    write_data.write_duties()
    write_data.close_connection()


if len(sys.argv) > 1:
    print("here")
else:
    print("there")
    calc_duties()


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
#
# for member in data.members:
#    if member.m_num == 279:
#        print (member)
#        print (member.more_than_30_days_since_last_duty(datetime(2018, 3, 30)))
