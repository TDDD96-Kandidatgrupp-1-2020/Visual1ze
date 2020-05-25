import axios from 'axios';
import auth from '../auth';

// -----------------------------------------------------------------------------
export const LOGIN = 'LOGIN'
export const LOGIN_SUCCESS = 'LOGIN_SUCCESS'
export const LOGIN_FAIL = 'LOGIN_FAIL'

/**
 * SignIn function that handles the "changing" of the url. If succcessful login it stores
 * the userinformation in sessionStorage. And calls for auth.login with the cb function.
 * The cb function in this case is a history push to the correct place based on user info.
 */
export const login = (email, password, cb) => async(dispatch) => {
  dispatch({type: LOGIN})
  axios.post("/login", {
    "email": email,
    "password": password
  }).then(response => {
    console.log(response)
    const userInformation = {
      "isAuthenticated": true,
      "name": response.data.name,
      "surname": response.data.surname,
      "email": response.data.email,
      "role": response.data.role,
      "token": response.data.access_token,
      "header": { 'headers': { 'Authorization': 'Bearer ' + response.data.access_token }},
    }
    sessionStorage.clear();
    sessionStorage.setItem("userInformation", JSON.stringify(userInformation));
    const role = JSON.parse(sessionStorage.getItem("userInformation")).role;
    auth.login(cb(role));
    dispatch({type: LOGIN_SUCCESS,})
  })
  .catch(error => {
    console.log(error.response.data)
    dispatch({
      type: LOGIN_FAIL,
      payload: error.response,
  })});
}

// -----------------------------------------------------------------------------

export const LOGOUT = 'LOGOUT';
export const LOGOUT_SUCCESS = 'LOGOUT_SUCCESS';
export const LOGOUT_FAIL = 'LOGOUT_FAIL';

/**
 * Invalidates the token that the server keeps.
 */
export const logout = () => async(dispatch) => {
  const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));
  dispatch({type: LOGOUT})
  axios.post("/logout", {}, userInformation.header)
  .then(response => {
    dispatch({
     type: LOGOUT_SUCCESS,
    })
  })
  .catch(error => {
    dispatch({
      type: LOGOUT_FAIL,
      payload: error.response,
    })
  })
}

// -----------------------------------------------------------------------------
