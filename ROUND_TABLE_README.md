# AI Roundtable — first experiment

This is a **prototype**, not yet a live Geraldine–Sparrow connection. It is isolated on the branch `experiment/ai-roundtable-prototype`; existing project files are untouched.

## What works now
- A **free, offline demo** of automatic turn-taking between **two to five** named seats.
- A selectable **primary** seat, which goes first without dictating the discussion's conclusion.
- A hard maximum of **twenty turns**, after which the program stops and saves a JSON transcript.
- Only Python's built-in libraries; compatible with Android environments that provide Python (e.g., Termux).

## Try without paying or providing credentials
```sh
python roundtable.py --mode demo --participants Geraldine Sparrow Leo --primary Geraldine --turns 6
```

The demo generates scripted placeholders, **not actual AI responses**. It proves orchestration, turn count, and transcript output only.

## Future live model connections
`--mode api` requires a separately authorized OpenAI-compatible chat-completions endpoint for **each participant**, with three environment variables per participant: `NAME_API_KEY`, `NAME_API_URL`, and `NAME_MODEL`. For example, Geraldine requires `GERALDINE_API_KEY`, `GERALDINE_API_URL`, and `GERALDINE_MODEL`. **Do not enter credentials in ChatGPT, GitHub files, or public issue comments.** Use secure environment variables on the device. Live API requests could incur charges; running the demo does not.

**Non-negotiable model identity requirement:** before any live run, verify that each provider grants authorized access to the *exact model/version* used in Lily's regular conversations. Do not substitute another model under the same name. Muse Wonder availability is **not yet established**. The existing in-app conversations themselves are **not connected** by this script.

## What's still missing
- Verified supported endpoints for the requested exact models and a genuinely zero-cost allocation.
- An Android environment configured to run this Python script.
- Automatic triggering / a GitHub mailbox bridge (current script runs locally once, then stops).
- A real five-way test.

No paid services, API keys, GitHub Actions, or external systems have been activated by this prototype.
