/**
 * UsernameButton takes care of the dropdown menu for the user.
 * Based on the role different things will appear.
 */

import React, { useState } from 'react';
import { Button, Menu, MenuItem } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import { BrowserRouter as Router, Redirect } from 'react-router-dom';
import { withRouter } from 'react-router-dom';
import auth from '../../auth';
import { colorTheme } from '../../App';
import MenuIcon from '@material-ui/icons/Menu';

import { useDispatch } from 'react-redux';
import { resetState } from '../../actions/roomActions';
import { logout } from '../../actions/userActions';

// Variable containing styling of components in the render function below.
const useStyles = makeStyles(() => ({
  menuButton: {
    alignItems: 'center',
    borderRadius: 5,
    color: colorTheme.palette.primary.contrastText,
    height: 40,
    fontSize: colorTheme.font.size,
    '&:hover': {
      backgroundColor: colorTheme.palette.primary.dark,
    }
  },
  menuItem: {
    color: colorTheme.palette.primary.contrastText,
    height: 40,
    fontSize: colorTheme.font.size,
    backgroundColor: colorTheme.palette.primary.main,
    "&:hover": {
      backgroundColor: colorTheme.palette.primary.dark,
    }
  },
}));

/**
 * This component is the the dropdown menu. It contains different things depending
 * on the user's role. All roles have sign out button.
 * props parameter is passed down from withRouter in order to access browser history.
 */
function UsernameButton(props) {
  // Fetch styles-variable
  const classes = useStyles();
  // Contains whether the dropdown menu is open.
  const [anchorEl, setAnchorEl] = useState(null);
  // Fetch user information stored in sessionStorage
  const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));

  const dispatch = useDispatch();

  /**
   * Handles the access event. If user is approver and presses
   * manage own access the user will be redirected to a reader start page.
   */
  const handlePersonalAccess = () => {
    props.history.push("/" +  userInformation.role + "/personal_access");
  }

  /**
   * Handles the request event. If user is approver and presses
   * see pending request the user will be redirected to requestTable.
   */
  const handleRequest = () => {
    props.history.push("/" + userInformation.role + "/requests");
  }

  /**
   * Handles the click event. If user clicks then
   * dropdown menu will appears.
   */
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  /**
   * Closes the dropdown menu.
   */
  const handleClose = () => {
    setAnchorEl(null);
  }

  /**
   * Call on auth.logout and send user back to log-in page.
   */
  const handleSignOut = () => {
    // Reset Redux-state
    dispatch(resetState());
    dispatch(logout());
    auth.logout(()=> {
      props.history.push("/");
    })
  }

  /**
   * Push the user to admin/edit_map. This can only be done if user is an admin!
   */
  const handleEditMap = () => {
    props.history.push("/admin/edit_map");
  }

  const handleLockdown = () => {
    props.history.push("/admin/lockdown")
  }

  // If not logged in take the user back to loginpage!
  if (!auth.isAuthenticated()) {
    return <Redirect to="/"/>
  }

  return (
      <Router>
        <div>
          <Button className={classes.menuButton} variant='text'
            color='primary' onClick={handleClick}
          >
            <b>{JSON.parse(sessionStorage.getItem("userInformation")).name}</b>
            <div style={{width: '0.5em'}}></div>
            <MenuIcon/>
          </Button>
          <Menu
            MenuListProps={{ disablePadding: true }}
            getContentAnchorEl={null}
            anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
            transformOrigin={{ vertical: "top", horizontal: "center" }}
            anchorEl={anchorEl}
            keepMounted
            open={Boolean(anchorEl)}
            onClose={handleClose}
          >
            <Router>
              {userInformation.role === "admin" &&
              <MenuItem className={classes.menuItem} onClick={handleEditMap}>Edit map</MenuItem>}
              {((userInformation.role === "approver") || (userInformation.role === "admin") ) &&
              <MenuItem className={classes.menuItem} onClick={handlePersonalAccess}>Manage personal access</MenuItem>}
              {((userInformation.role === "approver") || (userInformation.role === "admin") ) &&
              <MenuItem className={classes.menuItem} onClick={handleRequest}>See pending requests</MenuItem>}
            </Router>
            <MenuItem className={classes.menuItem} onClick={handleSignOut}>Sign out</MenuItem>
          </Menu>
        </div>
      </Router>
  );
} export default withRouter(UsernameButton)
// Exporting the component wrapped around "withRouter" gives the component access to props.history,
// which means that the component can route the users to other pages.
