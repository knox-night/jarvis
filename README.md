# JARVIS AI

JARVIS AI is a lightweight personal assistant project designed to evolve into a voice-first, cloud-connected productivity assistant for Windows PCs and Android devices.

This repository is the initial foundation for the system: a modular Python backend with a provider-independent AI interface, memory management, and a voice-service skeleton.

## Goals

- Keep the project free and lightweight.
- Put the AI brain in the cloud.
- Keep the PC-side agent minimal.
- Make the AI provider replaceable.
- Build the foundations before adding complex voice or automation features.

## Architecture

The project is organized around these core concerns:

- Frontend / client layer: future Windows and Android interfaces.
- Backend: FastAPI service for chat, memory, and orchestration.
- AI provider: abstract interface with mock and Google Gemini implementations.
- Memory system: persistent user-controlled memory store.
- Voice system: STT/TTS service layer for future voice features.
- Action engine: future integrations for email, tasks, and PC automation.

## Quick start

1. Open a terminal in this folder.
2. Create a virtual environment if desired.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the API:

```bash
python -m jarvis.main
```

5. Visit:

- http://localhost:8000/health
- http://localhost:8000/docs

## AI provider design

The AI layer is intentionally abstracted.

- `AIProvider` is the shared contract.
- `MockAIProvider` is used by default for local development.
- `GeminiProvider` uses Google's official `google-genai` SDK and the `gemini-3.6-flash` model.

This makes it easy to switch providers without rewriting the application.

To enable Gemini, copy `.env.example` to `.env`, then set `JARVIS_PROVIDER=gemini` and add your API key to `GOOGLE_API_KEY` in `.env`. Keep `.env` private; it is excluded by `.gitignore`. Restart the API after changing settings. Gemini sends chat messages and relevant memory context to Google. Check Google's current pricing and free-tier limits before use; this project does not enable billing.

To run the tests without making a Gemini API request, set `PYTHONPATH=src` and run `python -m pytest -q` from the project folder. The Gemini unit test uses a mock SDK client.

## Memory design

JARVIS stores user-controlled memory in a JSON file by default. This keeps the initial version simple while proving the concept of persistent context and editable memory.

## Voice design

The voice layer is intentionally minimal. The project does not add full voice features yet because the main priority is a reliable text-based foundation.

## Recommended next phases

1. Add secure backend authentication.
2. Add a proper cloud database.
3. Add Windows agent features.
4. Add Android client connectivity.
5. Add scheduled morning briefings and reminders.

## Notes

This is a foundation only. It is intentionally conservative and avoids paid services or large local model downloads.
