/**
 * This component implements lockdown of building.
 */

import React, { useState } from 'react';
import styled from 'styled-components';
import { makeStyles } from '@material-ui/core/styles';
import { Button, Container, Typography } from '@material-ui/core';
import { Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle } from '@material-ui/core';
import { useDispatch } from 'react-redux';
import { lockdown } from '../../actions/roomActions';
import { colorTheme } from '../../App';

const useStyles = makeStyles((theme) => ({
    container: {
        gridArea: 'button-lockdown',
        placeSelf: 'center center',
    },
    textButton: {
        fontSize: 50,
    },
    help: {
        marginTop: '12px',
		marginBottom: '12px',
    },
}));

const GridLayout = styled.div`
  height: 100vh;
  padding: 0em 1em;
  gap: 1em 1em;
  display: grid;
  box-sizing: border-box;
  grid-template-areas:
      "header"
      "button-lockdown";
  grid-template-rows: 70px 1fr;
`;

/**
 * Component that contains a button and some dialog functionality.
 */
export default function Lockdown() {
    const classes = useStyles();
    const [openDialog, setOpenDialog] = useState(false);
    const [isLockdown, setIsLockdown] = useState(false);
    const dispatch = useDispatch();

    const handleClose = () => {
        setOpenDialog(false);
    };

    const handleOpen = () => {
        setOpenDialog(true);
    }

    const handleLockdown = () => {
        //dispatch(lockdown());
        setIsLockdown(!isLockdown);
        setOpenDialog(false);
    }

    return (
        <GridLayout>
            <Container className={classes.container}>
                <Button
                    fullWidth
                    className={classes.button}
                    variant="contained"
                    color={isLockdown ? "primary" : "secondary"}
                    onClick={handleOpen}
                >
                    <Typography className={classes.textButton}>
                        {isLockdown ? "Open up building" : "Lockdown building"}
                    </Typography>
                </Button>
                <Dialog
                    open={openDialog}
                    onClose={handleClose}
                    aria-labelledby="alert-dialog-title"
                    aria-describedby="alert-dialog-description"
                >
                    <DialogTitle>
                        {isLockdown ? "Are you sure you want to open up?" : "Are you sure you want to lock down the building?"}
                    </DialogTitle>
                    <DialogContent>
                        <DialogContentText>
                            {isLockdown ? "Opening up the building will unblock doors as it was before lockdown."
                                        : "Locking down building will block doors in and out of the building."}
                        </DialogContentText>
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={handleClose} variant="contained" color="secondary">
                            No just kidding
                        </Button>
                        <Button onClick={handleLockdown} variant="contained" color="primary" autoFocus>
                            Yes I'm sure
                        </Button>
                    </DialogActions>
                </Dialog>
            </Container>
        </GridLayout>
    )
}
