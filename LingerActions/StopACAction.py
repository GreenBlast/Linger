import LingerActions.LingerBaseAction as lingerActions

class StopACAction(lingerActions.LingerBaseAction):
    """Stops the AC"""
    def __init__(self, configuration):
        super(StopACAction, self).__init__(configuration)
        self.rmbridge_adapter_uuid = configuration["rmbridge_adapter_uuid"]
        
    def rmbridge_adapter(self):
        return self.get_adapter_by_uuid(self.rmbridge_adapter_uuid)

    def act(self, configuration):
        self.rmbridge_adapter().stop_ac()

class StopACActionFactory(lingerActions.LingerBaseActionFactory):
    """Base action factory for linger"""
    def __init__(self):
        super(StopACActionFactory, self).__init__()
        self.item = StopACAction 

    def get_instance_name(self):
        return "StopACAction"

    def get_fields(self):
        fields, optional_fields = super(StopACActionFactory, self).get_fields()
        fields += [("rmbridge_adapter_uuid","Adapters")]
        return (fields, optional_fields)
