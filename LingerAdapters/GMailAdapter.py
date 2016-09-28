import LingerAdapters.LingerBaseAdapter as lingerAdapters 

# Operation specific imports
import imaplib
import smtplib
import email
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import re
import uuid
import os

class GMailAdapter(lingerAdapters.LingerBaseAdapter):
    """GMailAdapter ables sending mails"""

    def __init__(self, configuration):
        super(GMailAdapter, self).__init__(configuration)
        self.logger.debug("GMailAdapter started")

        self.scheduled_job = None
        self.subscribers_dict = {}
        self.find_uid_reg = re.compile(r"""\(UID\ (?P<UID>\d+)\)""")
        
        # fields
        self._gmail_user = self.configuration["gmail_user"]
        self._gmail_password = self.configuration["gmail_password"]
        self.interval = float(self.configuration["intervalSec"])

        self.logger.info("GMailAdapter configured with user=%s" % (self._gmail_user,))



    def connect_to_imap_server(self):
        self.imap_server = imaplib.IMAP4_SSL("imap.gmail.com",993)
        self.imap_server.login(self._gmail_user, self._gmail_password)

    def disconnect_from_imap_server(self):
        self.imap_server().close()
        self.imap_server().logout()


    def subscribe_for_new_mails(self, callback):
        subscription_uuid = uuid.uuid4()
        
        # If it's the first time we are connecting
        if self.subscribers_dict == {}:
            self.start_monitor_mails()

        self.subscribers_dict[subscription_uuid] = callback
        return subscription_uuid

    def unsubscribe(self, subscription_uuid):
        del self.subscribers_dict[subscription_uuid]

        # If it's the first time we are connecting
        if self.subscribers_dict == {}:
            self.stop_monitor_mails()

    def start_monitor_mails(self):
        self.connect_to_imap_server()
        self.last_uid = self.get_last_uid()
        self.scheduled_job = self.scheduler.add_job(self.monitor_new_mails, 'interval', seconds=self.interval)

    def stop_monitor_mails(self):
        if self.scheduled_job != None:
            self.scheduled_job.remove()
        
        self.imap_server.close()
            
    def get_last_uid(self):
        # Getting last uid
        _, last_message  = self.imap_server.select('INBOX')
        _, last_message_uid_info = self.imap_server.fetch(last_message[0], '(UID)')
        
        last_uid = self.find_uid_reg.findall(last_message_uid_info[0])[0]

        return last_uid

    def monitor_new_mails(self):
        update_uid_flag = False
        try:
            _, last_message  = self.imap_server.select('INBOX')
        except Exception, e:
            self.connect_to_imap_server()
            _, last_message  = self.imap_server.select('INBOX')

        result, data = self.imap_server.uid('search', None, 'UID', self.last_uid + ':*')
        messages = data[0].split()

        int_last_uid = int(self.last_uid)
        mail_list = []
        for message_uid in messages:
            # SEARCH command *always* returns at least the most
            # recent message, even if it has already been synced
            if int(message_uid) > int_last_uid:
                update_uid_flag = True
                result, data = self.imap_server.uid('fetch', message_uid, '(RFC822)')
                mail_list.append(data[0][1])

        if update_uid_flag:
            self.last_uid = self.get_last_uid()
            update_uid_flag = False

        for mail in mail_list:
            for subscriber_callback in self.subscribers_dict.itervalues():
                subscriber_callback(email.message_from_string(mail))


    def send_mail(self, to, subject, text, attach_image_path = None):
        message = MIMEMultipart()

        message['From'] = self._gmail_user
        message['To'] = to
        message['Subject'] = subject

        message.attach(MIMEText(text))

        if attach_image_path is not None:
            image_part = MIMEBase('application', 'octet-stream')
            image_part.set_payload(open(attach_image_path, 'rb').read())
            Encoders.encode_base64(image_part)
            image_part.add_header('Content-Disposition',
                                  'attachment; filename="%s"' % os.path.basename(attach_image_path))
            message.attach(image_part)
            
        mailServer = smtplib.SMTP("smtp.gmail.com", 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(self._gmail_user, self._gmail_password)
        mailServer.sendmail(self._gmail_user, to, message.as_string())
        mailServer.quit()

class GMailAdapterFactory(lingerAdapters.LingerBaseAdapterFactory):
    """GMailAdapterFactory generates GMailAdapter instances"""
    def __init__(self):
        super(GMailAdapterFactory, self).__init__()
        self.item = GMailAdapter 
    
    def get_instance_name(self):
        return "GMailAdapter"

    def get_fields(self):
        fields, optional_fields = super(GMailAdapterFactory, self).get_fields()

        fields += [('gmail_user',"string"),
                    ('gmail_password',"string"),
                    ("intervalSec","float"),
                    ]
        return (fields,optional_fields)
