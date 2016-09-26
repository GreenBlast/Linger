import { PropTypes } from 'react';
import { connect } from 'react-redux';
import { changeFieldAction } from '../actions';
import { setItemToAddAction } from '../actions';
import TextField from 'material-ui/TextField';

const ConfigBox = ({uuid, field, value, changeField}) => (
	<div className = "configBoxContainer">
		<TextField
		defaultValue={value}
		hintText={field}
		floatingLabelText={field}
		floatingLabelFixed={true}
		fullWidth={true}
		onChange={ (e) => changeField(uuid, field, e.target.value)}
		/>
	</div>
)
ConfigBox.propTypes = {
	uuid:PropTypes.string.isRequired,
	field:PropTypes.string.isRequired,
	value:PropTypes.string.isRequired,
	changeField: PropTypes.func.isRequired,
}


const mapStateToAddNewItemConfigBoxProps = (state, ownProps) => {
	const item = state.Configurator.items_to_add[ownProps.uuid];

	return {
		field: ownProps.field,
		value: ownProps.field in item ? item[ownProps.field] : "",
		uuid: ownProps.uuid
	}
}

const mapDispatchToAddNewItemConfigBoxProps = (dispatch) => {
	return {
		changeField: (uuid, field, value) =>
		{
      		dispatch(setItemToAddAction({uuid:uuid, [field]:value}));
		}
	}
}

export const AddNewItemConfigBoxContainer = connect(
	mapStateToAddNewItemConfigBoxProps,
	mapDispatchToAddNewItemConfigBoxProps
)(ConfigBox)



const mapStateToConfigBoxProps = (state, ownProps) => {
	const item = state.Linger.Items[ownProps.uuid];

	return {
		field: ownProps.field,
		value: item[ownProps.field],
		uuid: ownProps.uuid
	}
}

const mapDispatchToConfigBoxProps = (dispatch) => {
	return {
		changeField: (uuid, field, value) =>
		{
      		dispatch(changeFieldAction({uuid:uuid, field:field, value:value}));
		}
	}
}


export const ConfigBoxContainer = connect(
	mapStateToConfigBoxProps,
	mapDispatchToConfigBoxProps
)(ConfigBox)
