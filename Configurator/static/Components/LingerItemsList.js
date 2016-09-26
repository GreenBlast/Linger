import { PropTypes } from 'react';
import { connect } from 'react-redux';
import { LingerItemContainer } from './LingerItem';

const LingerItemsList =  ({ids}) => (
	<div>
		{ids.map( uuid => 
			<LingerItemContainer
			uuid = {uuid}
			key = {uuid + ":LingerItem"}
			/>
			)}
	</div>
)
LingerItemsList.propTypes = {
	ids:PropTypes.array.isRequired,
}

const mapStateToLingerItemListProps = (state, ownProps) => {
	const filteredIds = Object.keys(state.Linger.Items).filter(key => (state.Linger.Items[key].type == ownProps.itemType))
	return {
		ids: filteredIds
	}
}

export const LingerItemsListContainer = connect(
	mapStateToLingerItemListProps,
	null
)(LingerItemsList);

