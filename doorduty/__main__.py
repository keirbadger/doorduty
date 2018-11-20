import sys
import argparse
from dateutil.relativedelta import relativedelta

from doorduty.duty import Duty
from doorduty.readdata import ReadData
from datetime import datetime
from datetime import timedelta
from operator import attrgetter

from doorduty.writedata import WriteData


argument_parser = argparse.ArgumentParser('doorduty')
argument_parser.add_argument('--start-date',
                             required=True,
                             help="Start date in the format "
                                  "%%Y-%%m-%%d, i.e . 2018-12-01")
argument_parser.add_argument('--num-months',
                             required=True,
                             help="Number of months to run door duty for")
argument_parser.add_argument('--dry-run',
                             action='store_true',
                             default=False,
                             help="Optional: If set then the duties will "
                                  "not be written to the DB")
arguments = argument_parser.parse_args()


def calc_duties(dry_run=False):
    start = datetime.strptime(arguments.start_date, '%Y-%m-%d')
    stop = start + relativedelta(months=+int(arguments.num_months))
    read_data = ReadData(start)
    write_data = WriteData()

    while start < stop:
        for session in read_data.sessions:
            if start.strftime("%A") == session.day:
                for member in sorted(read_data.members,
                                     key=attrgetter('avg_num_duties'),
                                     reverse=False):
                    if not member.excempt_from_duties() and \
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
                        write_data.add_duty(
                            member.m_num,
                            session.session_id,
                            start)
                        break
        start = start + relativedelta(days=+1)

    if not dry_run:
        write_data.write_duties()
    else:
        print("dry run - DB not updated")

    write_data.close_connection()


# if len(sys.argv) > 1:
#     print("here")
# else:
#     print("there")
calc_duties(arguments.dry_run)


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
