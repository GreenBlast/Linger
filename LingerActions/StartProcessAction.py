import LingerActions.LingerBaseAction as lingerActions

class StartProcessAction(lingerActions.LingerBaseAction):
    """Logging that there was a change in a file"""
    def __init__(self, configuration):
        super(StartProcessAction, self).__init__(configuration)
        
        # Fields
        self.process_adapter = self.configuration['process_adapter']

    def get_process_adapter(self):
        return self.get_adapter_by_uuid(self.process_adapter)

    def act(self, configuration):
        self.get_process_adapter().start_process()

class StartProcessActionFactory(lingerActions.LingerBaseActionFactory):
    """StartProcessActionFactory generates StartProcessAction instances"""
    def __init__(self):
        super(StartProcessActionFactory, self).__init__()
        self.item = StartProcessAction

    def get_instance_name(self):
        return "StartProcessAction"

    def get_fields(self):
        fields, optional_fields = super(StartProcessActionFactory, self).get_fields()

        fields += [('process_adapter','uuid')]

        return (fields, optional_fields)
