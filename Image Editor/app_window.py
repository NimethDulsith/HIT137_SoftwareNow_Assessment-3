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
        self.root.title("Professional Image Editor | HIT137 Assignment 3")
        self.root.geometry("1400x850")
        self.root.configure(bg='white')
        
        self.processor = ImageProcessor()
        self.history = HistoryManager()
        
        self._build_gui()
        self._setup_shortcuts()
    
    def _build_gui(self):
        """Build all GUI components."""
        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = GUIBuilder.create_image_canvas(main_frame)
        self.status_bar = GUIBuilder.create_status_bar(self.root)
        
        self.handlers = EventHandlers(self.processor, self.history, self.canvas, self.status_bar)
        
        handler_callbacks = {
            'grayscale': self.handlers.apply_grayscale,
            'edge_detection': self.handlers.apply_edge_detection,
            'blur': self.handlers.apply_blur,
            'brightness': self.handlers.apply_brightness,
            'contrast': self.handlers.apply_contrast,
            'rotate': self.handlers.rotate_image,
            'flip': self.handlers.flip_image,
            'resize': self.handlers.resize_image,
            'undo': self.handlers.undo_action,
            'redo': self.handlers.redo_action
        }