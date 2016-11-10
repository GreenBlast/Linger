import LingerActions.LingerBaseAction as lingerActions

# Operation specific imports
import subprocess
import shlex

class ShellCommandAction(lingerActions.LingerBaseAction):
    """Starting ISpy monitoring"""
    def __init__(self, configuration):
        super(ShellCommandAction, self).__init__(configuration)
        
        # Fields
        self.command =  configuration["command"]

        self.parsed_command = shlex.split(self.command)

    def act(self, configuration):
        self.logger.debug("Action engaged")
        result = subprocess.call(self.parsed_command)
        self.logger.info("command exited with result:{}".format(result))

class ShellCommandActionFactory(lingerActions.LingerBaseActionFactory):
    """Base action factory for linger"""
    def __init__(self):
        super(ShellCommandActionFactory, self).__init__()
        self.item = ShellCommandAction 

    def get_instance_name(self):
        return "ShellCommandAction"

    def get_fields(self):
        fields, optional_fields = super(ShellCommandActionFactory, self).get_fields()
        fields += [("command","string")]
        return (fields, optional_fields)
