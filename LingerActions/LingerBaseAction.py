from LingerPlugin.LingerPlugin import LingerPlugin
from LingerPlugin.LingerItem import LingerItem

class LingerBaseAction(LingerItem):
    """Base Action for linger"""
    def __init__(self, configuration):
        super(LingerBaseAction, self).__init__(configuration)

    def act(self, configuration=None):
        """
        Performing the defined action of the LingerAction
        """
        self.logger.debug("Action engaged, Configuration:%s", configuration)

class LingerBaseActionFactory(LingerPlugin):
    """Base action factory for linger"""
    def __init__(self):
        super(LingerBaseActionFactory, self).__init__()
        self.item = LingerBaseAction

    def get_instance(self, configuration):
        """
        Returns an instance of the action
        """
        return self.item(configuration)

    def get_fields(self):
        fields, optional_fields = super(LingerBaseActionFactory, self).get_fields()
        return (fields, optional_fields)
