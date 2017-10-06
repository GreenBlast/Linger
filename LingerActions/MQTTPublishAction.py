"""
MQTTPublishAction publish a message to the broker
"""
import threading
import LingerActions.LingerBaseAction as lingerActions

class MQTTPublishAction(lingerActions.LingerBaseAction):
    """Publish a message to the broker"""
    DEFAULT_TIMEOUT = 30
    def __init__(self, configuration):
        super(MQTTPublishAction, self).__init__(configuration)

        # Fields
        self.mqtt_adapter_uuid = configuration["mqtt_adapter_uuid"]
        self.topic = configuration["topic"]
        self.message = configuration["message"]

        # Optional Fields
        self.timeout = int(configuration.get("timeout", self.DEFAULT_TIMEOUT))

        self.answer_events = {}
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
        subscribed_event = self.answer_events.get(topic, None)
        if subscribed_event:
            subscribed_event.set()

    def act(self, configuration=None):
        if configuration:
            if "should_return" in configuration and configuration["should_return"] and "trigger_label" in configuration:
                self.mqtt_adapter().subscribe(configuration["trigger_label"], self.callback)
                self.mqtt_adapter().publish_mqtt_message(self.topic, self.message)

                self.answer_events[configuration["trigger_label"]] = threading.Event()
                wait_result = self.answer_events[configuration["trigger_label"]].wait(self.DEFAULT_TIMEOUT)
                self.mqtt_adapter().unsubscribe(configuration["trigger_label"], self.callback)

                if not wait_result:
                    self.logger.debug("No answer given")
                    return None
                else:
                    self.logger.debug("Recieved info %s", self.received_info)
                    return self.received_info
            elif "command" in configuration and configuration["command"]:
                self.mqtt_adapter().publish_mqtt_message(self.topic, configuration["command"])
        else:
            self.mqtt_adapter().publish_mqtt_message(self.topic, self.message)


class MQTTPublishActionFactory(lingerActions.LingerBaseActionFactory):
    """Factory for MQTTPublishAction"""
    def __init__(self):
        super(MQTTPublishActionFactory, self).__init__()
        self.item = MQTTPublishAction

    @staticmethod
    def get_instance_name():
        return "MQTTPublishAction"

    def get_fields(self):
        fields, optional_fields = super(MQTTPublishActionFactory, self).get_fields()
        fields += [("mqtt_adapter_uuid", "Adapters"),
                   ("topic", "string"),
                   ("message", "string")]
        return (fields, optional_fields)
