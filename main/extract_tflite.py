# extract_tflite.py
import zipfile
from pathlib import Path


def extract_tflite(task_filename: str, output_dir: str = "models"):
    base_dir = Path(__file__).resolve().parent
    project_root = base_dir.parent

    task_path = project_root / "models" / task_filename
    output_path = project_root / output_dir

    if not task_path.exists():
        print(f"파일을 찾을 수 없습니다: {task_path}")
        return []

    output_path.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(task_path, "r") as z:
        print("task 내부 파일 목록:")
        for name in z.namelist():
            print(f"  {name}")

        extracted = []

        for name in z.namelist():
            if name.endswith(".tflite"):
                target_file = output_path / Path(name).name

                with open(target_file, "wb") as f:
                    f.write(z.read(name))

                extracted.append(str(target_file))
                print(f"추출 완료: {target_file}")

        if not extracted:
            print(".tflite 파일을 찾을 수 없습니다.")

        return extracted


if __name__ == "__main__":
    extract_tflite("pose_landmarker_lite.task")