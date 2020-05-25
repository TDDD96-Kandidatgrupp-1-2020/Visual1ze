/**
 * Rectangles used in Viewer-mode.
 * Color for each room depends its on access-levels.
 */

import React, { useEffect } from 'react';
import {Rect} from 'react-konva';

/**
 * Returns a Rectangle with shifting color based on associated room's
 * access level (for the current user).
 */
export default function Rectangle({
  shapeProps, isSelected, isHighlighted, inSelectedRoom, onSelect, hasAccess, isResponsible, isExpiring })
{
  const shapeRef = React.useRef();

  useEffect(() => {
    if (inSelectedRoom) {
      shapeRef.current.setAttr('fill', 'blue');
    } else if (isHighlighted) {
      shapeRef.current.setAttr('fill', 'lightblue');
    } else if (isExpiring) {
      shapeRef.current.setAttr('fill', 'yellow');
    } else if (hasAccess) {
      shapeRef.current.setAttr('fill', 'green');
    } else if (isResponsible) {
      shapeRef.current.setAttr('fill', 'lightgreen');
    } else {
      shapeRef.current.setAttr('fill', 'grey');
    }
    shapeRef.current.getLayer().batchDraw();
  }, [isSelected, inSelectedRoom, hasAccess, isHighlighted, isExpiring, isResponsible]);

  return (
    <React.Fragment>
      <Rect
        onClick={onSelect}
        onTap={onSelect}
        ref={shapeRef}
        {...shapeProps}
      />
    </React.Fragment>
  );
};
