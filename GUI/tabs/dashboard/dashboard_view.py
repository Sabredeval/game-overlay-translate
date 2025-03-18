import tkinter as tk
from tkinter import ttk
from GUI.common.app_theme import AppTheme

class DashboardView(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.controller = None
        
        self.stat_values = {
            "total_words": tk.StringVar(value="0"),
            "words_to_learn": tk.StringVar(value="0"),
            "learning_streak": tk.StringVar(value="0 days"),
            "words_mastered": tk.StringVar(value="0"),
            "review_due": tk.StringVar(value="0"),
            "last_activity": tk.StringVar(value="Never")
        }

        self.recommendation_frames = []
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.study_tab = self.create_study_dashboard_tab()
        self.notebook.add(self.study_tab, text="Study Dashboard")
    
    def set_controller(self, controller):
        self.controller = controller
    
    def create_study_dashboard_tab(self):
        tab = ttk.Frame(self.notebook)
        
        summary_frame = ttk.LabelFrame(tab, text="Learning Summary")
        summary_frame.pack(fill=tk.X, padx=10, pady=10)
        
        stats_grid = ttk.Frame(summary_frame)
        stats_grid.pack(fill=tk.X, padx=20, pady=10)
        
        stats_data = [
            ("Total Words", self.stat_values["total_words"]),
            ("Words to Learn", self.stat_values["words_to_learn"]),
            ("Learning Streak", self.stat_values["learning_streak"]),
            ("Words Mastered", self.stat_values["words_mastered"]),
            ("Review Due", self.stat_values["review_due"]),
            ("Last Activity", self.stat_values["last_activity"])
        ]
        
        for i, (label, var) in enumerate(stats_data):
            row, col = i // 3, i % 3
            
            stat_frame = ttk.Frame(stats_grid, padding=10)
            stat_frame.grid(row=row, column=col, padx=10, pady=5, sticky="nsew")
            
            ttk.Label(stat_frame, text=label, font=AppTheme.SMALL_FONT).pack(anchor=tk.W)
            ttk.Label(stat_frame, textvariable=var, font=AppTheme.HEADING_FONT).pack(anchor=tk.W)
        
        for i in range(2):
            stats_grid.rowconfigure(i, weight=1)
        for i in range(3):
            stats_grid.columnconfigure(i, weight=1)
        
        charts_frame = ttk.Frame(tab)
        charts_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        progress_frame = ttk.LabelFrame(charts_frame, text="Learning Progress")
        progress_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.progress_canvas = tk.Canvas(progress_frame, background="white", height=200)
        self.progress_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        placeholder_text = ttk.Label(self.progress_canvas, text="Progress chart will appear here", 
                                   background="white")
        placeholder_text.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        categories_frame = ttk.LabelFrame(charts_frame, text="Word Categories")
        categories_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.categories_canvas = tk.Canvas(categories_frame, background="white", height=200)
        self.categories_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        placeholder_text2 = ttk.Label(self.categories_canvas, text="Category distribution will appear here", 
                                    background="white")
        placeholder_text2.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        recommendations_frame = ttk.LabelFrame(tab, text="Learning Recommendations")
        recommendations_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.recommendations_container = ttk.Frame(recommendations_frame)
        self.recommendations_container.pack(fill=tk.X, padx=10, pady=10)
        
        for i in range(3):
            rec_frame = ttk.Frame(self.recommendations_container, padding=10)
            rec_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            title_label = ttk.Label(rec_frame, text="Coming soon", font=AppTheme.HEADING_FONT)
            title_label.pack(fill=tk.X)
            
            desc_label = ttk.Label(rec_frame, text="Personalized recommendations will appear here based on your learning progress", wraplength=200)
            desc_label.pack(fill=tk.X, pady=5)
            
            action_button = ttk.Button(rec_frame, text="Explore")
            action_button.pack(pady=5)
            
            self.recommendation_frames.append({
                "frame": rec_frame,
                "title": title_label,
                "description": desc_label,
                "button": action_button
            })
        
        return tab
    
    def update_statistics(self, stats):
        self.stat_values["total_words"].set(str(stats.get("total_words", 0)))
        self.stat_values["words_to_learn"].set(str(stats.get("words_to_learn", 0)))
        self.stat_values["learning_streak"].set(str(stats.get("learning_streak", "0 days")))
        self.stat_values["words_mastered"].set(str(stats.get("words_mastered", 0)))
        self.stat_values["review_due"].set(str(stats.get("review_due", 0)))
        self.stat_values["last_activity"].set(str(stats.get("last_activity", "Never")))