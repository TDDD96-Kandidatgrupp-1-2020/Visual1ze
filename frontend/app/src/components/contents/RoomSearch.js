/**
 * Component representing the search bar for AGs. Exists in ReaderStart.
 */

import React, { useEffect } from 'react';
import styled from 'styled-components';
import { TextField, Typography } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import { colorTheme } from '../../App';
import { Autocomplete } from '@material-ui/lab';
import { withRouter } from 'react-router-dom';
import { useDispatch, useSelector} from 'react-redux';
import { selectRoom, getRoomDataReader, selectShape 
       } from '../../actions/roomActions';

// Variable containing styling of components in the render function below.
const useStyles = makeStyles((theme) => ({
    search: {
      float: "right",
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
function RoomSearch(props) {
  // Fetch styles-variable
  const classes = useStyles();
  // React-redux syntax
  const dispatch = useDispatch();
  
  // State variable containing a list of all access groups
  const roomData = useSelector(state => state.rooms.roomData);
  // Currently selected access group

  /**
   * Fetch from server a list from all existing AGs and save in state
   * variable accessGroups.
   */
  useEffect(() => {
      dispatch(getRoomDataReader());
  }, [dispatch]);

  /**
   *
   */
  const setSelectedRoom = (event, values) => {
    if (values) {
      var key = Object.keys(roomData).find(key => roomData[key] === values);
      dispatch(selectShape(key + ":::" + 0));
      dispatch(selectRoom(key)); // Changes highLightedRooms.
    } else {
      dispatch(selectShape([]));
      dispatch(selectRoom([])); // Changes highLightedRooms.
    }
  }

  return (
  <UserSearchArea>
    <div className={classes.search}>
      <Autocomplete
        classes= {{inputRoot: classes.searchBar}}
        id={"RoomSearch"}
        options={roomData ? Object.values(roomData) : []}
        onChange={setSelectedRoom}
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
        <TextField {...params} label="Search Room" variant="outlined" />}
      />
    </div>
  </UserSearchArea>
  );
} export default withRouter(RoomSearch)
