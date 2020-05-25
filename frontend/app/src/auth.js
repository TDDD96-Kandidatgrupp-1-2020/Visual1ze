/**
 * This mimics a singleton class with one instance of login.
 * Instead of just setting the authenticated to true or false we must set it
 * based on the correct login with the server.
 * 
 * Token should be "stored" here (obviously we should store it as a cookie or localstorage,
 *  but we should be able to get it and check it from here)
 */

/**
 * Singleton instance of Auth class. This class will be created upon visiting the website
 * and there will only ever be one Auth. (That is also why all references to this class
 * are in lowercase letters.)
 */

class Auth {
    constructor() {
        if (sessionStorage.length === 0)
        {
            this.authenticated = false;
        }
        else {
            //check if the token match the token in server!
            this.authenticated = true;
        }
    }
    /**
     * Save this code please! We need to check if the token is right before initializing a new instance of this class.
     *
    constructor() {
        this.state = {
            authenticated: null
        }
        axios.get("/get_reader/access", sessionStorage.header).then(function (response) {
            this.state.authenticated=  true;
          })
            .catch(function (error) {
              console.log("ERROR");
              console.log(error.response);
              //state.authenticated = false;
            }); 
    }
    */



    /**
     * Login function that takes in a function cb (callBack function). Upon entering it will set authenticated
     * to true and will execute the cb funtion. No checks are done here, instead the checks are done in LoginPage.
     */
    login(cb) {
        this.authenticated = true; 
        cb();
        const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));
        console.log(userInformation);
    }

    /**
     * Logout is very similar to login. It takes in a cb function (callBack). Again no checks are done here, instead
     * the system checks everything when the user presses the signout button i UsernameDropdown. 
     * First it clears the sessionStorage then sets authenticated to false and after thet it executes the 
     * cb funtion.
     *
     * NOTE: for both login and logout the cb function should focus on pushing a new URL to browserHistory.
     */
    logout(cb) {
        sessionStorage.clear();
        this.authenticated = false;
        cb();
    }

 
    /**
     * Mostly a placeholder for checking if the user is still logged in.
     */
    isAuthenticated() {
        /*
            Check for token in localstorage here!
            Example: store token in local storage and when called upon check if local token is same as server token.
            return true or false!
        */
       const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));
       if ((window.location.pathname === "/") || window.location.pathname.includes(userInformation.role)) {
        return this.authenticated;
       }
       else {
           return false;
       }
    }

    //NOTE: We are exporting a new Auth! this is important for the singleton pattern.
} export default new Auth()