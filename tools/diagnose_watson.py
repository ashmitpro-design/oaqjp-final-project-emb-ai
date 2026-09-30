"""Check course-service connectivity without printing credentials or proxy URLs."""

import os
from pathlib import Path
import platform
import socket
import sys
from urllib.parse import urlsplit

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from EmotionDetection.emotion_detection import DEFAULT_URL, MODEL_ID

lines = [f"Runtime: {platform.system()} / Python {platform.python_version()}",
         f"Actual project root: {ROOT}", f"Course URL: {DEFAULT_URL}",
         f"Model header: grpc-metadata-mm-model-id: {MODEL_ID}",
         'Payload: {"raw_document": {"text": "I am glad this happened"}}',
         f"Endpoint override configured: {bool(os.environ.get('WATSON_EMOTION_URL'))}"]
host = urlsplit(DEFAULT_URL).hostname
try:
    addresses = sorted({entry[4][0] for entry in socket.getaddrinfo(host, 443)})
    lines.append(f"DNS resolution: {', '.join(addresses)}")
except OSError as error:
    lines.append(f"DNS resolution failed: {type(error).__name__}")

for label, url, method in (
    ("Public internet control", "https://www.ibm.com", "GET"),
    ("Course EmotionPredict", DEFAULT_URL, "POST"),
):
    try:
        kwargs = {"timeout": (10, 30)}
        if method == "POST":
            kwargs.update(headers={"grpc-metadata-mm-model-id": MODEL_ID},
                          json={"raw_document": {"text": "I am glad this happened"}})
        response = requests.request(method, url, **kwargs)
        lines.append(f"{label}: HTTP {response.status_code}")
    except requests.RequestException as error:
        lines.append(f"{label}: {type(error).__name__}; no successful response")

output = "\n".join(lines) + "\n"
(ROOT / "evidence" / "watson_network_diagnostics.txt").write_text(output, encoding="utf-8")
print(output)
