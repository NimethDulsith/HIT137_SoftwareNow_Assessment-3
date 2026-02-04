
import cv2
import numpy as np
from base_classes import ImageFilter, FileHandler


class GrayscaleFilter(ImageFilter):
    
    def __init__(self):
        """
        SUPER() - Call parent constructor
        """
        super().__init__("Grayscale")
    
    def apply(self, image):
        """Override abstract method from parent."""
        if not self.validate_image(image):
            return None
        
        if len(image.shape) == 2:
            return image.copy()
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)


class BlurFilter(ImageFilter):
    """INHERITANCE: Another child of ImageFilter."""
    
    def __init__(self, intensity=5):
        """SUPER() with additional parameter."""
        super().__init__("Blur")
        self.intensity = intensity
    
    def apply(self, image):
        """METHOD OVERRIDING: Specific blur implementation."""
        if not self.validate_image(image):
            return None
        
        intensity = self.intensity if self.intensity % 2 == 1 else self.intensity + 1
        intensity = max(1, min(99, intensity))
        return cv2.GaussianBlur(image, (intensity, intensity), 0)
    
    def set_intensity(self, value):
        """Additional method specific to BlurFilter."""
        self.intensity = value
    
    # MAGIC METHOD - Addition operator
    def __add__(self, other):
        """
        OPERATOR OVERLOADING
        Allows: blur1 + blur2 to combine intensities
        """
        if isinstance(other, BlurFilter):
            return BlurFilter(self.intensity + other.intensity)
        return NotImplemented


class EdgeDetectionFilter(ImageFilter):
    """INHERITANCE: Edge detection implementation."""
    
    def __init__(self, threshold1=50, threshold2=150):
        super().__init__("Edge Detection")
        self.threshold1 = threshold1
        self.threshold2 = threshold2
    
    def apply(self, image):
        """METHOD OVERRIDING."""
        if not self.validate_image(image):
            return None
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, self.threshold1, self.threshold2)
        edges_inverted = cv2.bitwise_not(edges)
        return cv2.cvtColor(edges_inverted, cv2.COLOR_GRAY2BGR)


class BrightnessFilter(ImageFilter):
    """INHERITANCE: Brightness adjustment."""
    
    def __init__(self, value=0):
        super().__init__("Brightness")
        self.value = value
    
    def apply(self, image):
        """METHOD OVERRIDING."""
        if not self.validate_image(image):
            return None
        return cv2.convertScaleAbs(image, alpha=1, beta=self.value)


class ContrastFilter(ImageFilter):
    """INHERITANCE: Contrast adjustment."""
    
    def __init__(self, value=1.0):
        super().__init__("Contrast")
        self.value = value
    
    def apply(self, image):
        """METHOD OVERRIDING."""
        if not self.validate_image(image):
            return None
        return cv2.convertScaleAbs(image, alpha=self.value, beta=0)


class AdvancedImageProcessor(ImageFilter, FileHandler):
    """
    MULTIPLE INHERITANCE
    Inherits from BOTH ImageFilter AND FileHandler
    Demonstrates combining functionality from multiple parents.
    """
    
    def __init__(self, name="Advanced Processor"):
        """SUPER() with multiple inheritance."""
        super().__init__(name)
        self._filters_chain = []
    
    def apply(self, image):
        """Apply all filters in chain."""
        result = image.copy()
        for filter_obj in self._filters_chain:
            result = filter_obj.apply(result)
        return result
    
    def add_filter(self, filter_obj):
        """Add a filter to the processing chain."""
        self._filters_chain.append(filter_obj)
    
    # MAGIC METHOD
    def __len__(self):
        """Return number of filters in chain."""
        return len(self._filters_chain)
    
    def __getitem__(self, index):
        """Allow indexing: processor[0] to get first filter."""
        return self._filters_chain[index]
