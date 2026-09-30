"use strict";

const form = document.querySelector("#emotion-form");
const input = document.querySelector("#textToAnalyze");
const output = document.querySelector("#system_response");
const submitted = document.querySelector("#submitted-text");
const button = document.querySelector("#analyze-button");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const text = input.value;
  output.classList.remove("error");
  input.removeAttribute("aria-invalid");
  submitted.hidden = true;
  if (!text.trim()) {
    output.textContent = "Invalid input! Try again.";
    output.classList.add("error");
    input.setAttribute("aria-invalid", "true");
    input.focus();
    return;
  }

  submitted.textContent = `Your text: “${text}”`;
  submitted.hidden = false;
  button.disabled = true;
  output.textContent = "Analyzing your text…";
  output.setAttribute("aria-busy", "true");
  try {
    const query = new URLSearchParams({ textToAnalyze: text });
    const response = await fetch(`/emotionDetector?${query}`);
    output.textContent = await response.text();
    output.classList.toggle("error", !response.ok);
  } catch {
    output.textContent = "Cannot reach the application. Please try again.";
    output.classList.add("error");
  } finally {
    button.disabled = false;
    output.removeAttribute("aria-busy");
  }
});
