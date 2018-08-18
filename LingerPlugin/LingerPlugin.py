"""
LingerPlugin is the base plugin for Linger plugins infrastructure
"""
import logging
from yapsy.IPlugin import IPlugin

from LingerPlugin.LingerItem import LingerItem


class InstanceNameNotImplementedException(Exception):
    """InstanceNameNotImplementedException is raised when the derived class didn't implemented the function"""
    pass


class LingerPlugin(IPlugin):
    """LingerPlugin is the base for linger plugins"""
    def __init__(self):
        super(LingerPlugin, self).__init__()
        self.logger = logging.getLogger('Linger')
        self.item = LingerItem

    @staticmethod
    def get_instance_name():
        """Returns instance name"""
        raise InstanceNameNotImplementedException()

    def get_instance(self, configuration):
        """
        Return an instance of the item for the given configuration
        """
        return self.item(configuration)

    @staticmethod
    def get_fields():
        """
        Returns the fields of the item
        """
        fields = [("uuid", "uuid"),
                  ("label", "string"),
                  ("type", "string"),
                  ("subtype", "string")]
        optional_fields = []
        return fields, optional_fields
