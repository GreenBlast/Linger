import { PropTypes } from 'react';
import { connect } from 'react-redux';
import { Card, CardActions, CardHeader, CardText } from 'material-ui/Card';
import Toggle from 'material-ui/Toggle';
import { DisableToggleStyle } from '../styles';
import { toggleTriggerAction } from '../actions';
import {LingerItemsListContainer} from './LingerItemsList'
import {TriggerActionsItemsListContainer} from './TriggerActionsItemsList'

const TriggerActionsItem = ({title, uuid, isEnabled, handleToggle}) => (
	<Card>
    <CardHeader
      title={title}
      subtitle={uuid}
      actAsExpander={true}
      showExpandableButton={true}
    />
    <CardText expandable={true}>
    	  <TriggerActionsItemsListContainer uuid={uuid}/>
    </CardText>
    <CardActions style={{ textAlign: 'right' }}>
  	  <Toggle
            toggled={isEnabled}
            onToggle={() => handleToggle(uuid)}
            label={isEnabled ? "Disable" : "Enable" } 
            style={DisableToggleStyle}
       />
    </CardActions>
  </Card>
)
TriggerActionsItem.propTypes = {
	title:PropTypes.string.isRequired,
	uuid:PropTypes.string.isRequired,
	isEnabled:PropTypes.bool.isRequired,
	handleToggle:PropTypes.func.isRequired
}

const mapStateToTriggerActionsItemProps = (state, ownProps) => {
	const item = state.Linger.Items[ownProps.uuid];
	const title = item.label == "" ? item.subtype : [item.label, item.subtype].join(" - ")
	return {
		title:title,
		uuid: ownProps.uuid,
		isEnabled:ownProps.isEnabled,
	}
}

const mapDispatchToTriggerActionsItemProps = (dispatch) => {
	return {
		handleToggle: (uuid) =>
		{
			dispatch(toggleTriggerAction(uuid));
		}
	}
}


export const TriggerActionsItemContainer = connect(
	mapStateToTriggerActionsItemProps,
	mapDispatchToTriggerActionsItemProps
)(TriggerActionsItem)
