import { PropTypes } from 'react';
import { connect } from 'react-redux';
import { Card, CardActions, CardHeader, CardText } from 'material-ui/Card';
import RaisedButton from 'material-ui/RaisedButton';
import SelectField from 'material-ui/SelectField';
import MenuItem from 'material-ui/MenuItem';
import { LowerRightRaisedButtonStyle } from '../styles';
import { ADD_NEW_ITEM_UUID_READY } from '../actionTypes';
import { selectSubtypeToAddAction } from '../actions';
import { unsetItemToAddAction } from '../actions';
import { unsetCurrentFlowStateAction } from '../actions';
import { addItemAction } from '../actions';
import { AddingItemConfigPanelContainer } from './AddingItemConfigPanel';


const LingerItemAdder = ({itemType, newUuid, selectedSubtype, subtypes, selectSubtype, handleAdd, handleCancel, currentItem}) => (
	<div>
	<Card>
    <CardHeader
      title={"Adding new " + itemType}
      subtitle={"id: " + newUuid}
    />
    <CardText expandable={false}>
		<SelectField value={selectedSubtype}
					 floatingLabelText="Subtype"
					 onChange={(event, index, value) => selectSubtype(newUuid, value)}	>
			{subtypes.map( (type,index) =>
			<MenuItem 
				key={newUuid + ":" + type}
				value={type}
				primaryText ={type}
			/>)}
        </SelectField>
        <AddingItemConfigPanelContainer itemType={itemType} uuid={newUuid} selectedSubtype={selectedSubtype}/>
    </CardText>
    <CardActions style={{ width: '100%', textAlign: 'right' }}>
      <RaisedButton style={LowerRightRaisedButtonStyle} label="Add" onClick={() => handleAdd(newUuid, itemType, currentItem)} />
      <RaisedButton style={LowerRightRaisedButtonStyle} label="Cancel" onClick={() => handleCancel(newUuid, itemType)} />
    </CardActions>
  </Card>
  </div>
)
LingerItemAdder.propTypes = {
	itemType: PropTypes.string.isRequired,
	newUuid: PropTypes.string.isRequired,
	subtypes: PropTypes.array.isRequired,
	selectedSubtype: PropTypes.string.isRequired,
	handleAdd:PropTypes.func.isRequired,
	handleCancel:PropTypes.func.isRequired,
	currentItem:PropTypes.object.isRequired
}

const mapStateToLingerItemAdderProps = (state, ownProps) => {
	const newUuid = state.Configurator.flow_state[ADD_NEW_ITEM_UUID_READY+ownProps.itemType].new_uuid;
	const item = state.Configurator.items_to_add[newUuid]
	const subtypes = Object.keys(state.Configurator.item_structure[ownProps.itemType]);
	const selectedSubtype = item.subtype;

	// Filtering the fields that shouldn't be added
	const item_structure = state.Configurator.item_structure[ownProps.itemType][selectedSubtype];
	const mandatoryConfigFields = item_structure["mandatory"].map( field => field[0]);
	const optionalConfigFields = item_structure["optional"].map( field => field[0]);

	const relevantConfigFields = mandatoryConfigFields.concat(optionalConfigFields);
	let currentItem = relevantConfigFields.reduce((o, k) => { o[k] = item[k]; return o; }, {});

	return {
		newUuid: newUuid,
		itemType: ownProps.itemType,
		subtypes: subtypes,
		selectedSubtype: selectedSubtype,
		currentItem: currentItem
	}
}

const mapDispatchToLingerItemAdderProps = (dispatch) => {
  return {
    selectSubtype: (uuid, subtype) =>
    {	
      	dispatch(selectSubtypeToAddAction({uuid:uuid, subtype:subtype}));
    },
    handleAdd: (uuid, itemType, item) =>
    {	
      	dispatch(unsetCurrentFlowStateAction(ADD_NEW_ITEM_UUID_READY+itemType))
      	dispatch(addItemAction({uuid:uuid, item:item}));
      	dispatch(unsetItemToAddAction(uuid));
    },
    handleCancel: (uuid, itemType) =>
    {	
      	dispatch(unsetCurrentFlowStateAction(ADD_NEW_ITEM_UUID_READY+itemType))
      	dispatch(unsetItemToAddAction(uuid));
    }
  }
}

export const LingerItemAdderContainer = connect(
	mapStateToLingerItemAdderProps,
	mapDispatchToLingerItemAdderProps
)(LingerItemAdder);
