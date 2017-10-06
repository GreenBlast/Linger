import LingerActions.LingerBaseAction as lingerActions

# Operation specific imports
import os
import glob
import time

class GetGrabAndSendMailAction(lingerActions.LingerBaseAction):
    """Action for getting snapshot from camera and sending to MailAdapter"""

    CAMERA_ONLINE_TIMEOUT = 5
    MAIL_SUBJECT_DEFAULT = "Grab mail"
    MAIL_TEXT_DEFAULT = "Here"

    def __init__(self, configuration):
        super(GetGrabAndSendMailAction, self).__init__(configuration)

        # Fields
        self.local_ispy_adapter = configuration["local_ispy_adapter"]
        self.remote_ispy_adapter = configuration["remote_ispy_adapter"]
        self.communication_adapter = configuration["communication_adapter"]
        self.snapshots_location = configuration["snapshots_location"]
        self.mail_recipient = configuration["mail_recipient"] 

        # Optional fields
        self.mail_subject = self.configuration.get("patterns", self.MAIL_SUBJECT_DEFAULT)
        self.mail_text = self.configuration.get("ignored_patterns", self.MAIL_TEXT_DEFAULT)
        
    def get_local_ispy_adapter(self):
        return self.get_adapter_by_uuid(self.local_ispy_adapter)

    def get_remote_ispy_adapter(self):
        return self.get_adapter_by_uuid(self.remote_ispy_adapter)

    def get_communication_adapter(self):
        return self.get_adapter_by_uuid(self.communication_adapter)

    def _find_last_picture(self):
        return max(glob.iglob(os.path.join(self.snapshots_location, "*.jpg")), key=os.path.getctime)

    def wait_for_camera_online(self):
        time.sleep(self.CAMERA_ONLINE_TIMEOUT)

    def act(self, configuration=None):
        self.get_remote_ispy_adapter().cam_on()
        self.wait_for_camera_online()

        self.get_local_ispy_adapter().grab_snapshot()
        picture_path = self._find_last_picture()
        self.get_communication_adapter().send_message(self.mail_recipient, self.mail_subject, image_path=picture_path)



class GetGrabAndSendMailActionFactory(lingerActions.LingerBaseActionFactory):
    """Base action factory for linger"""
    def __init__(self):
        super(GetGrabAndSendMailActionFactory, self).__init__()
        self.item = GetGrabAndSendMailAction

    @staticmethod
    def get_instance_name():
        return "GetGrabAndSendMailAction"

    def get_fields(self):
        fields, optional_fields = super(GetGrabAndSendMailActionFactory, self).get_fields()
        
        fields += [("remote_ispy_adapter", "uuid"),
                   ("local_ispy_adapter", "uuid"),
                   ("communication_adapter", "uuid"),
                   ("mail_recipient", "string"),
                   ("snapshots_location", "string")]

        optional_fields += [("mail_text", "string"),
                            ("mail_subject", "string")]

        return fields, optional_fields
