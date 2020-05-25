/**
 * Component representing the search bar for AGs. Exists in ReaderStart.
 */

import React, { useEffect } from 'react';
import styled from 'styled-components';
import { TextField, Typography, Button } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import { colorTheme } from '../../App';
import { Autocomplete } from '@material-ui/lab';
import { withRouter } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { selectAccessGroup, fetchAccessGroups,
         fetchAccessGroupRooms, highlightRooms,
         changeAGSelected
       } from '../../actions/roomActions';

// Variable containing styling of components in the render function below.
const useStyles = makeStyles((theme) => ({
    search: {
      float: "left",
      justifyItems: 'center',
      display: 'flex',
      alignItems: 'center',
    },
    searchBar: {
      backgroundColor: colorTheme.palette.primary.white,
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
    },
    AGName : {
      fontSize: 13,
      color: colorTheme.palette.secondary.contrastText,
    },
  }));

// CSS-grid syntax. Declares which place in the screen the component will take.
const UserSearchArea = styled.div`
  grid-area: search;
  place-self: center normal;
`;

/**
 * Component representing the search for AGs.
 */
function AGSearch(props) {
  // Fetch styles-variable
  const classes = useStyles();
  // React-redux syntax
  const dispatch = useDispatch();
  
  // State variable containing a list of all access groups
  const accessGroups = useSelector(state => state.rooms.accessGroups);
  // Currently selected access group
  const accessGroup = useSelector(state => state.rooms.accessGroup);

  /**
   * Fetch from server a list from all existing AGs and save in state
   * variable accessGroups.
   */
  useEffect(() => {
      dispatch(fetchAccessGroups());
  }, [dispatch]);

  /**
   *
   */
  const setAccessGroup = (event, values) => {
    event.preventDefault();
    dispatch(selectAccessGroup(values));
    console.log(values);
    if (values) {
      dispatch(fetchAccessGroupRooms(values.id)); // Changes highLightedRooms.
    } else {
      dispatch(highlightRooms([]));
    }
  }

  return (
  <UserSearchArea>
    <div className={classes.search}>
      <Autocomplete
        classes= {{inputRoot: classes.searchBar}}
        id={"searchAG"}
        options={accessGroups ? Object.values(accessGroups) : []}
        onChange={setAccessGroup}
        getOptionLabel={(option) => option.name}
        renderOption={(option) => (
          <div>
            <Typography className={classes.AGName}>
              <b>{option.name}</b>
            </Typography>
          </div>
        )}
        style={{ width: 300 }}
        renderInput={(params) =>
        <TextField {...params} label="Search Access Group" variant="outlined" />}
      />

      <Button className={classes.button} onClick={() => {
        if (accessGroup) {
          const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));
          dispatch(changeAGSelected(true));
          dispatch(highlightRooms([]));
          props.history.push("/" + userInformation.role + "/requests/form");
        }
      }}> Request Access Group </Button>
    </div>
  </UserSearchArea>
  );
} export default withRouter(AGSearch)
