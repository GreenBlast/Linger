import { PropTypes } from 'react';
import { connect } from 'react-redux';
import { ConfigBoxContainer } from './ConfigBox';

const ConfigPanel = ({configFields, uuid}) => (
	<div>
		{configFields.map( field =>
			<ConfigBoxContainer
				key={uuid + ":" + field}
				uuid={uuid}
				field={field}
			/>
		)}
	</div>
)
ConfigPanel.propTypes = {
	configFields:PropTypes.array.isRequired,
	uuid: PropTypes.string.isRequired,
}

const mapStateToConfigPanelProps = (state, ownProps) => {
	const item = state.Linger.Items[ownProps.uuid];

	const nonEditableFields = ["uuid","type","subtype"]

	// Filtering fields that shouldn't be changed
	const configFields = Object.keys(item).filter( field => (nonEditableFields.indexOf(field) == -1));
	return {
		configFields: configFields,
		uuid: ownProps.uuid
	}
}

export const ConfigPanelContainer = connect(
	mapStateToConfigPanelProps,
	null
)(ConfigPanel)
