import logging

from picamera import PiCamera

class Camera:
    def __init__(self):
        self.camera = PiCamera()

        self.camera.resolution = (1920, 1080)
        self.camera.framerate = 30
        self.camera.sensor_mode = 1
        self.camera.shutter_speed = 0
        self.camera.exposure_mode = 'sports'
        self.camera.drc_strength = 'medium'
        self.camera.meter_mode = 'matrix'

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.camera.close()

    def start_recording(self, filename='test.h264'):
        logging.info('Start recording...')
        self.camera.start_recording(filename, format='h264', level='4.2', bitrate=17000000, quality=20)

    def stop_recording(self):
        logging.info('Stop recording...')
        if self.camera.recording:
            self.camera.stop_recording()

    def start_preview(self):
        self.camera.start_preview()
        self.camera.preview_fullscreen = True

    def stop_preview(self):
        if self.camera.previewing:
            self.camera.stop_preview()