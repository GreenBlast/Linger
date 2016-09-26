import requests
import sys
import json
import pickle 

list_of_commands = [
"start_ac",
"move_flap",
"set_25",
"set_26",
"set_27"
]

def main(bridge_address, mac_address):
    base_command = BASE_COMMAND_FORMAT.format(bridge_address)
    command = {}
    for command_name in list_of_commands:
        print "Now learning {} command".format(command_name)
        command['api_id'] = LEARN_API_ID
        command['command'] = LEARN_COMMAND
        command['mac'] = mac_address
        command['name'] = command_name
        answer = requests.get(base_command + json.dumps(command))
        if answer.status_code == 200 and json.loads(answer.content)["code"] == 0:
            raw_input("Press enter when finish\n")
            command['api_id'] = GET_API_ID
            command['command'] = GET_COMMAND
            answer = requests.get(base_command + json.dumps(command))
            # if answer.status_code == 200 and if json.loads(answer.content)["code"] == 0:
        else:
            sys.exit(1)
    command['api_id'] = LIST_API_ID
    command['command'] = LIST_COMMAND
    command['mac'] = mac_address
    command['name'] = command_name
    answer = requests.get(base_command + json.dumps(command))
    if answer.status_code == 200 and json.loads(answer.content)["code"] == 0:
        content = json.loads(answer.content)
        print content
        list_of_loaded_commands = content['list']
        print pickle.dumps(list_of_loaded_commands).encode('BASE64')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
