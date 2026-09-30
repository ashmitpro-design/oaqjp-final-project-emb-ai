"""Save genuine subprocess output and source excerpts for assignment evidence."""

import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"


def record(filename, arguments, extra_env=None):
    """Record a command's actual merged terminal output and exit status."""
    environment = {**os.environ, "PYLINTHOME": str(ROOT / ".pylint.d"),
                   **(extra_env or {})}
    result = subprocess.run(
        [sys.executable, *arguments], cwd=ROOT, env=environment,
        capture_output=True, text=True, encoding="utf-8", errors="replace", check=False,
    )
    command = subprocess.list2cmdline(["python", *arguments])
    output = (f"$ {command}\n" + result.stdout + result.stderr
              + f"\nExit code: {result.returncode}\n")
    (EVIDENCE / filename).write_text(output, encoding="utf-8")
    print(output, flush=True)
    return result.returncode


def main():
    """Run local checks, optionally including real Watson integration tests."""
    EVIDENCE.mkdir(exist_ok=True)
    for filename, source in {
        "2a_emotion_detection.txt": "EmotionDetection/emotion_detection.py",
        "3a_output_formatting.txt": "EmotionDetection/emotion_detection.py",
        "4a_packaging.txt": "EmotionDetection/__init__.py",
        "5a_unit_testing.txt": "test_emotion_detection.py",
        "6a_server.txt": "server.py",
        "7a_error_handling_function.txt": "EmotionDetection/emotion_detection.py",
        "7b_error_handling_server.txt": "server.py",
        "8a_server_modified.txt": "server.py",
    }.items():
        prefix = "" if filename == "6a_server.txt" else f"Source: {source}\n\n"
        (EVIDENCE / filename).write_text(
            prefix + (ROOT / source).read_text(encoding="utf-8"),
            encoding="utf-8",
        )
    (EVIDENCE / "6a_server").write_text(
        (ROOT / "server.py").read_text(encoding="utf-8"), encoding="utf-8")
    record("4c_import_smoke_test.txt", ["-c",
           "from EmotionDetection import emotion_detector; "
           "import EmotionDetection.emotion_detection; "
           "print('Package and module imports: PASS'); "
           "print('Blank input:', emotion_detector(''))"])
    tests = record("5b_unit_testing_result.txt", ["-m", "unittest", "-v",
                   "test_emotion_detection"], {"RUN_WATSON_LIVE_TESTS": "0"})
    lint = record("8b_static_code_analysis.txt", ["-m", "pylint", "server.py"])
    live_tests = 0
    live_evidence = 0
    if "--live" in sys.argv:
        live_evidence = record("live_evidence_run.txt", ["tools/capture_live_evidence.py"])
        live_tests = record("5c_live_unit_testing_result.txt", ["-m", "unittest", "-v",
                            "test_emotion_detection.WatsonLiveTests"],
                            {"RUN_WATSON_LIVE_TESTS": "1"})
    return bool(tests or lint or live_tests or live_evidence)


if __name__ == "__main__":
    sys.exit(main())
