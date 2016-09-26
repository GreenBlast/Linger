import { PropTypes } from 'react';
import { connect } from 'react-redux';
import { TriggerActionsItemContainer } from './TriggerActionsItem';

const TriggerActionsList =  ({enabledIds, disabledIds}) => (
	<div>
		{enabledIds.map( uuid => 
			<TriggerActionsItemContainer
			uuid = {uuid}
			key = {uuid + ":TriggerAction"}
			isEnabled = {true}
			/>
			)}
		{disabledIds.map( uuid => 
			<TriggerActionsItemContainer
			uuid = {uuid}
			key = {uuid + ":TriggerAction"}
			isEnabled = {false}
			/>
			)}
	</div>
)
TriggerActionsList.propTypes = {
	enabledIds:PropTypes.array.isRequired,
	disabledIds:PropTypes.array.isRequired,
}

const mapStateToTriggerActionsListProps = (state, ownProps) => {
	let filteredTriggers = Object.keys(state.Linger.Items).filter(key => (state.Linger.Items[key].type == "Triggers"))
	let enabled = []
	let disabled = []

	filteredTriggers.map( (uuid) => state.Linger.TriggerActions[uuid].enabled ? enabled.push(uuid): disabled.push(uuid));
	return {
		enabledIds: enabled,
		disabledIds: disabled
	}
}

export const TriggerActionsListContainer = connect(
	mapStateToTriggerActionsListProps,
	null
)(TriggerActionsList);