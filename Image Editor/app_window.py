# app_window.py
import tkinter as tk
from image_processor import ImageProcessor
from history_manager import HistoryManager
from gui_builder import GUIBuilder
from event_handlers import EventHandlers

class ImageEditorApp:
    """
    Main application window.
    Coordinates all components together.
    """
    
    def __init__(self, root):
        """Initialize the application."""
        self.root = root