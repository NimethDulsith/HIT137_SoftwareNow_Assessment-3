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
    
    # Image processing operations using filter objects (POLYMORPHISM)
    def apply_grayscale(self):
        """Apply grayscale using filter object."""
        if self.__current_image is None:
            return None
        self.__current_image = self._filters['grayscale'].apply(self.__current_image)
        return self.__current_image.copy()
    
    def apply_blur(self, intensity=5):
        """Apply blur using filter object."""
        if self.__current_image is None:
            return None
        self._filters['blur'].set_intensity(intensity)
        self.__current_image = self._filters['blur'].apply(self.__current_image)
        return self.__current_image.copy()
    
    def apply_edge_detection(self):
        """Apply edge detection using filter object."""
        if self.__current_image is None:
            return None
        self.__current_image = self._filters['edge'].apply(self.__current_image)
        return self.__current_image.copy()
    
    def adjust_brightness(self, value):
        """Adjust brightness using filter object."""
        if self.__current_image is None:
            return None
        self._filters['brightness'].value = value
        self.__current_image = self._filters['brightness'].apply(self.__current_image)
        return self.__current_image.copy()
    
    def adjust_contrast(self, value):
        """Adjust contrast using filter object."""
        if self.__current_image is None:
            return None
        self._filters['contrast'].value = value
        self.__current_image = self._filters['contrast'].apply(self.__current_image)
        return self.__current_image.copy()
    
    def rotate_image(self, angle):
        """Rotate image by 90, 180, or 270 degrees."""
        if self.__current_image is None:
            return None
        
        if angle == 90:
            self.__current_image = cv2.rotate(self.__current_image, cv2.ROTATE_90_CLOCKWISE)
        elif angle == 180:
            self.__current_image = cv2.rotate(self.__current_image, cv2.ROTATE_180)
        elif angle == 270:
            self.__current_image = cv2.rotate(self.__current_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        
        return self.__current_image.copy()
    
    def flip_image(self, direction):
        """Flip image horizontally or vertically."""
        if self.__current_image is None:
            return None
        
        if direction == 'horizontal':
            self.__current_image = cv2.flip(self.__current_image, 1)
        elif direction == 'vertical':
            self.__current_image = cv2.flip(self.__current_image, 0)
        
        return self.__current_image.copy()
    
    def resize_image(self, width, height):
        """Resize image to specified dimensions."""
        if self.__current_image is None:
            return None
        
        if not self.validate_dimensions(width, height):
            return None
        
        self.__current_image = cv2.resize(self.__current_image, (width, height))
        return self.__current_image.copy()
    
    def reset_to_original(self):
        """Reset to original loaded image."""
        if self.__original_image is not None:
            self.__current_image = self.__original_image.copy()
            return self.__current_image.copy()
        return None
    
    # MAGIC METHODS
    def __str__(self):
        """String representation for users."""
        if self.__current_image is None:
            return "ImageProcessor: No image loaded"
        info = self.get_image_info()
        return f"ImageProcessor: {info['width']}x{info['height']}, {info['channels']} channels"
    
    def __repr__(self):
        """String representation for developers."""
        return f"ImageProcessor(has_image={self.has_image})"
    
    def __bool__(self):
        """Boolean conversion - True if image is loaded."""
        return self.__current_image is not None
