import axios from 'axios';
import { takeEvery } from 'redux-saga'
import { fork, call, put, select } from 'redux-saga/effects'
import { loadDataAction } from './actions';
import { setErrorAction } from './actions';
import { setCurrentFlowStateAction } from './actions';
import { unsetCurrentFlowStateAction } from './actions';
import { loadItemsStructureAction } from './actions'
import { setItemToAddAction } from './actions'
import { GET_CONFIGURATION_FROM_SERVER } from './actionTypes'
import { ADD_NEW_ITEM_CLICKED } from './actionTypes'
import { ADD_NEW_ITEM_UUID_READY } from './actionTypes'
import { SAVE_CONFIGURATION_TO_SERVER } from './actionTypes'

// Selector for linger state
export const getLingerConfiguration = (state) => state.Linger

const getConfApi = (address) => {
	return axios.get("http://" + address + "/api/get_configuration");
}

const saveConfApi = (address, data) => {
	return axios.post("http://" + address + "/api/upload_configuration", data);
}

const getUuidApi = (address) => {
	return axios.get("http://" + address + "/api/get_uuid");
}

function* getDataSaga() {
	try {
		yield put(setCurrentFlowStateAction({'id':GET_CONFIGURATION_FROM_SERVER}));
		let lingerData = yield select(getLingerConfiguration);
		const data = yield getConfApi(lingerData.ApiServerAddress);
		yield put(loadDataAction(data.data["Linger"]));
		yield put(loadItemsStructureAction(data.data["ItemsStructure"]));
		yield put(unsetCurrentFlowStateAction(GET_CONFIGURATION_FROM_SERVER));
	}
	catch(error) {
		yield put(setErrorAction({'id':GET_CONFIGURATION_FROM_SERVER, 'error':error}));
		yield put(unsetCurrentFlowStateAction(GET_CONFIGURATION_FROM_SERVER));
	}	
}

function* saveDataSaga() {
	try {
		yield put(setCurrentFlowStateAction({'id':SAVE_CONFIGURATION_TO_SERVER}));
		let lingerData = yield select(getLingerConfiguration);
		yield saveConfApi(lingerData.ApiServerAddress, lingerData);
		yield put(unsetCurrentFlowStateAction(SAVE_CONFIGURATION_TO_SERVER));
	}
	catch(error) {
		yield put(setErrorAction({'id':SAVE_CONFIGURATION_TO_SERVER, 'error':error}));
		yield put(unsetCurrentFlowStateAction(SAVE_CONFIGURATION_TO_SERVER));
	}	
}


function* addNewItemClickedSaga(action_data) {
	try {
		yield put(setCurrentFlowStateAction({'id':ADD_NEW_ITEM_CLICKED+action_data.item_type}));
		let lingerData = yield select(getLingerConfiguration);
		const data = yield getUuidApi(lingerData.ApiServerAddress);
		yield put(setItemToAddAction({"uuid":data.data, "type":action_data.item_type}));
		yield put(setCurrentFlowStateAction({'id':ADD_NEW_ITEM_UUID_READY+action_data.item_type, "new_uuid":data.data}));
		yield put(unsetCurrentFlowStateAction(ADD_NEW_ITEM_CLICKED+action_data.item_type));
	}
	catch(error) {
		yield put(setErrorAction({'id':ADD_NEW_ITEM_CLICKED, 'error':error}));
		yield put(unsetCurrentFlowStateAction(ADD_NEW_ITEM_CLICKED+action_data.item_type));
	}	
}

export default function* rootSaga() {
	yield fork(takeEvery, GET_CONFIGURATION_FROM_SERVER, getDataSaga);
  	yield fork(takeEvery, SAVE_CONFIGURATION_TO_SERVER, saveDataSaga);
  	yield fork(takeEvery, ADD_NEW_ITEM_CLICKED, addNewItemClickedSaga);
}