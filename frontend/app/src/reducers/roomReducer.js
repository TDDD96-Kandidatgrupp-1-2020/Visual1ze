/**
 * This file contains the reducer for all of the room related actions.
 */

import {
  CREATE_ACCESS_GROUP,
  CREATE_ACCESS_GROUP_SUCCESS,
  CREATE_ACCESS_GROUP_FAIL,
  FETCH_ACCESS_GROUPS,
  FETCH_ACCESS_GROUPS_SUCCESS,
  FETCH_ACCESS_GROUPS_FAIL,
  FETCH_ACCESS_GROUP_ROOMS,
  FETCH_ACCESS_GROUP_ROOMS_SUCCESS,
  FETCH_ACCESS_GROUP_ROOMS_FAIL,
  FETCH_LEGAL_ROOMS,
  FETCH_LEGAL_ROOMS_SUCCESS,
  FETCH_LEGAL_ROOMS_FAIL,
  FETCH_READER_ACCESS,
  FETCH_READER_ACCESS_SUCCESS,
  FETCH_READER_ACCESS_FAIL,
  FETCH_RESPONSIBILITIES,
  FETCH_RESPONSIBILITIES_SUCCESS,
  FETCH_RESPONSIBILITIES_FAIL,
  FETCH_ROOM_DATA,
  FETCH_ROOM_DATA_SUCCESS,
  FETCH_ROOM_DATA_FAIL,
  FETCH_ROOM_GRAPHICS,
  FETCH_ROOM_GRAPHICS_SUCCESS,
  FETCH_ROOM_GRAPHICS_FAIL,
  REVOKE_ACCESS,
  REVOKE_ACCESS_SUCCESS,
  REVOKE_ACCESS_FAIL,
  HIGHLIGHT_ROOMS,
  SELECT_ROOM,
  SET_ROOMS,
  SELECT_SHAPE,
  SELECT_ACCESS_GROUP,
  RESET_STATE,
  IS_ACCESS_GROUP_SELECTED
} from '../actions/roomActions'

const initialState = {
  // Rectangles that are painted on
  roomGraphics: {},
  roomData: [],
  legalRoomIds: [],
  roomId: null,
  shape: null,
  accessGroup: null,
  accessGroups: [],
  highlightedRooms: [],
  approverResponsibilites: [],
  isAGSelected: false
}

/**
 * Updates the state using the given action {type, payload}.
 */
export default function(state = initialState, {type, payload}) {
  switch (type) {
    case REVOKE_ACCESS_SUCCESS:
    case CREATE_ACCESS_GROUP:
    case FETCH_ACCESS_GROUPS:
    case FETCH_ACCESS_GROUP_ROOMS:
    case FETCH_LEGAL_ROOMS:
    case FETCH_READER_ACCESS:
    case FETCH_RESPONSIBILITIES:
    case FETCH_ROOM_DATA:
    case FETCH_ROOM_GRAPHICS:
    case REVOKE_ACCESS:
      return {
        ...state,
        loading: true,
      }
    case CREATE_ACCESS_GROUP_FAIL:
    case FETCH_ACCESS_GROUPS_FAIL:
    case FETCH_ACCESS_GROUP_ROOMS_FAIL:
    case FETCH_LEGAL_ROOMS_FAIL:
    case FETCH_READER_ACCESS_FAIL:
    case FETCH_RESPONSIBILITIES_FAIL:
    case FETCH_ROOM_DATA_FAIL:
    case FETCH_ROOM_GRAPHICS_FAIL:
    case REVOKE_ACCESS_FAIL:
      return {
        ...state,
        loading: false,
        error: payload
      }
    case CREATE_ACCESS_GROUP_SUCCESS:
      return {
        ...state,
        loading: false,
      }
    case FETCH_RESPONSIBILITIES_SUCCESS:
      return {
        ...state,
        approverResponsibilites: payload
      }
    case FETCH_READER_ACCESS_SUCCESS:
      return {
        ...state,
        roomData: payload,
      }
    case HIGHLIGHT_ROOMS:
    case FETCH_ACCESS_GROUP_ROOMS_SUCCESS:
      return {
        ...state,
        highlightedRooms: payload
      }
    case FETCH_ACCESS_GROUPS_SUCCESS:
      return {
        ...state,
        accessGroups: payload
      }
    case FETCH_LEGAL_ROOMS_SUCCESS:
      return {
        ...state,
        legalRoomIds: payload
      }
    case FETCH_ROOM_GRAPHICS_SUCCESS:
      return {
        ...state,
        roomGraphics: payload
      }
    case FETCH_ROOM_DATA_SUCCESS:
      return {
        ...state,
        roomData: payload
      }
    case SELECT_ROOM:
      return {
        ...state,
        roomId: payload
      }
    case SET_ROOMS:
      return {
        ...state,
        roomGraphics: payload
      }
    case SELECT_SHAPE:
      return {
        ...state,
        shape: payload
      }
    case SELECT_ACCESS_GROUP:
      return {
        ...state,
        accessGroup: payload
      }
    case RESET_STATE:
      return {
        ...initialState
      }
    case REVOKE_ACCESS:
      return {
        ...state
      }
    case IS_ACCESS_GROUP_SELECTED:
      return {
        ...state,
        isAGSelected: payload
      }
    default:
      return state;
  }
}
