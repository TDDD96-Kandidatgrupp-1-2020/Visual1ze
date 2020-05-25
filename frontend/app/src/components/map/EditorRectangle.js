/**
 * Rectangles used in Editor-mode. 
 * These Rectangles support 'Transform' (resizing, rotation, etc.) and is draggable,
 * unlike 'ViewerRectangle'.
 */

import React, { useEffect } from 'react';
import { Rect, Transformer } from 'react-konva';

/**
 * Returns Rectangles that support 'Transform' (resizing, rotation, etc.).
 */
export default function Rectangle({shapeProps, isSelected, inSelectedRoom, onSelect, onChange}) {
  const shapeRef = React.useRef();
  const trRef = React.useRef();

  useEffect(() => {
    if (isSelected) {
      // we need to attach transformer manually
      trRef.current.setNode(shapeRef.current);
      trRef.current.getLayer().batchDraw();
    }

    if (inSelectedRoom) {
      shapeRef.current.setAttr('fill', 'red');
    } else {
      shapeRef.current.setAttr('fill', 'blue');
    }
  }, [isSelected, inSelectedRoom]);

  return (
    <React.Fragment>
      <Rect
        onClick={onSelect}
        onTap={onSelect}
        ref={shapeRef}
        {...shapeProps}
        draggable
        onDragEnd={event => {
          onChange({
            x: event.target.x(),
            y: event.target.y(),
            width: shapeProps.width,
            height: shapeProps.height

          });
        }}
        onTransformEnd={e => {
          const node = shapeRef.current;
          const scaleX = node.scaleX();
          const scaleY = node.scaleY();
          const width = node.width();
          const height = node.height();

          // we will reset it back
          node.scaleX(1);
          node.scaleY(1);
          node.width(width * scaleX);
          node.height(height * scaleY);

          onChange({
            x: Math.floor(node.x()),
            y: Math.floor(node.y()),
            // set minimal value
            width: Math.floor(Math.max(2, width * scaleX)),
            height: Math.floor(Math.max(2, height * scaleY))
          });
        }}
      />
      {isSelected && (
        <Transformer ref={trRef}/>
      )}
    </React.Fragment>
  );
};
