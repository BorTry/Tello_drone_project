class event_listener:
    """
    Basic event listener
    """
    def __init__(self, event_name:str, event_code:int, check_func=None):
        """
        Basic event listener.

        required:
        - event_name : name of the event.
        - event_code : code for the event.
    
        optional:
        - check_func: function which describes if the listener should trigger
        """
        self.name = event_name
        self.type = event_code

        self.check_func = check_func

    def is_same(self, event_code:int):
        return event_code == self.type
    
    def check(self, *args):
        return self.check_func(*args) if self.check_func else True