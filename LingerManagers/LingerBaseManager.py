import logging
from yapsy.PluginManager import PluginManager

class LingerBaseManager(object):
    """LingerBaseManager is the base for all linger mangers"""
    def __init__(self, plugin_path):
        super(LingerBaseManager, self).__init__()
        self.logger = logging.getLogger('Linger')
        self.plugin_path = plugin_path
        self.manager_type = "Base"

        # Loading plugins
        self.plugin_manager = PluginManager()
        self.plugin_manager.setPluginPlaces(self.plugin_path)
        self.plugin_manager.collectPlugins()

        # Creating a dictionary of {Instance type name: respective factory instance}
        self.loaded_plugins_by_types = {plugin.plugin_object.get_instance_name():plugin.plugin_object for plugin in self.plugin_manager.getAllPlugins()}
    
    def get_loaded_plugins_types_names(self):
        return self.loaded_plugins_by_types.keys()
