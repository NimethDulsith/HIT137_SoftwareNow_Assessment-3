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
    
    @property
    def filepath(self):
        """PROPERTY: Get current file path."""
        return self.__filepath
    
    @property
    def has_image(self):
        """PROPERTY: Check if image is loaded."""
        return self.__current_image is not None
    
    # STATIC METHOD
    @staticmethod
    def validate_dimensions(width, height):
        """
        STATIC METHOD
        Validate image dimensions without needing instance
        """
        return width > 0 and height > 0 and width <= 10000 and height <= 10000
    
    # CLASS METHOD
    @classmethod
    def get_processed_count(cls):
        """CLASS METHOD: Get total images processed."""
        return cls.images_processed_count
    
    def load_image(self, filepath):
        """Load an image from file path."""
        self.__current_image = cv2.imread(filepath)
        if self.__current_image is not None:
            self.__original_image = self.__current_image.copy()
            self.__filepath = filepath
        return self.__current_image is not None
    
    def set_current_image(self, image):
        """Set the current image (used for undo/redo)."""
        self.__current_image = image.copy() if image is not None else None
    
    def get_image_info(self):
        """Get current image information."""
        if self.__current_image is None:
            return None
        height, width = self.__current_image.shape[:2]
        channels = self.__current_image.shape[2] if len(self.__current_image.shape) > 2 else 1
        return {'width': width, 'height': height, 'channels': channels}