# Grading corrections

The supplied grading feedback marks Questions 3, 5, 7, 10, and 11 as failed.
Questions 1, 2, 4, 6, 8, 9, 12, 13, 14, 15, and 16 were marked passed.

## Question 10: corrected deployment code

The final server explicitly imports the detector from its application module,
uses Flask route decorators for `/` and `/emotionDetector`, reads
`textToAnalyze`, returns all five scores and the dominant emotion, and runs
with `app.run(host="0.0.0.0", port=5000)`. Blank-input handling remains
`Invalid input! Try again.` without calling the detector. The full code is in
`6a_server` and `6a_server.txt`; paste the code itself into Question 10.

The unit tests still pass and Pylint remains 10.00/10. A grading outcome cannot
be guaranteed; the earlier Question 10 feedback did not identify a precise
code defect.

## Questions 3, 5, 7, and 11: live service blocked

New genuine calls were attempted, including the required exact import and an
angry sample. The evidence now shows the actual project root and the commands
executed. All live results remain unavailable; these are not passing prediction
evidence and should not be resubmitted expecting a different result.

Network diagnostics found that the course hostname resolves to private
10.241.0.50 and 10.241.64.14 addresses. A public IBM HTTP request succeeded,
but the course POST timed out. No endpoint override is configured. The request
uses the course URL, raw_document.text payload, and English emotion model ID.
See `watson_network_diagnostics.txt` for the actual diagnostic output.

Run `python tools/capture_live_evidence.py` in a course lab checkout that can
reach the service. It writes the exact module import, actual path, and real
happy/angry predictions to the three evidence files. It reports failure if
scores are unavailable or the angry sample does not produce anger.

Then start `python server.py`, open the port 5000 preview, analyze a sentence,
and save a genuine successful page screenshot as `6b_deployment_test.png`.
The existing screenshot still shows the unavailable-service state.

## Preserved passing behavior

The detector and its HTTP 400 handling, package exports, unit-test assertions,
blank-input wording, and blank-input screenshot remain unchanged. No mocked
test values are presented as live Watson output. No lint checks were disabled.
