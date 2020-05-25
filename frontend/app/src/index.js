/**
 * Index render. The index.html will call on this to render the entire App.
 */

import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import { BrowserRouter } from "react-router-dom";

ReactDOM.render(<BrowserRouter><App /></BrowserRouter>, document.getElementById('root'));