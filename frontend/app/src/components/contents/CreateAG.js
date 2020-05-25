/**
 * This file contains the editor for access groups
 */

import React, { useState } from 'react';
import { TextField, Button } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import { colorTheme } from '../../App';
import MapViewer from '../map/MapViewer.js';
import { withRouter } from 'react-router-dom';
import styled from 'styled-components';
import ApproverSearch from './ApproverSearch.js';
import { useDispatch, useSelector } from 'react-redux'
import { highlightRooms, createAccessGroup } from '../../actions/roomActions';

const GridLayout = styled.div`
  height: 100vh;
  padding: 0em 1em;
  gap: 1em 1em;
  display: grid;
  box-sizing: border-box;
  grid-template-areas:
    "header header header"
    "submit name search"
    "map map map";
  grid-template-rows: 70px auto 1fr;
  grid-template-columns: auto auto 1fr;
`;

const useStyles = makeStyles(() => ({
	paper: {
    gridArea: 'name',
    placeSelf: "center normal",
    maxWidth: "300px"
	},
  name: {
    backgroundColor: colorTheme.palette.primary.white,
  },
  button_div: {
    gridArea: 'submit',
    placeSelf: "center normal",
    maxWidth: "200px"
  }

}));

/**
 * Start component. Contains the MapViewer and a button for simulating pressing on a room.
 * The parameter props comes from withRouter (see bottom of document)
 */
function CreateAG() {
  // Fetch styles-variable
  const classes = useStyles();

  const dispatch = useDispatch();
  const highlightedRooms = useSelector(state => state.rooms.highlightedRooms);
  const [name, setName] = useState("");
  const [approvers, setApprovers] = useState([]);

  const handleRoomClick = (roomId) => {
    const index = highlightedRooms.indexOf(roomId);
    if (index > -1) {
        const newRooms = [...highlightedRooms];
        newRooms.splice(index, 1);
        dispatch(highlightRooms(newRooms))
    } else {
        dispatch(highlightRooms([...highlightedRooms, roomId]))
    }
  }

  const handleSubmit = (event) => {
    event.preventDefault();
    const data = {
        ag_name: name,
        approvers: approvers,
        room_text_ids: highlightedRooms
    }
    dispatch(createAccessGroup(data))
	}

	return(
		<GridLayout>
			<MapViewer approver={true} onSelect={handleRoomClick}/>
			<ApproverSearch setApprovers={setApprovers}/>
      <div className={classes.paper}>
        <TextField
          className={classes.name}
          fullWidth
          margin="normal"
          label="Access Group Name"
          variant="outlined"
          value={name}
          onChange={event => setName(event.target.value)}
        />
      </div>
      <div className={classes.button_div}>
        <Button
          onClick={handleSubmit}
          fullWidth
          variant="contained"
          color="primary"
        >
          Create Access Group
        </Button>
      </div>
		</GridLayout>
	)
} export default withRouter(CreateAG)
// Exporting the component wrapped around "withRouter" gives the component access to props.history,
// which means that the component can route the users to other pages.
