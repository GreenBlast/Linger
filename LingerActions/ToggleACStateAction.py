import LingerActions.LingerBaseAction as lingerActions

class ToggleACStateAction(lingerActions.LingerBaseAction):
    """Toggles the AC state in the rmbridge adapter"""
    def __init__(self, configuration):
        super(ToggleACStateAction, self).__init__(configuration)
        self.rmbridge_adapter_uuid = configuration["rmbridge_adapter_uuid"]
        
    def rmbridge_adapter(self):
        return self.get_adapter_by_uuid(self.rmbridge_adapter_uuid)

    def act(self, configuration):
        self.rmbridge_adapter().toggle_ac_status()

class ToggleACStateActionFactory(lingerActions.LingerBaseActionFactory):
    """Base action factory for linger"""
    def __init__(self):
        super(ToggleACStateActionFactory, self).__init__()
        self.item = ToggleACStateAction 

    def get_instance_name(self):
        return "ToggleACStateAction"

    def get_fields(self):
        fields, optional_fields = super(ToggleACStateActionFactory, self).get_fields()
        fields += [("rmbridge_adapter_uuid","Adapters")]
        return (fields, optional_fields)
