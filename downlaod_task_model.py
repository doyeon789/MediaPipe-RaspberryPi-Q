import urllib.request
import os

# 현재 스크립트 위치 기준으로 절대 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")

# 폴더 생성
os.makedirs(MODELS_DIR, exist_ok=True)
print(f"저장 경로: {MODELS_DIR}")

# 모델 다운로드
url = "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/latest/pose_landmarker_lite.task"
save_path = os.path.join(MODELS_DIR, "pose_landmarker_lite.task")

print("모델 다운로드 중...")
urllib.request.urlretrieve(url, save_path)
print(f"다운로드 완료: {save_path}")