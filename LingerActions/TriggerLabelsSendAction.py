"""
TriggerLabelsSendAction sends a message containing the list of labels associated with a trigger
"""
# Operation specific imports
import json

import LingerActions.LingerBaseAction as lingerActions
import LingerConstants


class TriggerLabelsSendAction(lingerActions.LingerBaseAction):
    """Sends a message containing the list of labels associated with a trigger"""
    def __init__(self, configuration):
        super(TriggerLabelsSendAction, self).__init__(configuration)

        # Fields
        self.communication_adapter_uuid = configuration["communication_adapter"]
        self.trigger_uuid = configuration["trigger"]

        # Optional Fields

    def communication_adapter(self):
        """
        Getting the communication adapter
        """
        return self.get_adapter_by_uuid(self.communication_adapter_uuid)

    def act(self, configuration=None):
        labels = self.configuration["get_trigger_labels_of_actions"](self.trigger_uuid)
        data = {LingerConstants.LABELS_LIST: labels}

        self.communication_adapter().send_message(self.label, json.dumps(data))


class TriggerLabelsSendActionFactory(lingerActions.LingerBaseActionFactory):
    """Factory for TriggerLabelsSendAction"""
    def __init__(self):
        super(TriggerLabelsSendActionFactory, self).__init__()
        self.item = TriggerLabelsSendAction

    def get_instance_name(self):
        return "TriggerLabelsSendAction"

    def get_fields(self):
        fields, optional_fields = super(TriggerLabelsSendActionFactory, self).get_fields()
        fields += [("communication_adapter", "Adapters"),
                   ("trigger", "Triggers")]
        return (fields, optional_fields)
