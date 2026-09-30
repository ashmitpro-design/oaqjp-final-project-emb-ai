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
    output = (f"$ python {' '.join(arguments)}\n" + result.stdout + result.stderr
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
        (EVIDENCE / filename).write_text(
            f"Source: {source}\n\n" + (ROOT / source).read_text(encoding="utf-8"),
            encoding="utf-8",
        )
    record("4b_packaging_test.txt", ["-c",
           "from EmotionDetection import emotion_detector; "
           "import EmotionDetection.emotion_detection; "
           "print('Package and module imports: PASS'); "
           "print('Blank input:', emotion_detector(''))"])
    tests = record("5b_unit_testing_result.txt", ["-m", "unittest", "-v",
                   "test_emotion_detection"], {"RUN_WATSON_LIVE_TESTS": "0"})
    lint = record("8b_static_code_analysis.txt", ["-m", "pylint", "server.py"])
    live_tests = 0
    if "--live" in sys.argv:
        record("2b_application_creation.txt", ["-c",
               "from EmotionDetection.emotion_detection import emotion_detector; "
               "print('Application module import: PASS'); "
               "print('Live call: I am so happy I am doing this.'); "
               "print(emotion_detector('I am so happy I am doing this.'))"])
        (EVIDENCE / "3b_formatted_output_test.txt").write_text(
            (EVIDENCE / "2b_application_creation.txt").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        live_tests = record("5c_live_unit_testing_result.txt", ["-m", "unittest", "-v",
                            "test_emotion_detection.WatsonLiveTests"],
                            {"RUN_WATSON_LIVE_TESTS": "1"})
    return bool(tests or lint or live_tests)


if __name__ == "__main__":
    sys.exit(main())
