# Materials descriptor extractor

A lightweight Python helper that pulls common materials descriptors—chemical formulas and key physical properties—from unstructured text. It relies solely on regex heuristics, so it runs anywhere without external NLP dependencies.

## Installation

No special dependencies are required beyond Python 3.11+. Clone the repository and run the scripts directly:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .  # not strictly required, but keeps imports tidy
```

## Usage

### Quick start (命令行)

Process either raw text or a text file:

```bash
python -m src.materials_extractor --text "The band gap of TiO2 is 3.2 eV." --json
```

```bash
python -m src.materials_extractor --file examples/paper_excerpt.txt
```

What the flags do:

- `--text` / `--file`: choose to pass text directly or point to a UTF-8 text file.
- `--json`: output structured JSON (omit for a human-readable summary).

Example output (human readable) for the sample file:

```
Materials: TiO2, SiO2, Al2O3
Properties:
  - band_gap: 3.2 eV (context: band gap of TiO2 is 3.2 eV at room temperature)
  - density: 2.2 g/cm3 (context: The density of SiO2 glass is about 2.2 g/cm3)
```

### Use as a Python helper (Python 调用示例)

```python
from src.materials_extractor import extract_descriptors

text = "The band gap of TiO2 is 3.2 eV and SiO2 density is 2.2 g/cm3."
result = extract_descriptors(text)

print(result["materials"])      # ['SiO2', 'TiO2']
print(result["properties"])     # list of dictionaries with name/value/unit/context
```

The Python API returns a dictionary with `materials` (list of formulas) and `properties` (list of dictionaries containing `name`, `value`, `unit`, and a short `context` snippet). This makes it easy to post-process or store the results in your own pipeline.

## Development

Run the unit suite with:

```bash
python -m unittest discover -s tests
```

Feel free to extend `src/materials_extractor.py` with additional property patterns or smarter context detection as your corpus demands.
