import os
import cv2

class Camera(object):
    def __init__(self, path=None):
    
        if path is not None:
            assert(os.path.isfile(path))

        inp = path or 0
        self.video = cv2.VideoCapture(inp)
    
    def __del__(self):
        
        if self.video is not None:
            self.video.release()
    
    def get_frame(self):
        image = self.read_video()

        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def take_picture(self):
        '''Use video to take a picture.'''

        image = self.read_video()
        return image

    def read_video(self):
        
        success, image = self.video.read()
        if not success: raise Exception('Failure reading video...')

        return image        

def save_picture(img, path=None):
    '''save jpg to file.'''

    fn = path or 'face.jpg'
    cv2.imwrite(fn, img)
