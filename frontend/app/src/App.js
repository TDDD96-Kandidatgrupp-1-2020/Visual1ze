/**
 * This file represents the react app. It contains the logic to switch between the
 * different pages depending on the user's role.
 */

import React from 'react'
import LoginPage from './components/pages/LoginPage'
import ReaderPage from './components/pages/ReaderPage'
import AdminPage from './components/pages/AdminPage'
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import { ProtectedRoute } from './protected.route'
import ApproverPage from './components/pages/ApproverPage';
import { createMuiTheme } from '@material-ui/core/styles';

import { Provider } from 'react-redux';
import store from './store';

export const colorTheme = createMuiTheme({
    palette: {
      primary: {
        light: '#7694e4',
        background: '#e1e2e1',
        white: '#f5f5f6',
        main: '#4267B2',
        dark: '#003d82',
        green: '#55a342',
        contrastText: '#fff',
      },
      secondary: {
        light: '#666ad1',
        main: '#303f9f',
        dark: '#001970',
        contrastText: '#000',
      },
    },
    font: {
      size: '1em'
    }
  });

/**
 * Function wrapper for the entire App component. Depending on the routing
 * the user will see different components inside App. Please note that there are routes
 * and protected routes! New user will always end up on loginpage component first.
 * when logged in the user will have access to the protected routes based on the role and token.
 */
export default function App() {
  return (
    <Provider store={store}>
      <Router>
        <Switch>
          <Route exact path="/" component={LoginPage} />
          <ProtectedRoute path="/reader" component={ReaderPage} />
          <ProtectedRoute path="/approver" component={ApproverPage} />
          <ProtectedRoute path="/admin" component={AdminPage} />
          <Route path="*" component={() => "404 - Page not found"} />
        </Switch>
      </Router>
    </Provider>
  );
}
