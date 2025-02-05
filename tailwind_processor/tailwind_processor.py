import subprocess
import textwrap
from pathlib import Path
from typing import List
import shutil


import logging

log = logging.getLogger(__name__)


class TailwindProcessor:
    """
    Process Tailwind classes into raw CSS.
    """

    def process(self, tailwind_classes: List[str]) -> str:
        """
        Process Tailwind classes into CSS.
        """
        tailwind_apply = textwrap.dedent("""
            @tailwind base;
            @tailwind components;
            @tailwind utilities;
        """)

        parent = Path(__file__).parent / "tmp"
        parent.mkdir(parents=True, exist_ok=True)

        # All temporary files
        input_file = parent / "input.css"
        content_file = parent / "content.html"
        configs = parent / "tailwind.config.js"

        # Write the content file
        tw_classes = " ".join(tailwind_classes)
        content_file.write_text(f"<div class='{tw_classes}'></div>")

        # Write the config file
        config_content = (
            textwrap.dedent("""
            /** @type {import('tailwindcss').Config} */
            module.exports = {
                content: ['%s'],
                theme: {
                    extend: {},
                },
                plugins: [],
            }
            """)
        ) % content_file.as_posix()

        configs.write_text(config_content)
        input_file.write_text(tailwind_apply)
        base_task = "uv run tailwindcss".split(" ")
        command = [
            *base_task,
            "-c", configs.as_posix(),
            "-i", input_file.as_posix(),
            "--minify",
        ]

        result = subprocess.run(command, capture_output=True, text=True)

        shutil.rmtree(parent.as_posix())

        if result.stderr:
            log.info(result.stderr)

        return result.stdout
