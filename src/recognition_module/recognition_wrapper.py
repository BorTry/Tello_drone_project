import cv2

class recognition_wrapper:
    def __init__(self, init_func, get_image_func, processing_func, detection, classes=[], run_once=False, name="webcam"):
        self.init_val = init_func

        self.gen = generator(get_image_func, self.init_val, run_once)

        self.next = get_image_func
        self.proc = processing_func

        self.det = detection

        self.classes = classes
        self.name = name

    def run(self):
        pass

    def draw(self, detection_objects, frame):
        match(len(detection_objects)):
            case 4: # bare x, y, w og h verdier.
                for (x, y, w, h) in detection_objects:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            case 6: # inneholder alle hjørner, sikkerhets verdier og 
                for (x1,y1,x2,y2,cls,score) in detection_objects:
                    cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
                    cv2.putText(frame, f"{self.classes[cls]} {score:.2f}", (x1, max(15, y1-7)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
            case _: # du har fucket opp no ass
                print("???")
                pass
        
        cv2.imshow(self.name, frame)

    def __get_image(self, ):
        pass

def generator(gen_func, gen_val, run_once):
    def wrap(): 
        return gen_func() if not run_once else gen_val
    
    return wrap

class recognition_wrapper:
    def __init__(self, init_func, get_image_func, processing_func, cascade, run_once=False, name="webcam"):
        self.init_func = init_func
        self.name = name

        self.generator = init_func()
        self.run_once = run_once

        self.next = get_image_func
        self.processing = processing_func

        self.cascade = cascade

    def run(self):
        cap = generator(self.init_func, self.generator, self.run_once)

        ok, frame = self.next(cap)

        if not ok:
            return False

        return self.processing(frame, self)

def main():
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    def image_proc(frame, wrap):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = wrap.cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,     # image pyramid step
            minNeighbors=5,      # higher = fewer (more confident) detections
            minSize=(40, 40)     # ignore tiny detections
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow(wrap.name, frame)

    cam = recognition_wrapper(lambda:cv2.VideoCapture(1, cv2.CAP_AVFOUNDATION), lambda cap: cap.read(), image_proc, face_cascade)

    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        cam.run()

main()