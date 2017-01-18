import LingerAdapters.LingerBaseAdapter as lingerAdapters 

# Operation specific imports
import requests
import threading
import json
import pickle

# The commands are the output of the RMProTeacher.py in the help scripts
PICKLED_PRETEACHED_COMMANDS_LIST = """KGxwMAooZHAxClZtYWMKcDIKVmI0OjQzOjBkOmU0OjM3OjczCnAzCnNWZGF0YQpwNApWMjYwMGJjMDA2NDdiM2YyMTFlM2YzZDIwMWYyMDFmMjAxZjFkMWYyMDFmMjAxZjNlMWYxZDQwM2U0MDFlMWUyMTFlMjExZjIwMWYxZDFlMjExZTIxMWUyMTFlMWUxZTIxMWUyMTFlMjExZTFlMWUyMTFmMjAxZTIxMWUzYzQwMjA2NDdhNDAyMDIwM2QzZDIxMWUyMDFmMjExZjFkMWUyMTFmMjAxZTNlMWYxZTNmM2YzZjFlMWYyMDFlMjExZTIxMWUxZTFlMjExZTIxMWUyMTFlMWUxZTIxMWUyMTFmMjAxZjFkMWYyMDFmMjAxZjIwMWYzYjQwMjA2NDdhNDAyMTFlM2YzYzIxMWUyMTFlMjExZTFlMWUyMTFlMjExZTNmMWUxZTNmM2YzZjFlMWUyMTFlMjExZTIxMWUxZTFlMjExZTIxMWQyMjFlMWUxZTIxMWYyMDFmMjExYzIwMWMyMzFjMjMxZTIxMWMzZTNkMjM4MTAwMDEzYzA4MDAwZDA1MDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwCnA1CnNWbmFtZQpwNgpWc3RhcnRfYWMKcDcKc2EoZHA4ClZtYWMKcDkKVmI0OjQzOjBkOmU0OjM3OjczCnAxMApzVmRhdGEKcDExClYyNjAwYjgwMDYzNWUxZDIyMWQyMjFkNDAzYjIzMWMyMzFjNDEzYTIzMWMyMzFjNDEzYTIzMWM0MTNkMjAxYzIzMWMyMzFjMjMxYzIwMWMyMzFjMjMxYzIzMWQxZjFkMjIxZDIyMWQyMjFkMWYxZDIyMWQyMjFkMjIxZDNlM2QyMzYxNWYxYzIzMWMyMzFjNDEzYTIzMWMyMzFjNDEzYTIzMWMyMzFjNDEzYTIzMWM0MTNlMWYxZDIyMWQyMjFkMjIxZDFmMWQyMjFkMjIxZDIyMWQyMDFjMjMxYzIzMWMyMzFjMjAxYzIzMWMyMzFjMjMxYzNlM2QyMzYxNWYxYzIzMWMyMzFjNDEzYTIzMWMyMzFkNDAzYjIyMWQyMjFkNDAzYjIyMWQ0MDNlMjAxYzIzMWMyMzFjMjMxYzIwMWMyMzFjMjMxYzIzMWMyMDFjMjMxYzIzMWMyMzFjMjAxYzIzMWMyMzFjMjMxYzNlM2QyMzgwMDAwZDA1CnAxMgpzVm5hbWUKcDEzClZtb3ZlX2ZsYXAKcDE0CnNhKGRwMTUKVm1hYwpwMTYKVmI0OjQzOjBkOmU0OjM3OjczCnAxNwpzVmRhdGEKcDE4ClYyNjAwN2MwMTY1NWMxZjIwMWYyMDFmM2UzZDIwMWYyMTFlMjExZTFlMWUyMTFlMjExZTNmM2MzZjNmMjExZjFkMWYyMDFmMjAxZjIwMWYxZDFmMjAxZjIwMWYyMDFmMWQxZjIwMWYyMDFmMjAxZjFkMWYyMDFmMjAxZjIwMWYzYjQwMjA2NDVjMWYyMTFlMjExZTNmM2MyMTFlMjExZjIwMWYxZDFmMjAxZjIwMWYzZTNkM2U0MDIwMWYxZDFmMjAxZjIwMWYyMDFmMWQxZjIwMWYyMDFmMjAxZjFkMWYyMDFmMjAxZjIxMWUxZTFlMjExZTIxMWUyMTFlM2MzZjIxNjQ1YTIxMjAxZjIwMWYzZTNkMjAxZjIwMWYyMDFmMWQxZjIwMWYyMDFmM2UzZDNlNDAyMDFmMWQxZjIwMWYyMDFmMjExZTFlMWUyMTFlMjExZTIxMWUxZTFlMjExZTIxMWUyMTFmMWQxZjIwMWYyMDFmMjAxZjNiNDAyMDgyMDAwNjZjNjU1YzFmMjAxZjIwMWYzZTNkMjAxZjIwMWYyMDFmMWQxZjIwMWYyMDFmM2UzZDNmM2YyMTFlMWUxZTIxMWUyMTFmMjAxZjFkMWYyMDFmMjAxZjIwMWYxZDFmMjAxZjIwMWYyMDFmMWQxZjIwMWYyMDFmMjAxZjNiNDAyMDY0NWMxZjIwMWYyMDFmM2UzZDIxMWUyMTFlMjExZTFlMWUyMTFlMjExZTNmM2QzZTQwMjAxZjFkMWYyMDFmMjAxZjIwMWYxZDFmMjAxZjIwMWYyMDFmMWQxZjIwMWYyMDFmMjAxZjFkMWYyMDFmMjAxZjIxMWUzYjQwMjE2MzVkMWUyMTFlMjExZTNmM2MyMTFmMjAxZjIwMWYxZDFmMjAxZjIwMWUzZjNkM2UzZjIxMWUxZTFlMjExZTIxMWUyMTFlMWUxZTIxMWUyMTFkMjMxYzIwMWMyMzFjMjMxYzIzMWMyMDFjMjMxYzIzMWMyMzFjM2UzZDIzODEwMDBkMDUwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAKcDE5CnNWbmFtZQpwMjAKVnNldF8yNQpwMjEKc2EoZHAyMgpWbWFjCnAyMwpWYjQ6NDM6MGQ6ZTQ6Mzc6NzMKcDI0CnNWZGF0YQpwMjUKVjI2MDA3YzAxNjM1ZTFkMjIxZDIyMWQ0MDNiMjIxZDIyMWQyMzFjMjAxYzIzMWMyMzFjNDEzYTQxMWYyMDNkMjAxYzIzMWMyMzFjMjMxYzIwMWMyMzFjMjMxYzIzMWMyMDFjMjMxYzIzMWMyMzFkMWYxZDIyMWQyMjFkMjIxZDNkM2UyMjYyNWUxZDIzMWMyMzFjNDEzYTIzMWMyMzFjMjMxYzIwMWMyMzFjMjMxYzQxM2E0MTFmMjAzZDIwMWMyMzFjMjMxZDIyMWQxZjFkMjIxZDIyMWQyMjFkMWYxZDIyMWQyMjFkMjIxZDIwMWMyMzFjMjMxYzIzMWMzZTNkMjM2MTVmMWMyMzFjMjMxYzQxM2EyMzFjMjMxYzIzMWMyMDFjMjMxYzIzMWQ0MDNiNDAyMDFmM2UxZjFkMjIxZDIyMWQyMjFkMWYxZDIzMWMyMzFjMjMxYzIwMWMyMzFjMjMxYzIzMWMyMDFjMjMxYzIzMWMyMzFjM2QzZTIzN2YwMDA5ZTg2MjVmMWMyMzFjMjMxYzQxM2EyMzFjMjMxYzIzMWMyMDFjMjMxYzIzMWM0MTNhNDExZjIwM2QyMDFjMjMxZDIyMWQyMjFkMWYxZDIyMWQyMjFkMjIxZDIwMWMyMjFkMjMxYzIzMWMyMDFjMjMxYzIzMWMyMzFjM2UzZDIzNjM1ZDFjMjMxYzIzMWM0MTNhMjMxYzIzMWMyMzFjMjAxYzIzMWQyMjFkNDAzYjQwMjAxZjNlMWYxZDIyMWQyMjFkMjIxZDIwMWMyMzFjMjMxYzIzMWMyMDFjMjMxYzIzMWMyMzFjMjAxYzIzMWMyMzFjMjMxYzNlM2QyMzYzNWQxYzIzMWQyMjFkNDAzYjIyMWQyMjFkMjIxZDFmMWQyMjFkMjIxZDQxM2MzZjFmMjAzZjFlMWMyMzFjMjMxZTIxMWMyMDFjMjMxYzIzMWMyMzFlMWUxYzIzMWMyMzFjMjMxYzIwMWMyMzFlMjExZDIyMWQzZDNmMjE4MjAwMGQwNTAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMApwMjYKc1ZuYW1lCnAyNwpWc2V0XzI2CnAyOApzYShkcDI5ClZtYWMKcDMwClZiNDo0MzowZDplNDozNzo3MwpwMzEKc1ZkYXRhCnAzMgpWMjYwMDg2MDExZTIxMWUyMTFlM2YzZDIwMWYyMDFmMjAxZjFkMWYyMDFmMjAxZjNlMWYxZDQwMjAxZjIwMWYxZDFmMjAxZjIwMWYyMDFmMWQxZjIwMWYyMDFmMjAxZjFkMWYyMTFlMjExZTIxMWUxZTFlMjExZTIxMWUyMTFlM2MzZjIxNjQ1YzFmMjAxZjIwMWYzZTNkMjAxZjIwMWYyMDFmMWQxZjIwMWYyMDFmM2UxZjFkNDAyMDFmMjAxZjFkMWYyMTFlMjExZTIxMWUxZTFlMjExZTIxMWUyMTFlMWUxZTIxMWUyMTFlMjExZTFlMWUyMTFmMjAxZjIwMWYzYjQwMjA2NDVjMWYyMDFmMjAxZjNlM2QyMDFmMjAxZjIwMWYxZTFlMjExZTIxMWUzZjFlMWUzZjIxMWUyMTFlMWUxZTIxMWUyMTFlMjExZjFkMWYyMDFmMjAxZjIwMWYxZDFmMjAxZjIwMWYyMDFmMWQxZjIwMWYyMDFmMjAxZjNiNDAyMDgxMDAwZDA1NjM1ZTFkMjIxZDIyMWQ0MDNiMjMxYzIzMWMyMzFjMjAxYzIzMWMyMzFjNDExYzIwM2YyMTFlMjExZTFlMWUyMTFlMjExZjIwMWYxZDFmMjAxZjIwMWYyMDFmMWQxZjIwMWYyMDFmMjAxZjFkMWQyMjFkMjIxZDIzMWMzZTNkMjM2MTVmMWQyMjFkMjIxYzQxM2IyMjFjMjMxYzIzMWMyMDFjMjMxYzIzMWM0MTFjMjAzZTIyMWQyMjFmMWQxZDIyMWQyMjFkMjIxZDFmMWYyMDFmMjExYzIzMWMyMDFjMjMxYzIzMWUyMTFjMjAxYzIzMWMyMzFjMjMxYzNlM2QyMzYxNWYxYzIzMWQyMjFkNDAzYjIyMWQyMjFkMjIxZTFlMWQyMjFkMjIxZDQwMWUxZTNlMjMxYzIzMWMyMDFjMjMxYzIzMWMyMzFjMjAxYzIzMWMyMzFjMjMxYzIwMWQyMjFjMjMxYzIzMWMyMDFkMjIxYzIzMWMyMzFkM2QzZDIzODAwMDBkMDUwMDAwCnAzMwpzVm5hbWUKcDM0ClZzZXRfMjcKcDM1CnNhLg=="""

class RMBridgeAdapter(lingerAdapters.LingerBaseAdapter):
    """RMBridgeAdapter ables commanding RMBridge"""

    BASE_COMMAND_FORMAT =  r"http://{}:{}/?cmd="
    LIST_API_ID = 1006
    LIST_COMMAND = 'list_codes'
    TEACH_API_ID = 1007
    TEACH_COMMAND = 'add_codes'
    LEARN_API_ID = 1002
    LEARN_COMMAND = 'learn_code'
    GET_API_ID = 1003
    GET_COMMAND = 'get_code'
    SEND_API_ID = 1004
    SEND_COMMAND = 'send_code'
    TEMPERATURE_API_ID = 1011
    TEMPERATURE_COMMAND = 'temperature'

    START_AC_COMMAND_NAME = 'start_ac'

    BASE_COMMAND_FORMAT = r"http://{}:{}/?cmd="

    def __init__(self, configuration):
        super(RMBridgeAdapter, self).__init__(configuration)
        self.logger.debug("RMBridgeAdapter started")
        self.lock = threading.Lock()
        self.preteached_commands_list = pickle.loads(PICKLED_PRETEACHED_COMMANDS_LIST.decode('BASE64'))
        self.list_of_command_names = [x["name"] for x in self.preteached_commands_list]
        self.ac_is_on = False

        # fields
        self.rmbridge_ip = configuration["rmbridge_ip"]
        self.rmbridge_port = configuration["rmbridge_port"]
        self.rmpro_mac = configuration["rmpro_mac"]

        # Setting the base command, and comparing command on the bridge with preteached commands
        self.base_command = self.BASE_COMMAND_FORMAT.format(self.rmbridge_ip, self.rmbridge_port)
        self.compare_current_commands_to_preteached_commands()
        self.logger.info("RMBridgeAdapter configured with ip=%s, port=%s" % (self.rmbridge_ip, self.rmbridge_port,))
        self.logger.debug("RMBridgeAdapter configured")

    def compare_current_commands_to_preteached_commands(self):
        command = {}
        command['api_id'] = self.LIST_API_ID
        command['command'] = self.LIST_COMMAND
        answer = self.send_raw_command(command)
        if set(self.list_of_command_names) == set([x['name'] for x in answer['list']]):
            self.logger.info("Current commands in bridge are the same as preteached")
            self.logger.info("Supported commands are:{}".format(self.list_of_command_names))
        else:
            # Later should add automatic teach sequence here
            self.logger.info("Current commands in bridge are not valid")
            # Now set the list of commands to empty, to prevent sending commands by name
            self.list_of_command_names = []

    def send_command_by_name(self, command_name):
        command = {}

        if command_name in self.list_of_command_names:
            command['api_id'] = self.SEND_API_ID
            command['command'] = self.SEND_COMMAND
            command['name'] = command_name
            self.send_raw_command(command)
        else:
            self.logger.info("Command is not in commands")

    def toggle_ac_status(self):
        self.logger.debug("ac state on before toggling is:{}".format(self.ac_is_on))
        self.ac_is_on = not self.ac_is_on

    def start_ac(self):
        if not self.ac_is_on:
            self.send_command_by_name(self.START_AC_COMMAND_NAME)
            self.toggle_ac_status()

    def stop_ac(self):
        if self.ac_is_on:
            self.send_command_by_name(self.START_AC_COMMAND_NAME)
            self.toggle_ac_status()

    def get_temperature(self):
        command = {}
        command['api_id'] = self.TEMPERATURE_API_ID
        command['command'] = self.TEMPERATURE_COMMAND
        command['mac'] = self.rmpro_mac
        answer = self.send_raw_command(command)

        return answer['temperature']

    def send_raw_command(self, command):
        with self.lock:
            command_string = json.dumps(command)
            answer = requests.get(self.base_command + command_string)
            if answer.status_code == 200 and json.loads(answer.content)["code"] == 0:
                self.logger.info("Success on command: %s" % (self.base_command + command_string))
                return json.loads(answer.content)
            else:
                self.logger.info("Failure on command: %s" % (self.base_command + command_string))
                return None

class RMBridgeAdapterFactory(lingerAdapters.LingerBaseAdapterFactory):
    """RMBridgeAdapterFactory generates RMBridgeAdapter instances"""
    def __init__(self):
        super(RMBridgeAdapterFactory, self).__init__()
        self.item = RMBridgeAdapter

    def get_instance_name(self):
        return "RMBridgeAdapter"

    def get_fields(self):
        fields, optional_fields = super(RMBridgeAdapterFactory, self).get_fields()
        fields += [('rmbridge_ip',"string"), ('rmbridge_port',"integer"), ('rmpro_mac',"string")]
        return (fields, optional_fields)
