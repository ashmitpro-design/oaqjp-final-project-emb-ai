"""Public interface for the Watson NLP emotion detection package."""

from . import emotion_detection
from .emotion_detection import emotion_detector

__all__ = ["emotion_detection", "emotion_detector"]
