import logging
import os
import subprocess
import textwrap
from pathlib import Path
from typing import List
import tempfile

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

        with tempfile.TemporaryDirectory() as temp_dir:
            parent = Path(temp_dir)
            parent.mkdir(parents=True, exist_ok=True)

            input_file = parent / "input.css"
            output_file = parent / "output.css"
            content_file = parent / "content.html"
            configs = parent / "tailwind.config.js"

            tw_classes = " ".join(tailwind_classes)
            content_file.write_text(f'<div class="{tw_classes}"></div>')

            config_content = textwrap.dedent("""
                /** @type {import('tailwindcss').Config} */
                module.exports = {
                    content: ['%s'],
                    safelist: [%s],
                    theme: {
                        extend: {},
                    },
                    plugins: [],
                }
                """) % (content_file.as_posix(), ",".join(f"'{e}'" for e in tailwind_classes))

            configs.write_text(config_content)
            input_file.write_text(tailwind_apply)

            c = configs.as_posix()
            i = input_file.as_posix()
            o = output_file.as_posix()

            env = os.environ.copy()
            env["TAILWINDCSS_VERSION"] = "3.2.7"

            command = [
                "uv", "run", "tailwindcss",
                "-c", c,
                "-i", i,
                "-o", o,
                "--minify"
            ]

            try:
                result = subprocess.run(command, capture_output=True, text=True, check=True)
                log.info("Command output:\n%s", result.stdout)
            except subprocess.CalledProcessError as e:
                log.error("Tailwind command failed with code %s: %s", e.returncode, e.stderr)
                raise

            final_css = output_file.read_text()
            return final_css

