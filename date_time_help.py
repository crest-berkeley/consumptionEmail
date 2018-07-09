__author__ = 'chriswhsu'

import time
import datetime

import pytz
import re

utc = pytz.utc

pacific = pytz.timezone('US/Pacific')
singapore = pytz.timezone('Asia/Singapore')



# TODO flesh this out with intelligent derivation of timezone
current_tz = singapore


def curr_tz():
    return current_tz


def trunc_date_for_datetime(my_datetime):
    return datetime.date(year=my_datetime.year, month=my_datetime.month, day=my_datetime.day)


def gmt_date_for_ts(ts):
    utc_datetime = datetime.datetime.fromtimestamp(ts, utc)
    return utc_datetime.replace(hour=0, minute=0, second=0, microsecond=0)


def gmt_date():
    ts = time.time()
    return gmt_date_for_ts(ts)


def unix_time_from_date(date, tz=utc):
    dt = datetime.datetime(date.year, date.month, date.day, tzinfo=tz)
    return unix_time(dt)


def unix_time(dt):
    epoch = datetime.datetime.fromtimestamp(timestamp=0, tz=utc)
    delta = dt - epoch
    return delta.total_seconds()


def unix_time_from_date_millis(date, tz=utc):
    dt = datetime.datetime(date.year, date.month, date.day, tzinfo=tz)
    return unix_time_millis(dt)


def unix_time_millis(dt):
    return unix_time(dt) * 1000.0


def days_in_sec(days):
    return days * 24 * 60 * 60


def now_date(timezone=None):
    now = datetime.datetime.now(tz=timezone)
    return datetime.date(now.year, now.month, now.day)


def local_datetime_from_str(datetime_str):
    return current_tz.localize(datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M'))


def local_date_from_str(datetime_str):
    return current_tz.localize(datetime.datetime.strptime(datetime_str, '%Y-%m-%d'))


def now_utc_tz():
    return datetime.datetime.now(tz=pytz.utc)


def now_cur_tz():
    return datetime.datetime.now(tz=current_tz)


def now_time_cur_tz():
    date_time =  datetime.datetime.now(tz=current_tz)
    return datetime.time(hour=date_time.hour, minute=date_time.minute, second=date_time.second, microsecond=date_time.microsecond)


def now_cur_tz_trunc():
    return trunc_date_for_datetime(now_cur_tz())


def datetime_from_pi_timestamp(timestamp):
    timestamp = re.split("\.", timestamp)[0]  # Removes microseconds for consistency
    timestamp = re.split("Z", timestamp)[0]  # Removes Z for consistency if it exists
    return current_tz.normalize(pytz.utc.localize(datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')))


def pi_timestamp_from_datetime(the_datetime):
    return utc.normalize(the_datetime, utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def start_datetime_from_date(date, tz):
    return tz.localize(datetime.datetime(date.year, date.month, date.day))


def end_datetime_from_date(date, tz):
    return tz.localize(datetime.datetime(date.year, date.month, date.day, hour=23, minute=59, second=59, microsecond=999999))


def end_of_time():
    return datetime.datetime(9999, 12, 31, tzinfo=current_tz)


def end_of_time_trunc():
    return trunc_date_for_datetime(end_of_time())