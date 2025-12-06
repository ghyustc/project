"""Lightweight extraction helpers for materials descriptors from free text.

The module exposes simple heuristics for pulling out material formulas and
common property/value pairs from literature text without external NLP
dependencies. It intentionally favors transparency over completeness so that it
can serve as a starting point for experimentation.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Sequence


@dataclass
class PropertyMatch:
    """Structured representation of a property extracted from text."""

    name: str
    value: float
    unit: str
    context: str


# Regex patterns for common materials properties.
_PROPERTY_PATTERNS: Sequence[tuple[str, re.Pattern[str]]] = [
    (
        "band_gap",
        re.compile(
            r"band gap(?: energy)?(?:\s+(?:of|for))?.{0,40}?(?:is|=|:)?\s*(?P<value>\d+(?:\.\d+)?)\s*(?P<unit>eV)",
            re.IGNORECASE,
        ),
    ),
    (
        "density",
        re.compile(
            r"density(?:\s+(?:of|for))?.{0,40}?(?:is|=|:)?\s*(?P<value>\d+(?:\.\d+)?)\s*(?P<unit>g/cm3|g\s*cm-3|kg/m3)",
            re.IGNORECASE,
        ),
    ),
    (
        "melting_point",
        re.compile(
            r"melting point.{0,20}?(?:is|=|:|around|about)?\s*(?P<value>\d+(?:\.\d+)?)\s*(?P<unit>K|°C|C)",
            re.IGNORECASE,
        ),
    ),
    (
        "thermal_conductivity",
        re.compile(
            r"thermal conductivity.{0,20}?(?:is|=|:)?\s*(?P<value>\d+(?:\.\d+)?)\s*(?P<unit>W/mK|W\s*m-1\s*K-1)",
            re.IGNORECASE,
        ),
    ),
    (
        "electrical_conductivity",
        re.compile(
            r"electrical conductivity.{0,20}?(?:is|=|:)?\s*(?P<value>\d+(?:\.\d+)?)\s*(?P<unit>S/cm|S/m)",
            re.IGNORECASE,
        ),
    ),
    (
        "youngs_modulus",
        re.compile(
            r"young'?s modulus.{0,20}?(?:is|=|:)?\s*(?P<value>\d+(?:\.\d+)?)\s*(?P<unit>GPa)",
            re.IGNORECASE,
        ),
    ),
    (
        "lattice_parameter",
        re.compile(
            r"(?:lattice parameter|lattice constant).{0,20}?(?:a\s*)?(?:is|=|:)?\s*(?P<value>\d+(?:\.\d+)?)\s*(?P<unit>Å|A|nm)",
            re.IGNORECASE,
        ),
    ),
    (
        "hardness",
        re.compile(
            r"hardness.{0,20}?(?:is|=|:)?\s*(?P<value>\d+(?:\.\d+)?)\s*(?P<unit>GPa|HV)",
            re.IGNORECASE,
        ),
    ),
]

# Heuristic pattern for chemical formulas with at least two element blocks
# (e.g., TiO2, Al2O3, Fe3O4). This is intentionally conservative to avoid
# picking up single-element abbreviations.
_MATERIAL_PATTERN = re.compile(r"\b(?:[A-Z][a-z]?[0-9]*[+-]?){2,}\b")


def _normalize_unit(raw: str) -> str:
    unit = raw.replace(" ", "")
    unit = unit.replace("cm-3", "/cm3")
    unit = unit.replace("m-1K-1", "/mK")
    if unit == "A":
        unit = "Å"
    if unit == "C":
        unit = "°C"
    return unit


def _context_snippet(text: str, start: int, end: int, radius: int = 40) -> str:
    prefix_start = max(start - radius, 0)
    suffix_end = min(end + radius, len(text))
    snippet = text[prefix_start:suffix_end]
    return snippet.strip()


def extract_materials(text: str) -> List[str]:
    """Return unique material formulas discovered in the text."""

    matches = {m.group(0) for m in _MATERIAL_PATTERN.finditer(text)}
    return sorted(matches)


def extract_properties(text: str) -> List[PropertyMatch]:
    """Return property/value matches based on predefined regex patterns."""

    found: list[PropertyMatch] = []
    for name, pattern in _PROPERTY_PATTERNS:
        for match in pattern.finditer(text):
            value = float(match.group("value"))
            unit = _normalize_unit(match.group("unit"))
            context = _context_snippet(text, match.start(), match.end())
            found.append(PropertyMatch(name=name, value=value, unit=unit, context=context))
    return found


def extract_descriptors(text: str) -> dict:
    """Extract materials and key property descriptors from raw text."""

    materials = extract_materials(text)
    properties = extract_properties(text)
    return {
        "materials": materials,
        "properties": [asdict(p) for p in properties],
    }


def _read_source(text: str | None, file_path: Path | None) -> str:
    if text:
        return text
    if file_path:
        return file_path.read_text(encoding="utf-8")
    raise ValueError("Either text or file_path must be provided.")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extract materials descriptors from text.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", help="Raw text to process.")
    group.add_argument("--file", type=Path, help="Path to a text file to process.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of human-friendly text.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    raw_text = _read_source(args.text, args.file)
    descriptors = extract_descriptors(raw_text)

    if args.json:
        print(json.dumps(descriptors, indent=2))
    else:
        materials_line = ", ".join(descriptors["materials"]) or "(none found)"
        print(f"Materials: {materials_line}")
        if descriptors["properties"]:
            print("Properties:")
            for prop in descriptors["properties"]:
                print(f"  - {prop['name']}: {prop['value']} {prop['unit']} (context: {prop['context']})")
        else:
            print("Properties: (none found)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
