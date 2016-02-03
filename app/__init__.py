"""
config.py: Application initialization

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""
from flask import Flask
from flask.ext.mail import Mail
from flask.ext.babel import Babel
import config
import logging
import logging.handlers


class TlsSMTPHandler(logging.handlers.SMTPHandler):
    """
    Subclass of SMTPHandler. Allows TLS communcation with the GMail servers
    Used for sending errors by email
    """

    def emit(self, record):
        """
        Emit a record.
        Format the record and send it to the specified addressees.
        :param record: the record to be emitted
        """
        # noinspection PyBroadException
        try:
            import smtplib
            try:
                from email.utils import formatdate
            except ImportError:
                formatdate = self.date_time
            port = self.mailport
            if not port:
                port = smtplib.SMTP_PORT
            smtp = smtplib.SMTP(self.mailhost, port)
            msg = self.format(record)
            msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (
                self.fromaddr,
                ",".join(self.toaddrs),
                self.getSubject(record),
                formatdate(), msg)
            if self.username:
                smtp.ehlo()  # for tls add this line
                smtp.starttls()  # for tls add this line
                smtp.ehlo()  # for tls add this line
                smtp.login(self.username, self.password)
            smtp.sendmail(self.fromaddr, self.toaddrs, msg)
            smtp.quit()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
"""
=================================================== App Initilization ====================================
"""


app = Flask(__name__)

# For session security
app.secret_key = 'F12Zr47jyX R~X@H!jmM]Lwf/,?KT'

app.config.from_object('config')

# Flask-Mail
mail = Mail(app)

# Flask-Babel
babel = Babel(app)

# Error Handling (send email)

if not app.debug and config.MAIL_SERVER != '':
    credentials = None

    if config.MAIL_USERNAME or config.MAIL_PASSWORD:
        credentials = (config.MAIL_USERNAME, config.MAIL_PASSWORD)

    mail_handler = TlsSMTPHandler(("smtp.gmail.com", 587),
                                  'no-reply@' + config.MAIL_SERVER, config.ADMINS,
                                  '[asmaislidas] Application error', credentials)

    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)


from app import views
