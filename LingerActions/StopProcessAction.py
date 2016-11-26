import LingerActions.LingerBaseAction as lingerActions

class StopProcessAction(lingerActions.LingerBaseAction):
    """Logging that there was a change in a file"""
    def __init__(self, configuration):
        super(StopProcessAction, self).__init__(configuration)
        
        # Fields
        self.process_adapter = self.configuration['process_adapter']

    def get_process_adapter(self):
        return self.get_adapter_by_uuid(self.process_adapter)

    def act(self, configuration):
        self.get_process_adapter().stop_process()

class StopProcessActionFactory(lingerActions.LingerBaseActionFactory):
    """StopProcessActionFactory generates StopProcessAction instances"""
    def __init__(self):
        super(StopProcessActionFactory, self).__init__()
        self.item = StopProcessAction

    def get_instance_name(self):
        return "StopProcessAction"

    def get_fields(self):
        fields, optional_fields = super(StopProcessActionFactory, self).get_fields()

        fields += [('process_adapter','uuid')]

        return (fields,optional_fields)
