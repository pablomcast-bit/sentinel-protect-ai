from datetime import datetime

from config import FPS

from modules.recorder import Recorder


class EventEngine:

    def __init__(self):

        self.recorder = Recorder()

        self.recording = False

        self.photo_path = None

        self.video_path = None

    # =====================================
    # INICIAR EVENTO
    # =====================================

    def start(self, frame, zone):

        if self.recording:

            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        photo_name = f"{zone}_{timestamp}.jpg"

        video_name = f"{zone}_{timestamp}.avi"

        self.photo_path = self.recorder.save_photo(

            frame,

            photo_name

        )

        self.recorder.start_video(

            video_name,

            frame,

            FPS

        )

        self.recording = True

        print(f"🚨 EVENTO EN {zone}")

        print(f"📷 {photo_name}")

        print(f"🎥 {video_name}")

    # =====================================
    # GRABAR
    # =====================================

    def update(self, frame):

        if self.recording:

            self.recorder.write(frame)

    # =====================================
    # FINALIZAR
    # =====================================

    def stop(self):

        if not self.recording:

            return

        self.video_path = self.recorder.stop()

        self.recording = False

        print("✅ Evento finalizado")