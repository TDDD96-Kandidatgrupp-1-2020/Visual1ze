/**
 * This module contains the map viewer, that is used when checking
 * your own accesses. This is the "read only" version.
 */
import React, { useState, useEffect, useLayoutEffect } from 'react';
import {Stage, Layer, Rect, Text } from 'react-konva';
import { makeStyles } from '@material-ui/core/styles';
import mapImg from '../../res/Plan2-B-hus.png';
import styled from 'styled-components';
import UrlImage from './UrlImage';
import Rectangle from './ViewerRectangle';
import { withRouter } from 'react-router-dom';
import {zoom, constrainImagePos} from './utils';
import { useSelector, useDispatch } from 'react-redux';
import { noSelectedRoom, fetchReadersForRoom } from '../../actions/otherUserActions'
import { getRoomGraphics, getRoomDataReader, selectRoom,
        selectShape, fetchResponsibilities, changeAGSelected }
        from '../../actions/roomActions';


const useStyles = makeStyles((theme) => ({
  button: {
    borderRadius: 5,
    color: 'black',
    height: 40,
    fontSize: "1em",
  },
  input: {
    display:'flex',
    flexWrap: 'wrap',
    '& > *': {
      margin: theme.spacing(11),
      width: theme.spacing(20),
      height: theme.spacing(7)
    },
  },
}));

const MapArea = styled.div`
  grid-area: map
`;

/**
 * Function for the map component.
 */
function MapViewer(props) {
	const classes = useStyles();
  const dispatch = useDispatch();

  // Array of dictionaries representing the rooms.
  // Dictionary values are arrays representing the rectangles that belong to that room.
  // Format: {room1 : [room1rects], ...}
  const rooms = useSelector(state => state.rooms.roomGraphics);

  // ID of the currently selected shape.
  const selectedShape = useSelector(state => state.rooms.shape);

  // ID of the currently selected room.
  const selectedRoom = useSelector(state => state.rooms.roomId);

  // IDs of highlighted rooms.
  const highlightedRooms = useSelector(state => state.rooms.highlightedRooms);

  // This contains the users responsibilities if it is an approver.
  const approverResponsibilites = useSelector(state => state.rooms.approverResponsibilites);

  // The position the stage starts in when MapViewer is loaded. Feel free to change!
  const startXY = [-800, -700];

  // The scale the stage starts in when Mapviewer is loaded. Feel free to change!
  const startScale = 0.5;

//------------------------------------------------------------------------------
// Meta-data of the rooms as given from database.
//------------------------------------------------------------------------------
  // All meta-data about all rooms.
  const roomsData = useSelector(state => state.rooms.roomData);
  const selectedUser = useSelector(state => state.otherUsers.selectedUser)

  // Access-until-date of the user for the given room.
  const [accessUntil, setAccessUntil] = useState();

  // Boolean that indicates whether the selected user has access to a room or not.
  const [hasAccess, setHasAccess] = useState(false);

  const [isResponsible, setIsResponsible] = useState(false);

  const [popupVisible, setPopupVisible] = useState(false);
  const [popupPos, setPopupPos] = useState([0,0]);

  // Width and height of image. Used in constrainImagePos.
  const [imgDim, setImgDim] = useState(null);


  //------------------------------------------------------------------------------
  // The dimensions of the Konva stage.
  const [dimensions, setDimensions] = useState({});

  //https://stackoverflow.com/questions/49058890/how-to-get-a-react-components-size-height-width-before-render
  const RESET_TIMEOUT = 100;
  let movement_timer = null;

  /**
   * Checks the size of the container outisde the stage and sets the dimentions
   * of the stage to match it.
   */
  const test_dimensions = () => {
    let container = document.querySelector('#stage-parent')
    if (container) {
      setDimensions({
        width: container.offsetWidth,
        height: container.offsetHeight,
      });
    }
  }

  /** Triggers before the browser paints the stage. (See docs) */
  useLayoutEffect(() => {
      test_dimensions();
    }, []);

  /**
   * Listens for resize events of the browser window, but only at intervals
   * of RESET_TIMEOUT.
   */
  window.addEventListener('resize', ()=>{
    clearInterval(movement_timer);
    movement_timer = setTimeout(test_dimensions, RESET_TIMEOUT);
  });
//------------------------------------------------------------------------------

  /**
   * Checks for clicks outside of Rectangles to deselect them.
   */
  const checkDeselect = event => {
    // deselect when clicked on empty area
    const clickedOnEmpty =
      event.target === event.target.getStage() ||
      event.target.hasName('map');

    if (clickedOnEmpty) {
      dispatch(selectShape(null));
      dispatch(selectRoom(null));
      dispatch(noSelectedRoom())
      setAccessUntil("-");
      setPopupVisible(false);
    }
  };

  /**
   * Sets the data used by Mapmeta-component.
   */
  const setMetadata = async(room_id) => {
    if (roomsData && room_id && roomsData[room_id]) {
      setHasAccess(roomsData[room_id]["access"]);

      if (roomsData[room_id]["access"]) {
        setAccessUntil(roomsData[room_id]["expires"]);
      } else {
        setAccessUntil("-");
      }

      if (approverResponsibilites.includes(room_id)) {
        setIsResponsible(true);
      } else {
        setIsResponsible(false);
      }
    }
  }

  const showPopup = async(event) => {
    var x = event.target.x() + event.target.width();
    var y = event.target.y();

    setPopupVisible(true);
    setPopupPos([x, y]);

    event.target.getStage().batchDraw();
  }

//------------------------------------------------------------------------------
// Server requests
//------------------------------------------------------------------------------

  /**
   * Call the server when the application loads, so the map data can be shown.
   */
  useEffect(() => {
    let mounted = true;
    if (mounted) {
      if (props.approver) {
        dispatch(fetchResponsibilities());
      }
      dispatch(getRoomGraphics());
      dispatch(getRoomDataReader());
    }
    return () => mounted = false;
  }, [dispatch, props.approver])



//------------------------------------------------------------------------------

  //https://www.gitmemory.com/issue/konvajs/react-konva/397/522453841
	return(
    <React.Fragment>
      <MapArea id="stage-parent" className={classes.root} tabIndex={1}>
  			<Stage
  				width={dimensions.width}
          height={dimensions.height}
          x={startXY[0]}
          y={startXY[1]}
          scaleX={startScale}
          scaleY={startScale}
          draggable={true}
          onDragMove={constrainImagePos(dimensions, imgDim)}
  				onWheel={zoom(dimensions, imgDim)}
          onMouseDown={checkDeselect}
          onTouchStart={checkDeselect}
  			>
  				<Layer>
            <UrlImage
              imageUrl={mapImg} name="map"
              setDim={setImgDim}/>
          </Layer>

          <Layer>
            {Object.entries(rooms).map(([room_id, rects]) => {
              return (
                rects.map((rect, i) => {
                  const shapeProps =
                    Object.assign({},
                                  rect,
                                  {id: room_id + ":::" + i,
                                  opacity: 0.5,
                                  name: room_id}
                                  )
                  return (
                    <Rectangle
                      key={i}
                      shapeProps={shapeProps}
                      isSelected={room_id + ":::" + i === selectedShape}
                      isHighlighted={highlightedRooms.includes(room_id)}
                      inSelectedRoom={room_id === selectedRoom}
                      inSelectedAG={false}
                      onSelect={event => {
                        if (props.onSelect) {
                            props.onSelect(room_id);
                        }
                        if (props.approver) {
                            dispatch(fetchReadersForRoom(room_id))
                        }
                        dispatch(selectShape(room_id + ":::" + i));
                        dispatch(selectRoom(room_id));
                        setMetadata(room_id);
                        showPopup(event);
                      }}
                      hasAccess={props.approver && !selectedUser ?
                          false :
                          roomsData && roomsData[room_id] && roomsData[room_id]["access"]
                      }

                      isResponsible={
                        props.approver ?
                          (JSON.parse(sessionStorage.getItem("userInformation")).role === "admin" ?
                            true :
                            approverResponsibilites.includes(room_id)
                          ) :
                          false
                      }
                      isExpiring={props.approver ? false : roomsData && roomsData[room_id] && roomsData[room_id]["warn_date"]}
                    />
                  );
                })
              );
            })}
          </Layer>
          <Layer visible={selectedRoom ? popupVisible : false}>
            <Rect fill={"white"} x={popupPos[0]} y={popupPos[1]} width={400} height={230}
               opacity={1} stroke={"black"} strokeWidth={8}/>
            <Text x={popupPos[0]+20} y={popupPos[1]+20} fontSize={30}
              text={"Room: " + (roomsData[selectedRoom] && roomsData[selectedRoom].name)} />
            <Text x={popupPos[0]+20} y={popupPos[1]+60} fontSize={30}
              text={"ID: " + selectedRoom} />
            <Text x={popupPos[0]+20} y={popupPos[1]+100} fontSize={30} width={360}
              text={"Access until: " + accessUntil}
              visible={
                props.approver ?
                  (selectedUser ?
                    ((JSON.parse(sessionStorage.getItem("userInformation")).role === "admin" || isResponsible) && hasAccess
                    ) : false
                  ) : hasAccess
              }
            />
            <Rect x={popupPos[0]+40} y={popupPos[1]+170} width={300} height={50}
              fill={"white"} stroke={"black"} strokeWidth={4} opacity={1}
              visible={
                props.approver ?
                  (selectedUser ?
                    ((JSON.parse(sessionStorage.getItem("userInformation")).role === "admin" || isResponsible) && hasAccess
                    ) : false
                  ) : true
              }
              onClick={() => {
                const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));
                if (props.approver) {
                  props.history.push("/" + userInformation.role + "/requests/revoke");
                } else {
                  props.history.push("/" + userInformation.role + "/requests/form");
                }
              }}/>
            <Text x={popupPos[0]+58} y={popupPos[1]+180} fontSize={30}
              text={props.approver ? "Revoke access" : "Request This Room"}
              visible={
                props.approver ?
                  (selectedUser ?
                    ((JSON.parse(sessionStorage.getItem("userInformation")).role === "admin" || isResponsible) && hasAccess
                    ) : false
                  ) : true
              }
              onClick={() => {
                const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));
                if (props.approver) {
                  props.history.push("/" + userInformation.role + "/requests/revoke");
                } else {
                  dispatch(changeAGSelected(false));
                  props.history.push("/" + userInformation.role + "/requests/form");
                }
              }}/>
          </Layer>
  			</Stage>
      </MapArea>
		</React.Fragment>
	)
}

export default withRouter(MapViewer)
