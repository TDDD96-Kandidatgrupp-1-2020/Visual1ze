/**
 * This file contains the Start content component for approvers.
 */

import React, { useState } from 'react';
import MapViewer from '../map/MapViewer.js';
import { withRouter } from 'react-router-dom';
import styled from 'styled-components';
import PendingRequest from './PendingRequest';
import UserSearch from './UserSearch.js';
import AnsweringRequest from './AnsweringRequest';


const GridLayout = styled.div`
  height: 100vh;
  padding: 0em 1em;
  gap: 1em 1em;
  display: grid;
  box-sizing: border-box;
  grid-template-areas:
    "header header"
    ". search"
    "pending map";
  grid-template-rows: 70px auto 1fr;
  grid-template-columns: 1fr 5fr;
`;

/**
 * Start component. Contains the MapViewer and a button for simulating pressing on a room.
 * The parameter props comes from withRouter (see bottom of document)
 */
function ApproverStart(props) {
	// Variable that decides which component is to be shown: PendingRequests or AnsweringRequest
	const [showPendingRequests, setShowPendingRequest] = useState(true);

	return(
  	<GridLayout>
  		<MapViewer approver={true}/>
  		{showPendingRequests &&
  		<PendingRequest showPendingRequests={showPendingRequests} setShowPendingRequest={setShowPendingRequest}/>
  		}
  		{!showPendingRequests &&
  		<AnsweringRequest setShowPendingRequest={setShowPendingRequest} />
  		}
  		<UserSearch />
  	</GridLayout>
	)
} export default withRouter(ApproverStart)
// Exporting the component wrapped around "withRouter" gives the component access to props.history,
// which means that the component can route the users to other pages.
