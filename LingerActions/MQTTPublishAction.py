"""
MQTTPublishAction publish a message to the broker
"""
import json
import threading
import LingerActions.LingerBaseAction as lingerActions
import LingerConstants

from future.utils import iteritems


class MQTTPublishAction(lingerActions.LingerBaseAction):
    """Publish a message to the broker"""
    DEFAULT_TIMEOUT = 30

    def __init__(self, configuration):
        super(MQTTPublishAction, self).__init__(configuration)

        # Fields
        self.mqtt_output_communication_adapter_uuid = configuration["mqtt_output_communication_adapter_uuid"]
        self.mqtt_input_communication_adapter_uuid = configuration["mqtt_input_communication_adapter_uuid"]

        # Optional Fields
        self.timeout = int(configuration.get("timeout", self.DEFAULT_TIMEOUT))

        self.callbacks = {}
        self.lock = threading.Lock()
        self.received_info = None

    def mqtt_output_adapter(self):
        """
        Getting the mqtt adapter
        """
        return self.get_adapter_by_uuid(self.mqtt_output_communication_adapter_uuid)

    def mqtt_input_adapter(self):
        """
        Getting the mqtt adapter
        """
        return self.get_adapter_by_uuid(self.mqtt_input_communication_adapter_uuid)

    def got_command_callback(self, topic, payload, **kwargs):
        with self.lock:
            for current_callback, linger_name in iteritems(self.callbacks):
                current_callback(linger_name, payload, **kwargs)

    def act(self, configuration=None):
        if configuration:
            if configuration.get(LingerConstants.TRIGGER_ACTION, None) == LingerConstants.SUBSCRIBE_ACTION and \
                            LingerConstants.TRIGGER_CALLBACK in configuration and \
                            LingerConstants.LINGER_NAME in configuration:
                with self.lock:
                    if not self.callbacks:
                        self.mqtt_input_adapter().subscribe(self.got_command_callback)

                    self.callbacks[configuration[LingerConstants.TRIGGER_CALLBACK]] = configuration[LingerConstants.LINGER_NAME]

                payload = {LingerConstants.COMMAND_NAME: self.label}
                self.mqtt_output_adapter().send_message(self.label, json.dumps(payload))
            elif configuration.get(LingerConstants.TRIGGER_ACTION,
                                   None) == LingerConstants.REQUEST_COMMAND_ACTION and LingerConstants.TRIGGER_CALLBACK in configuration:

                payload = {LingerConstants.COMMAND_NAME: self.label}
                self.mqtt_output_adapter().send_message(self.label, json.dumps(payload))
            elif configuration.get(LingerConstants.TRIGGER_ACTION,
                                   None) == LingerConstants.UNSUBSCRIBE_ACTION and LingerConstants.TRIGGER_CALLBACK in configuration:
                with self.lock:
                    del self.callbacks[configuration[LingerConstants.TRIGGER_CALLBACK]]
                    if not self.callbacks:
                        self.mqtt_input_adapter().unsubscribe(self.got_command_callback)
            else:
                self.mqtt_output_adapter().send_message(self.label, json.dumps(configuration))


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
        fields += [("mqtt_output_communication_adapter_uuid", "Adapters"),
                   ('mqtt_input_communication_adapter_uuid', "Adapters")]
        return fields, optional_fields
