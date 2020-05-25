/**
 * This is the searchbar handeling the search for users.
 * When the page loads it will fetch all users from the server, then
 * letting the approver sort the list by searching for a specific user.
 */

import React, { useEffect } from 'react';
import styled from 'styled-components';
import { TextField, Typography } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import { colorTheme } from '../../App';
import { Autocomplete } from '@material-ui/lab';
import { useDispatch, useSelector } from 'react-redux';
import { fetchApprovers } from '../../actions/otherUserActions';

/**
 * StyleSheet for UserSearch, this makes sure that button and
 * Autocomplete ends up in the same spot. It also makes sure that
 * it follows the theme of the overall application.
 */
const useStyles = makeStyles((theme) => ({
    searchBar: {
      backgroundColor: colorTheme.palette.primary.white,
    },
    search: {
      float: "left",
      justifyItems: 'center',
      display: 'flex',
      alignItems: 'center',
    },
    // Override a specific class in material UI
    inputRoot: {
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
    button: {
      float: "left",
      height: "100%",
      color: colorTheme.palette.primary.white,
      backgroundColor: colorTheme.palette.primary.main,
      marginLeft: theme.spacing(1),
      padding: theme.spacing(1.8),
      '&:hover': {
        backgroundColor: colorTheme.palette.primary.dark,
      }
    }
  }));

// CSS-grid syntax. Declares which place in the screen the component will take.
const UserSearchArea = styled.div`
  grid-area: search;
  place-self: center normal
`;

/**
 * This is the function wrapper for UserSearch, it contains the search bar
 * as Autocomplete and confirmation button as See access.
 */
export default function ApproverSearch({setApprovers}) {
  // Fetch styles-variable
  const classes = useStyles();
  // React-redux syntax
  const dispatch = useDispatch();
  // State variable containing list of all users. Set after fetch from server
  const users = useSelector(state => state.otherUsers.approvers);

  /**
   * When the component is rendered it fetches all users as a list of JSON objects.
   */
  useEffect(() => {
    dispatch(fetchApprovers());
  },[]);

  /**
   *
   */
  const changeApprovers = (event, values) => {
    event.preventDefault();
    if (values) {
      setApprovers([...values].map(approver => approver.email))
    } else {
      setApprovers([])
    }
  }

  return (
    <UserSearchArea>
      <div className={classes.search}>
        <Autocomplete
          multiple
          classes={{inputRoot: classes.searchBar}}
          id="searchUser"
          options={users}
          onChange={changeApprovers}
          getOptionLabel={(option) => option.email}
          renderOption={(option) => (
            /**
             * This is the list that will be rendered based on what the
             * user types in the textfield.
             */
            <div >
              <Typography className={classes.names}>
                <b>{option.name} {option.surname} </b>
              </Typography>

              <Typography className= {classes.email}>
                {option.email}
              </Typography>
            </div>
            )}
          style={{ minWidth: 300 }}
          renderInput={(params) => <TextField  {...params} label="Add approvers" variant="outlined"  />}
        />
      </div>
    </UserSearchArea>
  );
}
