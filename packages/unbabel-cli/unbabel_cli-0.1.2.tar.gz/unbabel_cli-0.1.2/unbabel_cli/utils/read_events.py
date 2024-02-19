import json
from datetime import datetime
from pathlib import Path
from typing import List

from unbabel_cli.utils.interfaces import RawTranslationEvent, TranslationEvent


def read_event(path_of_file: Path) -> List[TranslationEvent]:

    raw_event = None
    if path_of_file.name.endswith(".json"):
        raw_event = read_json(path_of_file)
    if path_of_file.name.endswith(".jsonl"):
        raw_event = read_jsonl(path_of_file)

    if raw_event is None:
        raise ValueError("Invalid file format")

    return [parse_event(event) for event in raw_event]


def parse_event(event: RawTranslationEvent) -> TranslationEvent:
    event["timestamp"] = datetime.strptime(event["timestamp"], "%Y-%m-%d %H:%M:%S.%f")
    event["nr_words"] = int(event["nr_words"])
    event["duration"] = int(event["duration"])
    return event


def read_json(path_of_file: Path) -> List[RawTranslationEvent]:
    with open(path_of_file, encoding="utf-8") as f:
        data = json.load(f)
    return data


def read_jsonl(path_of_file: Path) -> List[RawTranslationEvent]:
    data = []
    with open(path_of_file, encoding="utf-8") as f:
        for line in f:
            data.append(json.loads(line))
    return data
