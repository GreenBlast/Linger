import { PropTypes } from 'react';
import { connect } from 'react-redux';
import RaisedButton from 'material-ui/RaisedButton';
import LinearProgress from 'material-ui/LinearProgress';
import { GenericRaisedButtonStyle } from '../styles';
import { LingerItemsListContainer } from './LingerItemsList'
import { LingerItemAdderContainer } from './LingerItemAdder'
import { ADD_NEW_ITEM_CLICKED } from '../actionTypes';
import { ADD_NEW_ITEM_UUID_READY } from '../actionTypes';

const LingerItemsBox = ({itemType, gettingIdAndDetails, readyToInsertData, addNewItem}) => (
	<div>
		<LingerItemsListContainer itemType={itemType}/>
		{readyToInsertData?
		<LingerItemAdderContainer itemType={itemType}/>
		:
		gettingIdAndDetails? 
		<LinearProgress mode="indeterminate" />
		:
		 <RaisedButton style={GenericRaisedButtonStyle} fullWidth={true} onClick={() => addNewItem(itemType)}>Add new {itemType}...</RaisedButton>
		}
	</div>
)
LingerItemsBox.propTypes = {
	itemType: PropTypes.string.isRequired,
}

const mapStateToLingerItemsBoxProps = (state, ownProps) => {
	const gettingIdAndDetails = -1 != Object.keys(state.Configurator.flow_state).indexOf(ADD_NEW_ITEM_CLICKED+ownProps.itemType);
	const readyToInsertData = -1 != Object.keys(state.Configurator.flow_state).indexOf(ADD_NEW_ITEM_UUID_READY+ownProps.itemType);
	return {
		itemType: ownProps.itemType,
		gettingIdAndDetails: gettingIdAndDetails,
		readyToInsertData: readyToInsertData
	}
}

const mapDispatchToLingerItemsBoxProps = (dispatch) => {
  return {
    addNewItem: (itemType) =>
    {	
      	dispatch({ type: ADD_NEW_ITEM_CLICKED, item_type:itemType});
    }
  }
}

export const LingerItemsBoxContainer = connect(
	mapStateToLingerItemsBoxProps,
	mapDispatchToLingerItemsBoxProps
)(LingerItemsBox);
