import LingerActions.LingerBaseAction as lingerActions

class NotifyAction(lingerActions.LingerBaseAction):
    """Starting ISpy monitoring"""
    def __init__(self, configuration):
        super(NotifyAction, self).__init__(configuration)

        # Fields 
        self.notify_adapter_uuid = configuration["notify_adapter_uuid"]
        self.message_subject = configuration["message_subject"]
        self.message_text = configuration["message_text"]

    def notify_adapter(self):
        return self.get_adapter_by_uuid(self.notify_adapter_uuid)

    def act(self, configuration):
        self.logger.debug("Action engaged")
        self.notify_adapter().send_message(self.message_subject,self.message_text)

class NotifyActionFactory(lingerActions.LingerBaseActionFactory):
    """Base action factory for linger"""
    def __init__(self):
        super(NotifyActionFactory, self).__init__()
        self.item = NotifyAction 

    def get_instance_name(self):
        return "NotifyAction"

    def get_fields(self):
        fields, optional_fields = super(NotifyActionFactory, self).get_fields()
        fields += [("notify_adapter_uuid","Adapters")]
        return (fields, optional_fields)
