import LingerAdapters.LingerBaseAdapter as lingerAdapters 

# Operation specific imports
import subprocess
import threading
import time
import os
import shlex
import psutil

class ProcessAdapter(lingerAdapters.LingerBaseAdapter):
    """ProcessAdapter ables activating processes"""
    KILL_WAIT_SECS_DEFAULT = 60
    SLEEP_TIMEOUT_SECS_DEFAULT = 0.25
    KILL_TIMEOUT_SECS_DEFAULT = 60
    def __init__(self, configuration):
        super(ProcessAdapter, self).__init__(configuration)
        self.logger.debug("ProcessAdapter started")
        self.process = None
        self.lock = threading.Lock()

        # Fields
        self.command = self.configuration["command"]

        # Optional fields
        self.kill_wait = self.configuration.get("kill_wait", self.KILL_WAIT_SECS_DEFAULT)
        self.sleep_timeout = self.configuration.get("sleep_timeout", self.SLEEP_TIMEOUT_SECS_DEFAULT)
        self.kill_timeout = self.configuration.get("kill_timeout", self.KILL_TIMEOUT_SECS_DEFAULT)

    def start(self):
        self.logger.info("Starting process:%s" % self.command)
        with self.lock:
            if self.process is None:
                self.process = subprocess.Popen(shlex.split(self.command))

            if self.process is not None:
                self.logger.info("Started process:%s success" % self.command)
        
    def stop(self):
        with self.lock:
            self.logger.info("killing process: %s" % self.command)
            if self.process is None:
                self.logger.info("process:%s is Not active, can't kill" % self.command)
                return

            self.process.kill()
            kill_time = time.time() + self.kill_timeout
            self.logger.info("kill time is {}, is bigger than time: {}".format(kill_time,(time.time() < kill_time)))
            while time.time() < kill_time:
                poll = self.process.poll()
                if poll is not None:
                    self.logger.info("poll is: {}".format(poll))
                    break
                time.sleep(self.sleep_timeout)

            try:
                self.logger.info("killing using kill 9")
                os.kill(self.process.pid, 9)
            except OSError:
                self.logger.info("Got os error")
                # Process is already gone
                pass
            
            self.process = None

            self.logger.info("killed process:%s" % self.command)
            time.sleep(self.kill_wait)
    
    def restart(self):
        self.logger.info("restarting process:%s" % self.command)
        self.stop()
        self.start()

    def stop_with_all_children(self):
        with self.lock:
            if self.process is None:
                self.logger.info("process:%s is Not active, can't kill" % self.command)
                return

            self.logger.info("stopping all children processes")
            for child_process in psutil.Process(self.process.pid).children():
                self.logger.info("killing pid:{}".format(child_process.pid))
                child_process.kill()       
                del child_process                                              

            self.logger.info("killing process")
            self.process.kill()
            del self.process
            self.process = None

class ProcessAdapterFactory(lingerAdapters.LingerBaseAdapterFactory):
    """ProcessAdapterFactory generates ProcessAdapter instances"""
    def __init__(self):
        super(ProcessAdapterFactory, self).__init__()
        self.item = ProcessAdapter

    def get_instance(self, configuration):
        adapter = ProcessAdapter(configuration)
        return adapter
    
    def get_instance_name(self):
        return "ProcessAdapter"

    def get_fields(self):
        fields, optional_fields = super(ProcessAdapterFactory, self).get_fields()
        fields += [("command","string")]
        optional_fields += [("kill_wait","number"),("sleep_timeout","number"),("kill_timeout","number")]
        return (fields,optional_fields)
