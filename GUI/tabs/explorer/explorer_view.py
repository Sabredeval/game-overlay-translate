import tkinter as tk
from tkinter import StringVar, ttk, Canvas
from GUI.common.app_theme import AppTheme

class ExplorerView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Initialize variables
        self.controller = None
        self.explorer_search_var = StringVar()
        self.view_var = StringVar()
        
        # Create UI components
        self._create_search_area()
        self._create_options_area()
        self._create_visualization_area()
    
    def set_controller(self, controller):
        """Binds view with its controller"""
        self.controller = controller
        
        # Connect event handlers
        self.explore_button.config(command=self._on_explore)
        self.view_dropdown.bind("<<ComboboxSelected>>", self._on_view_changed)
    
    def _create_search_area(self):
        """Create the search input area"""
        search_frame = ttk.Frame(self)
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(search_frame, text="Explore Word:").pack(side=tk.LEFT, padx=5)
        
        explorer_entry = ttk.Entry(search_frame, textvariable=self.explorer_search_var, width=30)
        explorer_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.explore_button = ttk.Button(search_frame, text="Explore", style="Accent.TButton")
        self.explore_button.pack(side=tk.LEFT, padx=5)
    
    def _create_options_area(self):
        """Create visualization options area"""
        options_frame = ttk.Frame(self)
        options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(options_frame, text="View:").pack(side=tk.LEFT, padx=5)
        
        self.view_options = ["Word Network", "Etymology Tree", "Word Family", "Semantic Field"]
        self.view_var.set(self.view_options[0])
        
        self.view_dropdown = ttk.Combobox(
            options_frame, 
            textvariable=self.view_var, 
            values=self.view_options, 
            state="readonly", 
            width=15
        )
        self.view_dropdown.pack(side=tk.LEFT, padx=5)
    
    def _create_visualization_area(self):
        """Create the visualization area"""
        self.viz_frame = ttk.LabelFrame(self, text="Word Network")
        self.viz_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Placeholder for when no word is selected
        self.viz_placeholder = ttk.Label(
            self.viz_frame, 
            text="Enter a word above to explore its relationships",
            font=AppTheme.HEADING_FONT
        )
        self.viz_placeholder.pack(expand=True, pady=50)
        
        # Canvas for actual visualization
        self.canvas = Canvas(self.viz_frame, background="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.pack_forget()  # Hide initially
    
    def update_visualization_title(self, title):
        """Update the visualization frame title"""
        self.viz_frame.config(text=title)
    
    def show_placeholder(self):
        """Show the placeholder message"""
        self.canvas.pack_forget()
        self.viz_placeholder.pack(expand=True, pady=50)
    
    def show_canvas(self):
        """Show the visualization canvas"""
        self.viz_placeholder.pack_forget()
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
    def clear_canvas(self):
        """Clear the visualization canvas"""
        self.canvas.delete("all")
    
    def get_current_word(self):
        """Get the currently entered word"""
        return self.explorer_search_var.get().strip()
    
    def get_current_view_type(self):
        """Get the currently selected view type"""
        return self.view_var.get()
    
    def _on_explore(self):
        """Handle explore button click"""
        if self.controller:
            self.controller.explore_word()
    
    def _on_view_changed(self, event):
        """Handle view type change"""
        if self.controller:
            self.controller.change_visualization_type(self.get_current_view_type())
    
    # Methods for drawing different visualizations
    def draw_word_network(self, nodes, edges):
        """Draw a network of related words"""
        self.clear_canvas()
        self.show_canvas()
        
        # Draw nodes
        node_objects = {}
        for node in nodes:
            x, y = node['position']
            color = node.get('color', AppTheme.PRIMARY)
            
            # Draw circle
            circle_id = self.canvas.create_oval(
                x-20, y-20, x+20, y+20,
                fill=color,
                outline=""
            )
            
            # Draw label
            text_id = self.canvas.create_text(
                x, y,
                text=node['word'],
                fill="white",
                font=AppTheme.BODY_FONT
            )
            
            node_objects[node['id']] = (circle_id, text_id)
        
        # Draw edges
        for edge in edges:
            from_id = edge['from']
            to_id = edge['to']
            
            from_node = next((n for n in nodes if n['id'] == from_id), None)
            to_node = next((n for n in nodes if n['id'] == to_id), None)
            
            if from_node and to_node:
                from_x, from_y = from_node['position']
                to_x, to_y = to_node['position']
                
                # Draw line
                self.canvas.create_line(
                    from_x, from_y, to_x, to_y,
                    width=1,
                    fill=AppTheme.BORDER,
                    dash=(4, 2) if edge.get('dashed', False) else None
                )
        
        return node_objects