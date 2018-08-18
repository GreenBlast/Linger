"""
MQTTCommunicationAdapter implements publishing messages to an MQTT broker with a predefined topic
"""

# Operation specific imports
import json
import base64

import LingerAdapters.LingerBaseAdapter as lingerAdapters
import LingerConstants


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

    def subscribe(self, callback):
        self.mqtt_adapter().subscribe(self.topic, callback)

    def unsubscribe(self, callback):
        self.mqtt_adapter().unsubscribe(self.topic, callback)

    def send_message(self, subject, text, **kwargs):
        if kwargs:
            data = kwargs.copy()
            if LingerConstants.IMAGE_DATA in data:
                data[LingerConstants.IMAGE_BASE64_DATA] = base64.b64encode(kwargs[LingerConstants.IMAGE_DATA]).decode('utf-8')
                del data[LingerConstants.IMAGE_DATA]

            data = json.dumps(data)
            self.mqtt_adapter().publish_mqtt_message(self.topic, data)
        else:
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

        return fields, optional_fields
