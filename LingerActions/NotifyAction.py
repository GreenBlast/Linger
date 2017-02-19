"""
NotifyAction notifies the user given a communication adapter
"""
import LingerActions.LingerBaseAction as lingerActions

class NotifyAction(lingerActions.LingerBaseAction):
    """Starting ISpy monitoring"""
    def __init__(self, configuration):
        super(NotifyAction, self).__init__(configuration)

        # Fields
        self.communication_adapter_uuid = configuration["communication_adapter_uuid"]
        self.message_subject = configuration["message_subject"]
        self.message_text = configuration["message_text"]

    def communication_adapter(self):
        """
        Getter for the communication adapter
        """
        return self.get_adapter_by_uuid(self.communication_adapter_uuid)

    def act(self, configuration=None):
        self.logger.debug("Action engaged")
        self.communication_adapter().send_message(self.message_subject, self.message_text)

class NotifyActionFactory(lingerActions.LingerBaseActionFactory):
    """Base action factory for linger"""
    def __init__(self):
        super(NotifyActionFactory, self).__init__()
        self.item = NotifyAction

    @staticmethod
    def get_instance_name():
        """Returns instance name"""
        return "NotifyAction"

    def get_fields(self):
        fields, optional_fields = super(NotifyActionFactory, self).get_fields()
        fields += [("communication_adapter_uuid", "Adapters")]
        return (fields, optional_fields)
