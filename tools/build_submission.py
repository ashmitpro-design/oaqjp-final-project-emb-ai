"""Assemble copy-ready submission fields directly from source and real evidence."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://github.com/ashmitpro-design/emotion-detector/blob/main/"
FIELDS = (
    ("README URL", "README.md", "url"),
    ("Emotion detection application code", "evidence/2a_emotion_detection.txt", "python"),
    ("Application import and real execution", "evidence/2b_application_creation.txt", "text"),
    ("Formatted emotion detection code", "evidence/3a_output_formatting.txt", "python"),
    ("Actual formatted output", "evidence/3b_formatted_output_test.txt", "text"),
    ("Package __init__.py URL", "EmotionDetection/__init__.py", "url"),
    ("Package validation output", "evidence/4b_packaging_test.txt", "text"),
    ("Complete unit test code", "evidence/5a_unit_testing.txt", "python"),
    ("Actual unit test results", "evidence/5b_unit_testing_result.txt", "text"),
    ("Complete Flask server code", "evidence/6a_server.txt", "python"),
    ("Deployment screenshot", "evidence/6b_deployment_test.png", "image"),
    ("HTTP 400 handling code", "evidence/7a_error_handling_function.txt", "python"),
    ("Flask blank-input handling code", "evidence/7b_error_handling_server.txt", "python"),
    ("Blank-input screenshot", "evidence/7c_error_handling_interface.png", "image"),
    ("Final server code for static analysis", "evidence/8a_server_modified.txt", "python"),
    ("Actual Pylint command and result", "evidence/8b_static_code_analysis.txt", "text"),
)


def main():
    """Keep code excerpts and terminal results identical to their evidence files."""
    lines = [
        "# Emotion Detector: Questions 1-16",
        "",
        "Numbering follows the supplied activity/evidence order. No separate question wording was supplied.",
        "",
        "Repository: https://github.com/ashmitpro-design/emotion-detector",
        "",
        "**Live-service limitation:** Watson could not be reached (ConnectTimeout). "
        "The five live tests failed; 16 offline tests passed. HTTP fixtures in offline "
        "tests are explicitly synthetic. The deployment screenshot shows the genuine "
        "unavailable-service message, not a successful prediction.",
        "",
        "All code excerpts are the completed implementation captured during verification; "
        "no earlier incomplete version is presented as the final source.",
        "",
    ]
    for number, (title, path, kind) in enumerate(FIELDS, start=1):
        lines.extend([f"## Question {number}: {title}", "", f"[{path}]({BASE}{path})", ""])
        if kind == "url":
            lines.extend([BASE + path, ""])
        elif kind == "image":
            lines.extend([f"![{title}]({path.removeprefix('evidence/')})", ""])
            if number == 11:
                lines.extend(["This is real Flask deployment evidence; live emotion inference remains blocked.", ""])
        else:
            content = (ROOT / path).read_text(encoding="utf-8")
            if kind == "python":
                content = content.split("\n\n", 1)[1]
            lines.extend([f"```{kind}", content.rstrip(), "```", ""])
    lines.extend([
        "## Additional live verification",
        "",
        f"[Actual network probe]({BASE}evidence/watson_live_probe.txt)",
        f"[Five real integration-test failures]({BASE}evidence/5c_live_unit_testing_result.txt)",
        f"[Real browser verification]({BASE}evidence/6c_browser_verification.txt)",
        "",
        "To finish live verification, run the project in your course Skills Network lab "
        "or a network with access to the course service. Run the opt-in live tests and "
        "recapture the deployment screenshot after receiving a genuine prediction. "
        "See README.md for exact commands.",
        "",
    ])
    target = ROOT / "evidence" / "ASSIGNMENT_FIELDS.md"
    target.write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated {target.relative_to(ROOT)} from actual source and evidence.")


if __name__ == "__main__":
    main()
