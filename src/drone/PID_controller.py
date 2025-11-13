from math import pi

U_MIN = -60
U_MAX = 60

class PID_controller:
    def __init__(self, Kp:float, Ki:float, dt, u_min=U_MIN, u_max=U_MAX, i_min=None, i_max=None, setpoint:float=0):
        """
        PID controller

        required:

        - kp: Proportional k factor
        - ki: Integrator k factor
        - dt: Time differation between each update

        optional:

        - u_min: Minimum value for the output of the controller
        - u_max: Maximum value for the output of the controller
        - i_min: Minimum value for the input of the controller
        - i_max: Maximum value for the input of the controller
        - setpoint: Target value you want the controller to get to, defaults to 0
        """

        self.Kp = Kp
        self.Ki = Ki
        self.dt = dt

        self.setpoint = setpoint

        self.integral = 0

        self.i_min = i_min if i_min is not None else u_min
        self.i_max = i_max if i_max is not None else u_max
        self.u_max = u_max
        self.u_min = u_min

    def update(self, measurement):
        e = self.setpoint - measurement

        # Integrate with clamping (anti-windup)
        self.integral += e * self.dt
        if self.integral > self.i_max:
            self.integral = self.i_max
        elif self.integral < self.i_min:
            self.integral = self.i_min

        u = self.Kp * e + self.Ki * self.integral

        return max(min(u, self.u_max), self.u_min)
    
    def new_setpoint(self, n_setpoint):
        self.setpoint = n_setpoint

def angle_error(setpoint, measurement):
    """
    Wrap a measurement to [-pi, pi]
    """
    e = setpoint - measurement
    e = (e + pi) % (2 * pi) - pi
    return e

def deadzone(u, thresh=5):
    """
    Filters out the values that are smaller than the threshold
    """
    return 0 if abs(u) < thresh else int(u)


if __name__ == "__main__":
    import time
    pid = PID_controller(Kp=1.0, Ki=0.3, Kd=0.05, setpoint=10.0)

    measurement = 0.0
    last_time = time.time()

    for _ in range(30):
        now = time.time()
        dt = now - last_time
        last_time = now

        control = pid.update(measurement, dt)

        # toy process: move measurement toward control a bit
        measurement += 0.2 * (control - measurement)

        print(f"meas={measurement:.2f}, control={control:.2f}")
        time.sleep(0.1)