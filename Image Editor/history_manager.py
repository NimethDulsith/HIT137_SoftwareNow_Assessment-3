
class HistoryManager:
    
    
    # CLASS ATTRIBUTE
    max_default_history = 20
    
    def __init__(self, max_history=None):
        """CONSTRUCTOR with default parameter."""
        self.__history = []  # ENCAPSULATION: Private list
        self.__current_index = -1  # ENCAPSULATION: Private index
        self.__max_history = max_history if max_history else HistoryManager.max_default_history
    
    # PROPERTY DECORATORS
    @property
    def current_index(self):
        """PROPERTY: Get current history index."""
        return self.__current_index
    
    @property
    def history_size(self):
        """PROPERTY: Get total history size."""
        return len(self.__history)
    
    def save_state(self, image):
        """Save current image state to history."""
        if image is None:
            return
        
        self.__history = self.__history[:self.__current_index + 1]
        self.__history.append(image.copy())
        self.__current_index += 1
        
        if len(self.__history) > self.__max_history:
            self.__history.pop(0)
            self.__current_index -= 1
    
    def undo(self):
        """Go back to previous state."""
        if self.can_undo():
            self.__current_index -= 1
            return self.__history[self.__current_index].copy()
        return None
    
    def redo(self):
        """Go forward to next state."""
        if self.can_redo():
            self.__current_index += 1
            return self.__history[self.__current_index].copy()
        return None
    
    def can_undo(self):
        """Check if undo is possible."""
        return self.__current_index > 0
    
    def can_redo(self):
        """Check if redo is possible."""
        return self.__current_index < len(self.__history) - 1
    
    def clear_history(self):
        """Clear all history."""
        self.__history = []
        self.__current_index = -1
    
    # MAGIC METHODS
    def __len__(self):
        """
        MAGIC METHOD: len(history_manager)
        Returns number of states in history
        """
        return len(self.__history)
    
    def __str__(self):
        """String representation for users."""
        return f"History: {len(self.__history)} states, at index {self.__current_index}"
    
    def __repr__(self):
        """String representation for developers."""
        return f"HistoryManager(size={len(self.__history)}, index={self.__current_index})"
    
    def __bool__(self):
        """Boolean conversion - True if has history."""
        return len(self.__history) > 0
    
    def __getitem__(self, index):
        """
        MAGIC METHOD: Allow indexing
        Example: history[0] returns first state
        """
        if 0 <= index < len(self.__history):
            return self.__history[index].copy()
        raise IndexError("History index out of range")
    
    def __contains__(self, item):
        """
        MAGIC METHOD: Check if state exists
        Example: if image in history_manager
        """
        return item in self.__history
