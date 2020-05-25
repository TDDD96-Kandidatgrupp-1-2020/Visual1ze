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
import { changeAGSelected, selectShape, highlightRooms, selectRoom } from '../../actions/roomActions';
import axios from 'axios'

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
		gridArea: 'container-form',
		margin: 'auto',
		backgroundColor: colorTheme.palette.primary.white,
		paddingTop: '16px',
		paddingBottom: '8px',
		borderRadius: '10px',
		borderColor: colorTheme.palette.primary.main,
		borderStyle: 'solid'
	},
	Checkbox : {
		color: colorTheme.palette.primary.main,
	},
	pr: {
		color: colorTheme.palette.primary.main,
	},
  formHelperText: {
    color: "red",
    fontSize: 15
  }
}));

/**
 * This component is the one that the user uses in order to fill in its room or AG order.
 * It contains the component's front-end logic (in return) and server communication (in
 * handleSubmit).
 */
function RequestForm(props) {
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
	// State holding the user's justification to order.
	const [justification, setJustification] = useState("");
	// Fetch JSON object containing user information that is stored in the browser's sessionStorage.
	const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));
	// Get selected room or AG
	const selectedRoom = useSelector(state => state.rooms.roomId);
	const accessGroup = useSelector(state => state.rooms.accessGroup);
	// Fetch from sessionStorage if we're applying for an AG or not. Set in AGSearch.js.
	const isAG = useSelector(state => state.rooms.isAGSelected);

	const dispatch = useDispatch();

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
		if(!isAG) {
			if (termsAccepted) {
				axios.post("/reader/room", {
					"room_text_id": selectedRoom,
					"justification": justification,
				}, userInformation.header)
				.then(function (response) {
					// Restore value of the checkbox to false before leaving RequestForm page.
					setTermsAccepted(false);
					// Restore value of errorDisplayed if user hadn't pressed the "Terms and conditions"-checkbox.
					setErrorDisplayed(false);
					setServerErrorDisplayed(false);
					setServerError("");
					dispatch(changeAGSelected(false)); // Reset isAGSelected.
					dispatch(highlightRooms([]));
					dispatch(selectRoom());
					// Route to start page.
					props.history.push("/" + userInformation.role + "/start");
				})
				.catch(function (error) {
					console.log("Error in RequestForm");
					console.log(error.response);
					setServerErrorDisplayed(true);
					setServerError(String(error.response.data.error));
				});
			}
			else {
				setErrorDisplayed(true);
			}
		} else {
			if (termsAccepted) {
				axios.post("/reader/ag", {
					"ag_id": accessGroup.id,
					"justification": justification
				}, userInformation.header)
				.then(function (response) {
					// Restore value of the checkbox to false before leaving RequestForm page.
					setTermsAccepted(false);
					// Restore value of errorDisplayed if user hadn't pressed the "Terms and conditions"-checkbox.
					setErrorDisplayed(false);
					setServerErrorDisplayed(false);
					setServerError("");
					dispatch(highlightRooms([]));
					dispatch(selectRoom());
					// Route to start page.
					props.history.push("/" + userInformation.role + "/start");
				  })
				.catch(function (error) {
					console.log("Error in RequestForm");
					console.log(error.response);
					setServerErrorDisplayed(true);
					setServerError(String(error.response.data.error));
				});
			}
			else {
				setErrorDisplayed(true);
			}
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
						Create request
					</Typography>
					<form className={classes.form} noValidate>
  					<TextField
  						disabled
  						fullWidth
  						margin="normal"
  						label="Name"
  						defaultValue={userInformation.name + " " + userInformation.surname}
  						variant="outlined"
  					/>
  					<TextField
  						disabled
  						fullWidth
  						margin="normal"
  						label={isAG ? "AG name" : "Room name"}
  						defaultValue={isAG ? accessGroup.name : selectedRoom}
  						variant="outlined"
  					/>
  					<TextField
  						onChange={(text) => setJustification(text.target.value)}
  						required
  						multiline
  						autoFocus
  						fullWidth
  						margin="normal"
  						label="Required"
  						defaultValue="Your motivation here."
  						rows="5"
  						variant="outlined"
  						/>
  					<FormControl required error={errorDisplayed} >
  						<FormControlLabel
  							control={<Checkbox required onChange={handleChange} color="primary" checked={termsAccepted}	/>}
  							label="I agree with the terms and conditions."
  						/>
  					</FormControl>
  					{errorDisplayed && <FormHelperText className={classes.formHelperText}>You need to accept the terms and conditions.</FormHelperText>}
  					{serverErrorDisplayed && <FormHelperText className={classes.formHelperText}>{serverError}</FormHelperText>}
  					<Button onClick={handleSubmit} fullWidth variant="contained" color="primary" className={classes.submit}>
  						Send request
  					</Button>
					</form>
				</div>
			</Container>
		</GridLayout>
	);
} export default withRouter(RequestForm)
// Exporting the component wrapped around "withRouter" gives the component access to props.history which means that the component can route the users to other pages.
