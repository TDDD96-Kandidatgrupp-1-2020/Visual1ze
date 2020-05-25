/**
 * This file contain the actions related to handeling room data.
 */

import axios from 'axios';
import { selectUser } from './otherUserActions';

// -----------------------------------------------------------------------------

export const FETCH_ACCESS_GROUPS = 'FETCH_ACCESS_GROUPS';
export const FETCH_ACCESS_GROUPS_SUCCESS = 'FETCH_ACCESS_GROUPS_SUCCESS';
export const FETCH_ACCESS_GROUPS_FAIL = 'FETCH_ACCESS_GROUPS_FAIL';

/**
 * Fetches all of the access groups in the database.
 */
 export const fetchAccessGroups = () => async(dispatch) => {
  const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));
  dispatch({type: FETCH_ACCESS_GROUPS})
   axios.get("/reader/ag", userInformation.header)
   .then(response => dispatch({
     type: FETCH_ACCESS_GROUPS_SUCCESS,
     payload: response.data.access_groups
   }))
   .catch(error => dispatch({
     type: FETCH_ACCESS_GROUPS_FAIL,
     payload: error.response
   }))
 }

// -----------------------------------------------------------------------------

export const FETCH_ACCESS_GROUP_ROOMS = 'FETCH_ACCESS_GROUP_ROOMS';
export const FETCH_ACCESS_GROUP_ROOMS_SUCCESS = 'FETCH_ACCESS_GROUP_ROOMS_SUCCESS';
export const FETCH_ACCESS_GROUP_ROOMS_FAIL = 'FETCH_ACCESS_GROUP_ROOMS_FAIL';

/**
 * Fetches the room ids of the access group with the given agId.
 */
 export const fetchAccessGroupRooms = (agId) => async(dispatch) => {
   const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));
   dispatch({type: FETCH_ACCESS_GROUP_ROOMS})
   axios.get("/reader/rooms_in_ag/" + agId.toString(), userInformation.header)
   .then(response => dispatch({
     type: FETCH_ACCESS_GROUP_ROOMS_SUCCESS,
     payload: response.data.rooms
   }))
   .catch(error => dispatch({
     type: FETCH_ACCESS_GROUP_ROOMS_FAIL,
     payload: error.response
   }))
 }

// -----------------------------------------------------------------------------

export const FETCH_READER_ACCESS = 'FETCH_READER_ACCESS';
export const FETCH_READER_ACCESS_SUCCESS = 'FETCH_READER_ACCESS_SUCCESS';
export const FETCH_READER_ACCESS_FAIL = 'FETCH_READER_ACCESS_FAIL';

/**
 * Fetches the rooms that the reader has access to in the current UserSearch
 * responsibility area.
 */
 export const fetchReaderAccess = (reader) => async(dispatch) => {
  const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));
  dispatch({type: FETCH_READER_ACCESS});
  axios.get("/approver/access_for_reader/" + reader, userInformation.header)
  .then(response => dispatch({
    type: FETCH_READER_ACCESS_SUCCESS,
    payload: response.data
  }))
  .catch(error => dispatch({
    type: FETCH_READER_ACCESS_FAIL,
    payload: error.response
  }))
 }

// -----------------------------------------------------------------------------

export const FETCH_ROOM_GRAPHICS = 'FETCH_ROOM_GRAPHICS';
export const FETCH_ROOM_GRAPHICS_SUCCESS = 'FETCH_ROOM_GRAPHICS_SUCCESS';
export const FETCH_ROOM_GRAPHICS_FAIL = 'FETCH_ROOM_GRAPHICS_FAIL';

/**
 * Gets the room graphics object from the server.
 */
export const getRoomGraphics = () => async(dispatch) => {
  const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));
  dispatch({type: FETCH_ROOM_GRAPHICS})
  axios.get("/reader/map", userInformation.header)
  .then(response => dispatch({
    type: FETCH_ROOM_GRAPHICS_SUCCESS,
    payload: response.data
  }))
  .catch( error => dispatch({
    type: FETCH_ROOM_GRAPHICS,
    payload: error.response
  }))
}

// -----------------------------------------------------------------------------

export const FETCH_ROOM_DATA = 'FETCH_ROOM_DATA';
export const FETCH_ROOM_DATA_SUCCESS = 'FETCH_ROOM_DATA_SUCCESS';
export const FETCH_ROOM_DATA_FAIL = 'FETCH_ROOM_DATA_FAIL';

/**
 * Gets the room data conected to the logged in reader.
 */
export const getRoomDataReader = () => async(dispatch) => {
  const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));
  dispatch({type: FETCH_ROOM_DATA})
  axios.get("/reader/access", userInformation.header)
  .then(response => {
    dispatch({
      type: FETCH_ROOM_DATA_SUCCESS,
      payload: response.data
    })
    // This prevents the approvers room data from showing upp when in the start
    // page. Bug appeared when selecting a user, viewing own acesses and then
    // going back to start.
    dispatch(selectUser(null))
  })
  .catch(error => dispatch({
    type: FETCH_ROOM_DATA_FAIL,
    payload: error.response
  }))
}

// -----------------------------------------------------------------------------

export const FETCH_RESPONSIBILITIES = 'FETCH_RESPONSIBILITIES';
export const FETCH_RESPONSIBILITIES_SUCCESS = 'FETCH_RESPONSIBILITIES_SUCCESS';
export const FETCH_RESPONSIBILITIES_FAIL = 'FETCH_RESPONSIBILITIES_FAIL';

/**
 * Fetches the room ids of the rooms that the current approver is responsble for.
 */
export const fetchResponsibilities = () => async(dispatch) => {
  const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));
  dispatch({type: FETCH_RESPONSIBILITIES});
  axios.get("/approver/responsibilities", userInformation.header)
  .then(response => dispatch({
    type: FETCH_RESPONSIBILITIES_SUCCESS,
    payload: response.data.responsibilities
  }))
  .catch(error => dispatch({
    type: FETCH_RESPONSIBILITIES_FAIL,
    payload: error.response
  }))
}

// -----------------------------------------------------------------------------

export const FETCH_LEGAL_ROOMS = 'FETCH_LEGAL_ROOMS';
export const FETCH_LEGAL_ROOMS_SUCCESS = 'FETCH_LEGAL_ROOMS_SUCCESS';
export const FETCH_LEGAL_ROOMS_FAIL = 'FETCH_LEGAL_ROOMS_FAIL';

/**
 * This gets all of the room ids, that exist in the database.
 */
export const getLegalRoomIds = () => async(dispatch) => {
  const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));
  dispatch({type: FETCH_LEGAL_ROOMS})
  axios.get("/admin/rooms", userInformation.header)
  .then(response => dispatch({
    type: FETCH_LEGAL_ROOMS_SUCCESS,
    payload: response.data.rooms
  }))
  .catch(error => dispatch({
    type: FETCH_LEGAL_ROOMS_FAIL,
    payload: error.response
  }))
}

// -----------------------------------------------------------------------------

export const REVOKE_ACCESS = 'REVOKE_ACCESS';
export const REVOKE_ACCESS_SUCCESS = 'REVOKE_ACCESS_SUCCESS';
export const REVOKE_ACCESS_FAIL = 'REVOKE_ACCESS_FAIL';

/**
 *  Revokes the access to 'ID' for user with 'userEmail'.
 * 'isAG' selects between AG- and room-behaviour.
 */
export const revokeAccess = (isAG, ID, userEmail) => async(dispatch) => {
  const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));
  // TODO: call to remove reader from AG.
  var route;
  var items;

  if (isAG) {
    route = "ag";
    items = {
      "ag_id": ID,
      "email": userEmail
    }
  ;} else {
  route = "room";
  items = {
    "room_text_id": ID,
    "email": userEmail
    }
  ;}

  axios.post("/approver/revoke/" + route, items, userInformation.header)
  .then(response => {
    dispatch({
      type: REVOKE_ACCESS_SUCCESS
    })
    dispatch(fetchReaderAccess(userEmail));
  }).catch(error => dispatch({
    type: REVOKE_ACCESS_FAIL,
    payload: error.response
  }))
}

// -----------------------------------------------------------------------------

export const CREATE_ACCESS_GROUP = 'CREATE_ACCESS_GROUP'
export const CREATE_ACCESS_GROUP_SUCCESS = 'CREATE_ACCESS_GROUP_SUCCESS';
export const CREATE_ACCESS_GROUP_FAIL = 'CREATE_ACCESS_GROUP_FAILED'

/**
 * Creates the access group with the given data.
 * {ag_name: string, approvers: [email, ...], room_text_ids: [roomId, ...]}
 */
export const createAccessGroup = (data) => async(dispatch) => {
  const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));
  dispatch({type: CREATE_ACCESS_GROUP})
  axios.post("/admin/ag", data, userInformation.header)
  .then(response => dispatch({
    type: CREATE_ACCESS_GROUP_SUCCESS
  }))
  .catch(error => dispatch({
    type: CREATE_ACCESS_GROUP_FAIL,
    payload: error.response
  }))
}

// -----------------------------------------------------------------------------

export const SELECT_ROOM = 'SELECT_ROOM';

/**
 * Selects the room with the given roomId
 */
export const selectRoom = (roomId) => {
  return {
    type: SELECT_ROOM,
    payload: roomId
  }
}

// -----------------------------------------------------------------------------

export const SELECT_SHAPE = 'SELECT_SHAPE';

/**
 * Sets the selected shape (one of the rectangles representing a room).
 */
export const selectShape = (shape) => {
  return {
    type: SELECT_SHAPE,
    payload: shape
  }
}

// -----------------------------------------------------------------------------

export const SET_ROOMS = 'SET_ROOMS';

/**
 * Used to set the room graphics in the map editor.
 */
export const setRooms = (rooms) => {
  return {
    type: SET_ROOMS,
    payload: rooms
  }
}

// -----------------------------------------------------------------------------

export const SELECT_ACCESS_GROUP = 'SELECT_ACCESS_GROUP';

/**
 * Saves the name of the access group with the given name.
 */
export const selectAccessGroup = (accessGroup) => {
  return {
    type: SELECT_ACCESS_GROUP,
    payload: accessGroup
  }
}

// -----------------------------------------------------------------------------

export const HIGHLIGHT_ROOMS = 'HIGHLIGHT_ROOMS';

/**
 * Takes an array rooms with roomIds and saves them to be highlited in the map.
 */
export const highlightRooms = (rooms) => {
  return {
    type: HIGHLIGHT_ROOMS,
    payload: rooms
  }
}

// -----------------------------------------------------------------------------

export const RESET_STATE = 'RESET_STATE';

/**
 * Resets the state of the map. Used when loging out or switching pages.
 */
export const resetState = () => {
  return {
    type: RESET_STATE
  }
}

// -----------------------------------------------------------------------------

export const IS_ACCESS_GROUP_SELECTED = 'IS_ACCESS_GROUP_SELECTED';

/**
 * Set if an access group is selected.
 */
export const changeAGSelected = (isAGSelected) => {
  return {
    type: IS_ACCESS_GROUP_SELECTED,
    payload: isAGSelected
  }
}

// -----------------------------------------------------------------------------
