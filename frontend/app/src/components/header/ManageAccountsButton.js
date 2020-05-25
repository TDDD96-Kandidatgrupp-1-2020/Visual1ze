/**
 * ManageAccounts takes care of the dropdown menu for the system account functionality.
 */

import React, { useState } from 'react';
import { Button, Menu, MenuItem } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import { BrowserRouter as Router, Redirect } from 'react-router-dom';
import { withRouter } from 'react-router-dom';
import auth from '../../auth';
import { colorTheme } from '../../App';


// Variable containing styling of components in the render function below.
const useStyles = makeStyles(() => ({
  menuButton: {
    borderRadius: 5,
    color: 'white',
    height: 40,
    fontSize: colorTheme.font.size,
    "&:hover": {
      backgroundColor: colorTheme.palette.primary.dark,
    }
  },
  menuItem: { 
    color: 'white',
    height: 40,
    fontSize: colorTheme.font.size,
    backgroundColor: colorTheme.palette.primary.main,
    '&:hover': {
      backgroundColor: colorTheme.palette.primary.dark,
    }
  }
}));

/**
 * This component is the the dropdown menu for ManageAccounts. It contains a few different things,
 * like create account and search account. 
 * props parameter is passed down from withRouter in order to access browser history.
 */
function ManageAccounts(props) {
  // Fetch styles-variable
  const classes = useStyles(); 
  // Contains whether the dropdown menu is open.
  const [anchorEl, setAnchorEl] = useState(null);
  
  /**
   * Handles click outside menu.
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

  const handleCreateAccount = () => {
    props.history.push("/admin/create_account");
  }

  const handleManageAccounts = () => {
    props.history.push("/admin/manage_accounts")
  }


  // If not logged in take the user back to loginpage!
  if (!auth.isAuthenticated()) {
    return <Redirect to="/"/>
  }
  
  return (
      <Router>
        <div>
          <Button 
            className={classes.menuButton} variant='text' color='primary' onClick={handleClick} >
            <b>Manage Accounts</b>
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
            <MenuItem className={classes.menuItem} onClick={handleCreateAccount} >Create account</MenuItem>
            <MenuItem className={classes.menuItem} onClick={handleManageAccounts} >Manage accounts</MenuItem>
          </Menu>
        </div>
      </Router>
  );
} export default withRouter(ManageAccounts)
// Exporting the component wrapped around "withRouter" gives the component access to props.history, 
// which means that the component can route the users to other pages.