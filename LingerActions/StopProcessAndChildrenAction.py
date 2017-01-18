import LingerActions.LingerBaseAction as lingerActions

class StopProcessAndChildrenAction(lingerActions.LingerBaseAction):
    """Logging that there was a change in a file"""
    def __init__(self, configuration):
        super(StopProcessAndChildrenAction, self).__init__(configuration)
        
        # Fields
        self.process_adapter = self.configuration['process_adapter']

    def get_process_adapter(self):
        return self.get_adapter_by_uuid(self.process_adapter)

    def act(self, configuration):
        self.logger.debug("In Stop Children action")
        self.get_process_adapter().stop_with_all_children()

class StopProcessAndChildrenActionFactory(lingerActions.LingerBaseActionFactory):
    """StopProcessAndChildrenActionFactory generates StopProcessAndChildrenAction instances"""
    def __init__(self):
        super(StopProcessAndChildrenActionFactory, self).__init__()
        self.item = StopProcessAndChildrenAction

    def get_instance_name(self):
        return "StopProcessAndChildrenAction"

    def get_fields(self):
        fields, optional_fields = super(StopProcessAndChildrenActionFactory, self).get_fields()

        fields += [('process_adapter','uuid')]

        return (fields, optional_fields)
