/**
 * StartButton component. Main function is to take the user back to start. 
 */

import React from 'react';
import { Button } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import { withRouter } from 'react-router-dom';
import { colorTheme } from '../../App';
import { useDispatch } from 'react-redux';
import { selectRoom, highlightRooms, changeAGSelected } from '../../actions/roomActions';

// Variable containing styling of components in the render function below.
const useStyles = makeStyles(() => ({
  root: {
    borderRadius: 5,
    color: colorTheme.palette.primary.contrastText,
    height: 40,
    fontSize: colorTheme.font.size,
    '&:hover': {
      backgroundColor: colorTheme.palette.primary.dark,
    }
  }, 
}));

/**
 * Function wrapper for startButton component. Contains one button and when pressed takes
 * the user back to start page. 
 * props parameter is passed down from withRouter in order to access webbrowser history.
 */
function StartButton(props) {
  // Fetch styles-variable
  const classes = useStyles(); 
	// Fetch JSON object containing user information that is stored in the browser's sessionStorage.
  const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));

  const dispatch = useDispatch();

  /**
   * Redirect page to the Start content page.
   */
  const handleClick = () => {
    dispatch(selectRoom());
    dispatch(highlightRooms([]));
    dispatch(changeAGSelected(false));
    props.history.push("/" + userInformation.role + "/start");
  }

  return (
      <Button className={classes.root} onClick={handleClick} variant='text'>
        <b>Start</b>
      </Button>
  );
} export default withRouter(StartButton);
// Exporting the component wrapped around "withRouter" gives the component access to props.history, 
// which means that the component can route the users to other pages.
