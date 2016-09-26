from LingerManagers.LingerBaseManager import LingerBaseManager

class AdaptersManager(LingerBaseManager):
    """AdaptersManager loads linger adapters, 
            and manages instances of them according to configuration"""
    def __init__(self, configuration):
        super(AdaptersManager, self).__init__(configuration['dir_paths']['Adapters'])
        self.configuration = configuration
        self.adapters_instances = {}
        self.manager_type = "Adapters"

    def create_adapter(self, configuration):
        configuration_to_send = configuration.copy()
        configuration_to_send.update(self.configuration)
        adapter_instance = self.loaded_plugins_by_types[configuration["subtype"]].get_instance(configuration_to_send)
        self.adapters_instances[configuration["uuid"]] = adapter_instance

    def get_adapter_by_uuid(self, uuid_of_adapter):
        return self.adapters_instances[uuid_of_adapter]