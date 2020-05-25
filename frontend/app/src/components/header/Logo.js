/**
 * Logo component containing the image of Visual1ze.
 */

import React from 'react';
import LogoImg from '../../res/logo.png';
import { makeStyles } from '@material-ui/core/styles';
import { IconButton } from '@material-ui/core';
import { withRouter } from 'react-router-dom';

// This maxHeight needs to be the same as the first value in grid-template-rows.
// Until we find a beter structure for css or decide that this is how we want
// to do things.
const useStyles = makeStyles((theme) => ({
  root: {
    paddingLeft: theme.spacing(0),
    borderRadius: '5%',
  },
  button: {
    maxHeight: '70px',
    padding: theme.spacing(0),
  }
}));

/**
 * Function component that contains the Visulal1ze logo.
 */
function Logo(props) {
  // Fetch styles-variable
  const classes = useStyles();
  // Fetch user information stored in sessionStorage
  const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));

  const handleClick = () => {
    props.history.push("/" + userInformation.role + "/start");
  }

    return (
      <IconButton className={classes.root} onClick={handleClick}>
        <img className={classes.button} src={LogoImg} alt="visual1ze"/>
      </IconButton>
    );
} export default withRouter(Logo)
