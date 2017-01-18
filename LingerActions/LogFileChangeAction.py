import LingerActions.LingerBaseAction as lingerActions

class LogFileChangeAction(lingerActions.LingerBaseAction):
    """Logging that there was a change in a file"""
    def __init__(self, configuration):
        super(LogFileChangeAction, self).__init__(configuration)
        self.log_adapter_uuid = configuration["log_adapter_uuid"]
        
    def log_adapter(self):
        return self.get_adapter_by_uuid(self.log_adapter_uuid)

    def act(self, configuration):
        self.logger.debug("Action engaged")
        log_line = "File changed: %s\nChange was:%s\n" % (configuration["src_path"], configuration["event_type"])
        self.log_adapter().log(log_line)

class LogFileChangeActionFactory(lingerActions.LingerBaseActionFactory):
    """LogFileChangeActionFactory generates LogFileChangeAction instances"""
    def __init__(self):
        super(LogFileChangeActionFactory, self).__init__()
        self.item = LogFileChangeAction

    def get_instance_name(self):
        return "LogFileChangeAction"

    def get_fields(self):
        fields, optional_fields = super(LogFileChangeActionFactory, self).get_fields()
        fields += [("log_adapter_uuid","Adapters")]
        return (fields, optional_fields)
