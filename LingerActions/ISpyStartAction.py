import LingerActions.LingerBaseAction as lingerActions

class ISpyStartAction(lingerActions.LingerBaseAction):
    """Starting ISpy monitoring"""
    def __init__(self, configuration,):
        super(ISpyStartAction, self).__init__(configuration)
        self.ispy_adapter_uuid = configuration["ispy_adapter_uuid"]
        
    def ispy_adapter(self):
        return self.get_adapter_by_uuid(self.ispy_adapter_uuid)

    def act(self, configuration):
        self.logger.debug("Action engaged")
        self.ispy_adapter().alerts_on()
        self.ispy_adapter().all_on()

class ISpyStartActionFactory(lingerActions.LingerBaseActionFactory):
    """Base action factory for linger"""
    def __init__(self):
        super(ISpyStartActionFactory, self).__init__()
        self.item = ISpyStartAction

    def get_instance_name(self):
        return "ISpyStartAction"

    def get_fields(self):
        fields, optional_fields = super(ISpyStartActionFactory, self).get_fields()
        fields += [("ispy_adapter_uuid","Adapters")]
        return (fields, optional_fields)
