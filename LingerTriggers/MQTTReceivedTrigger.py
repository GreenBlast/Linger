"""
MQTTReceivedTrigger triggers by MQTT message and calls all associated actions
"""
import json
from collections import defaultdict

import LingerTriggers.LingerBaseTrigger as lingerTriggers


class MQTTReceivedTrigger(lingerTriggers.LingerBaseTrigger):
    """Trigger that engaged when a message is received via MQTT"""

    def __init__(self, configuration):
        super(MQTTReceivedTrigger, self).__init__(configuration)
        self.subscription_id = None
        self.actions_by_labels = defaultdict(list)

        # Fields
        self.mqtt_adapter_uuid = configuration["mqtt_adapter"]
        self.topic = configuration["topic"]

        # Optional fields
        self.logger.debug("MQTTReceivedTrigger initialized")

    def mqtt_adapter(self):
        """
        Getter for the mail adapter
        """
        return self.get_adapter_by_uuid(self.mqtt_adapter_uuid)

    def trigger_check_condition(self, topic, payload):
        """
        Checking if trigger should call action
        """
        self.logger.debug("Got message with topic: %s payload is: %s", topic, payload)
        data = {}
        try:
            data = json.loads(payload.decode("utf-8"))
        except ValueError:
            data['payload'] = payload
            pass

        data['topic'] = topic
        self.trigger_engaged(data)

    def trigger_engaged(self, data=None):
        for action_uuid in self.actions:
            self.trigger_specific_action_callback(self.uuid, action_uuid, data)

    def start(self):
        self.mqtt_adapter().subscribe(self.topic, self.trigger_check_condition)
        self.logger.info("subscribed to topic: %s", self.topic)

    def stop(self):
        self.mqtt_adapter().unsubscribe(self.topic, self.trigger_check_condition)

    def register_action(self, action):
        super(MQTTReceivedTrigger, self).register_action(action)
        self.actions_by_labels[action.label] += [action]


class MQTTReceivedTriggerFactory(lingerTriggers.LingerBaseTriggerFactory):
    """MQTTReceivedTriggerFactory generates MQTTReceivedTrigger instances"""

    def __init__(self):
        super(MQTTReceivedTriggerFactory, self).__init__()
        self.item = MQTTReceivedTrigger

    @staticmethod
    def get_instance_name():
        """Returns instance name"""
        return "MQTTReceivedTrigger"

    def get_fields(self):
        fields, optional_fields = super(MQTTReceivedTriggerFactory, self).get_fields()

        fields += [('mqtt_adapter', 'uuid'),
                   ('topic', 'string')]

        return fields, optional_fields
