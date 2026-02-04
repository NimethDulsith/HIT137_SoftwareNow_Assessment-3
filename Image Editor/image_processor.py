
# image_processor.py

import cv2
import numpy as np
from filters import (GrayscaleFilter, BlurFilter, EdgeDetectionFilter,
                     BrightnessFilter, ContrastFilter)


class ImageProcessor:
    """
    Main image processing class.
    Demonstrates:
    - ENCAPSULATION (private attributes with __)
    - PROPERTY DECORATORS
    - INSTANCE ATTRIBUTES
    - CLASS ATTRIBUTES
    """
    
    # CLASS ATTRIBUTE - tracks total images processed
    images_processed_count = 0
    
    def __init__(self):
        """
        CONSTRUCTOR
        ENCAPSULATION: Private attributes with double underscore
        """
        self.__current_image = None  # Private attribute
        self.__original_image = None  # Private attribute
        self.__filepath = None  # Private attribute
        ImageProcessor.images_processed_count += 1
        
        # Initialize filter objects
        self._filters = {
            'grayscale': GrayscaleFilter(),
            'blur': BlurFilter(),
            'edge': EdgeDetectionFilter(),
            'brightness': BrightnessFilter(),
            'contrast': ContrastFilter()
        }
    
    # PROPERTY DECORATORS (@property)
    @property
    def current_image(self):
        """
        PROPERTY GETTER
        Controlled access to private attribute
        """
        return self.__current_image.copy() if self.__current_image is not None else None
    
    @property
    def dimensions(self):
        """PROPERTY: Get image dimensions."""
        if self.__current_image is None:
            return None
        height, width = self.__current_image.shape[:2]
        return (width, height)
    