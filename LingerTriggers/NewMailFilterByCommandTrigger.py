"""
NewMailFilterByCommandTrigger triggers by mail and calls action with the label in the received mail
"""
# Operation specific imports
import json
from collections import defaultdict
from email.header import decode_header
import ast

import LingerTriggers.LingerBaseTrigger as lingerTriggers

class NewMailFilterByCommandTrigger(lingerTriggers.LingerBaseTrigger):
    """
    Trigger that engaged when a new mail is recieved
        and calls an action with the label recieved in the message
    """
    def __init__(self, configuration):
        super(NewMailFilterByCommandTrigger, self).__init__(configuration)
        self.subscription_id = None
        self.actions_by_labels = defaultdict(list)
        # Fields
        self.mail_adapter_uuid = configuration["mail_adapter"]
        self.subject_to_filter = configuration["subject_to_filter"]
        # TODO this should be already a list in the configuration system
        self.authorized_keys = ast.literal_eval(configuration["authorized_keys"])

        # Optional fields
        self.logger.debug("NewMailFilterByCommandTrigger initialized")

    def mail_adapter(self):
        """
        Getter for the mail adapter
        """
        return self.get_adapter_by_uuid(self.mail_adapter_uuid)

    def trigger_check_condition(self, mail):
        """
        Checking if trigger should call action
        """
        mail_details = json.loads(mail.get_payload())
        subject = decode_header(mail['subject'])[0][0]
        command = mail_details["command"]
        password = mail_details["secret"]
        self.logger.debug("Got mail with subject: %s command is: %s password is: %s", subject, command, password)
        # TODO should use password to make sure that the user is authorized to this action/trigger
        if subject == self.subject_to_filter:
            if password in self.authorized_keys:
                if command in self.actions_by_labels.keys():
                    self.trigger_engaged(command)

    def trigger_engaged(self, command): # Command shouldn't be None pylint: disable=w0222
        trigger_data = {}
        for action in self.actions_by_labels[command]:
            self.trigger_specific_action_callback(self.uuid, action.uuid, trigger_data)

    def start(self):
        self.subscription_id = self.mail_adapter().subscribe_for_new_mails(self.trigger_check_condition)
        self.logger.info("command string is: {%s}", ",".join(["\"{}\":\"{}\"".format(x, x) for x in self.actions_by_labels.keys()]))

    def stop(self):
        if self.subscription_id != None:
            self.mail_adapter().unsubscribe(self.subscription_id)

        self.subscription_id = None

    def register_action(self, action):
        super(NewMailFilterByCommandTrigger, self).register_action(action)
        self.actions_by_labels[action.label] += [action]

class NewMailFilterByCommandTriggerFactory(lingerTriggers.LingerBaseTriggerFactory):
    """NewMailFilterByCommandTriggerFactory generates NewMailFilterByCommandTrigger instances"""
    def __init__(self):
        super(NewMailFilterByCommandTriggerFactory, self).__init__()
        self.item = NewMailFilterByCommandTrigger

    @staticmethod
    def get_instance_name():
        """Returns instance name"""
        return "NewMailFilterByCommandTrigger"

    def get_fields(self):
        fields, optional_fields = super(NewMailFilterByCommandTriggerFactory, self).get_fields()

        fields += [('mail_adapter', 'uuid'),
                   ('subject_to_filter', 'string'),
                   ('authorized_keys', ('array', 'string'))]

        return (fields, optional_fields)
