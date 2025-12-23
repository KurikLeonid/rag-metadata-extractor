from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


def normalize(tag: str) -> str:
    return " ".join(tag.strip().lower().split())


@dataclass
class Taxonomy:
    # canonical -> stats
    counts: Dict[str, int] = field(default_factory=dict)
    # alias -> canonical
    aliases: Dict[str, str] = field(default_factory=dict)

    def add_tags(self, tags: List[str]) -> List[str]:
        canonical_tags: List[str] = []
        for t in tags:
            nt = normalize(t)
            if not nt:
                continue

            canonical = self.aliases.get(nt, nt)
            self.counts[canonical] = self.counts.get(canonical, 0) + 1
            canonical_tags.append(canonical)

        # unique but keep order
        seen = set()
        out = []
        for t in canonical_tags:
            if t not in seen:
                seen.add(t)
                out.append(t)
        return out

    def add_alias(self, alias: str, canonical: str) -> None:
        self.aliases[normalize(alias)] = normalize(canonical)
