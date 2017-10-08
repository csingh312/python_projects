from email import Encoders
from email.mime.multipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.mime.text import MIMEText
import logging
import os
logger = logging.getLogger(__name__)
import smtplib

from jinja2 import Environment, FileSystemLoader


class Mailer(object):
    """ General purpose electronic mailer for the discrepancy package
    Args:
        object: A mailer object
    """

    def __init__(self, user, password, _recipients, templatedir='templates'):
        """ Initializes Mailer class with the email account credentials and recipient information
        Args:
            self: object currently running
            user: the email user
            password: the email password
            _recipients: the list of email recipients
        """

        self.user = user
        self.password = password
        self.recipient = _recipients if type (_recipients) is list else [_recipients]
        self.server = 'smtp.gmail.com'
        self.port = 587

        if os.path.isdir(templatedir):
            self.templatedir = templatedir
        else:
            self.templatedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), templatedir)

        self.env = Environment(loader=FileSystemLoader(self.templatedir))
    
    def send_message(self, subject, body, filename=None):
        """ Sends the email message with subject to recipients
        Args:
            self: object currently running
            subject: the email subject
            body: the email body
        """
        session = smtplib.SMTP(self.server, self.port)
        session.set_debuglevel(0)
        session.ehlo()
        session.starttls()
        session.ehlo
        session.login(self.user, self.password)

        msg = MIMEMultipart('alternative')
        msg['To'] = ",".join(self.recipient)
        msg['From'] = self.user
        msg['Subject'] = subject

        part = MIMEText(body, 'html')
        msg.attach(part)


        if filename is not None:
            directory = '/tmp'
            path = os.path.join(directory, filename)
            part = MIMEBase('application', "octet-stream")
            part.set_payload( open(path,"rb").read() )
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(filename))
            msg.attach(part)
        try:
            session.sendmail(self.user,self.recipient,msg.as_string())
            session.close()
        except Exception, e:
            logging.error("::: An exception occurred while trying to send mail.", exc_info=True)
            logging.error("::: Closing the mail session :::")
            self.session = None

    def render(self, data, template):
        template = template + ".tmpl"
        logger.debug("Rendering template '%s'" % (template))
        text = self.env.get_template(template)
        msg = text.render(data)
        return msg
