from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

import arduino_helper  # noqa: E402


class ArduinoHelperTests(unittest.TestCase):
    def test_resolve_fqbn_alias(self) -> None:
        self.assertEqual(arduino_helper.resolve_fqbn_name("Arduino Uno"), "arduino:avr:uno")
        self.assertEqual(arduino_helper.resolve_fqbn_name("esp32"), "esp32:esp32:esp32")

    def test_infer_library_candidates_from_includes(self) -> None:
        includes = ["ArduinoJson.h", "ESPAsyncWebServer.h", "CustomLib.h"]
        libraries = arduino_helper.infer_library_candidates(includes)
        self.assertIn("ArduinoJson", libraries)
        self.assertIn("ESP Async WebServer", libraries)
        self.assertIn("CustomLib", libraries)

    def test_extract_includes_from_example_project(self) -> None:
        project_path = REPO_ROOT / "examples" / "esp32-web-status"
        includes = arduino_helper.extract_includes(project_path)
        self.assertEqual(includes, ["ArduinoJson.h", "ESPAsyncWebServer.h", "WiFi.h"])

    def test_find_sketches_from_example_project(self) -> None:
        project_path = REPO_ROOT / "examples" / "uno-blink"
        sketches = arduino_helper.find_sketches(project_path)
        self.assertEqual([path.name for path in sketches], ["uno-blink.ino"])


if __name__ == "__main__":
    unittest.main()
