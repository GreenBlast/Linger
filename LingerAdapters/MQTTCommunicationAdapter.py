"""
MQTTCommunicationAdapter implements publishing messages to an MQTT broker with a predefined topic
"""

# Operation specific imports
import LingerAdapters.LingerBaseAdapter as lingerAdapters


class MQTTCommunicationAdapter(lingerAdapters.LingerBaseAdapter):
    """MQTTCommunicationAdapter ables publishing messages to an MQTT broker with a predefined topic"""

    def __init__(self, configuration):
        super(MQTTCommunicationAdapter, self).__init__(configuration)
        self.logger.debug("MQTTCommunicationAdapter started")

        # fields
        self.mqtt_adapter_uuid = configuration["mqtt_adapter"]
        self.topic = configuration["topic"]

        self.logger.info("MQTTCommunicationAdapter configured")

    def mqtt_adapter(self):
        """Getter for the bot adapter"""
        return self.get_adapter_by_uuid(self.mqtt_adapter_uuid)

    def send_message(self, subject, text):
        self.mqtt_adapter().publish_mqtt_message(self.topic, text)

class MQTTCommunicationAdapterFactory(lingerAdapters.LingerBaseAdapterFactory):
    """MQTTCommunicationAdapterFactory generates MQTTCommunicationAdapter instances"""
    def __init__(self):
        super(MQTTCommunicationAdapterFactory, self).__init__()
        self.item = MQTTCommunicationAdapter

    @staticmethod
    def get_instance_name():
        """Returns instance name"""
        return "MQTTCommunicationAdapter"

    def get_fields(self):
        fields, optional_fields = super(MQTTCommunicationAdapterFactory, self).get_fields()

        fields += [('mqtt_adapter', 'uuid'),
                   ('topic', 'string')]

        return (fields, optional_fields)
