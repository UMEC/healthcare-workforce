import React, { Component } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types'

import ViewHeader from '../../components/ViewHeader';
import ViewSection from '../../components/ViewSection';
import ViewContainer from '../../components/ViewContainer';
import ViewFooter from '../../components/ViewFooter';
import Panel from '../../components/Panel';

class ModelOutputContainer extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedFilters: {},
      modifiedModelAttributes: {},
      filteredModelOutput: {},
    }
  }

  updateModelAttributes = () => {
    console.log('attrinute updated!')
  }
  
  render() {
    let filtersCount = Object.keys(this.props.selectedFilters).length;
    let filtersApplied = Object.keys(this.props.selectedFilters).length > 0;

    return (
      <>
        <ViewContainer>
          <ViewHeader />
          <ViewSection updateModelAttributes={this.updateModelAttributes} title="">
            <p>NEW MODULES GO IN VIEW SECTIONS :)</p>
          </ViewSection>
          { filtersApplied ?
            <ViewFooter>
              <p>{`${filtersCount} filters applied to the model output` }</p>
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
    defaultModel: state.defaultModel,
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