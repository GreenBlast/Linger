import "babel-polyfill";
import { PropTypes } from 'react';
import ReactDOM from 'react-dom';
import { createStore, combineReducers, applyMiddleware, compose } from 'redux';
import { connect, Provider } from 'react-redux';
import createSagaMiddleware from 'redux-saga'
import injectTapEventPlugin from 'react-tap-event-plugin';
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import {Tabs, Tab} from 'material-ui/Tabs';
import DropDownMenu from 'material-ui/DropDownMenu';
import RaisedButton from 'material-ui/RaisedButton';
import RefreshIndicator from 'material-ui/RefreshIndicator';
import TextField from 'material-ui/TextField';
import {Toolbar, ToolbarGroup, ToolbarSeparator, ToolbarTitle} from 'material-ui/Toolbar';
import { ConfigurationReducer, LingerItemsReducer } from './reducers';
import { selectTabAction } from './actions';
import { APIServerAddressChangeAction } from './actions';
import { GET_CONFIGURATION_FROM_SERVER } from './actionTypes'
import { SAVE_CONFIGURATION_TO_SERVER } from './actionTypes'
import { GenericRaisedButtonStyle } from './styles'
import rootSaga from './sagas'
import { LingerItemsBoxContainer } from './Components/LingerItemsBox'
import { TriggerActionsListContainer } from './Components/TriggerActionsList'
// Needed for onTouchTap
// http://stackoverflow.com/a/34015469/988941
injectTapEventPlugin();


// Not calling onChange on Tabs because of bug causing it to be called on other actions as well
const ConfiguratorTabs = ({selectedIndex, handleSelect, indexTable}) => (
	<Tabs
	    value={selectedIndex}
        >
    <Tab label = {indexTable[0]}  value="0" onClick={() => handleSelect("0")} >
        <TriggerActionsListContainer />
    </Tab>
    <Tab label = {indexTable[1]} value="1" onClick={() => handleSelect("1")} >
        <LingerItemsBoxContainer itemType={indexTable[1]} />
    </Tab>
    <Tab label = {indexTable[2]} value="2" onClick={() => handleSelect("2")} >
        <LingerItemsBoxContainer itemType={indexTable[2]} />
    </Tab>
    <Tab label = {indexTable[3]} value="3" onClick={() => handleSelect("3")} >
        <LingerItemsBoxContainer itemType={indexTable[3]} />
    </Tab>
  </Tabs>
)
ConfiguratorTabs.propTypes = {
	selectedIndex: PropTypes.string.isRequired,
	handleSelect: PropTypes.func.isRequired,
	indexTable: PropTypes.array.isRequired
};

const mapStateToConfiguratorTabsProps = (state) =>
{	
	return {
		selectedIndex: state.Configurator.selectedIndex,
		indexTable: state.Configurator.indexTable
	}
}

const mapDispatchToConfiguratorTabsProps = (dispatch) =>
{
	return {
		handleSelect: (current_index) =>
		{
			dispatch(selectTabAction(current_index));
		}
	}
}

const ConfiguratorTabsContainer = connect(
  mapStateToConfiguratorTabsProps,
  mapDispatchToConfiguratorTabsProps
)(ConfiguratorTabs)

const ConfiguratorApp = ({error , isLoadingData, getConfiguration, saveConfiguration, serverAddress, onServerAddressChange}) => (
	<div>
		<Toolbar>
        	<ToolbarGroup >
        		<ToolbarTitle text="Linger configuration" />
          </ToolbarGroup>
          <ToolbarGroup >
            <TextField
                defaultValue={serverAddress}
                hintText="API server address"
                floatingLabelText="API server address"
                floatingLabelFixed={false}
                fullWidth={true}
                onChange={ (e) => onServerAddressChange(e.target.value)}
                />
        	</ToolbarGroup>
        	<ToolbarGroup lastChild={true} style={{float:'right'}}>
              {isLoadingData ?
              <RefreshIndicator
              size={40}
              left={-20}
              top={10}
              status= {isLoadingData ? "loading" : "hide"}
              style={{ marginLeft: '-50%' }}
              />
              :
              <RaisedButton label="Reload config" primary={true} onClick={() => getConfiguration()} />
              }
              <RaisedButton label="Save config" primary={true} onClick={() => saveConfiguration()}/>
              
          	</ToolbarGroup>
      	</Toolbar>
		<ConfiguratorTabsContainer />
	</div>
)
ConfiguratorApp.propTypes = {
  getConfiguration:PropTypes.func.isRequired
}

const mapStateToConfiguratriorAppProps = (state, ownProps,dispatch) => {
    const isLoadingData = -1 != Object.keys(state.Configurator.flow_state).indexOf(GET_CONFIGURATION_FROM_SERVER); 
    const isError = -1 != Object.keys(state.Configurator.flow_error_state).indexOf(GET_CONFIGURATION_FROM_SERVER);
    return {
    error: isError,
    isLoadingData: isLoadingData,
    serverAddress: state.Linger.ApiServerAddress
  }
}

const mapDispatchToConfiguratrorAppProps = (dispatch) => {
  return {
    getConfiguration: () =>
    {
      dispatch({ type: GET_CONFIGURATION_FROM_SERVER });
    },
    saveConfiguration: () =>
    {
      dispatch({ type: SAVE_CONFIGURATION_TO_SERVER });
    },
    onServerAddressChange: (value) => {
      dispatch(APIServerAddressChangeAction(value));
    }
  }
}


export const ConfiguratorAppContainer = connect(
  mapStateToConfiguratriorAppProps,
  mapDispatchToConfiguratrorAppProps
)(ConfiguratorApp);


const sagaMiddleware = createSagaMiddleware()

///// Entry point
const configurationStore = applyMiddleware(sagaMiddleware)(createStore)(combineReducers({
	Configurator:ConfigurationReducer,
	Linger:LingerItemsReducer
  }
	));

sagaMiddleware.run(rootSaga);

// Getting data from the server
configurationStore.dispatch({ type: GET_CONFIGURATION_FROM_SERVER });

// Loading initial data
ReactDOM.render(
	<MuiThemeProvider muiTheme={getMuiTheme(lightBaseTheme)}>
		<Provider store={configurationStore}>
			<ConfiguratorAppContainer/>
	</Provider>
	</MuiThemeProvider>,
	document.getElementById('content'));

