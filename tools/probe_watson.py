"""Record a real course endpoint request without substituting any response."""

from pathlib import Path
import sys

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from EmotionDetection.emotion_detection import DEFAULT_URL, MODEL_ID

lines = ["Live Watson HTTP probe (no mocks)", f"POST {DEFAULT_URL}",
         f"Model: {MODEL_ID}", "Input: I am so happy I am doing this."]
try:
    response = requests.post(
        DEFAULT_URL,
        headers={"grpc-metadata-mm-model-id": MODEL_ID},
        json={"raw_document": {"text": "I am so happy I am doing this."}},
        timeout=(5, 20),
    )
    lines.append(f"HTTP status: {response.status_code}")
    lines.append(f"Content-Type: {response.headers.get('Content-Type', 'unspecified')}")
    if response.status_code == 200:
        lines.append("Actual JSON response:")
        lines.append(response.text)
    else:
        lines.append("No successful emotion response received.")
except requests.RequestException as error:
    lines.append(f"Connection outcome: {type(error).__name__}")
    # Error type is enough; exception text can contain proxy credentials.
    lines.append("No HTTP response received; live prediction could not be verified.")
output = "\n".join(lines) + "\n"
(ROOT / "evidence" / "watson_live_probe.txt").write_text(output, encoding="utf-8")
print(output)
