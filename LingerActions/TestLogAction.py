import LingerActions.LingerBaseAction as lingerActions

class TestLogAction(lingerActions.LingerBaseAction):
    """Logging that there was a change in a file"""
    def __init__(self, configuration):
        super(TestLogAction, self).__init__(configuration)
        
        # Fields
        self.log_line = self.configuration['log_line']

    def act(self, configuration):
        self.logger.debug("Action engaged")
        self.logger.info(self.log_line)

class TestLogActionFactory(lingerActions.LingerBaseActionFactory):
    """TestLogActionFactory generates TestLogAction instances"""
    def __init__(self):
        super(TestLogActionFactory, self).__init__()
        self.item = TestLogAction

    def get_instance_name(self):
        return "TestLogAction"

    def get_fields(self):
        fields, optional_fields = super(TestLogActionFactory, self).get_fields()

        fields += [('log_line','string')]

        return (fields,optional_fields)
