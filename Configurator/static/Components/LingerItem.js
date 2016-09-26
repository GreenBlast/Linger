import { PropTypes } from 'react';
import { connect } from 'react-redux';
import { Card, CardActions, CardHeader, CardText } from 'material-ui/Card';
import RaisedButton from 'material-ui/RaisedButton';
import { LowerRightRaisedButtonStyle } from '../styles';
import {ConfigPanelContainer} from './ConfigPanel';
import { deleteItemAction } from '../actions';

const LingerItem = ({title, uuid, handleDelete}) => (
	<Card>
    <CardHeader
      title={title}
      subtitle={uuid}
      actAsExpander={true}
      showExpandableButton={true}
    />
    <CardText expandable={true}>
    	<ConfigPanelContainer key={uuid + ":config_panel"} uuid={uuid}/>
    </CardText>
    <CardActions style={{ width: '100%', textAlign: 'right' }}>
      <RaisedButton style={LowerRightRaisedButtonStyle} label="Delete" onClick={() => handleDelete(uuid)} />
    </CardActions>
  </Card>
)
LingerItem.propTypes = {
	title:PropTypes.string.isRequired,
	uuid:PropTypes.string.isRequired,
	handleDelete:PropTypes.func.isRequired
}

const mapStateToLingerItemProps = (state, ownProps) => {
	const item = state.Linger.Items[ownProps.uuid];
	const title = item.label == "" ? item.subtype : [item.label, item.subtype].join(" - ")
	return {
		title:title,
		uuid: ownProps.uuid,
	}
}

const mapDispatchToLingerItemProps = (dispatch) => {
	return {
		handleDelete: (uuid) =>
		{
      		dispatch(deleteItemAction(uuid));
		}
	}
}


export const LingerItemContainer = connect(
	mapStateToLingerItemProps,
	mapDispatchToLingerItemProps
)(LingerItem)
