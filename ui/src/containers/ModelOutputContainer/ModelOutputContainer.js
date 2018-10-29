import React, { Component } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types'

import ViewHeader from '../../components/ViewHeader';
import ViewSection from '../../components/ViewSection';
import ViewContainer from '../../components/ViewContainer';
import ViewFooter from '../../components/ViewFooter';
import Panel from '../../components/Panel';
import ProviderRoles from '../../modules/ProviderRoles';

class ModelOutputContainer extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedFilters: {},
      modifiedModelAttributes: {},
      filteredModelOutput: {},
      filtersApplied: false,
      modelParamsEdited: false,
    }
  }

  updateModelAttributes = (i, o) => {
    console.log(`attrinute for ${i} updated!`)
    console.log(o)
  }
  
  render() {
    console.log(this.props.currentModelOutput.servicesByProvider)
    let { servicesByProvider } = this.props.currentModelOutput;
    // let filtersCount = Object.keys(this.props.selectedFilters).length;
    let { modelParamsEdited} = this.state.filtersApplied;

    return (
      <>
        <ViewContainer>
          <ViewHeader />
          <div className="view-body">
            <ViewSection 
              updateModelAttributes={this.updateModelAttributes} title="">
              <ProviderRoles
                availableProviderTypes={['Physician']} 
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
        <Panel />
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
const mapDispatchToProps = () => {
  return {}
};

export default connect(mapStateToProps, mapDispatchToProps)(ModelOutputContainer);