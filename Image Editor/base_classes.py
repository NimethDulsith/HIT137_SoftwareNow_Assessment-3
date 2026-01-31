from abc import ABC, abstractmethod
import cv2
import numpy as np


class ImageFilter(ABC):
    """
    ABSTRACT BASE CLASS for all filters.
    """
    
    # CLASS ATTRIBUTE - shared by all filter instances
    total_filters_applied = 0
    supported_formats = ['jpg', 'jpeg', 'png', 'bmp']
    
    def __init__(self, name):
        """
        CONSTRUCTOR
        Demonstrates: Instance attributes, Encapsulation
        """
        self._name = name  # Protected attribute
        self._last_applied_time = None
        ImageFilter.total_filters_applied += 1
    
    @abstractmethod
    def apply(self, image):
        """
        ABSTRACT METHOD - must be implemented by child classes.
        Demonstrates: Polymorphism (different implementations in children)
        """
        pass
    
    @property
    def name(self):
        """
        PROPERTY DECORATOR (@property)
        Getter for filter name
        """
        return self._name
    
    @staticmethod
    def validate_image(image):
        """
        STATIC METHOD (@staticmethod)
        Utility method that doesn't need instance data.
        """
        if image is None:
            return False
        if not isinstance(image, np.ndarray):
            return False
        return True
    
    @classmethod
    def get_total_filters_applied(cls):
        """
        CLASS METHOD (@classmethod)
        Access class attributes
        """
        return cls.total_filters_applied
    
    @classmethod
    def reset_counter(cls):
        """CLASS METHOD to reset the counter."""
        cls.total_filters_applied = 0
    
    # MAGIC METHODS
    def __str__(self):
        """String representation for users."""
        return f"Filter: {self._name}"
    
    def __repr__(self):
        """String representation for developers."""
        return f"ImageFilter(name='{self._name}')"
    
    def __call__(self, image):
        """
        Makes the filter callable like a function.
        Example: filter(image) instead of filter.apply(image)
        """
        return self.apply(image)


class FileHandler:
    """
    MIXIN CLASS for file operations.
    Used for MULTIPLE INHERITANCE demonstration.
    """
    
    @staticmethod
    def get_file_extension(filepath):
        """Extract file extension."""
        return filepath.split('.')[-1].lower()
    
    @staticmethod
    def validate_file_format(filepath):
        """Validate if file format is supported."""
        ext = FileHandler.get_file_extension(filepath)
        return ext in ImageFilter.supported_formats
    
    def load_from_file(self, filepath):
        """Load image from file."""
        if self.validate_file_format(filepath):
            return cv2.imread(filepath)
        return None
    
    def save_to_file(self, image, filepath):
        """Save image to file."""
        if image is not None:
            return cv2.imwrite(filepath, image)
        return False
