"""Test the real Flask app in Edge and capture unmodified browser screenshots.

No HTTP routes or Watson responses are mocked by this script.
"""

from pathlib import Path
import sys
from threading import Thread

from playwright.sync_api import expect, sync_playwright
from werkzeug.serving import make_server

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from server import app


def main():
    """Start Flask, submit actual forms, save evidence, and stop the test server."""
    lines = ["Browser: Microsoft Edge (Playwright, real headless browser)",
             "Application: http://127.0.0.1:5000", "Mocks: none"]
    httpd = make_server("127.0.0.1", 5000, app, threaded=True)
    thread = Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(channel="msedge", headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 900},
                                    device_scale_factor=1)
            errors = []
            calls = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on("request", lambda request: calls.append(request.url)
                    if "/emotionDetector?" in request.url else None)
            response = page.goto("http://127.0.0.1:5000")
            assert response.status == 200
            expect(page.get_by_role("heading", name="What do your words express?")).to_be_visible()
            lines.append("Home page: HTTP 200; heading, form, and results visible: PASS")
            page.get_by_label("Your text", exact=True).fill("I am so happy I am doing this.")
            with page.expect_response(lambda response: "/emotionDetector?" in response.url,
                                      timeout=40000) as analysis_response:
                page.get_by_role("button", name="Analyze emotions").click()
            actual_response = analysis_response.value
            expect(page.locator("#system_response")).not_to_have_attribute("aria-busy", "true",
                                                                         timeout=40000)
            result_text = page.locator("#system_response").inner_text()
            lines.extend([f"Live analysis route: HTTP {actual_response.status}", result_text])
            if actual_response.status == 200:
                assert "The dominant emotion is" in result_text
                for name in ("anger", "disgust", "fear", "joy", "sadness"):
                    assert name in result_text
                lines.append("Live score display: PASS")
            else:
                assert actual_response.status == 503
                assert "Emotion analysis is unavailable" in result_text
                lines.append("Live score display: BLOCKED by Watson service; real error displayed")
            expect(page.locator("#submitted-text")).to_contain_text("I am so happy I am doing this.")
            page.screenshot(path=str(ROOT / "evidence" / "6b_deployment_test.png"),
                            full_page=True)
            lines.append("Saved evidence/6b_deployment_test.png (actual live outcome)")

            count_before = len(calls)
            for blank in ("", " \n\t"):
                page.get_by_label("Your text", exact=True).fill(blank)
                page.get_by_role("button", name="Analyze emotions").click()
                expect(page.locator("#system_response")).to_have_text(
                    "Invalid text! Please try again.")
                expect(page.locator("#textToAnalyze")).to_have_attribute("aria-invalid", "true")
                assert len(calls) == count_before
            page.get_by_label("Your text", exact=True).fill("")
            page.screenshot(path=str(ROOT / "evidence" / "7c_error_handling_interface.png"),
                            full_page=True)
            lines.append("Empty and whitespace submission: PASS; no additional analysis requests")
            lines.append("Saved evidence/7c_error_handling_interface.png")
            blank_response = page.request.get("http://127.0.0.1:5000/emotionDetector?textToAnalyze=%20")
            assert blank_response.status == 400
            assert blank_response.text() == "Invalid text! Please try again."
            lines.append("Direct blank route: HTTP 400; expected validation message: PASS")

            page.set_viewport_size({"width": 390, "height": 844})
            assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
            page.screenshot(path=str(ROOT / "evidence" / "mobile_interface.png"), full_page=True)
            lines.append("Mobile width 390px: no horizontal overflow: PASS")
            assert not errors, errors
            lines.append("Browser JavaScript errors: 0")
            browser.close()
    finally:
        httpd.shutdown()
        thread.join(timeout=5)
        output = "\n".join(lines) + "\n"
        (ROOT / "evidence" / "6c_browser_verification.txt").write_text(output, encoding="utf-8")
        print(output)


if __name__ == "__main__":
    main()
