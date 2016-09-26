import { createAction } from 'redux-act';
import axios from 'axios';
///// Action creators



// Linger
export const changeFieldAction = createAction('Changes a field');
export const addActionToTriggerAction = createAction('Adds an action to trigger');
export const removeActionFromTriggerAction = createAction('Removes an action to trigger');
export const toggleTriggerAction = createAction('Toggles trigger activation');
export const addItemAction = createAction('Deletes an item');
export const deleteItemAction = createAction('Deletes an item');
export const loadDataAction = createAction("Loads state with the given data");
export const APIServerAddressChangeAction = createAction("Changes the address of the API server");

// Configuration
export const loadItemsStructureAction = createAction("Loads item structure with the given data");
export const selectTabAction = createAction('Selects a tab');
export const addNewItemGetDetailsAction = createAction("Getting Id and details for new Item");
export const setCurrentFlowStateAction = createAction("setting state in progress to the state array");
export const unsetCurrentFlowStateAction = createAction("Removes function in progress to the loading array");
export const setErrorAction = createAction("Sets an error to the state");
export const unsetErrorAction = createAction("Unsets an error to the state");
export const setItemToAddAction = createAction("Sets fields to a new item to add");
export const unsetItemToAddAction = createAction("Unsets fields to a new item to add");
export const selectSubtypeToAddAction = createAction("Selects the subtypefor the new item to add");

