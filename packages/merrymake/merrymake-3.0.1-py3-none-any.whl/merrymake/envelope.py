import json
from dataclasses import dataclass

@dataclass
class Envelope:
    messageId: str
    traceId: str
    sessionId: str
