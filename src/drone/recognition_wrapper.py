import cv2

def generator(gen_func, gen_val, run_once):
    def wrap(): 
        return gen_func() if not run_once else gen_val
    
    return wrap

class recognition_wrapper:
    def __init__(self, init_func, get_image_func, processing_func, detection_func, run_once=False, name="webcam"):
        """
        Creates a wrapper for cv2 detection

        required:
        - init_func: Function for getting the capturing instance (camera, image)
        - get_image_func: Function for extracting the image from the capturing instance.
            - input:
                - capturing instance.
            - output:
                - boolean if the data got successfully returned.
                - image.
        - processing_func: 
            - input:
                - image.
            - output:
                - processed image.
        - detection_func: 
            - input:
                - processed image.
            - output:
                - detected objects. (The top left, and size) optionally confidence score and label

        optional:
        - run_once: If the init_func only has to run once or every iteration
        - name: The name for the wrapper
        """
        self.init_val = init_func()

        self.gen = generator(init_func, self.init_val, run_once)

        self.next = get_image_func
        self.proc = processing_func

        self.det = detection_func

        self.name = name

    def run(self):
        cap = self.gen() # få tak i capture function

        ok, col_frame = self.next(cap) # hent frem neste frame gjennom next funksjonen

        if not ok:
            return False

        frame = self.proc(col_frame) # prosesser bilder

        detection_objects = self.det(frame) # finn objekter i bilde 

        self.draw(detection_objects, col_frame) # tegn på rektangler for hvert objekt

    def draw(self, detection_objects, frame):
        if (len(detection_objects) > 0):
            match(len(detection_objects[0])):
                case 4: # bare x, y, w og h verdier.
                    for (x, y, w, h) in detection_objects:
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                case 6: # inneholder alle hjørner, classification og sikkerhets verdier
                    for (x1,y1,x2,y2,cls,score) in detection_objects:
                        cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
                        cv2.putText(frame, f"{self.classes[cls]} {score:.2f}", (x1, max(15, y1-7)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
        
        cv2.imshow(self.name, frame)

    def get_dominant_object(objects):
        """
        Returns the dominante object in a list of detection objects
        """
        if (len(objects) == 0):
            return None
        
        largest_index = 0
        mw, mh = largest_index[2], largest_index[3] # max width and height 

        for index in range(len(objects)):
            x, y, w, h = objects[index]

            if w * h > mw * mh:
                largest_index = index
                mw, mh = w, h

        return objects[largest_index]
    
    def stop(self):
        cap = self.gen()

        if hasattr(cap, "release") and callable(cap.release):
            cap.release()
        elif hasattr(cap, "close") and callable(cap.close):
            cap.close()
        elif hasattr(cap, "stop") and callable(cap.stop):
            cap.stop()