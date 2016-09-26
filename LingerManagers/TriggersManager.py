from LingerManagers.LingerBaseManager import LingerBaseManager

class TriggersManager(LingerBaseManager):
    """TriggersManager loads possible linger triggers, 
            and manages instances of them according to configuration"""
    def __init__(self, configuration):
        super(TriggersManager, self).__init__(configuration['dir_paths']['Triggers'])
        self.configuration = configuration
        self.trigger_instances = {}
        self.manager_type = "Triggers"

    def start(self):
        for trigger_instance_uuid, trigger_item in self.trigger_instances.iteritems():
            trigger_item.start()

    def stop(self):
        for trigger_instance_uuid, trigger_item in self.trigger_instances.iteritems():
            trigger_item.stop()

    def create_trigger(self, configuration):
        configuration_to_send = configuration.copy()
        configuration_to_send.update(self.configuration)
        trigger_instance = self.loaded_plugins_by_types[configuration["subtype"]].get_instance(configuration_to_send)
        self.trigger_instances[configuration["uuid"]] = trigger_instance

    def register_action_to_trigger(self, trigger_uuid, action):
        self.trigger_instances[trigger_uuid].register_action(action)