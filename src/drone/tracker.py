from drone.PID_controller import PID_controller, deadzone, angle_error

FACE_OPTIMAL_SIZE = (320, 320) # 50cm
FACE_ASSUMED_DISTANCE = 50 # cm
OPTIMAL_AREA = 102400

FACE_WANTED_DISTANCE = 200

class tracker:
    def __init__(self, screen_size, drone, dt):
        self.t_width, self.t_height = screen_size
        self.drone = drone

        self.x_contr = PID_controller(0.04, 0.1, dt) # left right
        self.y_contr = PID_controller(0.2, 0.01, dt) # for back
        self.z_contr = PID_controller(0.05, 0.01, dt) # up down
        self.yaw_contr = PID_controller(4, 0.01, dt, setpoint=FACE_WANTED_DISTANCE)

    def get_center_of_object(self, obj):
        """
        Gets the center of an object and returns it
        """
        x, y, w, h = obj
        return (x + (w//2), y + (h//2))
    
    def center_around_point(self, point):
        """
        
        """
        screen_middle = (self.t_width // 2, (self.t_height // 2))

        dx = screen_middle[0] - point[0]
        dy = screen_middle[1] - point[1]

        return (dx, dy)
    
    def get_distance_to_face(self, obj):
        """
        estimates the distance between a face and the camera
        """
        _, _ , w, h = obj

        area = w * h
        
        return (OPTIMAL_AREA / area) * FACE_ASSUMED_DISTANCE

    def run(self, obj, yaw):
        """
        
        """
        if obj is None:
            return

        center_point = self.get_center_of_object(obj)
        dx, dz = self.center_around_point(center_point) # measured face left, right, up and down
        dy = self.get_distance_to_face(obj) # measured distance to face

        print(dy)

        x_vel = deadzone(self.x_contr.update(dx))
        y_vel = deadzone(self.y_contr.update(dy))
        z_vel = deadzone(self.z_contr.update(dz))

        n_yaw = deadzone(self.yaw_contr.update(angle_error(self.yaw_contr.setpoint, yaw)))
        
        self.drone.rc(x_vel, -y_vel, -z_vel, n_yaw)