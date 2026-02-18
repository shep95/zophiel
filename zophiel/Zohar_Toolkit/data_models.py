from dataclasses import dataclass, field
from typing import List, Dict, Any
from enum import Enum
import hashlib
import datetime

class FindingType(Enum):
    API_KEY = "api_key"
    ENDPOINT = "endpoint"
    SUBDOMAIN = "subdomain"
    EMAIL = "email"
    PHONE_NUMBER = "phone_number"
    UUID = "uuid"
    SENSITIVE_DATA = "sensitive_data"
    CRYPTO_WALLET = "crypto_wallet"
    # Add other types as needed

class CorrelationType(Enum):
    CREDENTIAL_REUSE = "CREDENTIAL_REUSE"
    INFRASTRUCTURE_LINK = "INFRASTRUCTURE_LINK"
    PEOPLE_CONNECTION = "PEOPLE_CONNECTION"
    SUPPLY_CHAIN = "SUPPLY_CHAIN"
    TEMPORAL = "TEMPORAL"

class AttackObjective(Enum):
    DATA_ACCESS = "data_access"
    PRIVILEGE_ESCALATION = "privilege_escalation"

class Difficulty(Enum):
    TRIVIAL = "TRIVIAL"
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"

class DetectionRisk(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

@dataclass
class Finding:
    value: str
    type: FindingType
    source_module: str
    target: str
    confidence: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    id: str = field(init=False)

    def __post_init__(self):
        # Create a unique ID based on the content
        h = hashlib.sha256()
        h.update(self.value.encode())
        h.update(self.type.value.encode())
        h.update(self.source_module.encode())
        h.update(self.target.encode())
        self.id = h.hexdigest()

@dataclass
class Relationship:
    type: CorrelationType
    findings: List[Finding]
    description: str
    confidence: float
    impact: str
    
@dataclass
class AttackChain:
    steps: List[Finding]
    entry_point: Finding
    objective: AttackObjective
    difficulty: Difficulty
    detection_risk: DetectionRisk
