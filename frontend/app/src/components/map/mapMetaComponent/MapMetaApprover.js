/**
 * Component for displaying meta-data for a selected room. Used in approver-page.
 */

import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';

const useStyles = makeStyles((theme) => ({
  root: {
    width: '100%',
    maxWidth: 400,
    backgroundColor: theme.palette.background.paper,
    position: 'relative',
    overflow: 'auto',
    maxHeight: 200,
    borderColor: 'black',
    borderStyle: 'solid',
    margin: theme.spacing(0, 2),
  },
  item: {
    padding: theme.spacing(0, 1),
  },
}));

/**
 * Displays meta-data for a given room. Specialized for Reader access. 
 * (Under construction)
 */
export default function MapMetaApprover({room, access, accessUntil, approvers}) {
  var room_name = room ?
    `${room}` : `-`;
  var access = access ? 
    `Expires ${accessUntil}` : `-`;
  var approver = approvers ? 
    `${approvers[0]["name"]} ${approvers[0]["surname"]}` :
    `-`;

  const classes = useStyles();

  return (
    <List border={1} className={classes.root} subheader={<li />}>
      {[['Room name', room_name], ['Access', access],
       ['Approvers', approver]
      ].map((item) => (
        <ListItem className={classes.item} key={`${item[0]}`}>
          <ListItemText primary={`${item[0]}: ${item[1]}`}/>
        </ListItem>
      ))}
    </List>
  );
}
