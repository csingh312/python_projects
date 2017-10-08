import os
import pandas as pd
from datetime import datetime, timedelta
from mail import Mailer

class Util(object):
    """ Simple utility class providing commonly used functionality """

    def __init__(self):
        """ Initiates an instance of the utility class  """
        self.now = datetime.now()
    def get_arena_rtb(self):
        return """
                <html>
                <head></head>
                <body>
                    <p><strong>Please see the attached report for the Daily Arena RTB Dashboard Revenue Report</strong><p>
                    <p>Note: This is an automated e-mail. Please do not respond to this message. </p>
                </body>
                </html>
            """
    def send_mail(self, username, password, subject, recipients, body, filename=None):
        """ Sends an email
            Parameters:
            ___________
            self: object currently running
            username: the email user
            password: the email user's password
            subject: The subject of the user's email
            recipients: the recipients of the email
            body: the message body
            filename: the filename of the attachment
        """
        # log.msg ("::: Sending Email  :::", INFO)

        mailer = Mailer(username,password,recipients)
        mailer.send_message(subject,body,filename)
