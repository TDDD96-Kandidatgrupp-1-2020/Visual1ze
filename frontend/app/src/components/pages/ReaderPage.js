/**
 * This file contains the ReaderPage component. It wraps components such as
 * Header, Start and Map.
 */

import React, { useState } from 'react';
import Header from '../header/Header';
import ReaderStart from '../contents/ReaderStart';
import RequestForm from '../contents/RequestForm';
import RequestsTable from '../contents/RequestsTable';
import auth from '../../auth';
import { Redirect, Switch } from 'react-router-dom';
import { ProtectedRoute } from '../../protected.route';

/**
 * This funtion is a wrapper containing the following components:
 * Header and Map. It contains routing functionality in the return statement.
 */
export default function ReaderPage() {
  // If we are not logged in we must redirect back to login page!
  if (!auth.isAuthenticated()) {
    return <Redirect to="/"/>
  };

  return(
    <React.Fragment>
      <Header/>
      <Switch>
        <ProtectedRoute exact path="/reader/start" component={ReaderStart} />
        <ProtectedRoute exact path="/reader/requests" component={RequestsTable} />
        <ProtectedRoute exact path="/reader/requests/form" component={RequestForm}/>
      </Switch>
    </React.Fragment>
  )
}
