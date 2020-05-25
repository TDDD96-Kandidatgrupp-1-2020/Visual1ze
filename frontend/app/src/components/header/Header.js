/**
 * Header component. Will always render at the top of page (except log-in page).
 */

import React from 'react';
import { Grid, AppBar, Toolbar } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import Logo from './Logo';
import StartButton from './StartButton';
import RequestsButton from './RequestsButton';
import UsernameButton from './UsernameButton';
import ManageAGsButton from './ManageAGsButton';
import ManageAccountsButton from './ManageAccountsButton';
import { colorTheme } from '../../App';

// Variable containing styling of components in the render function below.
const useStyles = makeStyles((theme) => ({
  appbar: {
    maxHeight: '70px',
    backgroundColor: colorTheme.palette.primary.main
  },
  gridContainer: {
    marginLeft: theme.spacing(0),
    flexDirection: 'row',
    justifyContent: 'flex-start',
    alignItems: 'center',
  },
}));

/**
 * Function wrapper containing the following components:
 * Start, Requests, UsernameDropdown and Logo.
 */
export default function Header(props) {
  // Fetch styles-variable
  const classes = useStyles();
  // Fetch user information stored in sessionStorage
  const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));
  // userRole is a string that can be: reader, approver, admin
  const userRole= userInformation.role;

  return (
    <AppBar className={classes.appbar}>
      <Toolbar>
        <Grid container className={classes.gridContainer} spacing={3}>
          <Grid item xs>
            <Logo />
          </Grid>
          <Grid item>
            <StartButton />
          </Grid>
          {(userRole === "reader" || userRole === "approver") &&
          <Grid item>
            <RequestsButton />
          </Grid>}
          {userRole === "admin" &&
          <Grid item>
            <ManageAGsButton />
          </Grid>}
          {userRole === "admin" &&
          <Grid item>
            <ManageAccountsButton />
          </Grid>}
          <Grid item>
            <UsernameButton />
          </Grid>
        </Grid>
      </Toolbar>
    </AppBar>
  );
}
