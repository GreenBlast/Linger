import LingerActions.LingerBaseAction as lingerActions

class ISpyStopAction(lingerActions.LingerBaseAction):
    """Starting ISpy monitoring"""
    def __init__(self, configuration):
        super(ISpyStopAction, self).__init__(configuration)
        self.ispy_adapter_uuid = configuration["ispy_adapter_uuid"]
        
    def ispy_adapter(self):
        return self.get_adapter_by_uuid(self.ispy_adapter_uuid)

    def act(self, configuration):
        self.logger.debug("Action engaged")
        self.ispy_adapter().alerts_off()
        self.ispy_adapter().shutdown()

class ISpyStopActionFactory(lingerActions.LingerBaseActionFactory):
    """Base action factory for linger"""
    def __init__(self):
        super(ISpyStopActionFactory, self).__init__()
        self.item = ISpyStopAction 

    def get_instance_name(self):
        return "ISpyStopAction"

    def get_fields(self):
        fields, optional_fields = super(ISpyStopActionFactory, self).get_fields()
        fields += [("ispy_adapter_uuid","Adapters")]
        return (fields, optional_fields)
