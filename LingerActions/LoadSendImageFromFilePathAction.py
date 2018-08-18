"""
LoadSendImageFromFilePathAction loads an image from a given path and sends it via communication adapter
"""
import base64

import LingerActions.LingerBaseAction as lingerActions
import LingerConstants


class LoadSendImageFromFilePathAction(lingerActions.LingerBaseAction):
    """Loads and image and sends it"""

    def __init__(self, configuration):
        super(LoadSendImageFromFilePathAction, self).__init__(configuration)

        # Fields
        self.communication_adapter_uuid = configuration["communication_adapter_uuid"]

    def communication_adapter(self):
        """
        Getting the communication adapter
        """
        return self.get_adapter_by_uuid(self.communication_adapter_uuid)

    def act(self, configuration=None):
        if configuration and LingerConstants.FILE_PATH_SRC in configuration:
            with open(configuration[LingerConstants.FILE_PATH_SRC], 'rb') as image_handle:
                image_data = image_handle.read()
                data = {LingerConstants.IMAGE_DATA: image_data}
                self.communication_adapter().send_message("subject", "text", **data)


class LoadSendImageFromFilePathActionFactory(lingerActions.LingerBaseActionFactory):
    """Factory for LoadSendImageFromFilePathAction"""
    def __init__(self):
        super(LoadSendImageFromFilePathActionFactory, self).__init__()
        self.item = LoadSendImageFromFilePathAction

    @staticmethod
    def get_instance_name():
        return "LoadSendImageFromFilePathAction"

    def get_fields(self):
        fields, optional_fields = super(LoadSendImageFromFilePathActionFactory, self).get_fields()
        fields += [("communication_adapter_uuid", "Adapters")]
        return fields, optional_fields
