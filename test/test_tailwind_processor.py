import logging
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

    @patch("pytailwindcss.run")
    def test_process_exception_handling(self, mock_run):
        mock_run.side_effect = Exception("Simulated Tailwind processing error")
        tailwind_classes = ["text-red-500"]
        with self.assertLogs(level="ERROR") as log_context:
            try:
                result = self.tp.process(tailwind_classes)
                self.fail("Expected an exception to be logged")
            except Exception:
                log_messages = [record.getMessage() for record in log_context.records]
                self.assertTrue(
                    any("Tailwind command failed" in msg for msg in log_messages)
                )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("tailwind_processor")
    # logger.setLevel(logging.DEBUG)
    unittest.main()
