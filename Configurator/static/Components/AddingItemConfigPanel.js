import { PropTypes } from 'react';
import { connect } from 'react-redux';
import Subheader from 'material-ui/Subheader';
import { AddNewItemConfigBoxContainer } from './ConfigBox';


// First item in each field array is the field name, the second is the field type- can be used for validation later
const AddingItemConfigPanel = ({mandatoryConfigFields, optionalConfigFields, uuid}) => (
	<div>
        <Subheader>Mandatory fields</Subheader>
	    {mandatoryConfigFields.map( field =>
			<AddNewItemConfigBoxContainer 
				key={uuid + ":" + field[0]}
				uuid={uuid}
				field={field[0]}
			/>
		)}
        <Subheader>Optional fields</Subheader>
	    {optionalConfigFields.map( field =>
			<AddNewItemConfigBoxContainer 
				key={uuid + ":" + field[0]}
				uuid={uuid}
				field={field[0]}
			/>
		)}
	</div>
)
AddingItemConfigPanel.propTypes = {
	mandatoryConfigFields:PropTypes.array.isRequired,
	optionalConfigFields:PropTypes.array.isRequired,
	uuid: PropTypes.string.isRequired,
}

const mapStateToAddingItemConfigPanelProps = (state, ownProps) => {
	const item_structure = state.Configurator.item_structure[ownProps.itemType][ownProps.selectedSubtype];
	const nonEditableFields = ["uuid","type","subtype"]

	// Filtering the fields that shouldn't be added
	const mandatoryConfigFields = item_structure["mandatory"].filter( field => (nonEditableFields.indexOf(field[0]) == -1));
	const optionalConfigFields = item_structure["optional"];
	return {
		mandatoryConfigFields: mandatoryConfigFields,
		optionalConfigFields: optionalConfigFields,
		uuid: ownProps.uuid
	}
}

export const AddingItemConfigPanelContainer = connect(
	mapStateToAddingItemConfigPanelProps,
	null
)(AddingItemConfigPanel)
