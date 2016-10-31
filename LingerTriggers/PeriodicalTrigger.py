import LingerTriggers.LingerBaseTrigger as lingerTriggers

# Operation specific imports
from datetime import datetime, timedelta
from apscheduler.jobstores.base import JobLookupError

class PeriodicalTrigger(lingerTriggers.LingerBaseTrigger):
    """
        Trigger that is doing an action every given time
    """
    SHOULD_TRIGGER_ON_START_DEFAULT = True
    def __init__(self, configuration):
        super(PeriodicalTrigger, self).__init__(configuration)
        self.scheduled_job = None
        # Fields
        self.interval = float(self.configuration["intervalSec"])
        # Optional fields
        self.should_trigger_on_start = bool(self.configuration.get("should_trigger_on_start", self.SHOULD_TRIGGER_ON_START_DEFAULT))

        self.logger.debug("PeriodicalTrigger initialized")

    def trigger_check_condition(self):
        self.logger.debug("trigger_check_condition called")
        self.trigger_engaged()
        self.scheduled_job = self.scheduler.add_job(self.trigger_check_condition, 'interval', seconds=self.interval)
                        
    def trigger_engaged(self, event_details=None):
        self.trigger_callback(self.uuid, event_details)

    def start(self):
        if self.should_trigger_on_start:
            self.scheduled_job = self.scheduler.add_job(self.trigger_check_condition,'date', run_date=datetime.now() + timedelta(0,5))
        else:
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
        fields +=[("intervalSec","float")]
        optional_fields +=[("should_trigger_on_start","boolean")]
        return (fields,optional_fields)
