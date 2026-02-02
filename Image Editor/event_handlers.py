# event_handlers.py
from tkinter import filedialog, messagebox
import cv2
import os
from PIL import Image, ImageTk

class EventHandlers:
    """Handles all user events (button clicks, menu actions, etc.)"""
    
    def __init__(self, processor, history, canvas, status_bar):
        """Initialize with references to other components."""
        self.processor = processor
        self.history = history
        self.canvas = canvas
        self.status_bar = status_bar
        self.current_filepath = None
        self.tk_image = None