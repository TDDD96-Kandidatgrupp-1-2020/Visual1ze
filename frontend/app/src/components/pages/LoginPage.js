/**
 * LoginPage, handles the checks against the server to ensure that users get
 * directed to the right page.
 */

import React, { useState } from 'react';
import { Avatar, Box, Button, Checkbox, Container, CssBaseline, FormControlLabel,
         FormHelperText, Link, TextField, Typography, Grid } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import LogoImg from '../../res/logo.png';
import { BrowserRouter as Router, Redirect } from 'react-router-dom';
import auth from '../../auth';
import {colorTheme} from  '../../App';
import { login } from '../../actions/userActions';
import { useDispatch, useSelector } from 'react-redux';

function Copyright() {
  return (
    <Typography variant="body2" color="textSecondary" align="center">
      {'Copyright © '}
      <Link color="inherit" href="https://material-ui.com/">
        Visual1ze
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

// Variable containing styling of components in the render function below.
const useStyles = makeStyles((theme) => ({
  root: {
    backgroundColor: colorTheme.palette.primary.white,
    paddingLeft: '10px',
    paddingRight: '10px',
    paddingBottom: '20px',
    paddingTop: '20px',
    borderRadius: '10px',
    borderStyle: 'solid',
    borderColor: colorTheme.palette.primary.main,
  },
  paper: {
    display: 'flex',
    flexDirection: 'column',
    alignitems: 'center',
  },
  logo: {
    display: 'flex',
    '& > *': {
      margin: theme.spacing(0),
    },
    width: theme.spacing(25),
    height: theme.spacing(13),
  },
  form: {
    width: '100%',
    marginTop: theme.spacing(1),
  },
  submit: {
    backgroundColor: colorTheme.palette.primary.main,
    color: colorTheme.palette.primary.white,
    '&:hover':{
      backgroundColor: colorTheme.palette.primary.dark
    },
    margin: theme.spacing(3, 0, 2),
  },
  formHelperText: {
    color: "red",
    fontSize: 15
  }
}));

/**
 * This function contains the Log-in page component and its styling.
 */
export default function LoginPage(props) {
  // Fetch styles-variable
  const classes = useStyles();
  const dispatch = useDispatch();
  // Fetch email from localStorage
  const [email, setEmail] = useState(localStorage.getItem("email") || "");
  // Fetch password from localStorage (if there is anyone saved there which there aren't)
  const [password, setPassword] = useState(localStorage.getItem("password") || "");
  // Fetch from localStorage if user wants to be rememberd
  const [rememberMe, setRememberMe] = useState(localStorage.getItem("rememberMe") || false);
  // Fetch user information stored in sessionStorage
  const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));
  // Login error to be shown in case email or password are wrong
  const loginError = useSelector(state => state.user.error);

  // Redirect user away from login if the user is already logged in.
  if (auth.isAuthenticated()) {
    return <Redirect to={"/" + userInformation.role + "/start"} />
 }

  /**
   * SignIn function that handles the "changing" of the url. If succcessful login it stores
   * the userinformation in sessionStorage. And calls for auth.login with the cb function.
   * The cb function in this case is a history push to the correct place based on user info.
   */
  const handleSignIn = async(event) => {
    event.preventDefault();
    const cb = (role) => () => props.history.push("/" + role + "/start");
    dispatch(login(email, password, cb));
  }
  
  // Store email in localStorage.
  if (rememberMe) {
    localStorage.setItem("email", email);
  } else {
    localStorage.removeItem("email");
  }

  /**
   * Handle checkbox for remembering user email.
   */
  const handleRememberMe = (event) => {
    setRememberMe(event.target.checked);
    localStorage.setItem("rememberMe", event.target.checked);
  }

  return (
    <Router>
      <Grid container spacing={0} direction="column" alignItems="center" justify="center"
        style={{ minHeight: '100vh' }}
      >
      <Grid item classes={{item: classes.root}} xs={3}>
      <Container maxWidth="xs"  >
        <CssBaseline />
        <div className={classes.paper}>
          <div align="center">
            <Avatar className={classes.logo} src={LogoImg} variant="square" />
          </div>
          <form className={classes.form} onSubmit={handleSignIn} >
            <TextField
              onChange={(text) => setEmail(text.target.value)}
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="email"
              label="Email Address"
              name="email"
              defaultValue={email}
              autoComplete="email"
              autoFocus
            />
            <TextField
              onChange={(text) => setPassword(text.target.value)}
              variant="outlined"
              margin="normal"
              required
              fullWidth
              name="password"
              defaultValue={password}
              id="password"
              label="Password"
              type="password"
              autoComplete="current-password"
            />
            <FormControlLabel
              control={<Checkbox value="remember" color="primary" onChange={handleRememberMe} checked={rememberMe ? true : false}/>}
              label="Remember me"
            />
            <Button type="submit" fullWidth variant="contained" className={classes.submit}>
              Sign in
            </Button>
            {loginError && <FormHelperText className={classes.formHelperText} >
              {loginError.data.error}
            </FormHelperText>}
          </form>
          <Box mt={5}>
            <Copyright />
          </Box>
        </div>
      </Container>
      </Grid>
      </Grid>
    </Router>
  )
}
