/**
 * This file contains the definition of the Redux store.
 */

import { createStore, applyMiddleware, compose } from 'redux';
import thunk from 'redux-thunk';
import { composeWithDevTools } from 'redux-devtools-extension';
import rootReducer from './reducers';

const initialState = {};

// Thunk is used to be able to make async calls in actions.
const middleware = [thunk];

/**
 * Sets up the store, and conects it so that Redux devtools may be used.
 */
const store = createStore(
  rootReducer,
  initialState,
  composeWithDevTools(
      applyMiddleware(...middleware),
  )
);

export default store;
