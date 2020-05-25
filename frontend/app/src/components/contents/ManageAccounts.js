
/**
 * Component to which an admin comes to upon pressing button "Manage Accounts" in header.
 */

import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import { Container, Divider, TextField, Typography, Button, Paper } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import { colorTheme } from '../../App';
import { Autocomplete } from '@material-ui/lab';
import { useDispatch, useSelector } from 'react-redux';
import { fetchUsers, upgradeToApprover, upgradeToAdmin } from '../../actions/otherUserActions';
import { removeCard, deleteUser } from '../../actions/otherUserActions';

const role = ["Reader", "Approver", "Admin"];

const useStyles = makeStyles((theme) => ({
  container : {
		gridArea: 'userInfo',
		margin: 'auto',
		backgroundColor: colorTheme.palette.primary.white,
		borderColor: colorTheme.palette.primary.main,
    borderStyle: 'solid',
    borderRadius: '10px',
    paddingTop: theme.spacing(2),
    paddingBottom: theme.spacing(2),
    paddingLeft: theme.spacing(2),
    paddingRight: theme.spacing(2),
	},
  search: {
    gridArea: 'search',
    backgroundColor: colorTheme.palette.primary.white,
  },
  email : {
    fontSize: 13,
    color: colorTheme.palette.secondary.contrastText,
  },
  names : {
    flexGrow: 1,
    color: colorTheme.palette.primary.main,
  },
  paper: {
    height: "100%",
    padding: theme.spacing(2),
    marginTop: theme.spacing(2)
  },
  button: {
    padding: theme.spacing(1),
    marginTop: theme.spacing(2),
  },
  buttonRemove: {
    padding: theme.spacing(1),
    marginTop: theme.spacing(2),
    marginBottom: theme.spacing(2),
  },
}));

const GridLayout = styled.div`
  height: 100vh;
  padding: 0em 1em;
  gap: 1em 1em;
  display: grid;
  box-sizing: border-box;
  grid-template-areas:
  "header header header"
  ". search ."
  ". userInfo .";
  grid-template-rows: 70px auto 1fr;
  grid-template-columns: 5fr 6fr 5fr;
`;

/**
 * Contains functionality to update some information of a selected user.
 */
export default function ManageAccounts() {
    // Fetch styles-variable
    const classes = useStyles();
    // Create a link to dispatch. The hook useDespatch returns a function.
    const dispatch = useDispatch();
    // State containing list with all users.
    const allUsers = useSelector(state => state.otherUsers.users);
    // The email of the selected user
    const [selectedEmail, setSelectedEmail] = useState("");
    // The selected user, data suplied by using selectedEmail.
    const selectedUser = useSelector(state => {
      const all = state.otherUsers.users
      const user = all.find(user => user.email === selectedEmail)
      if (user) {
        return user
      } else {
        return {}
      }
    }, [selectedEmail])

    const [inputValue, setInputValue] = useState("");


    /**
     * When the component is rendered it fetches all users as a list of JSON objects.
     */
    useEffect(() => {
      dispatch(fetchUsers());
    }, [dispatch])

    /**
     *  Selects the user clicked in the search bar.
     */
    const handleChange = (event, values) => {
        event.preventDefault();
        console.log(values)
        if (values) {
          setInputValue(values);
          setSelectedEmail(values.email);
        }
        else {
          setSelectedEmail("")
        }
    }

    /**
     * Upgrades the selected user to approver or admin, if it is a reader.
     */
    const handleUpgradeRole = (event, values) => {
      event.preventDefault();
      if (selectedUser.email) {
        console.log(selectedUser.email);
        if (values === "Approver") {
          dispatch(upgradeToApprover(selectedUser.email));
        } else if (values === "Admin") {
          dispatch(upgradeToAdmin(selectedUser.email));
        }
      }
    }

    /**
     * Removes the selectedUser from the system.
     */
    const handleRemoveUser = () => {
      if (selectedUser && selectedUser.email) {
        dispatch(deleteUser(selectedUser.email));
        setSelectedEmail("")
      }
    }

    /**
     * Dispatch an action that communicates with server and blocks card.
     */
    const handleBlockCard = () => {
      if (selectedUser) {
        dispatch(removeCard(selectedUser.email));
      }
    }

    return(
      <GridLayout>
        <Autocomplete
            key={inputValue}
            onChange={handleChange}
            className={classes.search}
            id="searchUser"
            options={allUsers ? allUsers : []}
            getOptionLabel={(option) => option.email}
            renderOption={(option) => (
                <div>
                  <Typography className={classes.names}>
                      <b>{option.name} {option.surname} </b>
                  </Typography>
                  <Typography className= {classes.email}>
                      {option.email}
                  </Typography>
                </div>
                )}
            renderInput={(params) => <TextField  {...params} label="Search user" variant="outlined"  />}
          />
        <Container width={'100%'} className={classes.container}>
          <Typography component="h1" variant="h4" align="center">
            Manage account
          </Typography>
          <Paper className={classes.paper} width={'100%'}>
              <Typography variant="h6">User information</Typography>
              <Divider/>
              <Typography><b>Email  </b>{selectedUser.email}</Typography>
              <Typography><b>Name   </b>{selectedUser.name} {selectedUser.surname}</Typography>
              <Typography><b>Role   </b>{selectedUser.role}</Typography>
          </Paper>
          {selectedUser.email &&
          <Paper className={classes.paper} width={'100%'}>
              <Typography variant="h6">Actions</Typography>
              <Divider/>
              <Button fullWidth className={classes.button} variant="contained" color="primary" onClick={handleBlockCard}>
                Block card
              </Button>
              <Button fullWidth className={classes.buttonRemove} variant="contained" color="secondary" onClick={handleRemoveUser}>
                Remove user
              </Button>
              <Autocomplete
                fullWidth
                id="role"
                required
                onChange={handleUpgradeRole}
                options={role}
                getOptionLabel={(option) => option}
                renderInput={(params) => <TextField {...params} label="Edit user role" variant="outlined" />}
              />
          </Paper>}
        </Container>
      </GridLayout>
    )
}
