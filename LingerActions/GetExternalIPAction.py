"""
GetExternalIPAction sends the external IP of the current machine
"""
# Operation specific imports
from future.moves.urllib.request import urlopen
import json

import LingerActions.LingerBaseAction as lingerActions


class GetExternalIPAction(lingerActions.LingerBaseAction):
    """GetExternalIPAction sends the external IP of the current machine"""
    def __init__(self, configuration):
        super(GetExternalIPAction, self).__init__(configuration)
        self.communication_adapter_uuid = configuration["communication_adapter_uuid"]

    def communication_adapter(self):
        """
        Getter for the communication adapter
        """
        return self.get_adapter_by_uuid(self.communication_adapter_uuid)

    def act(self, configuration=None):
        data = json.loads(urlopen("http://ip.jsontest.com/").read().decode('utf-8'))
        self.communication_adapter().send_message("Here is the IP", data["ip"], )


class GetExternalIPActionFactory(lingerActions.LingerBaseActionFactory):
    """Base action factory for linger"""
    def __init__(self):
        super(GetExternalIPActionFactory, self).__init__()
        self.item = GetExternalIPAction

    @staticmethod
    def get_instance_name():
        return "GetExternalIPAction"

    def get_fields(self):
        fields, optional_fields = super(GetExternalIPActionFactory, self).get_fields()
        fields += [("communication_adapter_uuid", "Adapters")]
        return fields, optional_fields
