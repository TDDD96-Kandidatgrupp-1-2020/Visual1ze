/**
 * Component representing the component to which the user comes when a room is
 * requested. It contains a text field where the user writes its motivation etc.
 * Parent is ApproverPage.
 */

import React, { useState } from 'react';
import { FormControl, FormControlLabel, FormHelperText } from '@material-ui/core';
import { Button, Checkbox, Container, CssBaseline, TextField, Typography } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import { withRouter } from 'react-router-dom';
import styled from 'styled-components';
import { colorTheme } from '../../App';

import { useSelector, useDispatch } from 'react-redux';
import { revokeAccess } from '../../actions/roomActions';

const GridLayout = styled.div`
  height: 100vh;
  padding: 0em 1em;
  gap: 1em 1em;
  display: grid;
  box-sizing: border-box;
  grid-template-areas:
    "header"
    "container-form";
  grid-template-rows: 70px 1fr;
`;

// Variable containing styling of components in the render function below.
const useStyles = makeStyles(theme => ({
	paper: {
		display: 'flex',
		flexDirection: 'column',
		alignItems: 'center'
	},
	form: {
		width: '100%',
    	marginTop: theme.spacing(1),
	},
	submit: {
		margin: theme.spacing(3, 0, 2),
	},
	container : {
		gridArea: "container-form",
		margin: "auto",
		backgroundColor: colorTheme.palette.primary.white,
		paddingTop: "16px",
		paddingBottom: "8px",
		borderRadius: "10px",
		borderColor: colorTheme.palette.primary.main,
		borderStyle: "solid"
	},
	Checkbox : {
		color: colorTheme.palette.primary.main,
	},
	pr: {
		color: colorTheme.palette.primary.main,
	}
}));

/**
 * This component is the one that the user uses in order to fill in its room or AG order.
 * It contains the component's front-end logic (in return) and server communication (in
 * handleSubmit).
 */
function RequestForm(props) {
  const dispatch = useDispatch();
  // Fetch styles-variable
	const classes = useStyles();
	// Boolean storing whether user accepts terms.
	const [termsAccepted, setTermsAccepted] = useState(false);
	// Boolean storing whether the error message shall be displayed.
	const [errorDisplayed, setErrorDisplayed] = useState(false);
	// Boolean storing whether server message shall be displayed.
	const [serverErrorDisplayed, setServerErrorDisplayed] = useState(false);
	// State storing error message
	const [serverError, setServerError] = useState("");
	// Fetch JSON object containing user information that is stored in the browser's sessionStorage.
	const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));

  // All meta-data about all rooms.
  const roomsData = useSelector(state => state.rooms.roomData);
  // ID of the currently selected room.
	const selectedRoom = useSelector(state => state.rooms.roomId);
  // ID of the currently selected user. Used for approver functionality.
  const selectedUser = useSelector(state => state.otherUsers.selectedUser);

	/**
	 * Handles changing of the checkbox value (boolean) stored in termsAccepted.
	 */
	const handleChange = (event) => {
		setTermsAccepted(event.target.checked);
	}

	/**
	 * Sends the request to the server. The request contains the room or AG applied to,
	 * username and user-justification.
	 */
	const handleSubmit = async() => {
    if (termsAccepted) {
      // Remove access to specified room.
      if (roomsData && roomsData[selectedRoom] && roomsData[selectedRoom].ag_id) {
				// If Access Group.
      	dispatch(revokeAccess(true, roomsData[selectedRoom].ag_id, selectedUser));
      } else if (roomsData && roomsData[selectedRoom]) {
				// If room.
        dispatch(revokeAccess(false, selectedRoom, selectedUser));
      }

      // Restore value of the checkbox to false before leaving RequestForm page.
      setTermsAccepted(false);
      // Restore value of errorDisplayed if user hadn't pressed the "Terms and conditions"-checkbox.
      setErrorDisplayed(false);
      setServerErrorDisplayed(false);
      setServerError("");
      // Route to start page.
      props.history.push("/" + userInformation.role + "/start");
    }
    else {
      setErrorDisplayed(true);
      setServerErrorDisplayed(true);
    }
	}

	/**
	 * Creates front-end components that together build the form.
	 */
	return (
		<GridLayout>
			<Container maxWidth="xs" className={classes.container}>
				<CssBaseline />
				<div className={classes.paper}>
					<Typography component="h1" variant="h4" align="center">
						Revoke access
					</Typography>
					<form className={classes.form} noValidate>
            <TextField
              disabled
              fullWidth
              margin="normal"
              label="User"
              defaultValue={selectedUser}
              variant="outlined"
            />
            <TextField
              disabled
              fullWidth
              margin="normal"
              label={(roomsData[selectedRoom] && roomsData[selectedRoom].ag_id) ? "Access group ID" : "Room name"}
              defaultValue={(roomsData[selectedRoom] && roomsData[selectedRoom].ag_id) ? roomsData[selectedRoom].ag_id: selectedRoom}
              variant="outlined"
            />
						<FormControl required error={errorDisplayed} >
							<FormControlLabel
								control={<Checkbox required onChange={handleChange} color="primary" checked={termsAccepted}	/>}
								label="I agree with the terms and conditions."
							/>
						</FormControl>

						{errorDisplayed && <FormHelperText>You need to accept the terms and conditions.*</FormHelperText>}
						{serverErrorDisplayed && <FormHelperText>ERROR! {serverError}</FormHelperText>}

						<Button onClick={handleSubmit} fullWidth variant="contained" color="primary" className={classes.submit}>
							Revoke access
						</Button>
					</form>
				</div>
			</Container>
		</GridLayout>
	);
} export default withRouter(RequestForm)
// Exporting the component wrapped around "withRouter" gives the component access to props.history which means that the component can route the users to other pages.
