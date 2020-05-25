/**
 * This module contains the map editor, used for creating and editing the
 * the graphical representation of the map object.
 */

import React, { useState, useEffect, useLayoutEffect } from 'react';
import {Stage, Layer, Rect } from 'react-konva';
import { Paper, Input } from '@material-ui/core';
import { Button } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import mapImg from '../../res/Plan2-B-hus.png';
import kermitImg from '../../res/kermit.png';
import styled from 'styled-components';
import MapMetaAdmin from './mapMetaComponent/MapMetaAdmin.js';
import UrlImage from './UrlImage';
import Rectangle from './EditorRectangle';
import {zoom, constrainImagePos} from './utils';

import { useSelector, useDispatch } from 'react-redux';
import { getLegalRoomIds, getRoomGraphics, getRoomDataReader, selectRoom, setRooms,
          selectShape } from '../../actions/roomActions';

const axios = require('axios');

const useStyles = makeStyles((theme) => ({
  button: {
    borderRadius: 5,
    color: 'black',
    height: 40,
    fontSize: "1em",
  },
  input: {
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

const MetaArea = styled.div`
  grid-area: meta
`;

const EditArea = styled.div`
  grid-area: edit
`;


/**
 * Function for the map component.
 */
export default function Map(props) {
  const classes = useStyles();
  const dispatch = useDispatch();
  const [imgSrc, setImgSrc] = useState(mapImg);

  // Array of dictionaries representing the rooms.
  // Dictionary values are arrays representing the rectangles that belong to that room.
  // Format: {room1 : [room1rects], ...}
  const rooms = useSelector(state => state.rooms.roomGraphics);

  // The room ids that exist in the database.
  const legalRoomIds = useSelector(state => state.rooms.legalRoomIds);

  // ID of the currently selected shape.
  const selectedShape = useSelector(state => state.rooms.shape);

  // ID of the currently selected room.
  const selectedRoom = useSelector(state => state.rooms.roomId);

  const [creationId, setCreationId] = useState("");

  // The position the stage starts in when MapViewer is loaded. Feel free to change!
  const startXY = [-800, -700];

  // The scale the stage starts in when Mapviewer is loaded. Feel free to change!
  const startScale = 0.5;


//------------------------------------------------------------------------------
// Meta-data of the rooms as given from database.
//------------------------------------------------------------------------------
  // All meta-data about all rooms.
  const roomsData = useSelector(state => state.rooms.roomData)

  // Approvers for the given room, displayed in MapMeta.
  const [approversMeta, setApproversMeta] = useState();

  // Width and height of image. Used in constrainImagePos.
  const [imgDim, setImgDim] = useState(null);


  //----------------------------------------------------------------------------
  // The dimensions of the Konva stage
  const [dimensions, setDimensions] = useState({});

  // https://stackoverflow.com/questions/49058890/how-to-get-a-react-components-size-height-width-before-render
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
  //----------------------------------------------------------------------------

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
      setApproversMeta(null);
    }
  };

  /**
   * Removes selected Rectangle from rooms.
   */
  const deleteRect = event => {
    if (event.keyCode === 46) {
        if (selectedRoom) {
          const new_rooms = JSON.parse(JSON.stringify(rooms));
          const index = selectedShape.split(":::")[1]
          new_rooms[selectedRoom].splice(index, 1);
          if (new_rooms[selectedRoom].length === 0) {
            delete new_rooms[selectedRoom]
          }
          dispatch(setRooms(new_rooms));
          dispatch(selectShape(null));
        }
    }
  };

  /**
  * Switches the currently displayed image between kermitImg and mapImg.
  */
	const changeImg = () => {
		if (imgSrc === kermitImg) {
			setImgSrc(mapImg);
		}
		else {
			setImgSrc(kermitImg);
		}
	};

  /**
  * Adds a rect to 'new_rooms' on the position of mouse.
  */
	const addRect = event => {
    const new_rooms = JSON.parse(JSON.stringify(rooms));

    if (creationId !== "" &&
        !new_rooms[creationId] &&
        legalRoomIds &&
        legalRoomIds.includes(creationId)) {
      new_rooms[creationId] = [];
    }

    if (new_rooms[creationId]) {
      const stage = event.target.getStage();
      const scale = stage.scaleX();
      new_rooms[creationId].push(
        {
          x: (stage.pointerPos.x - stage.x()) / scale,
          y: (stage.pointerPos.y - stage.y()) / scale,
          width: 100, height: 100
        }
      );
      dispatch(setRooms(new_rooms));
    }
  };

  /** Sets the data used by Mapmeta-component. */
  const setMetadata = async(room_id) => {
    if (roomsData && room_id && roomsData[room_id]) {
      setApproversMeta(roomsData[room_id]["approvers"]);
    }
  }

//------------------------------------------------------------------------------
// Server requests
//------------------------------------------------------------------------------

  /**
   * Saves the data in rooms to the server.
   */
  const saveMap = async() => {
    const userInformation = JSON.parse(sessionStorage.getItem("userInformation"));
    axios.post("/admin/map", rooms, userInformation.header)
    .then(response => {
      console.log(response.data);
    })
    .catch(error => {
      console.log(error);
    });
  }

  /** Call the server when the application loads, so the map data can be shown. */
  useEffect(() => {
    dispatch(getLegalRoomIds());
    dispatch(getRoomGraphics());
    dispatch(getRoomDataReader());
  }, [dispatch])

//------------------------------------------------------------------------------

  //https://www.gitmemory.com/issue/konvajs/react-konva/397/522453841
	return(
    <React.Fragment>
      <MapArea id="stage-parent" className={classes.root} tabIndex={1} onKeyDown={deleteRect}>
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
  				onDblClick={addRect}
  			>
  				<Layer>
            <UrlImage
              imageUrl={imgSrc}
              name="map"
              setDim={setImgDim} />
            <Rect x={10} y={10} width={50} height={50} fill={"green"} stroke={"black"} onClick={changeImg}/>
  				</Layer>
          <Layer>
          {Object.entries(rooms).map(([room_id, rects]) => {
            return (
              rects.map((rect, i) => {
                const shapeProps =
                  Object.assign({},
                                rect,
                                {id: room_id + ":::" + i,
                                fill: 'blue',
                                opacity: 0.5,
                                name: room_id}
                                )
                return (
                  <Rectangle
                    key={i}
                    shapeProps={shapeProps}
                    isSelected={room_id + ":::" + i === selectedShape}
                    inSelectedRoom={room_id === selectedRoom}
                    onSelect={() => {
                      dispatch(selectShape(room_id + ":::" + i));
                      dispatch(selectRoom(room_id));
                      setMetadata(room_id);
                    }}
                    onChange={newAttrs => {
                      const new_rooms = JSON.parse(JSON.stringify(rooms));
                      new_rooms[room_id][i] = newAttrs;
                      dispatch(setRooms(new_rooms));
                    }}
                  />
                );
              })
            );
          })}
          </Layer>
  			</Stage>
      </MapArea>
      <EditArea>
        <Button
          className={classes.button} onClick={saveMap}
          variant='text' color='primary'
        >
          Save Map
        </Button>
        <Paper>
          <Input id='json-input' label='Rooms JSON'
          value={creationId} onInput={e => setCreationId(e.target.value)}
          />
        </Paper>
      </EditArea>
      <MetaArea>
        <MapMetaAdmin
          room={selectedRoom} approvers={approversMeta}
        />
      </MetaArea>
		</React.Fragment>
	)
}
