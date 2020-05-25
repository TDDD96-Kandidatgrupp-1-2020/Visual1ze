/**
 * This component handles the creation of a new Reader, Approver or Admin.
 */

import React, { useState } from 'react';
import { Button, Container, CssBaseline, TextField, Typography } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import styled from 'styled-components';
import { colorTheme } from '../../App';
import { Autocomplete } from '@material-ui/lab';
import { withRouter } from 'react-router-dom';

const axios = require('axios');

// The three different roles in the system
const role = ["Reader", "Approver", "Admin"];

const GridLayout = styled.div`
  height: 100vh;
  padding: 0em 1em;
  gap: 1em 1em;
  display: grid;
  box-sizing: border-box;
  grid-template-areas:
    "header"
    "form";
  grid-template-rows: 70px 1fr;
`;

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
		gridArea: 'form',
		margin: 'auto',
		backgroundColor: colorTheme.palette.primary.white,
		paddingTop: '16px',
		paddingBottom: '8px',
		borderRadius: '10px',
		borderColor: colorTheme.palette.primary.main,
		borderStyle: 'solid'
	},
}));

/**
 * CreateAccount contains the submit form for create a new user.
 */
 function CreateAccount(props) {
    const classes = useStyles();
    const [name, setName] = useState("");
    const [password, setPassword] = useState("");
    const [surname, setSurname] = useState("");
    const [email, setEmail] = useState("");
    const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));
    const [isError, setIsError] = useState(false);
    const [serverError, setServerError] = useState("");

    // Post information to server.
    const handleSubmit = async() => {
        if (String(document.getElementById("role").value) !== "") {
            axios.post("/admin/"+ document.getElementById("role").value.toLowerCase(), {
                "name": name,
                "surname": surname,
                "email": email,
                "password": password
            }, userInformation.header)
            .then(function (response) {
                console.log(response.data);
                setIsError(false);
                setServerError("");
                props.history.push("/" + userInformation.role + "/start");
            })
            .catch(function (error) {
                console.log("Error in CreateAccount");
                console.log(error.response);
                constructErrorMessage(error.response);
                setIsError(true);
            });
        } else {
            setIsError(true);
            setServerError("Role error: choose role!")
        }
    }

    const constructErrorMessage = (error) => {
        var errorStr;
        if (error.data.error.email) {
            setServerError("Email error: email must have format: A@B.C");
        } else if (error.data.error === "This email is already in use!") {
            setServerError(error.data.error)
        } else if (error.data.error.password) {
            errorStr = "Password error: ";
            for (const e of error.data.error.password) {
                errorStr += e;
            }
            setServerError(errorStr);
        } else if (error.data.error.name) {
            errorStr = "Name error: ";
            for (const e of error.data.error.name) {
                errorStr += e;
            }
            setServerError(errorStr);
        } else if (error.data.error.surname) {
            errorStr = "Surname error: ";
            for (const e of error.data.error.surname) {
                errorStr += e;
            }
            setServerError(errorStr);
        }
    }

    return(
        <GridLayout>
            <Container maxWidth="xs" className={classes.container}>
				<CssBaseline />
				<div className={classes.paper}>
					<Typography component="h1" variant="h4" align="center">
						Create user
					</Typography>
					<form className={classes.form} noValidate>
					<TextField
                        fullWidth
                        required
						margin="normal"
						label="Name"
                        variant="outlined"
                        onChange={(text) => setName(text.target.value)}
					/>
                    <TextField
                        fullWidth
                        required
						margin="normal"
						label="Surname"
                        variant="outlined"
                        onChange={(text) => setSurname(text.target.value)}
					/>
                    <TextField
                        fullWidth
                        required
						margin="normal"
						label="Email"
                        variant="outlined"
                        onChange={(text) => setEmail(text.target.value)}
					/>
                    <TextField
                        fullWidth
                        required
						margin="normal"
						label="Password"
                        variant="outlined"
                        onChange={(text) => setPassword(text.target.value)}
					/>
                     <Autocomplete
                        id="role"
                        required
                        options={role}
                        getOptionLabel={(option) => option}
                        style={{ width: "300", marginTop: "16px" }}
                        renderInput={(params) => <TextField {...params} label="Role" variant="outlined" />}
                    />
                    <Button onClick={handleSubmit} fullWidth variant="contained" color="primary" className={classes.submit}>
                        Add user
                    </Button>
					</form>
                    <Typography>{isError && String(serverError)}</Typography>
				</div>
			</Container>
        </GridLayout>
    )
} export default withRouter(CreateAccount)
