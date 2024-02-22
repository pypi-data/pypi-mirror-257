import time
from threading import Thread
import cv2

class RTSPVideoWriterObject(object):
    def __init__(self, src=0, output_path_name="output.avi"):
        # Create a VideoCapture object
        self.capture = cv2.VideoCapture(src)

        # Default resolutions of the frame are obtained (system dependent)
        self.frame_width = int(self.capture.get(3))
        self.frame_height = int(self.capture.get(4))

        # Set up codec and output video settings
        self.codec = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
        self.output_video = cv2.VideoWriter(output_path_name, self.codec, 30, (
        self.frame_width, self.frame_height))

        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        self.record_in_progress = False

    def update(self):
        # Read the next frame from the stream in a different thread
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()

    def show_frame(self):
        # Display frames in main program
        if self.status:
            cv2.imshow('frame', self.frame)

        # Press Q on keyboard to stop recording
        key = cv2.waitKey(1)
        if key == ord('q'):
            self.capture.release()
            self.output_video.release()
            cv2.destroyAllWindows()
            exit(1)

    def save_frame(self):
        # Save obtained frame into video output file
        self.output_video.write(self.frame)

    def start_record(self):
        self.record_in_progress = True
        while self.record_in_progress:
            try:
                self.save_frame()
            except AttributeError:
                pass

    def stop_record(self):
        self.record_in_progress = False

if __name__ == '__main__':
    rtsp_stream_link = 'rtsp://admin:Assa+123@192.168.60.110:554/Streaming/Channels/101'
    video_stream_widget = RTSPVideoWriterObject(src=rtsp_stream_link)
    Thread(target=video_stream_widget.start_record).start()
    time.sleep(15)
    video_stream_widget.stop_record()
