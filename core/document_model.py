from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

DocumentType = Literal["text", "table", "tree"]


@dataclass(slots=True)
class DocumentObject:
    """Unified intermediate representation for all parsed inputs."""

    type: DocumentType
    content: Any
    metadata: dict[str, Any] = field(default_factory=dict)
