import LingerActions.LingerBaseAction as lingerActions

class StartACIfTempAction(lingerActions.LingerBaseAction):
    """Starting AC if temperature is above min temperature"""
    def __init__(self, configuration):
        super(StartACIfTempAction, self).__init__(configuration)

        # Fields
        self.rmbridge_adapter_uuid = configuration["rmbridge_adapter_uuid"]
        self.min_temp = float(configuration["min_temp"])
        
    def rmbridge_adapter(self):
        return self.get_adapter_by_uuid(self.rmbridge_adapter_uuid)

    def act(self, configuration):
        current_temp = float(self.rmbridge_adapter().get_temperature())
        self.logger.debug("current temp is: {}, min temp is: {}, should start?: {}".format(current_temp, self.min_temp, current_temp > self.min_temp))
        if current_temp > self.min_temp:
            self.rmbridge_adapter().start_ac()

class StartACIfTempActionFactory(lingerActions.LingerBaseActionFactory):
    """Base action factory for linger"""
    def __init__(self):
        super(StartACIfTempActionFactory, self).__init__()
        self.item = StartACIfTempAction 

    def get_instance_name(self):
        return "StartACIfTempAction"

    def get_fields(self):
        fields, optional_fields = super(StartACIfTempActionFactory, self).get_fields()
        fields += [("rmbridge_adapter_uuid","Adapters"),
                    ("min_temp","float")]
        return (fields, optional_fields)
