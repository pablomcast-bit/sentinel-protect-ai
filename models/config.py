from pathlib import Path

# ==========================================
# RUTAS DEL PROYECTO
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

MODELS_DIR = BASE_DIR / "models"

MEDIA_DIR = BASE_DIR / "media"

PHOTOS_DIR = MEDIA_DIR / "photos"

VIDEOS_DIR = MEDIA_DIR / "videos"

FACES_DIR = MEDIA_DIR / "faces"

EMBEDDINGS_DIR = MEDIA_DIR / "embeddings"

LOGS_DIR = BASE_DIR / "logs"

# ==========================================
# MODELOS
# ==========================================

YOLO_MODEL = MODELS_DIR / "yolov8n.pt"

# ==========================================
# CÁMARA
# ==========================================

CAMERA_INDEX = 0

FRAME_WIDTH = 640

FRAME_HEIGHT = 480

FPS = 20

# ==========================================
# BUFFER DE VIDEO
# ==========================================

BUFFER_SECONDS = 10

BUFFER_SIZE = FPS * BUFFER_SECONDS

# ==========================================
# DETECCIÓN
# ==========================================

PERSON_CONFIDENCE = 0.40

START_THRESHOLD = 3

STOP_THRESHOLD = 10

# ==========================================
# FIREBASE
# ==========================================

FIREBASE_KEY = BASE_DIR / "firebase-key.json"