import { createReducer } from 'redux-act';
import { changeFieldAction } from './actions';
import { selectTabAction } from './actions';
import { deleteItemAction } from './actions';
import { toggleTriggerAction } from './actions';
import { addActionToTriggerAction } from './actions';
import { removeActionFromTriggerAction } from './actions';
import { loadDataAction } from './actions';
import { setCurrentFlowStateAction } from './actions';
import { unsetCurrentFlowStateAction } from './actions';
import { setErrorAction } from './actions';
import { unsetErrorAction } from './actions';
import { loadItemsStructureAction } from './actions';
import { setItemToAddAction } from './actions';
import { unsetItemToAddAction } from './actions';
import { selectSubtypeToAddAction } from './actions';
import { addItemAction } from './actions';
import { APIServerAddressChangeAction } from './actions';

///// Test data
var CONFIGURATION_DEFAULT_DATA = {
	"flow_state":{},
	"flow_error_state":{},
	"selectedIndex":"2",
	"indexTable": [ 
					"Triggers->Actions",
					"Triggers",
					"Actions",
					"Adapters"
				],
	"item_structure": {},
	"items_to_add" : {},
};

const LINGER_INITIAL_ITEM = {
	"Items": {
	},
	"dir_paths": {
		"ActionsManager": "LingerActions",
		"AdaptersManager": "LingerAdapters",
		"TriggersManager": "LingerTriggers",
	},
	"TriggerActions": {
	},
	"counter_keep_alive": 600,
	// Server address is a global that should be set by the server dynamically on load
	"ApiServerAddress": server_address,
}

const changeField = (state, payload) => {
	let newState = Object.assign({}, state);

	newState.Items[payload.uuid][payload.field] = payload.value;

	return newState;
};

const addItem = (state, payload) => {
	let newState = Object.assign({}, state);

	newState.Items[payload.uuid] = payload.item;

	// If item is a trigger, also add it to the trigger acions list
	if (payload.item.type == "Triggers") {
		newState.TriggerActions[payload.uuid] = {actions:[], enabled:false};
	}
	return newState;
};

const deleteItem = (state, uuid) => {
	let newState = Object.assign({}, state);


	// Check if the item is a trigger, if so, it should be removed from TriggerActions as well
	if ("Triggers" == newState.Items[uuid].type) {
		delete newState.TriggerActions[uuid];
	}

	// Check if the item is a action, if so, it should be removed from TriggerActions as well
	if ("Actions" == newState.Items[uuid].type) {
		for (let triggerActionUuid in newState.TriggerActions) {
    		if (newState.TriggerActions.hasOwnProperty(triggerActionUuid)) {
        		const indexOfAction = newState.TriggerActions[triggerActionUuid].actions.indexOf(uuid)
        		if (-1 != indexOfAction) {
					newState.TriggerActions[triggerActionUuid].actions.splice(indexOfAction,1);
        		}	
   			}
		}
	}

	delete newState.Items[uuid];
	return newState;
};

const toggleTrigger = (state, uuid) => {
	let newState = Object.assign({}, state);

	// If exist, toggle it's state
	newState.TriggerActions[uuid].enabled = !newState.TriggerActions[uuid].enabled;

	return newState;
}

const addActionToTrigger = (state, payload) => {
	let newState = Object.assign({}, state);

	newState.TriggerActions[payload.triggerUuid].actions.push(payload.actionUuid);

	return newState;
}

const removeActionFromTrigger = (state, payload) => {
	let newState = Object.assign({}, state);

	// Removing a given action
    const indexOfAction = newState.TriggerActions[payload.triggerUuid].actions.indexOf(payload.actionUuid);
	
	if (-1 != indexOfAction) {
		newState.TriggerActions[payload.triggerUuid].actions.splice(indexOfAction,1);
	}

	return newState;
}

const setCurrentFlowState = (state, payload) => {
	let newState = Object.assign({}, state);

	newState.flow_state[payload.id] = payload;	

	return newState;
}

const unsetCurrentFlowState = (state, flow_id) => {
	let newState = Object.assign({}, state);

	delete newState.flow_state[flow_id];

	return newState;
}

const setError = (state, payload) => {
	let newState = Object.assign({}, state);

	newState.flow_error_state[payload.id] = payload.error;

	return newState;
}

const unsetError = (state, error_id) => {
	let newState = Object.assign({}, state);

	delete newState.flow_error_state[error_id];

	return newState;
}


const setItemToAdd = (state, payload) => {
	let newState = Object.assign({}, state);

	if (!(payload.uuid in newState.items_to_add)) {
		newState.items_to_add[payload.uuid] = {}
	} 

	newState.items_to_add[payload.uuid] = Object.assign({}, newState.items_to_add[payload.uuid], {...payload});

	let item = newState.items_to_add[payload.uuid]

	// Setting subtype if undefined
	if (!("subtype" in item))
	{
		const defaultSubtype = Object.keys(newState.item_structure[payload.type])[0];
		newState = selectSubtype(newState, {uuid:payload.uuid, subtype:defaultSubtype})
	}

	// Deleting redundant uuid field 
	// delete newState.items_to_add[payload.uuid].uuid;

	return newState;
}

const unsetItemToAdd = (state, uuid) => {
	let newState = Object.assign({}, state);

	delete newState.items_to_add[uuid]

	return newState;
}


const selectSubtype = (state, payload) => {
	let newState = Object.assign({}, state);

	const type = newState.items_to_add[payload.uuid]["type"]
	let item = newState.items_to_add[payload.uuid]
	item["subtype"] = payload.subtype

	// Loading the relevant fields of the subtype: 
	const mandatoryFields = newState.item_structure[type][payload.subtype]["mandatory"]
	// Currently doesn't need optional fields to force enter the item fields
	// const optionalFields = newState.item_structure[type][payload.subtype]["optional"]

	// Using the [0] as it's the field name, [1] is the supplied type
	for (var i = 0; i < mandatoryFields.length; i++) {
		if (!(mandatoryFields[i][0] in item)) {
			item[mandatoryFields[i][0]] = "";
		}
	}

	return newState;
}


///// Reducers
export const ConfigurationReducer = createReducer({
	[selectTabAction]: (state, payload) => {return Object.assign({}, state, {"selectedIndex":payload})},
	[setCurrentFlowStateAction]: (state, payload) =>  setCurrentFlowState(state,payload),
	[unsetCurrentFlowStateAction]: (state, payload) => unsetCurrentFlowState(state,payload),
	[setErrorAction]: (state, payload) => setError(state,payload),
	[unsetErrorAction]: (state, payload) => unsetError(state,payload),
	[loadItemsStructureAction]: (state, payload) => {return Object.assign({}, state, {item_structure: payload})},
	[setItemToAddAction]: (state, payload) => setItemToAdd(state, payload),
	[unsetItemToAddAction]: (state, payload) => unsetItemToAdd(state, payload),
	[selectSubtypeToAddAction]: (state, payload) => selectSubtype(state, payload),
}, CONFIGURATION_DEFAULT_DATA);

export const LingerItemsReducer = createReducer({
	[addActionToTriggerAction]: (state, payload) => addActionToTrigger(state, payload),
	[removeActionFromTriggerAction]: (state, payload) => removeActionFromTrigger(state, payload),
	[toggleTriggerAction]: (state, payload) => toggleTrigger(state, payload),
	[deleteItemAction]: (state, payload) => deleteItem(state, payload),
	[addItemAction]: (state, payload) => addItem(state, payload),
	[changeFieldAction]: (state, payload) => changeField(state, payload),
	[loadDataAction]: (state, payload) => {return Object.assign({}, state, payload)},
	[APIServerAddressChangeAction]: (state, payload) => {return Object.assign({}, state, {ApiServerAddress:payload})},
}, LINGER_INITIAL_ITEM);
