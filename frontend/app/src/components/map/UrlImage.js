/**
 * Contains logic and properties of the image to be displayed.
 */

import React, {useEffect, useState} from 'react'
import {Image} from 'react-konva'
import PropTypes from 'prop-types'

/**
 * This function returns a konva Image object that automaticaly
 * redraws when the image is loaded.
 */
//https://github.com/konvajs/react-konva/issues/315
export default function UrlImage({ imageUrl, name, setDim , ...props}) {
  const [image, setImage] = useState(null);

  useEffect(() => {
    const loadImage = () => {
      const image = new window.Image();
      image.src = imageUrl;
      image.onload = () => {
        setImage(image);
      }
  
      setDim({
        width: image.width,
        height: image.height
      })
    }

    loadImage();
  }, [imageUrl, setDim]);

  

  return (
    <Image
      image={image}
      name={name}
      {...props}
    />
  );
}

UrlImage.propTypes = {
  imageUrl: PropTypes.string.isRequired,
  name: PropTypes.string.isRequired,
}
