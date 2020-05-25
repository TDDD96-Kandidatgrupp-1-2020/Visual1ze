import {
  LOGOUT,
  LOGOUT_SUCCESS,
  LOGOUT_FAIL,
  LOGIN,
  LOGIN_SUCCESS,
  LOGIN_FAIL,
} from '../actions/userActions'

const initialState = {
  error: null,
  loading: false,
}

export default function(state = initialState, {type, payload}) {
  switch (type) {
    case LOGOUT:
    case LOGIN:
      return {
        ...state,
        loading: true,
      }
    case LOGOUT_SUCCESS:
    case LOGIN_SUCCESS:
      return {
        ...state,
        loading: false,
      }
    case LOGIN_FAIL:
    case LOGOUT_FAIL:
      return {
        ...state,
        loading: false,
        error: payload,
      }
    default:
      return state;
  }
}
