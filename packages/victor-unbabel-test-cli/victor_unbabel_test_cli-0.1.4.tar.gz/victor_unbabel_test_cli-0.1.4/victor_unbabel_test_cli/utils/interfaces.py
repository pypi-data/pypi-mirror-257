from datetime import datetime
from typing import TypedDict


class RawTranslationEvent(TypedDict):
    timestamp: str
    translation_id: str
    source_language: str
    target_language: str
    client_name: str
    event_name: str
    nr_words: int
    duration: int


class TranslationEvent(RawTranslationEvent):
    timestamp: datetime
