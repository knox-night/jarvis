from __future__ import annotations

from pathlib import Path
from typing import Optional


class VoiceService:
    def transcribe_audio(self, audio_path: str | Path) -> str:
        raise NotImplementedError("Speech-to-text integration is not implemented yet.")

    def synthesize_speech(self, text: str, output_path: str | Path) -> str:
        raise NotImplementedError("Text-to-speech integration is not implemented yet.")


class SpeechToTextService(VoiceService):
    def transcribe_audio(self, audio_path: str | Path) -> str:
        raise NotImplementedError("Connect a cloud STT provider such as Google Speech-to-Text to enable this feature.")


class TextToSpeechService(VoiceService):
    def synthesize_speech(self, text: str, output_path: str | Path) -> str:
        raise NotImplementedError("Connect a cloud TTS provider such as Google Text-to-Speech to enable this feature.")
