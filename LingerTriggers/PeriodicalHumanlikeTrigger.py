import LingerTriggers.LingerBaseTrigger as lingerTriggers

# Operation specific imports
from apscheduler.jobstores.base import JobLookupError
from random import randint
import datetime


class PeriodicalHumanlikeTrigger(lingerTriggers.LingerBaseTrigger):
    """
        Trigger that is doing an action every given time
    """
    MIN_WAIT_DEFAULT = 60
    MAX_WAIT_DEFAULT = 600
    SLEEP_TIME_START_DEFAULT = "02:00"
    SLEEP_TIME_END_DEFAULT = "06:00"
    SHOULD_TRIGGER_ON_START_DEFAULT = True
    def __init__(self, configuration):
        super(PeriodicalHumanlikeTrigger, self).__init__(configuration)
        self.scheduled_job = None
        # Fields
        self.interval = float(self.configuration["intervalSec"])

        # Optional fields
        self.should_trigger_on_start = bool(self.configuration.get("should_trigger_on_start", self.SHOULD_TRIGGER_ON_START_DEFAULT))
        self.min_wait = int(self.configuration.get("min_wait", self.MIN_WAIT_DEFAULT))
        self.max_wait = int(self.configuration.get("max_wait", self.MAX_WAIT_DEFAULT))
        self.sleep_time_start = datetime.datetime.strptime(self.configuration.get("sleep_time_start", self.SLEEP_TIME_START_DEFAULT), '%H:%M').time()
        self.sleep_time_end = datetime.datetime.strptime(self.configuration.get("sleep_time_end", self.SLEEP_TIME_END_DEFAULT), '%H:%M').time()
        self.logger.debug("PeriodicalHumanlikeTrigger initialized")


    def time_in_range(self, start, end, x):
        today = datetime.date.today()
        start = datetime.datetime.combine(today, start)
        end = datetime.datetime.combine(today, end)
        x = datetime.datetime.combine(today, x)
        if end <= start:
            end += datetime.timedelta(1) # tomorrow!
        if x <= start:
            x += datetime.timedelta(1) # tomorrow!
        return start <= x <= end

    def get_random_interval(self):
        return randint(self.min_wait, self.max_wait)

    def is_in_sleep_time(self, next_job_interval_seconds):
        next_job_interval_time = (datetime.datetime.now() + datetime.timedelta(seconds = next_job_interval_seconds)).time()
        return self.time_in_range(self.sleep_time_start, self.sleep_time_end, next_job_interval_time)

    def trigger_check_condition(self):
        self.logger.debug("trigger_check_condition called")
        self.trigger_engaged()

        # schedule next task with random interval
        interval_to_next_job_in_seconds = self.interval + self.get_random_interval()

        while self.is_in_sleep_time(interval_to_next_job_in_seconds):
            interval_to_next_job_in_seconds += self.interval

        self.logger.debug("Next job in seconds is:{}".format(interval_to_next_job_in_seconds))
        self.scheduled_job = self.scheduler.add_job(self.trigger_check_condition, 'interval', seconds=interval_to_next_job_in_seconds)
                        
    def trigger_engaged(self, event_details=None):
        self.trigger_callback(self.uuid, event_details)

    def start(self):
        if self.should_trigger_on_start:
            self.scheduled_job = self.scheduler.add_job(self.trigger_check_condition,'date', run_date=datetime.datetime.now() + datetime.timedelta(0,10))
        else:
            self.scheduled_job = self.scheduler.add_job(self.trigger_check_condition, 'interval', seconds=self.interval)

    def stop(self):
        if self.scheduled_job != None:
            self.scheduled_job.remove()

class PeriodicalHumanlikeTriggerFactory(lingerTriggers.LingerBaseTriggerFactory):
    """PeriodicalHumanlikeTriggerFactory generates PeriodicalHumanlikeTrigger instances"""
    def __init__(self):
        super(PeriodicalHumanlikeTriggerFactory, self).__init__()
        self.item = PeriodicalHumanlikeTrigger

    def get_instance_name(self):
        return "PeriodicalHumanlikeTrigger"

    def get_fields(self):
        fields, optional_fields = super(PeriodicalHumanlikeTriggerFactory, self).get_fields()
        fields +=[("intervalSec","float")]
        optional_fields +=[
        ("should_trigger_on_start","boolean"),
        ("min_wait", "integer"),
        ("max_wait", "integer"),
        ("sleep_time_start", "time"),
        ("sleep_time_end", "time")
        ]
        return (fields,optional_fields)
