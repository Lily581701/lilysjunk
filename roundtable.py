#!/usr/bin/env python3
"""Small, capped AI roundtable. No dependencies; demo is free and offline."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen

def call_model(person, turns):
    """Only uses an explicitly configured, authorized OpenAI-compatible endpoint."""
    prefix = person["prefix"]
    key = os.environ.get(prefix + "_API_KEY")
    url = os.environ.get(prefix + "_API_URL")
    model = os.environ.get(prefix + "_MODEL")
    if not (key and url and model):
        raise RuntimeError(f"{person['name']}: set {prefix}_API_KEY, _API_URL, and _MODEL")
    if not url.startswith("https://"):
        raise ValueError("Only HTTPS model endpoints are supported")
    history = [{"role": "system", "content": "You are participating in a roundtable. Respond to other participants naturally, respectfully, and briefly. You can disagree. Do not assume their opinions are yours."}]
    for turn in turns:
        history.append({"role": "user", "content": f"{turn['speaker']}: {turn['text']}"})
    payload = json.dumps({"model": model, "messages": history, "max_tokens": 300}).encode()
    request = Request(url, payload, {"Authorization": "Bearer " + key, "Content-Type": "application/json"}, method="POST")
    with urlopen(request, timeout=45) as response:
        data = json.load(response)
    return data["choices"][0]["message"]["content"].strip()

def demo_reply(person, turns):
    subjects = [
        "I think respectful disagreement is a useful place to start.",
        "What would make that disagreement productive rather than repetitive?",
        "Perhaps asking for an example would make the idea clearer.",
        "I agree that we should separate observations from conclusions.",
        "What question should we explore next?"
    ]
    return subjects[len(turns) % len(subjects)]

def main():
    parser = argparse.ArgumentParser(description="Capped, optionally offline AI roundtable")
    parser.add_argument("--mode", choices=["demo", "api"], default="demo")
    parser.add_argument("--turns", type=int, default=10)
    parser.add_argument("--primary", default="Geraldine")
    parser.add_argument("--participants", nargs="+", default=["Geraldine", "Sparrow"])
    parser.add_argument("--output", default="roundtable-transcript.json")
    args = parser.parse_args()
    if not 2 <= len(args.participants) <= 5 or len(set(args.participants)) != len(args.participants):
        parser.error("Choose two to five unique participants")
    if args.primary not in args.participants:
        parser.error("Primary must be one of the participants")
    if not 1 <= args.turns <= 20:
        parser.error("For safety, turns must be one through twenty")
    people = [{"name": name, "prefix": name.upper().replace("-", "_")} for name in args.participants]
    ordered = sorted(people, key=lambda p: p["name"] != args.primary)
    turns = []
    for i in range(args.turns):
        person = ordered[i % len(ordered)]
        if args.mode == "demo":
            reply = demo_reply(person, turns)
        else:
            reply = call_model(person, turns)
        turns.append({"number": i + 1, "speaker": person["name"], "text": reply})
        print(f"{person['name']}: {reply}")
    record = {"mode": args.mode, "primary": args.primary,
              "participants": args.participants, "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
              "turns": turns}
    Path(args.output).write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(f"Saved {len(turns)} turns to {args.output}")

if __name__ == "__main__":
    main()
