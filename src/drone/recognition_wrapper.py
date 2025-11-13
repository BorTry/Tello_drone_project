import cv2

def generator(gen_func, gen_val, run_once):
    def wrap(): 
        return gen_func() if not run_once else gen_val
    
    return wrap

class recognition_wrapper:
    def __init__(self, init_func, get_image_func, processing_func, detection_func, run_once=False, name="webcam", draw=True, reuse_value=False):
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
        - draw: wether or not to draw rectangles around faces
        - reuse_value: wether to give the previous result back to the detection function. given as an int, for how many values the detection function returns
        """
        self.init_val = init_func()

        self.gen = generator(init_func, self.init_val, run_once)

        self.next = get_image_func
        self.proc = processing_func

        self.det = detection_func

        self.name = name
        self.draw_on_image = draw
        self.reuse_value = reuse_value

        self.last_frame = None
        self.unproccesed_frame = None
        self.result = None if not reuse_value else [0 for _ in range(reuse_value)]

    def run(self):
        cap = self.gen() # get the capture function

        ok, col_frame = self.next(cap) # get the next frame from the capture function

        if not ok:
            return False

        self.unproccesed_frame = col_frame.copy()

        frame = self.proc(col_frame) # process image

        if not self.reuse_value:
            self.result = self.det(frame) # run detection function

        if self.reuse_value:
            result = self.det(frame, self.result) # run detection function

            self.result = self.result if result is None else result
        
        if self.draw_on_image:
            self.draw(self.result, col_frame) # standard draw function
            cv2.imshow(self.name, col_frame)
        else:
            self.last_frame = frame

    def draw(self, detection_objects, frame):
        if (len(detection_objects) > 0):
            match(len(detection_objects[0])):
                case 4: # bare x, y, w og h verdier.
                    index = 0
                    index_largest, mw, mh = 0, 0, 0

                    for (x, y, w, h) in detection_objects:
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                        if w * h > mw * mh:
                            index_largest = index
                            mw, mh = w, h

                        index += 1
                
                    x, y, w, h = detection_objects[index_largest]
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    cv2.circle(frame, (x + (w//2), y + (h//2)), 5, (0, 0, 255))

                case 6: # inneholder alle hjørner, classification og sikkerhets verdier
                    for (x1,y1,x2,y2,cls,score) in detection_objects:
                        cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
                        cv2.putText(frame, f"{self.classes[cls]} {score:.2f}", (x1, max(15, y1-7)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

        self.last_frame = frame

    def show_frame(self):
        if not (self.last_frame is None):
            cv2.imshow(self.name, self.last_frame)

    def get_dominant_object(self, objects):
        """
        Returns the dominante object in a list of detection objects
        """

        if (objects is None or len(objects) == 0):
            return None
        
        largest_index = 0
        mw, mh = objects[0][2], objects[0][3] # max width and height 

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

    def get_image(self):
        return self.last_frame
    
    def get_unproc_image(self):
        return self.unproccesed_frame
    
    def get_result(self):
        return self.result