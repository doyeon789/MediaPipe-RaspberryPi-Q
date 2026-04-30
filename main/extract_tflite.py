import zipfile
from pathlib import Path

# MediaPipe .task 파일에서 내부에 포함된 .tflite 모델을 추출하여
# models 폴더에 저장하는 유틸 스크립트
def extract_tflite(task_filename: str, output_dir: str = "models"):
    

    base_dir = Path(__file__).resolve().parent
    project_root = base_dir.parent
    task_path = project_root / "models" / task_filename
    output_path = project_root / output_dir

    # task 파일 존재 여부 체크 (없으면 즉시 종료)
    if not task_path.exists():
        print(f"파일을 찾을 수 없습니다: {task_path}")
        return []

    # 출력 폴더가 없으면 자동 생성
    output_path.mkdir(parents=True, exist_ok=True)

    # .task 파일은 zip 구조이므로 ZipFile로 내부 탐색
    with zipfile.ZipFile(task_path, "r") as z:

        # 디버깅 목적: task 내부 구성 파일 목록 출력
        print("task 내부 파일 목록:")
        for name in z.namelist():
            print(f"  {name}")

        extracted = []

        # .tflite 모델 파일만 필터링하여 추출
        for name in z.namelist():
            if name.endswith(".tflite"):

                # models 폴더에 동일한 파일명으로 저장
                target_file = output_path / Path(name).name

                # zip 내부 바이너리를 그대로 파일로 저장
                with open(target_file, "wb") as f:
                    f.write(z.read(name))

                extracted.append(str(target_file))
                print(f"추출 완료: {target_file}")

        # tflite 파일이 없을 경우 안내 메시지 출력
        if not extracted:
            print(".tflite 파일을 찾을 수 없습니다.")

        return extracted


if __name__ == "__main__":
    # 실제 실행 엔트리 포인트: 지정된 task 파일에서 tflite 추출 수행
    extract_tflite("pose_landmarker_lite.task")