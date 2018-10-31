import React, { Component } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types'

import ViewHeader from '../../components/ViewHeader';
import ViewSection from '../../components/ViewSection';
import ViewContainer from '../../components/ViewContainer';
import ViewFooter from '../../components/ViewFooter';
import Panel from '../../components/Panel';
import ProviderRoles from '../../modules/ProviderRoles';

import { SET_MODEL_GEO_FILTER } from '../../actions';



class ModelOutputContainer extends Component {
  constructor(props) {
    super(props);
    this.state = {
      modifiedModelAttributes: {},
      filteredModelOutput: {},
      filtersApplied: false,
      modelParamsEdited: false,
    }

    this.handleGeoFilterUpdate = this.handleGeoFilterUpdate.bind(this);
  }

  componentWillUpdate(nextProps, nextState) {
    // console.log('new State', nextState)
  }

  updateModelAttributes = (currentServiceAttrs) => {
    this.setState({  
      modifiedModelAttributes: {...this.state.modifiedModelAttributes, currentServiceAttrs},
      modelParamsEdited: true,
    })
  }

  handleGeoFilterUpdate(filter) {

    // if (filter.geo.area == 'State of Utah') {
      
    //   // the 'all' filter is the state for no filters applied
    //   // so set the filters applied to false
    //   this.setState({ filtersApplied: false })
    // } else {
    //   // When applying filters to the model output, this piece of state 
    //   // can be used to programatically toggle components on and off.
    //   this.setState({ filtersApplied: true })
    // }
    this.props.setGeoFilter(filter)
  }
  
  render() {
    let { servicesByProvider } = this.props.currentModelOutput;
    // let filtersCount = Object.keys(this.props.selectedFilters).length;
    let { modelParamsEdited} = this.state.filtersApplied;

    return (
      <>
        <ViewContainer>
          <ViewHeader 
            currentGeoName={this.props.modelFilters.activeFilters.geo.area}  />
          <div className="view-body">
            <ViewSection 
              updateModelAttributes={this.updateModelAttributes} title="">
              <ProviderRoles
                activeFilters={this.props.modelFilters.activeFilters}
                servicesByProvider={servicesByProvider}
                updateModelAttributes={this.updateModelAttributes} />
            </ViewSection>
          </div>

          {modelParamsEdited ?
            <ViewFooter>
              <p>{`You've changed some model params!` }</p>
            </ViewFooter> 
            : null }
        </ViewContainer>
        <Panel modelFilters={this.props.modelFilters} handleGeoFilterUpdate={this.handleGeoFilterUpdate}/>
      </>
    );
  }

};

ModelOutputContainer.defaultProps = {
  modelOutput: {},
  selectedFilters: {
    geography: 'a',
    provider: 'phys',
  },
};

ModelOutputContainer.propTypes = {
  modelOutput: PropTypes.object.isRequired,
  selectedFilters: PropTypes.object.isRequired,
};

const mapStateToProps = (state) => {
  return {
    currentModelOutput: state.currentModelOutput,
    modelFilters: state.modelFilters,
  }
};


/**
 * mapStateToDispatch()
 * 
 * action creators that will need to be dispatched to the store
 * these actions ultimately update the redux store, and if an async
 * call needs to be made to the API, that will be handeled by a saga.
 * The result of the saga will be passed to the action when the saga
 * calls it with a put()
 * 
 * Sagas live in `/ui/src/sagas`
 */
const mapDispatchToProps = dispatch => {
  return {
    setGeoFilter: (newFilter) => dispatch({ type: SET_MODEL_GEO_FILTER, payload: newFilter })
  }
};

export default connect(mapStateToProps, mapDispatchToProps)(ModelOutputContainer);