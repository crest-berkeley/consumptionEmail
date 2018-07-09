####
import logging as _logging

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formatdate

import matplotlib.pyplot as plt
import numpy as np

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


message = '<b>Some <i>HTML</i> text</b> and an image.<br><img src="cid:Image" width="300"><br>Nifty!'

# send_mail("crestsensor@gmail.com", "chriswhsu@berkeley.edu", "Hello", message, 'images/00.png')
build_plot(400, 250)
send_mail("crestsensor@gmail.com", "chriswhsu@berkeley.edu", "Hello", message, 'tempImages/bar_plot.png')