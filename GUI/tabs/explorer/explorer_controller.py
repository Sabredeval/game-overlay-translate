import threading
from GUI.common.app_theme import AppTheme

class ExplorerController:
    def __init__(self, view, word_service, dictionary_controller=None):
        self.view = view
        self.view.set_controller(self)
        self.word_service = word_service
        self.dictionary_controller = dictionary_controller
        self.current_word = None
        self.current_view_type = "Word Network"
    
    def explore_word(self):
        word = self.view.get_current_word()
        if not word:
            return
        
        self.current_word = word
        self.current_view_type = self.view.get_current_view_type()
        
        threading.Thread(
            target=self._fetch_word_data,
            args=(word, self.current_view_type),
            daemon=True
        ).start()
    
    def change_visualization_type(self, view_type):
        if self.current_word and view_type != self.current_view_type:
            self.current_view_type = view_type
            self.view.update_visualization_title(view_type)
            
            threading.Thread(
                target=self._fetch_word_data,
                args=(self.current_word, view_type),
                daemon=True
            ).start()
    
    def _fetch_word_data(self, word, view_type):
        try:
            if view_type == "Word Network":
                data = self._generate_network_data(word)
            elif view_type == "Etymology Tree":
                data = self._generate_etymology_data(word)
            elif view_type == "Word Family":
                data = self._generate_family_data(word)
            else:  # Semantic Field
                data = self._generate_semantic_data(word)
            
            self.view.after(0, lambda: self._update_visualization(view_type, data))
                
        except Exception as e:
            self.view.after(0, lambda: self._handle_error(str(e)))
    
    def _update_visualization(self, view_type, data):
        if view_type == "Word Network":
            self.view.draw_word_network(data['nodes'], data['edges'])
    
    def _handle_error(self, error_message):
        self.view.show_placeholder()
        print(f"Error exploring word: {error_message}")
    
    def _generate_network_data(self, word):
        return {
            'nodes': [
                {'id': 0, 'word': word, 'position': (250, 150), 'color': AppTheme.PRIMARY},
                {'id': 1, 'word': f"syn1-{word}", 'position': (150, 80), 'color': AppTheme.PRIMARY},
                {'id': 2, 'word': f"syn2-{word}", 'position': (350, 80), 'color': AppTheme.PRIMARY},
                {'id': 3, 'word': f"ant1-{word}", 'position': (150, 220), 'color': AppTheme.ACCENT},
                {'id': 4, 'word': f"rel1-{word}", 'position': (350, 220), 'color': AppTheme.PRIMARY_DARK}
            ],
            'edges': [
                {'from': 0, 'to': 1},
                {'from': 0, 'to': 2},
                {'from': 0, 'to': 3, 'dashed': True},
                {'from': 0, 'to': 4}
            ]
        }
    
    def _generate_etymology_data(self, word):
        return self._generate_network_data(word)
    
    def _generate_family_data(self, word):
        return self._generate_network_data(word)
    
    def _generate_semantic_data(self, word):
        return self._generate_network_data(word)