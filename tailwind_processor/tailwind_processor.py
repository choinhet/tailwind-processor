import importlib.resources as pkg_resources
import logging
import os
import tempfile
import textwrap
from pathlib import Path
from typing import List

import pytailwindcss

import tailwind_processor.resources as rsc

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

            config = Path(str(pkg_resources.files(rsc))) / "config.js"
            config_content = config.read_text() % (
                content_file.as_posix(),
                ",".join(f"'{e}'" for e in tailwind_classes),
            )

            configs.write_text(config_content)
            input_file.write_text(tailwind_apply)

            c = configs.as_posix()
            i = input_file.as_posix()
            o = output_file.as_posix()

            env = os.environ.copy()
            env["TAILWINDCSS_VERSION"] = "v3.4.17"

            try:
                result = pytailwindcss.run(
                    ["-c", c, "-i", i, "-o", o, "--minify"],
                    auto_install=True,
                    env=env,
                )
                log.info("Command output:\n%s", result)
            except Exception as e:
                log.error("Tailwind command failed:\n%s" % e)
                raise

            if not output_file.exists():
                raise FileNotFoundError(f"Output CSS file not created at {o}")

            final_css = output_file.read_text()
            return final_css
