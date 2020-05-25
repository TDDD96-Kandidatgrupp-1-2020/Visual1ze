/**
 * This file contains the root reducer that combines all of the top level
 * reducers.
 */

import {combineReducers} from 'redux';
import roomReducer from './roomReducer';
import userReducer from './userReducer';
import otherUserReducer from './otherUserReducer';

export default combineReducers({
  rooms: roomReducer,
  user: userReducer,
  otherUsers: otherUserReducer
});
