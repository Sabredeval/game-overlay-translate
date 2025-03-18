import threading

class DashboardController:
    def __init__(self, view, db_manager):
        self.view = view
        self.view.set_controller(self)
        self.db_manager = db_manager
        
        self.load_dashboard_data()
    
    def load_dashboard_data(self):
        threading.Thread(target=self._fetch_dashboard_data, daemon=True).start()
    
    def _fetch_dashboard_data(self):
        try:
            stats = self._get_vocabulary_statistics()
            self.view.after(0, lambda: self.view.update_statistics(stats))
        except Exception as e:
            self.view.after(0, lambda: print(f"Dashboard data error: {e}"))
    
    def _get_vocabulary_statistics(self):
        stats = {
            "total_words": 0,
            "words_to_learn": 0,
            "learning_streak": "0 days",
            "words_mastered": 0,
            "review_due": 0,
            "last_activity": "Never"
        }
        
        if self.db_manager:
            # TODO - get data from database
            try:
                word_count = self.db_manager.count_words()
                stats["total_words"] = word_count
            except:
                pass
                
        return stats