"""
convert_to_onnx.py
pose_landmarks_detector.tflite → ONNX 변환 + onnxsim 최적화
(pose_detector는 tf2onnx reshape 오류로 제외)
main/ 폴더에서 실행 → ../models/ 에 저장
"""
import subprocess
import sys
import os


def convert(tflite_path: str, output_path: str = None):
    if not os.path.exists(tflite_path):
        print(f"❌ 파일 없음: {tflite_path}")
        return False

    if output_path is None:
        output_path = tflite_path.replace(".tflite", ".onnx")

    print(f"\n{'='*50}")
    print(f"변환 시작: {tflite_path}")
    print(f"출력 경로: {output_path}")
    print(f"{'='*50}")

    # Step 1: tflite → onnx (tf2onnx)
    cmd = [
        sys.executable, "-m", "tf2onnx.convert",
        "--tflite", tflite_path,
        "--output", output_path,
        "--opset", "13",
    ]
    print("\n[1/2] tf2onnx 변환 중...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("❌ 변환 실패:")
        print(result.stderr)
        return False

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"✅ ONNX 변환 완료: {output_path} ({size_mb:.2f} MB)")

    # Step 2: onnxsim 최적화
    sim_path = output_path.replace(".onnx", "_sim.onnx")
    print(f"\n[2/2] onnxsim 최적화 중...")
    try:
        import onnxsim
        import onnx
        model = onnx.load(output_path)
        model_sim, check = onnxsim.simplify(model)
        if check:
            onnx.save(model_sim, sim_path)
            size_mb = os.path.getsize(sim_path) / (1024 * 1024)
            print(f"✅ 최적화 완료: {sim_path} ({size_mb:.2f} MB)")
        else:
            print("⚠️  onnxsim 검증 실패 — 원본 onnx 사용하세요")
    except Exception as e:
        print(f"⚠️  onnxsim 오류: {e}")
        print("   원본 onnx 파일은 정상입니다. 계속 진행 가능합니다.")

    return True


if __name__ == "__main__":
    # main/ 에서 실행 기준 → ../models
    MODEL_DIR = "../models"

    # pose_detector는 tf2onnx 변환 불가 (내부 reshape 오류)
    # pose_landmarks_detector 하나만으로 전체 이미지 입력 추론 가능
    files = [
        "pose_landmarks_detector.tflite",
    ]

    success = []
    for f in files:
        tflite_path = os.path.join(MODEL_DIR, f)
        onnx_path   = os.path.join(MODEL_DIR, f.replace(".tflite", ".onnx"))
        ok = convert(tflite_path, onnx_path)
        if ok:
            success.append(f)

    print(f"\n{'='*50}")
    print(f"완료: {len(success)}/{len(files)}개 변환 성공")
    print("\n생성된 파일:")
    for f in files:
        for suffix in [".onnx", "_sim.onnx"]:
            out = os.path.join(MODEL_DIR, f.replace(".tflite", suffix))
            if os.path.exists(out):
                size_mb = os.path.getsize(out) / (1024 * 1024)
                print(f"  ✅ {out} ({size_mb:.2f} MB)")