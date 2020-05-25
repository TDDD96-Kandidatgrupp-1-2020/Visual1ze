// TODO: add description of what this is.

import React from 'react';
import MapMetaApprover from './MapMetaApprover';
import MapMetaReader from './MapMetaReader';

/**
 * Parent of MapMetaApprover and MapMetaReader. 
 * Chooses which one to display.
 */
export default function MapMeta(props) {
  return (
    props.approver ? 
    <MapMetaApprover room={props.room}  access={props.access} 
      accessUntil={props.accessUntil} approvers={props.approvers}/> 
    : <MapMetaReader room={props.room}  access={props.access} 
      accessUntil={props.accessUntil}/>
  )
}
