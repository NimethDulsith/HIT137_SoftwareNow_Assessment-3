class HistoryManager:
    
    # CLASS ATTRIBUTE
    max_default_history = 20
    
    def __init__(self, max_history=None):
        """CONSTRUCTOR with default parameter."""
        self.__history = []  # ENCAPSULATION: Private list
        self.__current_index = -1  # ENCAPSULATION: Private index
        self.__max_history = max_history if max_history else HistoryManager.max_default_history
