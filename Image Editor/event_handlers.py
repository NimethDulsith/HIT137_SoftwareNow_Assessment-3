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
    
    def open_image(self):
        """Open an image file."""
        filepath = filedialog.askopenfilename(
            title="Open Image",
            filetypes=[
                ("All Images", "*.jpg *.jpeg *.png *.bmp"),
                ("JPEG", "*.jpg *.jpeg"),
                ("PNG", "*.png"),
                ("BMP", "*.bmp")
            ]
        )
        
        if filepath:
            success = self.processor.load_image(filepath)
            if success:
                self.current_filepath = filepath
                self.history.clear_history()
                self.history.save_state(self.processor.current_image)
                self.display_image()
                self.update_status()
                messagebox.showinfo("Success", "Image loaded successfully!")
            else:
                messagebox.showerror("Error", "Failed to load image!")
    
    def save_image(self):
        """Save image (overwrites current file)."""
        if self.current_filepath is None:
            self.save_as_image()
            return
        
        current_img = self.processor.current_image
        if current_img is not None:
            cv2.imwrite(self.current_filepath, current_img)
            messagebox.showinfo("Success", "Image saved successfully!")
        else:
            messagebox.showwarning("Warning", "No image to save!")
    
    def save_as_image(self):
        """Save image to a new file."""
        current_img = self.processor.current_image
        if current_img is None:
            messagebox.showwarning("Warning", "No image to save!")
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp")]
        )
        
        if filepath:
            cv2.imwrite(filepath, current_img)
            self.current_filepath = filepath
            messagebox.showinfo("Success", f"Image saved to:\n{filepath}")
    
    def apply_grayscale(self):
        """Apply grayscale filter."""
        if not self._check_image_loaded():
            return
        
        self.history.save_state(self.processor.current_image)
        self.processor.apply_grayscale()
        self.display_image()
    
    def apply_blur(self, intensity):
        """Apply blur effect."""
        if not self._check_image_loaded():
            return
        
        self.history.save_state(self.processor.current_image)
        self.processor.apply_blur(int(intensity))
        self.display_image()
    
    def apply_edge_detection(self):
        """Apply edge detection."""
        if not self._check_image_loaded():
            return
        
        self.history.save_state(self.processor.current_image)
        self.processor.apply_edge_detection()
        self.display_image()
    
    def apply_brightness(self, value):
        """Apply brightness adjustment."""
        if not self._check_image_loaded():
            return
        
        self.history.save_state(self.processor.current_image)
        self.processor.adjust_brightness(int(value))
        self.display_image()
    
    def apply_contrast(self, value):
        """Apply contrast adjustment."""
        if not self._check_image_loaded():
            return
        
        self.history.save_state(self.processor.current_image)
        self.processor.adjust_contrast(float(value))
        self.display_image()
    
    def rotate_image(self, angle):
        """Rotate image."""
        if not self._check_image_loaded():
            return
        
        self.history.save_state(self.processor.current_image)
        self.processor.rotate_image(angle)
        self.display_image()
    
    def flip_image(self, direction):
        """Flip image."""
        if not self._check_image_loaded():
            return
        
        self.history.save_state(self.processor.current_image)
        self.processor.flip_image(direction)
        self.display_image()
    
    def resize_image(self, width_str, height_str):
        """Resize image based on user input."""
        if not self._check_image_loaded():
            return
        
        try:
            width = int(width_str)
            height = int(height_str)
            
            if width <= 0 or height <= 0:
                raise ValueError("Dimensions must be positive")
            
            self.history.save_state(self.processor.current_image)
            self.processor.resize_image(width, height)
            self.display_image()
            self.update_status()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid width and height values!")
    
    def reset_image(self):
        """Reset to original image."""
        if not self._check_image_loaded():
            return
        
        confirm = messagebox.askyesno("Confirm Reset", "Reset to original image? This will clear history.")
        if confirm:
            self.processor.reset_to_original()
            self.history.clear_history()
            self.history.save_state(self.processor.current_image)
            self.display_image()
    
    def undo_action(self):
        """Undo last action."""
        prev_image = self.history.undo()
        if prev_image is not None:
            self.processor.set_current_image(prev_image)
            self.display_image()
        else:
            messagebox.showinfo("Info", "Nothing to undo!")
    
    def redo_action(self):
        """Redo last undone action."""
        next_image = self.history.redo()
        if next_image is not None:
            self.processor.set_current_image(next_image)
            self.display_image()
        else:
            messagebox.showinfo("Info", "Nothing to redo!")
    
    def display_image(self):
        """Display the current image on canvas."""
        current_img = self.processor.current_image
        if current_img is None:
            return
        
        self.canvas.delete('placeholder')
        
        image_rgb = cv2.cvtColor(current_img, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image_rgb)
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width > 1 and canvas_height > 1:
            pil_image.thumbnail((canvas_width - 20, canvas_height - 20), Image.Resampling.LANCZOS)
        
        self.tk_image = ImageTk.PhotoImage(pil_image)
        
        self.canvas.delete("all")
        self.canvas.create_image(
            canvas_width // 2 if canvas_width > 1 else 400,
            canvas_height // 2 if canvas_height > 1 else 300,
            image=self.tk_image,
            anchor='center'
        )
    
    def update_status(self):
        """Update status bar with image info."""
        info = self.processor.get_image_info()
        if info:
            filename = os.path.basename(self.current_filepath) if self.current_filepath else "Untitled"
            status_text = f"File: {filename} | Size: {info['width']}x{info['height']} | Channels: {info['channels']}"
            self.status_bar.config(text=status_text)
        else:
            self.status_bar.config(text="Ready")
    
    def _check_image_loaded(self):
        """Check if an image is loaded."""
        if not self.processor.has_image:
            messagebox.showwarning("Warning", "Please load an image first!")
            return False
        return True
