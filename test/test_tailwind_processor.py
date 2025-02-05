import unittest
import logging

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
            r".h-dvh{height:100dvh}.text-red-500{--tw-text-opacity:1;color:rgb(239 68 68/var(--tw-text-opacity,1))}",
            processed,
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("tailwind_processor")
    # logger.setLevel(logging.DEBUG)
    unittest.main()
