"""
config.py: Application initialization

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""
from flask import Flask
from flask.ext.mail import Mail
from flask.ext.babel import Babel
from flask.json import JSONEncoder as BaseEncoder
from speaklater import _LazyString
from app.aml_config import ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
import logging
import logging.handlers

"""
=================================================== Custom Config Classes ====================================
"""


class JSONEncoder(BaseEncoder):
    """
    Subclass of BaseEncoder. Allows Flask-Babel lazy_gettext to render error messages on WTForms.
    """

    def default(self, o):
        if isinstance(o, _LazyString):
            return str(o)
        return BaseEncoder.default(self, o)


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

# Load Configurations
app.config.from_pyfile('aml_config.py')

# Flask-Mail
mail = Mail(app)

# Flask-Babel
babel = Babel(app)

# Custom JSON Serializer (necessary for Flask-Babel lazy_gettext to work)
app.json_encoder = JSONEncoder

# Error Handling (send email)
if not app.debug and MAIL_SERVER != '':
    credentials = None

    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)

    mail_handler = TlsSMTPHandler(("smtp.gmail.com", 587),
                                  'no-reply@' + MAIL_SERVER, ADMINS,
                                  '[asmaislidas] Application error', credentials)

    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

from app import views
