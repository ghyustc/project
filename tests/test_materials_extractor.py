import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src import materials_extractor as me


class DescriptorExtractionTests(unittest.TestCase):
    def test_extracts_materials_and_properties(self):
        text = (
            "The band gap of TiO2 is 3.2 eV. "
            "Al2O3 exhibits density of 3.95 g/cm3 and thermal conductivity is 30 W/mK. "
            "The lattice parameter a is 0.842 nm."
        )

        descriptors = me.extract_descriptors(text)

        self.assertEqual(descriptors["materials"], ["Al2O3", "TiO2"])
        props = descriptors["properties"]
        prop_names = {p["name"] for p in props}
        self.assertSetEqual(prop_names, {"band_gap", "density", "thermal_conductivity", "lattice_parameter"})

    def test_normalizes_units(self):
        text = "The melting point is about 1873 C and hardness is 20 HV."
        properties = me.extract_properties(text)
        units = {p.unit for p in properties}
        self.assertIn("°C", units)
        self.assertIn("HV", units)

    def test_cli_json_output(self):
        text = "Young's modulus of Fe3O4 is 200 GPa."
        exit_code = me.main(["--text", text, "--json"])
        self.assertEqual(exit_code, 0)


if __name__ == "__main__":
    unittest.main()
