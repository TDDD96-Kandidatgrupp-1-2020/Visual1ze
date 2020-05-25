/**
 * This component represents the table containing the pending requests. Shown in
 * approver and admin page.
 */

import React, { useEffect, useState } from 'react';
import auth from '../../auth';
import { makeStyles } from '@material-ui/core/styles';
import { Redirect } from 'react-router-dom';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@material-ui/core';
import { Box, Container, Paper, Typography } from '@material-ui/core';
import styled from 'styled-components';
import { colorTheme } from '../../App';
import { highlightRooms } from '../../actions/roomActions';
import { selectRequest } from '../../actions/otherUserActions';
import { useDispatch } from 'react-redux';
import axios from 'axios';

// Variable containing styling of components in the render function below.
const useStyles = makeStyles((theme) => ({
  tableContainer: {
    backgroundColor: colorTheme.palette.primary.light,
    gridArea: "pending",
  },
	table: {
		backgroundColor: colorTheme.palette.primary.light,
	},
	head: {
		backgroundColor: colorTheme.palette.primary.dark,
		color: colorTheme.palette.primary.contrastText,
		fontSize: 16,
		fontWeight: 'bold',
		textAlign: 'center',
	},
	box: {
		marginTop: theme.spacing(0.5),
		backgroundColor: colorTheme.palette.primary.main,
		'&:hover': {
			backgroundColor: colorTheme.palette.secondary.dark,
			cursor: 'pointer'
		  }
	},
	text: {
		marginLeft: theme.spacing(0.5),
    marginRight: theme.spacing(0.5),
		color: colorTheme.palette.primary.contrastText,
		fontSize: 15,
		paddingTop: theme.spacing(0.2),
		paddingLeft: theme.spacing(0.5),
		paddingBottom: theme.spacing(0.2),
	},
}));


export default function PendingRequest(props) {
  // Fetch styles-variable
  const classes = useStyles();
  // React-redux syntax
  const dispatch = useDispatch();
  // Variable containing pending requests fetched from server
  const [pendingRequests, setPendingRequests] = useState([]);

  /**
   * Fetch pending requests from server and save them in state pendingRequests.
   * This function in run everytime the component is rendered.
   */
  useEffect(() => {
	const fetchData = async () => {
		// Fetch JSON object containing user information that is stored in the browser's sessionStorage.
		const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));

		axios.get("/approver/orders", userInformation.header)
		.then(function (response) {
			setPendingRequests(response.data.orders);
		})
		.catch(function (error) {
			console.log("Error in PendingRequest");
			console.log(error.response);
		});
	};
	fetchData();
	}, [props.setShowPendingRequest]);

  // If we are not logged in we must redirect back to loginpage!
  if (!auth.isAuthenticated()) {
    return <Redirect to="/"/>
  }

  /**
   * Handles click in one of the requests in the table. It communicates with map
   * saying which room was clicked and changes value of state in parent component
   * so that another component is shown.
   */
  const handleClick = (request) => {
		// Show in the map the room/AG that this request is about
		if (request.access_name) {
			if (request.rooms) {
				dispatch(highlightRooms(request.rooms));
			} else if (request.room_id) {
				dispatch(highlightRooms([request.room_id]))
			}
		}
		// Update variable so that parent component shows AnsweringRequest instead
		props.setShowPendingRequest(false);
    dispatch(selectRequest(request))
	}

	const handleHover = (request) => {
		if (request.room_id) {
			dispatch(highlightRooms([request.room_id]));
		} else if (request.rooms) {
			dispatch(highlightRooms(request.rooms));
		}
	}

  return(
    <TableContainer component={Paper} className={classes.tableContainer}>
    	<Table stickyHeader className={classes.table}>
    		<TableHead>
    			<TableRow>
    				<TableCell className={classes.head}>Pending Requests</TableCell>
    			</TableRow>
    		</TableHead>
    		<TableBody>
    			{pendingRequests && pendingRequests.map((request, i) => {
    				return(
    					<TableRow key={i} >
    						<Box component="td" border={1} borderRadius={10} className={classes.box}
    							onMouseEnter={() => handleHover(request)}
    							onMouseLeave={() => dispatch(highlightRooms([]))}
    							onClick={() => {handleClick(request)}}>
    							<Typography className={classes.text}><b>{request.type}: </b>{request.access_name}</Typography>
    							<Typography className={classes.text}><b>User: </b>{request.reader.name}{" "}{request.reader.surname}</Typography>
    							<Typography className={classes.text}><b>Date: </b>{request.requested_datetime}</Typography>
                  {request.approver.name &&
                    <Typography className={classes.text}><b>Approver: </b>{request.approver.name}{" "}{request.approver.surname}</Typography>
                  }
    						</Box>
    					</TableRow>
    				);
    			})}
    		</TableBody>
    	</Table>
    </TableContainer>
  )
}
