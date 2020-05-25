import React from 'react';
import { Route, Redirect } from 'react-router-dom';
import auth from './auth';

/**
 * Handles secure routing. A user needs to have logged in in order to pass this function!
 * Component is the component that we want to route to
 *  ...rest is the rest of the props that we send with it.
 */
export const ProtectedRoute = ({ component: Component, ...rest}) => {
    return(
        <Route 
            {...rest}
            render={props => {
                if(auth.isAuthenticated()) {
                    //we are logged in! continue to forward the user to component.
                    return <Component {...rest} {...props} />
                }
                else {
                    //We are not logged in! send the user back to loginpage and send the location with it!
                    return <Redirect to={
                            {
                                pathname: "/",
                                state: {
                                    from: props.location
                                }
                            }
                        } />
                    }
                }
            }
        />
    );
}

