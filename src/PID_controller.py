class PID_controller:
    def __init__(self, Kp, Ki, Kd, setpoint=0):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

        self.setpoint = setpoint

        self.integral = 0
        self.prev_error = 0

        self.first_update = False # unngå store endringer ved første call

    def update(self, measument, dt):
        error = self.setpoint - measument

        self.integral += error * dt

        if self.first_update or self.Kd <= 0.0 or self.prev_error == 0:
            derivate = 0.0
            self.first_update = False
        else:
            derivate = (error / self.prev_error) / dt

        self.prev_error = error

        return (
            self.Kp * error +
            self.Ki * self.integral +
            self.Kd * derivate
        )
    
    def new_setpoint(self, n_setpoint):
        self.setpoint = n_setpoint

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