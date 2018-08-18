"""
TriggersManager manages the instances of all the triggers in Linger
"""
from future.utils import itervalues
from LingerManagers.LingerBaseManager import LingerBaseManager

class TriggersManager(LingerBaseManager):
    """TriggersManager loads possible linger triggers,
            and manages instances of them according to configuration"""
    def __init__(self, configuration):
        super(TriggersManager, self).__init__(configuration['dir_paths']['Triggers'])
        self.configuration = configuration
        self.manager_type = "Triggers"

    def start(self):
        """
        Start all the triggers
        """
        for trigger_item in itervalues(self.plugin_instances):
            if trigger_item.enabled is True:
                trigger_item.start()

    def stop(self):
        """
        Stops all the triggers
        """
        for trigger_item in itervalues(self.plugin_instances):
            trigger_item.stop()

    def set_enabled(self, trigger_uuid):
        """
        Sets a given trigger as enabled
        """
        self.plugin_instances[trigger_uuid].enabled = True

    def create_trigger(self, configuration):
        """
        Creates a trigger from configuration
        """
        configuration_to_send = configuration.copy()
        configuration_to_send.update(self.configuration)
        trigger_instance = self.loaded_plugins_by_types[configuration["subtype"]].get_instance(configuration_to_send)
        self.plugin_instances[configuration["uuid"]] = trigger_instance

    def register_action_to_trigger(self, trigger_uuid, action):
        """
        Registers an action to be associated with a trigger
        """
        self.plugin_instances[trigger_uuid].register_action(action)

    def get_trigger_labels_of_actions(self, trigger_uuid):
        """
        Returns a labels list of all actions associated with a trigger
        """
        labels = [action.label for action in self.plugin_instances[trigger_uuid].actions.values()]

        return labels
