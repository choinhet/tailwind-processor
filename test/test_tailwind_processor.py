import logging
import subprocess
import unittest
from unittest.mock import patch

from tailwind_processor.tailwind_processor import TailwindProcessor


class TestTailwindProcessor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tp = TailwindProcessor()

    def test_text_processor(self):
        tailwind_classes = [
            "text-red-500",
            "h-dvh",
        ]
        processed = self.tp.process(tailwind_classes)
        self.assertIn(
            r".h-dvh{height:100dvh}.text-red-500",
            processed,
        )

    def test_text_processor_error(self):
        tailwind_classes = [
            "text-red-500",
            "h-dvh",
        ]
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(
                returncode=1,
                cmd=["uv", "run", "tailwindcss", "-c", "dummy", "-i", "dummy", "-o", "dummy", "--minify"],
                output="",
                stderr="Simulated error"
            )
            with self.assertRaises(subprocess.CalledProcessError) as cm:
                self.tp.process(tailwind_classes)
            self.assertIn("Simulated error", cm.exception.stderr)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("tailwind_processor")
    # logger.setLevel(logging.DEBUG)
    unittest.main()
