import logging
from LingerPlugin.LingerPlugin import LingerPlugin
from LingerPlugin.LingerItem import LingerItem

class LingerBaseTrigger(LingerItem):
    """Base trigger for linger"""
    def __init__(self, configuration):
        super(LingerBaseTrigger, self).__init__(configuration)
        self.trigger_callback = configuration['trigger_callback']        
        self.trigger_specific_action_callback = configuration['trigger_specific_action_callback']        
        self.actions = {}

    def trigger_engaged(self):
        self.logger.debug("trigger_engaged")

    def start(self):
        pass

    def stop(self):
        pass

    def register_action(self, action):
        self.actions[action.uuid] = action

class LingerBaseTriggerFactory(LingerPlugin):
    """Base trigger factory for linger"""
    def __init__(self):
        super(LingerBaseTriggerFactory, self).__init__()
        self.item = LingerBaseTrigger

    def get_instance(self, configuration):
        return self.item(configuration)

    def get_fields(self):
        fields, optional_fields = super(LingerBaseTriggerFactory, self).get_fields()
        return (fields, optional_fields)

