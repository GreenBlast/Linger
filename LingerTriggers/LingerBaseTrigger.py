"""
Base implementation of a trigger for Linger
"""
from LingerPlugin.LingerPlugin import LingerPlugin
from LingerPlugin.LingerItem import LingerItem

class LingerBaseTrigger(LingerItem):
    """Base trigger for Linger"""
    def __init__(self, configuration):
        super(LingerBaseTrigger, self).__init__(configuration)
        self.trigger_callback = configuration['trigger_callback']
        self.trigger_specific_action_callback = configuration['trigger_specific_action_callback']
        self.actions = {}
        self.enabled = False

    def trigger_engaged(self, command=None):
        """Engaging trigger, most of the time should call the respective action"""
        self.logger.debug("trigger_engaged, command is %s", command)

    def start(self):
        """
        Start watch for triggered events
        """
        pass

    def stop(self):
        """
        Stop watch for triggered events
        """
        pass

    def register_action(self, action):
        """
        Associate an action with the trigger
        """
        self.actions[action.uuid] = action

class LingerBaseTriggerFactory(LingerPlugin):
    """Base trigger factory for linger"""
    def __init__(self):
        super(LingerBaseTriggerFactory, self).__init__()
        self.item = LingerBaseTrigger

    def get_fields(self):
        fields, optional_fields = super(LingerBaseTriggerFactory, self).get_fields()
        return (fields, optional_fields)
