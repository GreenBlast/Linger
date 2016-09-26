import logging
from yapsy.IPlugin import IPlugin

class LingerItem(object):
    """LingerItem is the base for linger items"""
    def __init__(self, configuration):
        super(LingerItem, self).__init__()
        self.configuration = configuration
        self.logger = logging.getLogger('Linger')
        self.scheduler = self.configuration["scheduler"]
        self.label = self.configuration["label"]
        self.uuid = self.configuration["uuid"]
        self.subtype = self.configuration["subtype"]
        self.get_adapter_by_uuid = self.configuration['get_adapter_by_uuid']
