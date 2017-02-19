"""
MQTTPublishAndGetAnswerAction asking for a list of actions from a trigger
"""
import threading
import LingerActions.LingerBaseAction as lingerActions

class MQTTPublishAndGetAnswerAction(lingerActions.LingerBaseAction):
    """Publish a message to the broker, and waiting for an answer"""
    DEFAULT_TIMEOUT = 30
    def __init__(self, configuration):
        super(MQTTPublishAndGetAnswerAction, self).__init__(configuration)

        # Fields
        self.mqtt_adapter_uuid = configuration["mqtt_adapter_uuid"]
        self.topic = configuration["topic"]
        self.message = configuration["message"]

        # Optional Fields
        self.timeout = int(configuration.get("timeout", self.DEFAULT_TIMEOUT))

        self.answer_event = threading.Event()
        self.received_info = None

    def mqtt_adapter(self):
        """
        Getting the mqtt adapter
        """
        return self.get_adapter_by_uuid(self.mqtt_adapter_uuid)

    def callback(self, topic, payload): # Callback function paramaters are set already pylint: disable=W0613
        """
        Callback function for the returning answer
        """
        self.received_info = payload
        self.answer_event.set()

    def act(self, configuration=None):
        self.mqtt_adapter().subscribe(self.topic, self.callback)
        self.mqtt_adapter().publish_mqtt_message(self.topic, self.message)

        wait_result = self.answer_event.wait(self.timeout)
        self.mqtt_adapter().unsubscribe(self.topic, self.callback)

        if not wait_result:
            self.logger.debug("No answer given")
            return None
        else:
            self.logger.debug("Recieved info %s", self.received_info)
            return self.received_info

class MQTTPublishAndGetAnswerActionFactory(lingerActions.LingerBaseActionFactory):
    """Factory for MQTTPublishAndGetAnswerAction"""
    def __init__(self):
        super(MQTTPublishAndGetAnswerActionFactory, self).__init__()
        self.item = MQTTPublishAndGetAnswerAction

    def get_instance_name(self):
        return "MQTTPublishAndGetAnswerAction"

    def get_fields(self):
        fields, optional_fields = super(MQTTPublishAndGetAnswerActionFactory, self).get_fields()
        fields += [("mqtt_adapter_uuid", "Adapters"),
                   ("topic", "string"),
                   ("message", "string")]
        optional_fields += [("timeout", "integer")]
        return (fields, optional_fields)
