import LingerActions.LingerBaseAction as lingerActions

class ShutdownLingerAction(lingerActions.LingerBaseAction):
    """Shutting down linger"""
    def __init__(self, configuration):
        super(ShutdownLingerAction, self).__init__(configuration)
        self.shutdown = self.configuration['shutdown']

    def act(self, configuration):
        self.logger.debug("Action engaged")
        self.shutdown()

class ShutdownLingerActionFactory(lingerActions.LingerBaseActionFactory):
    """ShutdownLingerActionFactory generates ShutdownLingerAction instances"""
    def __init__(self):
        super(ShutdownLingerActionFactory, self).__init__()
        self.item = ShutdownLingerAction

    def get_instance_name(self):
        return "ShutdownLingerAction"

    def get_fields(self):
        fields, optional_fields = super(ShutdownLingerActionFactory, self).get_fields()

        return (fields,optional_fields)
