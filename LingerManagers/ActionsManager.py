from LingerManagers.LingerBaseManager import LingerBaseManager

class ActionsManager(LingerBaseManager):
    """ActionsManager loads linger actions,
            and manages instances of them according to configuration"""
    def __init__(self, configuration):
        super(ActionsManager, self).__init__(configuration['dir_paths']['Actions'])
        self.configuration = configuration
        self.actions_instances = {}
        self.manager_type = "Actions"

    def create_action(self, configuration):
        self.logger.debug("Creating action")
        configuration_to_send = configuration.copy()
        configuration_to_send.update(self.configuration)
        action_instance = self.loaded_plugins_by_types[configuration["subtype"]].get_instance(configuration_to_send)
        self.actions_instances[configuration["uuid"]] = action_instance

    def get_action(self, uuid_of_action):
        return self.actions_instances[uuid_of_action]