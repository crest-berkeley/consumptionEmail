####
import logging as _logging

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formatdate

import matplotlib.pyplot as plt
import numpy as np
import requests
import datetime

from os.path import basename

# create logger
logger = _logging.getLogger('sendEmail')
logger.setLevel(_logging.INFO)
# create console handler and set level to debug
ch = _logging.StreamHandler()
ch.setLevel(_logging.INFO)
# create formatter
formatter = _logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)

# holds web_id's for reuse so only have to look up once.
web_id_cache = {}


# setupPiConnection:

# How long should a get or post wait before timeout in seconds
REQUEST_TIMEOUT_SECS = 2

username = "sensortag_post"
password = "Post2Pi"

PI_WEBAPI_URL = "https://sbb03.eecs.berkeley.edu/piwebapi"

piwebapi_sess = requests.Session()
piwebapi_sess.auth = (username, password)


def build_plot(baseline, current):
    # generate some data

    # let's assume that we are pulling in 15 minute increments
    # The goal of the "baseline" will be to pull the first two weeks, June 18 - July 9

    m = 14 * 24 * 4
    baseline_distribution = np.absolute(np.random.normal(0, 1, m) * np.sin(m))

    n = 7 * 24 * 4
    current_distribution = np.absolute(np.random.normal(1, 1, n) * np.sin(n))

    aggregate_array = [baseline, current]

    x = ["0_Your Baseline", "1_Last week usage"]
    plt.bar(x, aggregate_array)
    plt.savefig('tempImages/bar_plot.png', dpi=300)


def send_mail(send_from, send_to, subject, html, file=None):
    # try:

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(html, 'html'))

    logger.info("Trying to send log files.")

    with open(file, "rb") as fil:
        part = MIMEImage(
            fil.read()
        )
        part.add_header('Content-ID', '<Image>')
        msg.attach(part)

    server = smtplib.SMTP_SSL(host='smtp.gmail.com', port=465, timeout=15)
    server.ehlo()

    # server.login("social.game.CREATE2018@gmail.com", "CREATE123")
    server.login("crestsensor@gmail.com", "vy37F4YNkt")
    logger.info("logged in to smtp server.")

    server.sendmail(send_from, send_to, msg.as_string())
    logger.info("mail sent.")
    server.close()
    # except Exception as e:
    #     logger.warning("Error in send_mail: {0}".format(e))



# Get Web ID for a given element path
# don't bother buil
def get_web_id_for_element(element_path):
    if element_path in web_id_cache:
        web_id = web_id_cache[element_path]
    else:
        req = piwebapi_sess.get("{0}/elements?path={1}".format(PI_WEBAPI_URL, element_path),
                                verify=True, timeout=REQUEST_TIMEOUT_SECS)
        if req.status_code == requests.codes.ok:
            web_id = req.json()['WebId']
            web_id_cache[element_path] = web_id
        else:
            web_id = ''
    return web_id



def get_resource_history(start_dt=None, end_dt=None, interval=1800, measures=['temp_actual'],
                         resource_code='cory_406_zone_a'):
    logger.debug('starting: get_resource_history')

    if start_dt is None:
        start_dt = datetime.datetime.now(tz=dth.current_tz) - datetime.timedelta(days=1)
    if end_dt is None:
        end_dt = start_dt + datetime.timedelta(days=1)

    start_pits = dth.pi_timestamp_from_datetime(start_dt)
    stop_pits = dth.pi_timestamp_from_datetime(end_dt)

    # format wont substitute if no {} tokens in string
    web_id = Utils.get_web_id_from_resource_code(resource_code, 'Temperature')
    req = piwebapi_sess.get(
        "{0}/streams/{1}/interpolated?interval={2}s&startTime={3}&endTime={4}".format(PI_WEBAPI_URL, web_id,
                                                                                      interval,
                                                                                      start_pits,
                                                                                      stop_pits),
        verify=True)
    data = req.json()['Items']

    all_dict = dict()
    all_dict['value'] = []

    for item in data:
        if item['Good']:
            all_dict['value'].append(item['Value'])
    all_dict['start_time'] = dth.unix_time(start_dt)
    all_dict['interval'] = interval

    all_dict['result'] = 'success'

    return all_dict


message = '<b>Some <i>HTML</i> text</b> and an image.<br><img src="cid:Image" width="300"><br>Nifty!'

# send_mail("crestsensor@gmail.com", "chriswhsu@berkeley.edu", "Hello", message, 'images/00.png')
build_plot(400, 250)
send_mail("crestsensor@gmail.com", "chriswhsu@berkeley.edu", "Hello", message, 'tempImages/bar_plot.png')