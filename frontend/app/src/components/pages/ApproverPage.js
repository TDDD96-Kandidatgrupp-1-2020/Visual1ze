/**
 * This is the ApproverPage, user will be redirected here if they are
 * Approvers in the system. This page will contain a map and all
 * the pending request.
 */

import React from 'react';
import Header from '../header/Header';
import auth from '../../auth';
import RequestsTable from '../contents/RequestsTable';
import { Redirect, Switch } from 'react-router-dom';
import { ProtectedRoute } from '../../protected.route';
import ApproverStart from '../contents/ApproverStart';
import RequestForm from '../contents/RequestForm';
import ReaderStart from '../contents/ReaderStart';
import RevokeForm from '../contents/RevokeForm';

/**
 * This funtion is a wrapper for ApproverPage containing the following components:
 *      Start
 *      PendingRequest
 */
export default function ApproverPage() {
  // If we are not logged in we must redirect back to loginpage!
  if (!auth.isAuthenticated()) {
    return <Redirect to="/"/>
  }

  return(
    <React.Fragment>
      <Header/>
      <Switch>
        <ProtectedRoute exact path="/approver/start" >
          <ApproverStart/>
        </ProtectedRoute>

        <ProtectedRoute exact path="/approver/requests" >
          <RequestsTable/>
        </ProtectedRoute>

        <ProtectedRoute exact path="/approver/requests/form" >
          <RequestForm/>
        </ProtectedRoute>

        <ProtectedRoute exact path="/approver/personal_access" >
          <ReaderStart/>
        </ProtectedRoute>

        <ProtectedRoute exact path="/approver/requests/revoke" >
          <RevokeForm/>
        </ProtectedRoute>
      </Switch>
    </React.Fragment>
  )
}
