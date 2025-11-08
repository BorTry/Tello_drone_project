class event_listener:
    """
    Basic event listener for pygame events
    """
    def __init__(self, event_name:str, event_code:int, check_func=None):
        """
        Basic event listener for pygame events.

        required:
        - event_name : Name of the event.
        - event_code : Code for the event. A pygame event.
    
        optional:
        - check_func: Function which describes if the listener should trigger
            - required:
                - component: Every component that can trigger on the event
        """
        self.name = event_name
        self.type = event_code

        self.check_func = check_func

    def is_same(self, event_code:int):
        return event_code == self.type
    
    def check(self, *args):
        return self.check_func(*args) if self.check_func else True