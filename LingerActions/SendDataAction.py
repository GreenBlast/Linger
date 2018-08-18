"""
SendDataAction sends data via communication adapter
"""

import LingerActions.LingerBaseAction as lingerActions
import LingerConstants


class SendDataAction(lingerActions.LingerBaseAction):
    """Sends data via communication adapter"""

    def __init__(self, configuration):
        super(SendDataAction, self).__init__(configuration)

        # Fields
        self.communication_adapter_uuid = configuration["communication_adapter_uuid"]

    def communication_adapter(self):
        """
        Getting the communication adapter
        """
        return self.get_adapter_by_uuid(self.communication_adapter_uuid)

    def act(self, configuration=None):
        self.communication_adapter().send_message("subject", "text", **configuration)


class SendDataActionFactory(lingerActions.LingerBaseActionFactory):
    """Factory for SendDataAction"""
    def __init__(self):
        super(SendDataActionFactory, self).__init__()
        self.item = SendDataAction

    @staticmethod
    def get_instance_name():
        return "SendDataAction"

    def get_fields(self):
        fields, optional_fields = super(SendDataActionFactory, self).get_fields()
        fields += [("communication_adapter_uuid", "Adapters")]
        return fields, optional_fields
