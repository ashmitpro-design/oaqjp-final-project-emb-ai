"""Capture genuine live results from the actual project root for Q3, Q5, Q7."""

from contextlib import redirect_stderr, redirect_stdout
import io
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def capture(filename, text, expected=None):
    """Execute the displayed statements and record their real printed output."""
    stream = io.StringIO()
    namespace = {}
    commands = [
        "from EmotionDetection.emotion_detection import emotion_detector",
        "print('Application module import: PASS')",
        f"result = emotion_detector({text!r})",
        "print(result)",
    ]
    with redirect_stdout(stream), redirect_stderr(stream):
        print("$ pwd")
        print(Path.cwd())
        if str(ROOT).replace("\\", "/") != "/home/project/final_project":
            print("Runtime note: this is the actual local project root, not the course's Linux lab path.")
        print(f"Python interpreter: {sys.executable}")
        for command in commands:
            print(f">>> {command}")
            exec(command, namespace)
        result = namespace["result"]
        numeric = all(isinstance(result[key], (int, float)) for key in (
            "anger", "disgust", "fear", "joy", "sadness"))
        passed = numeric and result["dominant_emotion"] is not None
        if expected:
            passed = passed and result["dominant_emotion"] == expected
        print("Live verification: " + ("PASS" if passed else "BLOCKED: no required live prediction obtained"))
    output = stream.getvalue()
    for suffix in ("", ".txt"):
        (ROOT / "evidence" / (filename + suffix)).write_text(output, encoding="utf-8")
    print(output, flush=True)
    return passed


if __name__ == "__main__":
    os.chdir(ROOT)
    outcomes = [
        capture("2b_application_creation", "I am so happy I am doing this."),
        capture("3b_formatted_output_test", "I am glad this happened"),
        capture("4b_packaging_test", "I am very angry and furious", "anger"),
    ]
    sys.exit(0 if all(outcomes) else 1)
