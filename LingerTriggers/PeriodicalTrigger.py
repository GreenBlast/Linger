import LingerTriggers.LingerBaseTrigger as lingerTriggers

# Operation specific imports

class PeriodicalTrigger(lingerTriggers.LingerBaseTrigger):
    """
        Trigger that is doing an action every given time
    """
    def __init__(self, configuration):
        super(PeriodicalTrigger, self).__init__(configuration)
        self.scheduled_job = None
        # Fields
        self.interval = float(self.configuration["intervalSec"])

        # Optional fields

        self.logger.debug("PeriodicalTrigger initialized")

    def trigger_check_condition(self):
        self.logger.debug("trigger_check_condition called")
                
    def trigger_engaged(self, event_details):
        self.trigger_callback(self.uuid, event_details)

    def start(self):
        self.scheduled_job = self.scheduler.add_job(self.trigger_check_condition, 'interval', seconds=self.interval)

    def stop(self):
        if self.scheduled_job != None:
            self.scheduled_job.remove()

class PeriodicalTriggerFactory(lingerTriggers.LingerBaseTriggerFactory):
    """PeriodicalTriggerFactory generates PeriodicalTrigger instances"""
    def __init__(self):
        super(PeriodicalTriggerFactory, self).__init__()
        self.item = PeriodicalTrigger

    def get_instance_name(self):
        return "PeriodicalTrigger"

    def get_fields(self):
        fields, optional_fields = super(PeriodicalTriggerFactory, self).get_fields()
        fields +=[("intervalSec","number")]

        return (fields,optional_fields)
