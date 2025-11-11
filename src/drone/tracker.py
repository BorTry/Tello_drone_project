from math import sqrt, pow

class tracker:
    def __init__(self, screen_size, drone):
        self.t_width, self.t_height = screen_size
        self.drone = drone

    def get_center_of_object(self, obj):
        """
        Gets the center of an object and returns it
        """
        x, y, w, h = obj
        return (x + (w//2), y + (h//2))
    
    def center_around_point(self, point):
        """
        
        """
        screen_middle = (self.t_width // 2, self.t_height // 2)

        dx = point[0] - screen_middle[0]
        dy = point[1] - screen_middle[1]

        return (dx, dy)

    def get_distance(self, p1, p2):
        return max(sqrt(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2)), 0.001)
    
    def run(self, obj):
        """
        
        """
        if obj is None:
            return

        center_point = self.get_center_of_object(obj)
        dx, dy = self.center_around_point(center_point)
        distance = self.get_distance(center_point, (center_point[0] - dx, center_point[1] - dy))

        self.drone.to(dx, dy, 0, distance/100)