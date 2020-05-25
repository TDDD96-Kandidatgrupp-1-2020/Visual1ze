/**
 * This file contains the Start content component for the Reader.
 */

import React from 'react';
import MapViewer from '../map/MapViewer.js';
import { withRouter } from 'react-router-dom';
import styled from 'styled-components';
import AGSearch from './AGSearch.js';
import RoomSearch from './RoomSearch.js';

// 100vh is 100% of the viewport, it is set to 98 to avoid a scrollbar appearing
const GridLayout = styled.div`
  height: 100vh;
  padding: 0em 1em;
  gap: 1em 1em;
  display: grid;
  box-sizing: border-box;

  grid-template-areas:
    "header"
    "search"
	  "map";
  grid-template-rows: 70px auto 1fr;
  grid-template-columns: 1fr;
`;

/**
 * Start component. Contains the MapViewer and a button for simulating pressing on a room.
 * The parameter props comes from withRouter (see bottom of document)
 */
function ReaderStart(props) {
	// Fetch JSON object containing user information that is stored in the browser's sessionStorage.
	const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));

	// Based on the role from userinformation we can direct the user to the right request form
	/**
	 * Example: role = "reader"
	 * URL will become: "/reader/request/form"
	 * This will ensure that reader can't get to an admin or approver page.
	 */
	const handleRequest = () => {
		props.history.push("/" + userInformation.role + "/requests/form");
	}

	return(
		<GridLayout>
			<MapViewer approver={false} handleRequest={handleRequest}
			selectedRoom={props.selectedRoom} selectRoom={props.selectRoom}/>
			<AGSearch setAG={props.setAG} selectedAG={props.selectedAG} />
			<RoomSearch/>
		</GridLayout>
	)
} export default withRouter(ReaderStart)
// Exporting the component wrapped around "withRouter" gives the component access to props.history,
// which means that the component can route the users to other pages.
