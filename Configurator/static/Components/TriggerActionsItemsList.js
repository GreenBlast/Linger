import { PropTypes } from 'react';
import { connect } from 'react-redux';
import {List, ListItem} from 'material-ui/List';
import Subheader from 'material-ui/Subheader';
import Divider from 'material-ui/Divider';
import { addActionToTriggerAction } from '../actions';
import { removeActionFromTriggerAction } from '../actions';

const TriggerActionsItemsList =  ({uuid, enabledIds, disabledIds, removeAction, addAction}) => (
	  <List>
        <Subheader>Actions in trigger</Subheader>
		{enabledIds.map( action => 
        <div  key={uuid + ":" + action.uuid + ":Div"}>
        <ListItem
               	  key={uuid + ":" + action.uuid + ":TriggerActionsList"}
                  primaryText={action.text}
                  secondaryText={action.uuid}
                  secondaryTextLines={1}
                  onClick = { () => removeAction(uuid, action.uuid)}
                />
        <Divider inset={true} key={uuid + ":" + action.uuid + ":TriggerActionsListDivider"}/>
        </div>
        )}
        <Subheader>Actions not in trigger</Subheader>
		{disabledIds.map( action => 
        <div  key={uuid + ":" + action.uuid + ":Div"}>
        <ListItem
       	  key={uuid + ":" + action.uuid + ":TriggerActionsList"}
          primaryText={action.text}
          secondaryText={action.uuid}
          secondaryTextLines={1}
          onClick = { () => addAction(uuid, action.uuid)}
        />
        <Divider inset={true} key={uuid + ":" + action.uuid + ":TriggerActionsListDivider"}/>
        </div>
		)}
		</List>
)
TriggerActionsItemsList.propTypes = {
	uuid:PropTypes.string.isRequired,
	enabledIds:PropTypes.array.isRequired,
	disabledIds:PropTypes.array.isRequired,
}

const getAction = (Items, uuid) => {
	const action = Items[uuid];
	const title = action.label == "" ? action.subtype : [action.label, action.subtype].join(" - ")
	return {
		uuid:uuid,
		text:title,
	}
}

const mapStateToTriggerActionsItemsListProps = (state, ownProps) => {
	const filteredTriggers = Object.keys(state.Linger.Items).filter(key => (state.Linger.Items[key].type == "Actions"))
	let enabled = []
	let disabled = []
	filteredTriggers.map( (actionUuid) => state.Linger.TriggerActions[ownProps.uuid].actions.indexOf(actionUuid) >= 0 ? enabled.push(getAction(state.Linger.Items, actionUuid)): disabled.push(getAction(state.Linger.Items, actionUuid)));
	return {
		uuid: ownProps.uuid,
		enabledIds: enabled,
		disabledIds: disabled
	}
}

const mapDispatchToTriggerActionsItemsListProps = (dispatch) => {
	return {
		removeAction: (uuid,actionUuid) =>
		{
			dispatch(removeActionFromTriggerAction({triggerUuid:uuid, actionUuid:actionUuid}));
		},
		addAction: (uuid,actionUuid) =>
		{
			dispatch(addActionToTriggerAction({triggerUuid:uuid, actionUuid:actionUuid}));
		}
	}
}


export const TriggerActionsItemsListContainer = connect(
	mapStateToTriggerActionsItemsListProps,
	mapDispatchToTriggerActionsItemsListProps
)(TriggerActionsItemsList);

