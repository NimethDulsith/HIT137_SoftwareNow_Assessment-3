import tkinter as tk
from app_window import ImageEditorApp
from image_processor import ImageProcessor
from base_classes import ImageFilter
from filters import BlurFilter

def demonstrate_oop_concepts():
    """
    Optional: Demonstrate OOP concepts in console.
    This function shows all the OOP features.
    """
    print("=" * 60)
    print("IMAGE EDITOR - OOP CONCEPTS DEMONSTRATION")
    print("=" * 60)
    
    # 1. CLASS ATTRIBUTES
    print(f"\n1. CLASS ATTRIBUTES:")
    print(f"   Total filters applied: {ImageFilter.get_total_filters_applied()}")
    print(f"   Images processed: {ImageProcessor.get_processed_count()}")
    
    # 2. MAGIC METHODS
    print(f"\n2. MAGIC METHODS (__str__, __repr__, __len__, __add__):")
    blur1 = BlurFilter(10)
    blur2 = BlurFilter(20)
    print(f"   Blur1: {blur1}")  # Calls __str__
    print(f"   Blur1 repr: {repr(blur1)}")  # Calls __repr__
    combined = blur1 + blur2  # Calls __add__
    print(f"   Combined blur intensity: {combined.intensity}")
    
    # 3. STATIC METHODS
    print(f"\n3. STATIC METHODS:")
    print(f"   Valid dimensions (800, 600)? {ImageProcessor.validate_dimensions(800, 600)}")
    print(f"   Valid dimensions (-10, 600)? {ImageProcessor.validate_dimensions(-10, 600)}")
    
    print("\n" + "=" * 60)
    print("All OOP concepts are integrated in the application!")
    print("=" * 60 + "\n")

def main():
    """Main entry point."""
    # Optional: Show OOP demonstration in console
    demonstrate_oop_concepts()
    
    # Launch GUI application
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
