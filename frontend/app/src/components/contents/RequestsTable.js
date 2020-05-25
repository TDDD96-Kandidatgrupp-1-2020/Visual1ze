/**
 * Component containing the request to which the user comes to when pressing Requests.
 * Parent component is ApproverPage.
 *
 * OBS: will be refactored so that it looks better than it does now.
 */

import React, { useEffect, useState } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@material-ui/core';
import { Container, Paper, Typography } from '@material-ui/core';
import { makeStyles, withStyles } from '@material-ui/core/styles';
import styled from 'styled-components';
import { colorTheme } from  '../../App';
import axios from 'axios';

const GridLayout = styled.div`
  height: 100vh;
  padding: 0em 1em;
  gap: 1em 1em;
  display: grid;
  box-sizing: border-box;
  grid-template-areas:
    "header header header"
    ". table .";
  grid-template-rows: 70px 1fr;
  grid-template-columns: 1fr 7fr 1fr
`;

const StyledTableCell = withStyles((theme) => ({
	head: {
		backgroundColor: colorTheme.palette.primary.main,
		color: colorTheme.palette.primary.contrastText,
		fontSize: 18,
		fontWeight: 'bold',
	},
	body: {
		backgroundColor: colorTheme.palette.primary.light,
		color: colorTheme.palette.primary.contrastText,
		fontSize: 16,
	}
}))(TableCell);

// Variable containing styling of components in the render function below.
const useStyles = makeStyles(() => ({
	table: {
		minWidth: 300,
	},
	container: {
		gridArea: 'table',
		marginTop: '25px',

	},
	paperRounded:{
		borderRadius: "0px 0px 5px 5px",
	},
	title: {
		padding: '20px 20px 20px 20px',
		backgroundColor: colorTheme.palette.primary.white,
		borderRadius: '5px 5px 0px 0px',
		borderStyle: 'solid',
		borderColor: colorTheme.palette.primary.main,
	}
}));

/**
 * This component displays the historic of all requests made by the user. It contains
 * the component's logic, communication with server and styling.
 */
export default function RequestsTable() {
  	// Fetch styles-variable
	const classes = useStyles();

	//var userRequests = JSON.parse(sessionStorage.getItem("userRequests"));
	const [userRequests, setUserRequests] = useState();


	/**
	 * This hook is called automatically when the component is rendered. It fetches each of the requests
	 * that the user has made.
	 */
	useEffect(() => {
		const fetchData = async () => {
			// Fetch JSON object containing user information that is stored in the browser's sessionStorage.
			const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));

			axios.get("/reader/orders", userInformation.header)
			.then(function (response) {
				setUserRequests(response.data.orders);
			})
			.catch(function (error) {
				console.log("ERROR");
				console.log(error);
				console.log(error.response);
			});
		};
		fetchData();
	}, [setUserRequests]);

	return (
		<GridLayout>
			<Container maxWidth="xl" className={classes.container}>
				<Typography variant="h5" align="center" className={classes.title}>
					List of requests
				</Typography>
				<TableContainer component={Paper} classes={{root: classes.paperRounded}}>


				<Table stickyHeader className={classes.table}>
					<TableHead>
						<TableRow>
							<StyledTableCell>Access name</StyledTableCell>
							<StyledTableCell>Type</StyledTableCell>
							<StyledTableCell>Date</StyledTableCell>
							<StyledTableCell>Approver</StyledTableCell>
						</TableRow>
					</TableHead>
					<TableBody>
						{userRequests && userRequests.map((request, i) => (
							<TableRow key={i}>
								<StyledTableCell>{request.name}</StyledTableCell>
								<StyledTableCell>{request.type}</StyledTableCell>
								<StyledTableCell>{request.date}</StyledTableCell>
								<StyledTableCell>{request.approver}</StyledTableCell>
							</TableRow>
						))}
					</TableBody>
				</Table>
			</TableContainer>
		</Container>
	</GridLayout>
	);
}
