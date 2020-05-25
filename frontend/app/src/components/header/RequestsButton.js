/**
 * Component that renders the Requests button shown inside of the header. 
 */

import React from 'react';
import { Button } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import { withRouter } from 'react-router-dom';
import { colorTheme } from '../../App';

// Variable containing styling of components in the render function below.
const useStyles = makeStyles(() => ({
  requestsButton: {
    borderRadius: 5,
    color: 'white',
    height: 40,
    fontSize: colorTheme.font.size,
    '&:hover': {
      backgroundColor: colorTheme.palette.primary.dark,
    }
  },
}));

/**
 * This component is the button "Request".  Its parent is Header.js. 
 */
function RequestsButton(props) {
  // Fetch styles-variable
  const classes = useStyles(); 
  // Fetch user information stored in sessionStorage
  const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));

  /**
   * Redirect user to the Request content page when "Requests"-button clicked.
   */
  const handleClick = () => {
    props.history.push("/" + userInformation.role + "/requests")
  }

  return (
      <Button 
        className={classes.requestsButton} 
        variant='text' 
        color='primary'
        onClick={handleClick}
      >
        <b>Requests</b>
      </Button>
  );
} export default withRouter(RequestsButton)
// Exporting the component wrapped around "withRouter" gives the component access to props.history, 
// which means that the component can route the users to other pages.