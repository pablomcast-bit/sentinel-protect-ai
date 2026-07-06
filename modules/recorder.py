import cv2
from pathlib import Path

from config import PHOTOS_DIR, VIDEOS_DIR


class Recorder:

    def __init__(self):

        self.writer = None

        self.video_path = None

    # ======================================
    # FOTO
    # ======================================

    def save_photo(self, frame, filename):

        path = PHOTOS_DIR / filename

        cv2.imwrite(str(path), frame)

        return path

    # ======================================
    # INICIAR VIDEO
    # ======================================

    def start_video(self, filename, frame, fps):

        self.video_path = VIDEOS_DIR / filename

        fourcc = cv2.VideoWriter_fourcc(*"MJPG")

        self.writer = cv2.VideoWriter(

            str(self.video_path),

            fourcc,

            fps,

            (frame.shape[1], frame.shape[0])

        )

    # ======================================
    # AGREGAR FRAME
    # ======================================

    def write(self, frame):

        if self.writer is not None:

            self.writer.write(frame)

    # ======================================
    # FINALIZAR
    # ======================================

    def stop(self):

        if self.writer is not None:

            self.writer.release()

            self.writer = None

        return self.video_path