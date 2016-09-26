# Imports
import os
import sys
# Adding current directory to the path 
sys.path.append(os.getcwd())

from flask import Flask, request, render_template, Response
import json
import uuid

# Linger imports
from LingerManagers.AdaptersManager import AdaptersManager
from LingerManagers.ActionsManager import ActionsManager
from LingerManagers.TriggersManager import TriggersManager


import logging
LOG_LEVEL = logging.INFO
logging.basicConfig(level=LOG_LEVEL,
                    format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Configurations
DEBUG = True
SECRET_KEY = 'Development key'

# Upload files configurations
CONFIG_FILE = 'Linger.config'

# Create application
app = Flask(__name__)
app.config.from_object(__name__)

# Helper methods
def get_configuration():
    with open(CONFIG_FILE, 'r') as f:
        returned_branch = json.loads(f.read())

    return returned_branch

def set_configuration(configuration):
    with open(CONFIG_FILE, 'w') as fw:
        fw.write(json.dumps(configuration))

def parse_fields(fields):
# This method should be updated in case of updating the fields system in Linger
    parsed = {}
    parsed["mandatory"] = [] 
    parsed["optional"] = [] 
    for field in fields[0]:
        parsed["mandatory"].append(field) 
    for field in fields[1]:
        parsed["optional"].append(field)

    return parsed

def get_items_structure(loading_configuration):
    managers = []
    item_structure = {}
    managers.append(AdaptersManager(loading_configuration))
    managers.append(ActionsManager(loading_configuration))
    managers.append(TriggersManager(loading_configuration))

    for manager in managers:
        item_structure[manager.manager_type] = {}
        for item_type, item_factory in manager.loaded_plugins_by_types.iteritems():
            item_structure[manager.manager_type][item_type] = parse_fields(item_factory.get_fields())

    return item_structure

@app.route('/')
def conifgurator():
    return render_template('index.html', server_address=request.host)

@app.route('/api/get_configuration', methods=['GET'])
def get_configuration_handler():
    configuration = {} 
    configuration["Linger"] = get_configuration()
    configuration["ItemsStructure"] = get_items_structure(configuration["Linger"])


    return Response(
        json.dumps(configuration),
        mimetype='application/json',
        headers={
            'Cache-Control': 'no-cache'
        }
    )

@app.route('/api/get_uuid', methods=['GET'])
def get_uuid_for_add_handler():
    uuid_hex = uuid.uuid4().get_hex()

    return Response(
        json.dumps(uuid_hex),
        mimetype='application/json',
        headers={
            'Cache-Control': 'no-cache'
        }
    )

@app.route('/api/upload_configuration', methods=['GET','POST'])
def upload_configuration():
    error = None
    # Uploading config file
    if request.method == 'POST':
        configuration = json.loads(request.data)
        try:
            set_configuration(configuration)
        except Exception, e:
            app.logger.debug(e)
            error = "problem while saving configuration"

    return render_template('upload_configuration.html', error=error)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response

if __name__ == '__main__':
    # Reloader is bugged, Doesn't work on HGFS(VMWare filesystem).
    app.run(host='0.0.0.0', use_reloader = True, debug=True )
    # app.run(host='0.0.0.0')
