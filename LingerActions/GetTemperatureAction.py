import LingerActions.LingerBaseAction as lingerActions

class GetTemperatureAction(lingerActions.LingerBaseAction):
    """Getting temperature from the RMPro"""
    def __init__(self, configuration):
        super(GetTemperatureAction, self).__init__(configuration)
        self.rmbridge_adapter_uuid = configuration["rmbridge_adapter_uuid"]
        self.communication_adapter_uuid = configuration["communication_adapter_uuid"]
        
    def rmbridge_adapter(self):
        return self.get_adapter_by_uuid(self.rmbridge_adapter_uuid)

    def communication_adapter(self):
        return self.get_adapter_by_uuid(self.communication_adapter_uuid)

    def act(self, configuration):
        answer = self.rmbridge_adapter().get_temperature()
        self.communication_adapter().send_message("Here is the temperature",str(answer))

class GetTemperatureActionFactory(lingerActions.LingerBaseActionFactory):
    """Base action factory for linger"""
    def __init__(self):
        super(GetTemperatureActionFactory, self).__init__()
        self.item = GetTemperatureAction 

    def get_instance_name(self):
        return "GetTemperatureAction"

    def get_fields(self):
        fields, optional_fields = super(GetTemperatureActionFactory, self).get_fields()
        fields += [("rmbridge_adapter_uuid","Adapters"),
                   ("communication_adapter_uuid","Adapters")]
        return (fields, optional_fields)
