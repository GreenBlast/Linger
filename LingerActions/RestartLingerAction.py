import LingerActions.ShutdownLingerAction as shutdownLingerAction

class RestartLingerAction(shutdownLingerAction.ShutdownLingerAction):
    """Restarting linger"""
    def __init__(self, configuration):
        super(RestartLingerAction, self).__init__(configuration)
        self.set_should_restart = self.configuration['set_should_restart']

    def act(self, configuration):
        super(RestartLingerAction, self).act(configuration)
        self.set_should_restart(True)

class RestartLingerActionFactory(shutdownLingerAction.ShutdownLingerActionFactory):
    """RestartLingerActionFactory generates RestartLingerAction instances"""
    def __init__(self):
        super(RestartLingerActionFactory, self).__init__()
        self.item = RestartLingerAction

    def get_instance_name(self):
        return "RestartLingerAction"

    def get_fields(self):
        fields, optional_fields = super(RestartLingerActionFactory, self).get_fields()

        return (fields, optional_fields)
