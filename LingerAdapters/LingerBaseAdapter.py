import logging
from LingerPlugin.LingerPlugin import LingerPlugin
from LingerPlugin.LingerItem import LingerItem

class LingerBaseAdapter(LingerItem):
    """Base adapter for linger"""
    def __init__(self, configuration):
        super(LingerBaseAdapter, self).__init__(configuration)

    def send_message(self, subject, text):
        self.logger.info("Sending message with subject:{} message text:{}".format(subject, text))
        
class LingerBaseAdapterFactory(LingerPlugin):
    """Base adapter factory for linger"""
    def __init__(self):
        super(LingerBaseAdapterFactory, self).__init__()
        self.item = LingerBaseAdapter 

    def get_instance(self, configuration):
        return self.item(configuration)

    def get_fields(self):
        fields, optional_fields = super(LingerBaseAdapterFactory, self).get_fields()
        return (fields, optional_fields)