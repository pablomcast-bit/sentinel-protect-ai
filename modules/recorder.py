import cv2
from collections import deque

from config import (
    PHOTOS_DIR,
    VIDEOS_DIR,
    BUFFER_SIZE
)


class Recorder:

    def __init__(self):

        self.writer = None

        self.video_path = None

        # Buffer circular
        self.buffer = deque(maxlen=BUFFER_SIZE)

    # =====================================
    # AGREGAR FRAME AL BUFFER
    # =====================================

    def update_buffer(self, frame):

        self.buffer.append(frame.copy())

    # =====================================
    # FOTO
    # =====================================

    def save_photo(self, frame, filename):

        path = PHOTOS_DIR / filename

        cv2.imwrite(str(path), frame)

        return path

    # =====================================
    # INICIAR VIDEO
    # =====================================

    def start_video(self, filename, frame, fps):

        self.video_path = VIDEOS_DIR / filename

        fourcc = cv2.VideoWriter_fourcc(*"MJPG")

        self.writer = cv2.VideoWriter(

            str(self.video_path),

            fourcc,

            fps,

            (frame.shape[1], frame.shape[0])

        )

        # ==========================
        # ESCRIBIR BUFFER
        # ==========================

        for img in self.buffer:

            self.writer.write(img)

    # =====================================
    # ESCRIBIR FRAME
    # =====================================

    def write(self, frame):

        if self.writer:

            self.writer.write(frame)

    # =====================================
    # FINALIZAR
    # =====================================

    def stop(self):

        if self.writer:

            self.writer.release()

            self.writer = None

        return self.video_path