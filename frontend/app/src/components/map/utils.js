/**
 * Utility functions for the map editor and viewer.
 */

/**
  * Re-scales and moves the stage to zoom in on mouse pointer.
  */
export const zoom = (dimensions, imgDim) => event => {
  event.evt.preventDefault();

  var stage = event.target.getStage();
  var oldScale = stage.scaleX();

  if (oldScale < 0.15 && event.evt.deltaY > 0) {
  return;
  }

  //Find mouse position relative to stage.
      var mousePointTo = {
          x: (stage.pointerPos.x - stage.x()) / oldScale,
          y: (stage.pointerPos.y - stage.y()) / oldScale
      };

  const scaleBy = 1.05;
  //Zoom in or zoom out?
  var newScale =
      event.evt.deltaY < 0 ? oldScale * scaleBy : oldScale / scaleBy;
  stage.scale({ x: newScale, y: newScale });

  //Move stage to new position (centered around mouse).
  var newPos = {
      x:
          -(mousePointTo.x - stage.pointerPos.x / newScale) *
          newScale,
      y:
          -(mousePointTo.y - stage.pointerPos.y / newScale) *
          newScale
  };
  stage.position(newPos);
  constrainImagePos(dimensions, imgDim)(event);
  stage.batchDraw();
};


export const constrainImagePos = (dimensions, imgDim) => async(event) => {
  var stage = event.target.getStage();
  var x = stage.x();
  var y = stage.y();

  var newX = x >= 0 ? 0 : x;
  if (dimensions.width <= imgDim.width*stage.scaleX()) {
    newX = x <= dimensions.width - (imgDim.width*stage.scaleX())
    ? dimensions.width - (imgDim.width*stage.scaleX()) : newX;
  } else {
    newX = 0;
  }

  var newY = y >= 0 ? 0 : y;
  if (dimensions.height <= imgDim.height*stage.scaleY()) {
    newY = y <= dimensions.height - (imgDim.height*stage.scaleY())
    ? dimensions.height - (imgDim.height*stage.scaleY()) : newY;
  } else {
    newY = 0;
  }

  stage.x(newX);
  stage.y(newY);
}
