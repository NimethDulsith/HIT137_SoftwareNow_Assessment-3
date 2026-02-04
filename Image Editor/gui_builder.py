# gui_builder.py
import tkinter as tk
from tkinter import ttk


class GUIBuilder:
    """
    Professional GUI builder with modern design.
    """
    
    # Color Palette
    COLORS = {
        'bg_dark': '#2C3E50',
        'bg_medium': '#34495E',
        'accent': '#3498DB',
        'accent_hover': '#5DADE2',
        'success': '#27AE60',
        'warning': '#E67E22',
        'danger': '#E74C3C',
        'text_light': '#ECF0F1',
        'text_dark': '#2C3E50',
        'canvas_bg': '#F8F9FA',
        'button_bg': '#3498DB',
        'button_hover': '#5DADE2'
    }
    
    @staticmethod
    def create_menu_bar(root, handlers):
        """Create professional menu bar."""
        menubar = tk.Menu(root, bg=GUIBuilder.COLORS['bg_dark'], 
                         fg=GUIBuilder.COLORS['text_light'],
                         activebackground=GUIBuilder.COLORS['accent'],
                         activeforeground='white')
        root.config(menu=menubar)
        
        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0, 
                           bg=GUIBuilder.COLORS['bg_medium'],
                           fg=GUIBuilder.COLORS['text_light'],
                           activebackground=GUIBuilder.COLORS['accent'])
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Image", command=handlers['open'], accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=handlers['save'], accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=handlers['save_as'])
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        
        # Edit Menu
        edit_menu = tk.Menu(menubar, tearoff=0,
                           bg=GUIBuilder.COLORS['bg_medium'],
                           fg=GUIBuilder.COLORS['text_light'],
                           activebackground=GUIBuilder.COLORS['accent'])
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=handlers['undo'], accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=handlers['redo'], accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Reset to Original", command=handlers['reset'])
    
    @staticmethod
    def create_styled_button(parent, text, command, color='accent', width=20):
        """Create a styled button with hover effect."""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            width=width,
            bg=GUIBuilder.COLORS[color],
            fg='white',
            font=('Segoe UI', 9, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            padx=5,
            pady=3
        )
        
        # Hover effects
        def on_enter(e):
            btn.config(bg=GUIBuilder.COLORS.get(color + '_hover', GUIBuilder.COLORS['accent_hover']))
        
        def on_leave(e):
            btn.config(bg=GUIBuilder.COLORS[color])
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return btn
    
    @staticmethod
    def create_control_panel(parent, handlers):
        """Create professional scrollable control panel."""
        # Main panel container
        panel_container = tk.Frame(parent, width=280, bg=GUIBuilder.COLORS['bg_dark'])
        panel_container.pack(side=tk.LEFT, fill=tk.Y)
        panel_container.pack_propagate(False)
        
        # Create canvas for scrolling
        canvas = tk.Canvas(panel_container, bg=GUIBuilder.COLORS['bg_dark'], 
                          highlightthickness=0, width=280)
        scrollbar = tk.Scrollbar(panel_container, orient="vertical", command=canvas.yview)
        
        # Scrollable frame
        scrollable_frame = tk.Frame(canvas, bg=GUIBuilder.COLORS['bg_dark'])
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Now build content in scrollable_frame
        panel = scrollable_frame
        
        # === HEADER ===
        header = tk.Frame(panel, bg=GUIBuilder.COLORS['bg_dark'])
        header.pack(fill=tk.X, pady=(10, 15))
        
        title = tk.Label(
            header,
            text="IMAGE EDITOR",
            font=('Segoe UI', 14, 'bold'),
            bg=GUIBuilder.COLORS['bg_dark'],
            fg=GUIBuilder.COLORS['text_light']
        )
        title.pack()
        
        subtitle = tk.Label(
            header,
            text="Professional Tools",
            font=('Segoe UI', 8),
            bg=GUIBuilder.COLORS['bg_dark'],
            fg=GUIBuilder.COLORS['accent']
        )
        subtitle.pack()
        
        # === UNDO/REDO SECTION ===
        undo_frame = tk.Frame(panel, bg=GUIBuilder.COLORS['bg_dark'])
        undo_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        undo_btn = GUIBuilder.create_styled_button(
            undo_frame, "UNDO", handlers['undo'], 'warning', 12
        )
        undo_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        redo_btn = GUIBuilder.create_styled_button(
            undo_frame, "REDO", handlers['redo'], 'success', 12
        )
        redo_btn.pack(side=tk.LEFT)
        
        # Separator
        tk.Frame(panel, height=1, bg=GUIBuilder.COLORS['accent']).pack(fill=tk.X, padx=20, pady=8)
        
        # === FILTERS SECTION ===
        filters_label = tk.Label(
            panel,
            text="FILTERS",
            font=('Segoe UI', 10, 'bold'),
            bg=GUIBuilder.COLORS['bg_dark'],
            fg=GUIBuilder.COLORS['text_light'],
            anchor='w'
        )
        filters_label.pack(fill=tk.X, padx=15, pady=(5, 5))
        
        filters_frame = tk.Frame(panel, bg=GUIBuilder.COLORS['bg_dark'])
        filters_frame.pack(fill=tk.X, padx=15, pady=3)
        
        GUIBuilder.create_styled_button(
            filters_frame, "Grayscale", handlers['grayscale'], 'bg_medium', 24
        ).pack(pady=2)
        
        GUIBuilder.create_styled_button(
            filters_frame, "Edge Detection", handlers['edge_detection'], 'bg_medium', 24
        ).pack(pady=2)
        
        # === BLUR SECTION ===
        tk.Frame(panel, height=1, bg=GUIBuilder.COLORS['accent']).pack(fill=tk.X, padx=20, pady=8)
        
        blur_label = tk.Label(
            panel,
            text="BLUR EFFECT",
            font=('Segoe UI', 10, 'bold'),
            bg=GUIBuilder.COLORS['bg_dark'],
            fg=GUIBuilder.COLORS['text_light'],
            anchor='w'
        )
        blur_label.pack(fill=tk.X, padx=15, pady=(5, 5))
        
        blur_frame = tk.Frame(panel, bg=GUIBuilder.COLORS['bg_dark'])
        blur_frame.pack(fill=tk.X, padx=15, pady=3)
        
        blur_slider = tk.Scale(
            blur_frame,
            from_=1,
            to=50,
            orient='horizontal',
            bg=GUIBuilder.COLORS['bg_medium'],
            fg=GUIBuilder.COLORS['text_light'],
            troughcolor=GUIBuilder.COLORS['bg_dark'],
            activebackground=GUIBuilder.COLORS['accent'],
            highlightthickness=0,
            font=('Segoe UI', 8),
            length=230
        )
        blur_slider.set(5)
        blur_slider.pack(fill=tk.X, pady=3)
        
        GUIBuilder.create_styled_button(
            blur_frame, "Apply Blur", lambda: handlers['blur'](blur_slider.get()), 'accent', 24
        ).pack(pady=2)
        
        # === ADJUSTMENTS SECTION ===
        tk.Frame(panel, height=1, bg=GUIBuilder.COLORS['accent']).pack(fill=tk.X, padx=20, pady=8)
        
        adjust_label = tk.Label(
            panel,
            text="ADJUSTMENTS",
            font=('Segoe UI', 10, 'bold'),
            bg=GUIBuilder.COLORS['bg_dark'],
            fg=GUIBuilder.COLORS['text_light'],
            anchor='w'
        )
        adjust_label.pack(fill=tk.X, padx=15, pady=(5, 5))
        
        adjust_frame = tk.Frame(panel, bg=GUIBuilder.COLORS['bg_dark'])
        adjust_frame.pack(fill=tk.X, padx=15, pady=3)
        
        # Brightness
        tk.Label(
            adjust_frame,
            text="Brightness",
            bg=GUIBuilder.COLORS['bg_dark'],
            fg=GUIBuilder.COLORS['text_light'],
            font=('Segoe UI', 9)
        ).pack(anchor='w')
        
        brightness_slider = tk.Scale(
            adjust_frame,
            from_=-100,
            to=100,
            orient='horizontal',
            bg=GUIBuilder.COLORS['bg_medium'],
            fg=GUIBuilder.COLORS['text_light'],
            troughcolor=GUIBuilder.COLORS['bg_dark'],
            activebackground=GUIBuilder.COLORS['warning'],
            highlightthickness=0,
            font=('Segoe UI', 8),
            length=230
        )
        brightness_slider.set(0)
        brightness_slider.pack(fill=tk.X, pady=2)
        
        GUIBuilder.create_styled_button(
            adjust_frame, "Apply", lambda: handlers['brightness'](brightness_slider.get()), 'warning', 24
        ).pack(pady=2)
        
        # Contrast
        tk.Label(
            adjust_frame,
            text="Contrast",
            bg=GUIBuilder.COLORS['bg_dark'],
            fg=GUIBuilder.COLORS['text_light'],
            font=('Segoe UI', 9)
        ).pack(anchor='w', pady=(8, 0))
        
        contrast_slider = tk.Scale(
            adjust_frame,
            from_=0.5,
            to=3.0,
            resolution=0.1,
            orient='horizontal',
            bg=GUIBuilder.COLORS['bg_medium'],
            fg=GUIBuilder.COLORS['text_light'],
            troughcolor=GUIBuilder.COLORS['bg_dark'],
            activebackground=GUIBuilder.COLORS['warning'],
            highlightthickness=0,
            font=('Segoe UI', 8),
            length=230
        )
        contrast_slider.set(1.0)
        contrast_slider.pack(fill=tk.X, pady=2)
        
        GUIBuilder.create_styled_button(
            adjust_frame, "Apply", lambda: handlers['contrast'](contrast_slider.get()), 'warning', 24
        ).pack(pady=2)
        
        # === TRANSFORM SECTION ===
        tk.Frame(panel, height=1, bg=GUIBuilder.COLORS['accent']).pack(fill=tk.X, padx=20, pady=8)
        
        transform_label = tk.Label(
            panel,
            text="TRANSFORM",
            font=('Segoe UI', 10, 'bold'),
            bg=GUIBuilder.COLORS['bg_dark'],
            fg=GUIBuilder.COLORS['text_light'],
            anchor='w'
        )
        transform_label.pack(fill=tk.X, padx=15, pady=(5, 5))
        
        transform_frame = tk.Frame(panel, bg=GUIBuilder.COLORS['bg_dark'])
        transform_frame.pack(fill=tk.X, padx=15, pady=3)
        
        # Rotation
        tk.Label(
            transform_frame,
            text="Rotate:",
            bg=GUIBuilder.COLORS['bg_dark'],
            fg=GUIBuilder.COLORS['text_light'],
            font=('Segoe UI', 9)
        ).pack(anchor='w')
        
        rotate_frame = tk.Frame(transform_frame, bg=GUIBuilder.COLORS['bg_dark'])
        rotate_frame.pack(fill=tk.X, pady=2)
        
        GUIBuilder.create_styled_button(
            rotate_frame, "90 deg", lambda: handlers['rotate'](90), 'success', 7
        ).pack(side=tk.LEFT, padx=2)
        
        GUIBuilder.create_styled_button(
            rotate_frame, "180 deg", lambda: handlers['rotate'](180), 'success', 7
        ).pack(side=tk.LEFT, padx=2)
        
        GUIBuilder.create_styled_button(
            rotate_frame, "270 deg", lambda: handlers['rotate'](270), 'success', 7
        ).pack(side=tk.LEFT, padx=2)
        
        # Flip
        tk.Label(
            transform_frame,
            text="Flip:",
            bg=GUIBuilder.COLORS['bg_dark'],
            fg=GUIBuilder.COLORS['text_light'],
            font=('Segoe UI', 9)
        ).pack(anchor='w', pady=(8, 0))
        
        flip_frame = tk.Frame(transform_frame, bg=GUIBuilder.COLORS['bg_dark'])
        flip_frame.pack(fill=tk.X, pady=2)
        
        GUIBuilder.create_styled_button(
            flip_frame, "Horizontal", lambda: handlers['flip']('horizontal'), 'success', 11
        ).pack(side=tk.LEFT, padx=2)
        
        GUIBuilder.create_styled_button(
            flip_frame, "Vertical", lambda: handlers['flip']('vertical'), 'success', 11
        ).pack(side=tk.LEFT, padx=2)
        
        # Resize
        tk.Label(
            transform_frame,
            text="Resize:",
            bg=GUIBuilder.COLORS['bg_dark'],
            fg=GUIBuilder.COLORS['text_light'],
            font=('Segoe UI', 9)
        ).pack(anchor='w', pady=(8, 0))
        
        resize_frame = tk.Frame(transform_frame, bg=GUIBuilder.COLORS['bg_dark'])
        resize_frame.pack(fill=tk.X, pady=2)
        
        width_entry = tk.Entry(resize_frame, width=8, font=('Segoe UI', 9))
        width_entry.pack(side=tk.LEFT, padx=2)
        
        tk.Label(
            resize_frame,
            text="x",
            bg=GUIBuilder.COLORS['bg_dark'],
            fg=GUIBuilder.COLORS['text_light'],
            font=('Segoe UI', 10, 'bold')
        ).pack(side=tk.LEFT)
        
        height_entry = tk.Entry(resize_frame, width=8, font=('Segoe UI', 9))
        height_entry.pack(side=tk.LEFT, padx=2)
        
        GUIBuilder.create_styled_button(
            resize_frame, "Apply", lambda: handlers['resize'](width_entry.get(), height_entry.get()), 'danger', 5
        ).pack(side=tk.LEFT, padx=2)
        
        # Add some bottom padding so last item isn't cut off
        tk.Frame(panel, height=20, bg=GUIBuilder.COLORS['bg_dark']).pack()
        
        return {
            'blur_slider': blur_slider,
            'brightness_slider': brightness_slider,
            'contrast_slider': contrast_slider,
            'width_entry': width_entry,
            'height_entry': height_entry
        }
    
    @staticmethod
    def create_image_canvas(parent):
        """Create professional canvas for displaying images."""
        display_frame = tk.Frame(parent, bg='white')
        display_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        canvas = tk.Canvas(
            display_frame,
            bg=GUIBuilder.COLORS['canvas_bg'],
            highlightthickness=0
        )
        canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Stylish placeholder
        canvas.create_text(
            400, 280,
            text="No Image Loaded",
            font=('Segoe UI', 18, 'bold'),
            fill='#7F8C8D',
            tags='placeholder'
        )
        
        canvas.create_text(
            400, 320,
            text="Click File > Open to start editing",
            font=('Segoe UI', 11),
            fill='#95A5A6',
            tags='placeholder'
        )
        
        return canvas
    
    @staticmethod
    def create_status_bar(root):
        """Create professional status bar."""
        status_bar = tk.Label(
            root,
            text="Ready",
            bd=0,
            relief=tk.FLAT,
            anchor=tk.W,
            bg=GUIBuilder.COLORS['bg_dark'],
            fg=GUIBuilder.COLORS['text_light'],
            font=('Segoe UI', 9),
            padx=10,
            pady=5
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        return status_bar
