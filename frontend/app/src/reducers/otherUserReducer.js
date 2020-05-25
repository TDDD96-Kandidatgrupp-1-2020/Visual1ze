import {
  REMOVE_CARD,
  REMOVE_CARD_SUCCESS,
  REMOVE_CARD_FAIL,
  DELETE_USER,
  DELETE_USER_SUCCESS,
  DELETE_USER_FAIL,
  FETCH_USERS,
  FETCH_USERS_SUCCESS,
  FETCH_USERS_FAIL,
  FETCH_READERS,
  FETCH_READERS_SUCCESS,
  FETCH_READERS_FAIL,
  FETCH_READERS_FOR_ROOM,
  FETCH_READERS_FOR_ROOM_SUCCESS,
  FETCH_READERS_FOR_ROOM_FAIL,
  FETCH_APPROVERS,
  FETCH_APPROVERS_SUCCESS,
  FETCH_APPROVERS_FAIL,
  FETCH_ADMINS,
  FETCH_ADMINS_SUCCESS,
  FETCH_ADMINS_FAIL,
  SELECT_USER,
  SELECT_REQUEST,
  UPGRADE_TO_ADMIN,
  UPGRADE_TO_ADMIN_SUCCESS,
  UPGRADE_TO_ADMIN_FAIL,
  UPGRADE_TO_APPROVER,
  UPGRADE_TO_APPROVER_SUCCESS,
  UPGRADE_TO_APPROVER_FAIL,
  NO_SELECTED_ROOM,
} from '../actions/otherUserActions'

const initialState = {
  error: null,
  loading: false,
  users: [],
  readers: [],
  approvers: [],
  admins: [],
  selectedUser: null,
  selectedRequest: null,
  usersWithAccess: null,
}

export default function(state = initialState, {type, payload}) {
  switch (type) {
    case REMOVE_CARD:
    case DELETE_USER:
    case FETCH_USERS:
    case FETCH_READERS:
    case FETCH_APPROVERS:
    case FETCH_ADMINS:
    case UPGRADE_TO_ADMIN:
    case UPGRADE_TO_APPROVER:
    case FETCH_READERS_FOR_ROOM:
      return {
        ...state,
        loading: true,
      }
    case REMOVE_CARD_FAIL:
    case DELETE_USER_FAIL:
    case FETCH_USERS_FAIL:
    case FETCH_READERS_FAIL:
    case FETCH_APPROVERS_FAIL:
    case FETCH_ADMINS_FAIL:
    case UPGRADE_TO_ADMIN_FAIL:
    case UPGRADE_TO_APPROVER_FAIL:
    case FETCH_READERS_FOR_ROOM_FAIL:
      return {
        ...state,
        loading: false,
        error: payload,
      }
    case REMOVE_CARD_SUCCESS:
    case DELETE_USER_SUCCESS:
    case UPGRADE_TO_APPROVER_SUCCESS:
    case UPGRADE_TO_ADMIN_SUCCESS:
      return {
        ...state,
        loading: false,
      }
    case FETCH_USERS_SUCCESS:
      return {
        ...state,
        loading: false,
        users: payload,
      }
    case FETCH_READERS_SUCCESS:
      return {
        ...state,
        loading: false,
        readers: payload
      }
    case FETCH_APPROVERS_SUCCESS:
      return {
        ...state,
        loading: false,
        approvers: payload,
      }
    case FETCH_ADMINS_SUCCESS:
      return {
        ...state,
        loading: false,
        admins: payload,
      }
    case FETCH_READERS_FOR_ROOM_SUCCESS:
      return {
        ...state,
        loading: false,
        usersWithAccess: payload
      }
    case SELECT_USER:
      return {
        ...state,
        selectedUser: payload
      }
    case SELECT_REQUEST:
      return {
        ...state,
        selectedRequest: payload,
      }
    case NO_SELECTED_ROOM:
      return {
        ...state,
        usersWithAccess: null,
      }
    default:
      return state;
  }
}
