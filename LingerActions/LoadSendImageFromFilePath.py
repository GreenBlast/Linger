"""
LoadSendImageFromFilePath loads an image from a given path and sends it via communication adapter
"""
import threading
import LingerActions.LingerBaseAction as lingerActions

class LoadSendImageFromFilePath(lingerActions.LingerBaseAction):
    """Loads and image and sends it"""

    def __init__(self, configuration):
        super(LoadSendImageFromFilePath, self).__init__(configuration)

        # Fields
        self.communication_adapter_uuid = configuration["communication_adapter_uuid"]

        # TODO Remove commented
        # self.topic = configuration["topic"]
        # self.message = configuration["message"]

        # Optional Fields
        # self.timeout = int(configuration.get("timeout", self.DEFAULT_TIMEOUT))

        # self.answer_events = {}
        # self.received_info = None

    def communication_adapter(self):
        """
        Getting the mqtt adapter
        """
        return self.get_adapter_by_uuid(self.communication_adapter_uuid)

    # TODO remove
    # def callback(self, topic, payload): # Callback function paramaters are set already pylint: disable=W0613
    #     """
    #     Callback function for the returning answer
    #     """
    #     self.received_info = payload
    #     subscribed_event = self.answer_events.get(topic, None)
    #     if subscribed_event:
    #         subscribed_event.set()

    def act(self, configuration=None):
        if configuration and configuration.get('src_path', None):
            # Checking sleep status
            # Loading image from path
            file_path = configuration['src_path']
            # Sending via communication adapter
            # TODO Add subject and text
            self.communication_adapter().send_message("subject", "text", dict(image=) )
            # Resetting sleep status


class LoadSendImageFromFilePathFactory(lingerActions.LingerBaseActionFactory):
    """Factory for LoadSendImageFromFilePath"""
    def __init__(self):
        super(LoadSendImageFromFilePathFactory, self).__init__()
        self.item = LoadSendImageFromFilePath

    @staticmethod
    def get_instance_name():
        return "LoadSendImageFromFilePath"

    def get_fields(self):
        fields, optional_fields = super(LoadSendImageFromFilePathFactory, self).get_fields()
        fields += [("communication_adapter_uuid", "Adapters")]
        return fields, optional_fields
