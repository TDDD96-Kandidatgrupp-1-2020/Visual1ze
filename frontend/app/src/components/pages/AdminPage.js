/**
 * Component representing the whole page that an admin comes to upon login.
 */

import React from 'react';
import Header from '../header/Header';
import ApproverStart from '../contents/ApproverStart';
import auth from '../../auth';
import { Redirect, Switch } from 'react-router-dom';
import { ProtectedRoute } from '../../protected.route';
import Map from '../map/Map';
import styled from 'styled-components';
import CreateAccount from '../contents/CreateAccount';
import ManageAccounts from '../contents/ManageAccounts';
import Lockdown from '../contents/Lockdown'
import CreateAG from '../contents/CreateAG'
import ReaderStart from '../contents/ReaderStart';
import RequestsTable from '../contents/RequestsTable';
import RequestForm from '../contents/RequestForm';
import RevokeForm from '../contents/RevokeForm';

const GridLayout = styled.div`
  height: 100vh;
  padding: 0em 1em;
  gap: 1em 1em;
  display: grid;
  box-sizing: border-box;
  grid-template-areas:
    "header header"
    "map edit"
    "map meta"
		"map request";
  grid-template-rows: 70px min-content 1fr 1fr;
  grid-template-columns: 3fr 1fr;
`;

/**
 * This funtion is a wrapper containing the following components:
 * Header, ApproverStart, MapViwer, etc.
 */
export default function AdminPage() {
  // If we are not logged in we must redirect back to loginpage!
  if (!auth.isAuthenticated()) {
    return <Redirect to="/"/>
  }

  return(
    <React.Fragment>
      <Header/>
      <Switch>
        <ProtectedRoute exact path="/admin/start">
            <ApproverStart/>
        </ProtectedRoute>

        <ProtectedRoute exact path="/admin/personal_access">
            <ReaderStart />
        </ProtectedRoute>

        <ProtectedRoute exact path="/admin/requests">
            <RequestsTable />
        </ProtectedRoute>

        <ProtectedRoute exact path="/admin/requests/form" >
          <RequestForm/>
        </ProtectedRoute>

        <ProtectedRoute exact path="/admin/personal_access" >
          <ReaderStart/>
        </ProtectedRoute>

        <ProtectedRoute exact path="/admin/requests/revoke" >
          <RevokeForm/>
        </ProtectedRoute>

        <ProtectedRoute exact path="/admin/lockdown">
            <Lockdown/>
          </ProtectedRoute>

        <ProtectedRoute exact path="/admin/create_ag">
          <CreateAG/>
        </ProtectedRoute>

        <ProtectedRoute exact path="/admin/edit_map">
          <GridLayout>
            <Map/>
          </GridLayout>
        </ProtectedRoute>

        <ProtectedRoute exact path="/admin/create_account">
          <CreateAccount />
        </ProtectedRoute>

        <ProtectedRoute exact path="/admin/manage_accounts">
          <ManageAccounts />
        </ProtectedRoute>
      </Switch>
    </React.Fragment>
  )
}
