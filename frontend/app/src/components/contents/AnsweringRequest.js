/**
 * This component represents the component to which the approver comes when he's
 * chosen one of the cards in PendingRequest. It has functionality for the approver
 * to accept or deny the request.
 */

import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@material-ui/core';
import { Box, Button, Container, Paper, Typography } from '@material-ui/core';
import { colorTheme } from '../../App';
import { highlightRooms } from '../../actions/roomActions';
import { useDispatch, useSelector } from 'react-redux';
import styled from 'styled-components';
import axios from 'axios'

// Variable containing styling of components in the render function below.
const useStyles = makeStyles((theme) => ({
  tableContainer: {
    backgroundColor: colorTheme.palette.primary.light,
    gridArea: "pending",
  },
  table: {
    backgroundColor: colorTheme.palette.primary.light,
	},
	tableTitle: {
		backgroundColor: colorTheme.palette.primary.dark,
		color: colorTheme.palette.primary.contrastText,
		fontSize: 16,
		fontWeight: 'bold',
		textAlign: 'center',
	},
	box: {
    marginTop: theme.spacing(0.5),
    backgroundColor: colorTheme.palette.primary.main,
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
  acceptButton: {
    marginTop: theme.spacing(2),
    marginRight: theme.spacing(2),
    marginLeft: theme.spacing(2),
    color: colorTheme.palette.primary.contrastText,
    backgroundColor: "#4b8b3b", // accept-green
    '&:hover': {
	       backgroundColor: "#55a342",
    }
  },
  rejectButton: {
    marginTop: theme.spacing(2),
    marginRight: theme.spacing(2),
    marginLeft: theme.spacing(2),
    color: colorTheme.palette.primary.contrastText,
    backgroundColor: "#981815", // reject-red
    '&:hover': {
       backgroundColor: "#d5140f",
    }
  },
  backButton: {
    marginTop: theme.spacing(8),
    marginLeft: theme.spacing(10),
    marginRight: theme.spacing(10),
    color: colorTheme.palette.primary.contrastText,
    backgroundColor: colorTheme.palette.primary.main,
    '&:hover': {
       backgroundColor: colorTheme.palette.primary.dark,
     }
  }
}));

/**
 * This component contains functionality to see over a request. It contains
 * functionality to approver or deny request.
 */
export default function AnsweringRequest(props) {
  // Fetch styles-variable
  const classes = useStyles();
  // React-redux syntax
  const dispatch = useDispatch();
  // Fetch from sessionStorage information on which request was clicked
  const request = useSelector(state => state.otherUsers.selectedRequest);
  // Fetch user information stored in sessionStorage
	const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));

  /**
   * Handles what happens when approver presses "accept" or "deny". The parameter
   * isAccessGranted contains which one of the buttons was pressed. Send decision
   * to server, communicate with map and with parent component.
   */
  const handleDecision = async(isAccessGranted) => {
      axios.post("/approver/access",  {
          "request_id": request.request_id,
          "type": request.type,
          "is_access_granted": isAccessGranted,
      }, userInformation.header)
      .then(function (response) {
          // Go back to PendingRequest
          props.setShowPendingRequest(true);
      }).catch(function (error) {
          console.log("ERROR in AnsweringRequest");
          console.log(error.response);
          // Go back to PendingRequest
          props.setShowPendingRequest(true);
      });
      // Stop highlighting the selected room
      dispatch(highlightRooms([]));
  }

  /**
   * Handles what happens when approver presses the "back" button.
   */
  const handleBack = () => {
      // Stop highlighting the selected room.
      dispatch(highlightRooms([]));
      // Go back to PendingRequest
      props.setShowPendingRequest(true);
  }

  return (
    <TableContainer component={Paper} className={classes.tableContainer}>
      <Table stickyHeader className={classes.table}>
        <TableHead>
          <TableRow>
              <TableCell className={classes.tableTitle}>Request</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          <TableRow>
            <Box component="td" border={1} borderRadius={10} className={classes.box} >
              <Typography className={classes.text}><b>{request.type}:</b>{" "}{request.access_name}</Typography>
              <Typography className={classes.text}><b>User:</b>{" "}{request.reader.name}{" "}{request.reader.surname}</Typography>
              <Typography className={classes.text}><b>Date:</b>{" "}{request.requested_datetime}</Typography>
              {request.approver.name &&
                <Typography className={classes.text}><b>Approver: </b>{request.approver.name}{" "}{request.approver.surname}</Typography>
              }
            </Box>
          </TableRow>
          <TableRow>
            <Box component="td" border={1} borderRadius={10} className={classes.box}>
              <Typography className={classes.text}><b>Justification:</b></Typography>
              <Typography className={classes.text}></Typography>
              <Typography className={classes.text}>{request.justification}</Typography>
              <Button className={classes.acceptButton} onClick={() => handleDecision(true)} variant="outlined">Approve</Button>
              <Button className={classes.rejectButton} onClick={() => handleDecision(false)} variant="outlined">Deny</Button>
            </Box>
          </TableRow>
          <TableRow>
            <Box component="td">
              <Button className={classes.backButton} onClick={handleBack} variant="outlined">Back</Button>
            </Box>
          </TableRow>
          <TableRow/>
        </TableBody>
      </Table>
    </TableContainer>
  )
}
