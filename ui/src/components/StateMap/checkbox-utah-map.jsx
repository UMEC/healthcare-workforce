import React from 'react';
import { SVGMap } from 'react-svg-map';
import Utah from './utah';
import { getLocationName, getLocationSelected } from './utils';
// import { connect } from 'http2';
import { connect as reduxConnect } from 'react-redux';
//import '../../../src/svg-map.scss';

class CheckboxUtahMap extends React.Component {
	constructor(props) {
		super(props);

		this.state = {
			pointedLocation: null,
			focusedLocation: null,
			selectedLocations: new Set(),
         tooltipStyle: {
            display: 'none'
         }
		};

		this.handleLocationMouseOver = this.handleLocationMouseOver.bind(this);
		this.handleLocationMouseOut = this.handleLocationMouseOut.bind(this);
		this.handleLocationClick = this.handleLocationClick.bind(this);
		this.handleLocationFocus = this.handleLocationFocus.bind(this);
		this.handleLocationBlur = this.handleLocationBlur.bind(this);
		this.isLocationSelected = this.isLocationSelected.bind(this);
      this.handleLocationMouseMove = this.handleLocationMouseMove.bind(this);
	}

   handleLocationMouseMove(event) {
      const tooltipStyle = {
         display: 'block',
         top: event.clientY + 10,
         left: event.clientX - 100
      };
      this.setState({ tooltipStyle });
   }

	handleLocationMouseOver(event) {
		const pointedLocation = getLocationName(event);
		this.setState({ pointedLocation: pointedLocation });
	}

	handleLocationMouseOut() {
      this.setState({ pointedLocation: null, tooltipStyle: { display: 'none' } });
	}

	handleLocationClick(event) {
		const clickedLocation = getLocationName(event);
		const isSelected = getLocationSelected(event);
		let activeFilterArea = this.props.modelFilters.activeFilters.geo.area;

		let newGeoFilter = activeFilterArea !== clickedLocation
			? { geo: this.props.geoProfile[clickedLocation] }
			: { geo: this.props.geoProfile['State of Utah'] };
		this.props.handleGeoFilterUpdate(newGeoFilter);

		this.setState(prevState => {
			let selectedLocations = new Set(prevState.selectedLocations);

			if (isSelected) {
				selectedLocations.delete(clickedLocation);
			} else {
				selectedLocations.add(clickedLocation);
			}

			return { ...prevState, selectedLocations };
		});
	}

	handleLocationFocus(event) {
		const focusedLocation = getLocationName(event);
		this.setState({ focusedLocation: focusedLocation });
	}

	handleLocationBlur() {
		this.setState({ focusedLocation: null });
	}

	isLocationSelected(location) {
		return this.state.selectedLocations.has(location.name);
	}

	render() {
		return (
			<article className="examples__block">
				<MapHud
					pointedLocation={this.state.pointedLocation}
					focusedLocation={this.state.focusedLocation}
					selectedLocations={this.state.selectedLocations}/>
				<div className="examples__block__map">
					<SVGMap
						map={Utah}
						type="checkbox"
						onLocationMouseOver={this.handleLocationMouseOver}
						onLocationMouseOut={this.handleLocationMouseOut}
						onLocationClick={this.handleLocationClick}
						onLocationFocus={this.handleLocationFocus}
						onLocationBlur={this.handleLocationBlur}
                  onLocationMouseMove={this.handleLocationMouseMove}
						isLocationSelected={this.isLocationSelected} />
                  <div className="svg-map__tooltip" style={this.state.tooltipStyle}>
                     {this.state.pointedLocation}
                  </div>
				</div>
			</article>
		);
	}
}

const mapStateToProps = (state) => {
	return {
		geoProfile: state.geoProfile,
		modelFilters: state.modelFilters,
	}
}

export default reduxConnect(mapStateToProps)(CheckboxUtahMap);

const MapHud = props => {
	return (
		<>
			<h2 className="examples__block__title">
				Utah County Map
					</h2>
			<div className="examples__block__info">
				<div className="examples__block__info__item">
					Pointed location: {props.pointedLocation}
				</div>
				<div className="examples__block__info__item">
					Focused location: {props.focusedLocation}
				</div>
				<div className="examples__block__info__item">
					Selected locations:
							<ul>
						{
							[...props.selectedLocations].map(location => (<li key={location}>{location}</li>))
						}
					</ul>
				</div>
			</div>
		</>
	);
}