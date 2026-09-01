from pathlib import Path
#Project directory
BASE_DIR = Path(__file__).resolve().parent
#Input video
VIDEO_PATH = "static/videos/traffic.mp4"
#ML model
MODEL_PATH = BASE_DIR / "models" / "congestion_model.pkl"
#Database
DATABASE_PATH = BASE_DIR / "traffic.db"
#YOLO model
YOLO_MODEL = "yolo11n.pt"
#vehicle classes from COCD 
VEHICLE_CLASSES ={1: "car", 
                  2: "truck",
                    3: "bus",
                      4: "motorcycle"}
#Detection confidence
CONFIDENCE_THRESHOLD = 0.40
#Traffic-density limits 
LOW_LIMIT = 5
MEDIUM_LIMIT = 15
HIGH_LIMIT = 30
#Signal limits
MIN_GREEN_TIME = 15
MAX_GREEN_TIME = 90