import axios from 'axios';

// -----------------------------------------------------------------------------

export const DELETE_USER = 'DELETE_USER';
export const DELETE_USER_SUCCESS = 'DELETE_USER_SUCCESS';
export const DELETE_USER_FAIL = 'DELETE_USER_FAIL';

/**
 * Delete user with the given email.
 */
export const deleteUser = (email) => async(dispatch) => {
  const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));
  dispatch({type: DELETE_USER});
  axios.delete("/admin/user/" + email, userInformation.header)
  .then(response => {
    dispatch({
      type: DELETE_USER_SUCCESS
    })
    dispatch(fetchUsers());
  })
  .catch(error => dispatch({
    type: DELETE_USER_FAIL,
    payload: error.response
  }))
}

// -----------------------------------------------------------------------------

export const REMOVE_CARD = 'REMOVE_CARD';
export const REMOVE_CARD_SUCCESS = 'REMOVE_CARD_SUCCESS';
export const REMOVE_CARD_FAIL = 'REMOVE_CARD_FAIL';

/**
 * Block the acces card of the user with the given email.
 */
export const removeCard = (email) => async(dispatch) => {
  const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));
  dispatch({type: REMOVE_CARD})
  axios.delete("/admin/card/" + email, userInformation.header)
  .then(response => dispatch({
    type: REMOVE_CARD_SUCCESS,
  }))
  .catch(error => dispatch({
    type: REMOVE_CARD_FAIL,
    payload: error.response
  }))
}

// -----------------------------------------------------------------------------

export const FETCH_USERS = 'FETCH_USERS';
export const FETCH_USERS_SUCCESS = 'FETCH_USERS_SUCCESS';
export const FETCH_USERS_FAIL = 'FETCH_USERS_FAIL';

/**
 * Fetches all users in the system.
 * Returns
 * {
 *  email: "XXX@XX.X",
 *  name: "xxxxx",
 *  surnmane: "xxxx",
 *  role: "xxxx"
 * }
 *
 * Role is either reader, approver or admin.
 */
export const fetchUsers = () => async(dispatch) => {
  const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));
  dispatch({type: FETCH_USERS})
  axios.get("/admin/readers", userInformation.header)
  .then(response => dispatch({
    type: FETCH_USERS_SUCCESS,
    payload: response.data.users
  }))
  .catch( error => dispatch({
    type: FETCH_USERS_FAIL,
    payload: error.response
  }))
}

// -----------------------------------------------------------------------------

export const FETCH_READERS = 'FETCH_READERS';
export const FETCH_READERS_SUCCESS = 'FETCH_READERS_SUCCESS';
export const FETCH_READERS_FAIL = 'FETCH_READERS_FAIL';

/**
 * Fetches all readers in the system.
 * Returns
 * {
 *  email: "XXX@XX.X",
 *  name: "xxxxx",
 *  surnmane: "xxxx"
 * }
 */
export const fetchReaders = () => async(dispatch) => {
  const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));
  dispatch({type: FETCH_READERS})
  axios.get("/approver/readers", userInformation.header)
  .then(response => dispatch({
    type: FETCH_READERS_SUCCESS,
    payload: response.data.readers
  }))
  .catch( error => dispatch({
    type: FETCH_READERS_FAIL,
    payload: error.response
  }))
}

// -----------------------------------------------------------------------------

export const FETCH_APPROVERS = 'FETCH_APPROVERS';
export const FETCH_APPROVERS_SUCCESS = 'FETCH_APPROVERS_SUCCESS';
export const FETCH_APPROVERS_FAIL = 'FETCH_APPROVERS_FAIL';

/**
* Fetches all approvers in the system.
* Returns
* {
*  email: "XXX@XX.X",
*  name: "xxxxx",
*  surnmane: "xxxx",
*  role: "xxxx"
* }
*/
export const fetchApprovers = () => async(dispatch) => {
  const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));
  dispatch({type: FETCH_APPROVERS})
  axios.get("/admin/approvers/", userInformation.header)
  .then(response => dispatch({
    type: FETCH_APPROVERS_SUCCESS,
    payload: response.data.approvers
  }))
  .catch( error => dispatch({
    type: FETCH_APPROVERS_FAIL,
    payload: error.response
  }))
}

// -----------------------------------------------------------------------------

export const FETCH_ADMINS = 'FETCH_ADMINS';
export const FETCH_ADMINS_SUCCESS = 'FETCH_ADMINS_SUCCESS';
export const FETCH_ADMINS_FAIL = 'FETCH_ADMINS_FAIL';

/**
 * Fetches all admins in the system.
 * Fetches all users in the system.
 * Returns
 * {
 *  email: "XXX@XX.X",
 *  name: "xxxxx",
 *  surnmane: "xxxx",
 *  role: "xxxx"
 * }
 */
export const fetchAdmins = () => async(dispatch) => {
  const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));
  dispatch({type: FETCH_ADMINS})
  axios.get("/admin/approvers/", userInformation.header)
  .then(response => dispatch({
    type: FETCH_ADMINS_SUCCESS,
    payload: response.data.admin
  }))
  .catch( error => dispatch({
    type: FETCH_ADMINS_FAIL,
    payload: error.response
  }))
}

// -----------------------------------------------------------------------------

export const SELECT_USER = "SELECT_USER";

/**
 * Takes the email of the user that is to be selected.
 */
export const selectUser = (email) => {
  return {
    type: SELECT_USER,
    payload: email
  }
}

// -----------------------------------------------------------------------------

export const SELECT_REQUEST = "SELECT_REQUEST";

/**
 * Selects the given request on the form.
   "type": request.type,
   "access_name": request.access_name,
   reader: {
     "name": request.name,
     "surname": request.surname,
   },
   "requested_datetime": request.requested_datetime,
   "request_id": request.request_id,
   "justification": request.justification,
 */
 export const selectRequest = (request) => {
   return {
     type: SELECT_REQUEST,
     payload: request,
   }
 }

// -----------------------------------------------------------------------------

export const UPGRADE_TO_APPROVER = "UPGRADE_TO_APPROVER";
export const UPGRADE_TO_APPROVER_SUCCESS = "UPGRADE_TO_APPROVER_SUCCESS";
export const UPGRADE_TO_APPROVER_FAIL = "UPGRADE_TO_APPROVER_FAIL";

/**
 * Uppgrades a reader to the approver role.
 */
export const upgradeToApprover = (email) => async(dispatch) => {
  const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));
  dispatch({type: UPGRADE_TO_APPROVER})
  axios.post("/admin/upgrade_to_approver", {"email": email}, userInformation.header)
  .then(response => {
    dispatch({
      type: UPGRADE_TO_APPROVER_SUCCESS,
    })
    dispatch(fetchUsers())
  })
  .catch(error => dispatch({
    type: UPGRADE_TO_APPROVER_FAIL,
    payload: error.response
  }))
}

// -----------------------------------------------------------------------------

export const UPGRADE_TO_ADMIN = "UPGRADE_TO_ADMIN";
export const UPGRADE_TO_ADMIN_SUCCESS = "UPGRADE_TO_ADMIN_SUCCESS";
export const UPGRADE_TO_ADMIN_FAIL = "UPGRADE_TO_ADMIN_FAIL";

/**
 * Uppgrades a reader to the admin role.
 */
export const upgradeToAdmin = (email) => async(dispatch) => {
  const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));
  dispatch({type: UPGRADE_TO_ADMIN})
  axios.post("/admin/upgrade_to_admin", {"email": email}, userInformation.header)
  .then(response => {
    dispatch({
      type: UPGRADE_TO_ADMIN_SUCCESS,
    })
    dispatch(fetchUsers())
  })
  .catch(error => dispatch({
    type: UPGRADE_TO_ADMIN_FAIL,
    payload: error.response
  }))
}

// -----------------------------------------------------------------------------

export const FETCH_READERS_FOR_ROOM = 'FETCH_READERS_FOR_ROOM'
export const FETCH_READERS_FOR_ROOM_SUCCESS = 'FETCH_READERS_FOR_ROOM_SUCCESS'
export const FETCH_READERS_FOR_ROOM_FAIL = 'FETCH_READERS_FOR_ROOM_FAIL'

/**
 * Fetches all readers in the given room.
 */
export const fetchReadersForRoom = (roomId) => async(dispatch) => {
  const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));
  dispatch({type: FETCH_READERS_FOR_ROOM})
  axios.post("/approver/readers_for_room", {"room_text_id": roomId}, userInformation.header)
  .then(response => dispatch({
      type: FETCH_READERS_FOR_ROOM_SUCCESS,
      payload: response.data.reader_access
  }))
  .catch(error => dispatch({
    type: FETCH_READERS_FOR_ROOM_FAIL,
    payload: error.response
  }))
}

// -----------------------------------------------------------------------------

export const NO_SELECTED_ROOM = 'NO_SELECTED_ROOM'

/**
 * Called when a room is no longer selected.
 */
 export const noSelectedRoom = () => {
   return {
     type: NO_SELECTED_ROOM,
   }
 }

// -----------------------------------------------------------------------------
