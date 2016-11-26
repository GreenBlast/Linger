import LingerActions.LingerBaseAction as lingerActions

# Operation specific imports
import urllib, json

class GetExternalIPAction(lingerActions.LingerBaseAction):
    """Getting temperature from the RMPro"""
    def __init__(self, configuration):
        super(GetExternalIPAction, self).__init__(configuration)
        self.communication_adapter_uuid = configuration["communication_adapter_uuid"]
        
    def communication_adapter(self):
        return self.get_adapter_by_uuid(self.communication_adapter_uuid)

    def act(self, configuration):
        data = json.loads(urllib.urlopen("http://ip.jsontest.com/").read())
        self.communication_adapter().send_message("Here is the IP", data["ip"])

class GetExternalIPActionFactory(lingerActions.LingerBaseActionFactory):
    """Base action factory for linger"""
    def __init__(self):
        super(GetExternalIPActionFactory, self).__init__()
        self.item = GetExternalIPAction 

    def get_instance_name(self):
        return "GetExternalIPAction"

    def get_fields(self):
        fields, optional_fields = super(GetExternalIPActionFactory, self).get_fields()
        fields += [("communication_adapter_uuid","Adapters")]
        return (fields, optional_fields)
