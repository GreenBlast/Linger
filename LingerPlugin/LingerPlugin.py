import logging
from yapsy.IPlugin import IPlugin

class InstanceNameNotImplementedException(Exception):
    """InstanceNameNotImplementedException is raised when the derived class didn't implemented the function"""
    pass        

class LingerPlugin(IPlugin):
    """LingerPlugin is the base for linger plugins"""
    def __init__(self):
        super(LingerPlugin, self).__init__()
        self.logger = logging.getLogger('Linger')

    def get_instance_name(self):
        raise InstanceNameNotImplementedException()

    def get_fields(self):
        fields = [
        ("uuid","uuid"),
        ("label","string"),
        ("type","string"),
    	("subtype","string")
    	]
        optional_fields = []
    	return (fields, optional_fields)