# Emotion Detector

[Public repository](https://github.com/ashmitpro-design/oaqjp-final-project-emb-ai)

An IBM Coursera-style final project built from scratch with Python, Flask, and
the Watson NLP EmotionPredict REST service. It returns anger, disgust, fear,
joy, sadness, and the highest-scoring `dominant_emotion`.

## Verified status

- Package and module imports pass.
- 16 offline unit tests pass. These use explicitly synthetic HTTP fixtures and
  verify request construction, parsing, dominant emotion selection, failures,
  and Flask routes. They do **not** prove model predictions.
- Five separate live integration tests were attempted and failed because the
  Watson service was unreachable from this machine. The direct HTTP probe
  returned `ConnectTimeout`; no successful service response was obtained.
- Pylint reports **10.00/10** for `server.py`, without disabled checks or a custom
  scoring formula.
- Real Microsoft Edge browser checks pass for the page, service-unavailable
  message, empty/whitespace validation, and mobile layout. Blank submissions
  send no analysis request. No JavaScript errors were detected.
- `evidence/6b_deployment_test.png` shows the actual unavailable-service state, **not a
  successful prediction**. `evidence/7c_error_handling_interface.png` shows blank-input
  validation. Both are unmodified browser screenshots.

Full original command outputs and code excerpts are in [evidence](evidence/).
The [assignment field guide](evidence/ASSIGNMENT_FIELDS.md) collects the exact
code excerpts and actual outputs by activity.

## Setup and run

Requires Python 3.10 or newer; verified with Python 3.13 on Windows.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe server.py
```

Open http://127.0.0.1:5000. Enter an English sentence and select **Analyze
emotions**. The page preserves your input and displays all five scores and the
dominant emotion when Watson returns a valid result.

On Linux/macOS, replace `.\.venv\Scripts\python.exe` with `.venv/bin/python`.
For the Skills Network Cloud IDE, expose Flask using the lab's port preview:

```sh
python -m flask --app server run --host=0.0.0.0 --port=5000
```

## Watson integration and documentation

The implementation was checked against IBM's current primary documentation:

- [IBM Watson NLP Emotion REST API](https://www.ibm.com/docs/en/watson-libraries?topic=catalog-emotion)
  documents the `EmotionPredict` path, English model ID, `raw_document.text`
  input, and `emotionPredictions[].emotion` response.
- [IBM's public course starter](https://github.com/ibm-developer-skills-network/oaqjp-final-project-emb-ai)
  establishes the `templates` and `static` structure. Its public README does not
  contain endpoint instructions; the authenticated current lab instructions
  were not supplied for this project.
- [IBM course overview](https://www.coursera.org/learn/python-project-for-ai-application-development)
  identifies the Emotion Detector final project and its testing, error handling,
  and static analysis activities.

The standard course service URL implemented here is:

```text
https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict
```

The IBM API documentation verifies the REST path and schema, but does not
guarantee availability of this Skills Network hostname outside the course lab.
The actual request uses:

```text
grpc-metadata-mm-model-id: emotion_aggregated-workflow_lang_en_stock
```

```json
{"raw_document": {"text": "your input text"}}
```

The course endpoint uses a model-selection header, not an IBM Cloud NLU API
key. No secrets are included. `WATSON_EMOTION_URL` optionally selects a
course-provided replacement endpoint with the same REST contract; do not put
credentials into its URL. The project does not substitute a heuristic model
or sample predictions when Watson is unavailable.

## Python interface and error behavior

```python
from EmotionDetection import emotion_detector

result = emotion_detector("I am glad this happened")
print(result)
```

On success the dictionary preserves the service's five numerical scores and
adds `dominant_emotion`, selected with `max`. Ties use the first emotion in
the order anger, disgust, fear, joy, sadness.

HTTP 400, other non-200 responses, connection failures, invalid JSON, missing
fields, and invalid scores return:

```python
{
    "anger": None,
    "disgust": None,
    "fear": None,
    "joy": None,
    "sadness": None,
    "dominant_emotion": None,
}
```

Blank or non-string function input returns that structure without an HTTP call.
The web page and Flask route validate blank input before calling the detector.

`GET /emotionDetector?textToAnalyze=...` returns the course-style readable
summary as `text/plain`. Missing or whitespace input returns HTTP 400 with
`Invalid input! Try again.` A nonblank request with unavailable results
returns HTTP 503 with a service-unavailable message. Text is rendered using
`textContent`, so user input is not interpreted as HTML.

## Tests and genuine evidence

```powershell
.\.venv\Scripts\python.exe -m unittest -v test_emotion_detection
.\.venv\Scripts\python.exe -m pylint server.py
.\.venv\Scripts\python.exe tools\verify_project.py
```

The default test run executes 16 offline tests and explicitly skips the five
network-dependent tests. To run those real tests in a network environment that
can reach the course endpoint:

```powershell
$env:RUN_WATSON_LIVE_TESTS = "1"
.\.venv\Scripts\python.exe -m unittest -v test_emotion_detection.WatsonLiveTests
```

On Linux/macOS:

```sh
RUN_WATSON_LIVE_TESTS=1 python -m unittest -v test_emotion_detection.WatsonLiveTests
```

Live samples cover joy, anger, disgust, sadness, and fear. An unreachable
service causes an explicit failure, not a fabricated pass. To regenerate live
command evidence, use `python tools/verify_project.py --live` and
`python tools/probe_watson.py`.

Browser verification requires Microsoft Edge and the additional dependency:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe tools\verify_browser.py
```

Stop any existing server on port 5000 first. The script starts and stops its
own Flask server, drives a real headless Edge browser without mocks, and saves
both required screenshots in `evidence/`. If Watson remains unavailable,
the deployment screenshot correctly records that limitation. To capture them
manually, start `server.py`, open the page, submit a sentence, and save a full
browser screenshot as `evidence/6b_deployment_test.png`; then clear the field,
select Analyze emotions, and save `evidence/7c_error_handling_interface.png`.

## Structure

```text
EmotionDetection/
    __init__.py
    emotion_detection.py
templates/index.html
static/style.css
static/mywebscript.js
server.py
test_emotion_detection.py
requirements.txt
requirements-dev.txt
tools/
    verify_project.py
    probe_watson.py
    verify_browser.py
evidence/
    6b_deployment_test.png
    7c_error_handling_interface.png
```

## Repository isolation

The workspace previously contained Git metadata for Paradise Nursery. Its
`main` branch and `origin` remote are preserved. Emotion Detector is prepared
on an independent `emotion-detector` branch with no inherited project files
or history, and is published to a separate repository. Use the explicitly
named Emotion Detector remote for subsequent pushes.

```sh
git push coursera HEAD:main
```
