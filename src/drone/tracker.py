from math import sqrt, pow

DX_DY_CLAMPS = (-10, 10)
SCALAR = 5

HEIGHT_OFFSET = 200 # px
FACE_OPTIMAL_SIZE = (320, 320) # 50cm
FACE_ASSUMED_DISTANCE = 50 # cm
OPTIMAL_AREA = 102400

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
        screen_middle = (self.t_width // 2, (self.t_height // 2) + HEIGHT_OFFSET)

        dx = max(min((screen_middle[0] - point[0]) // SCALAR, DX_DY_CLAMPS[1]), DX_DY_CLAMPS[0])
        dy = max(min((screen_middle[1] - point[1]) // SCALAR, DX_DY_CLAMPS[1]), DX_DY_CLAMPS[0])

        return (dx, dy)
    
    def get_distance_to_face(self, obj):
        """
        estimates the distance between a face and the camera
        """
        _, _ , w, h = obj

        area = w * h
        
        return (OPTIMAL_AREA / area) * FACE_ASSUMED_DISTANCE
    
    def run(self, obj):
        """
        
        """
        if obj is None:
            return

        center_point = self.get_center_of_object(obj)
        dx, dz = self.center_around_point(center_point)
        dy = (FACE_ASSUMED_DISTANCE - self.get_distance_to_face(obj)) // (SCALAR * 4)
        
        self.drone.rc(-dx, -dy, dz, 0)