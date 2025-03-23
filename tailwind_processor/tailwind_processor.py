import importlib.resources as pkg_resources
import logging
import os
import tempfile
import textwrap
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pytailwindcss

import tailwind_processor.resources as rsc

log = logging.getLogger(__name__)


class TailwindProcessor:
    """
    Process Tailwind classes into raw CSS.
    """

    def _get_environment(self) -> Dict[str, Any]:
        env = os.environ.copy()
        env["TAILWINDCSS_VERSION"] = "v3.4.17"
        return env

    def _set_input(self, parent: Path) -> Tuple[Path, Optional[Exception]]:
        try:
            input_file = parent / "input.css"
            input_file.write_text(
                textwrap.dedent("""
                @tailwind base;
                @tailwind components;
                @tailwind utilities;
                """)
            )
            return input_file, None
        except Exception as e:
            return Path().home(), Exception(f"Failed to set input file:\n{e}")

    def _set_configs(
        self,
        parent: Path,
        content_file: str,
    ) -> Tuple[Path, Optional[Exception]]:
        try:
            configs = parent / "tailwind.config.js"
            config = Path(str(pkg_resources.files(rsc))) / "config.js"
            config_content = config.read_text() % content_file
            configs.write_text(config_content)
            return configs, None
        except Exception as e:
            return Path().home(), Exception(f"Failed to set configs file:\n{e}")

    def _set_output(self, parent: Path) -> Tuple[Path, Optional[Exception]]:
        try:
            output_file = parent / "output.css"
            return output_file, None
        except Exception as e:
            return Path().home(), Exception(f"Failed to set output file:\n{e}")

    def _run_command(
        self,
        config_path: Path,
        input_path: Path,
        output_path: Path,
    ) -> Optional[Exception]:
        result, args = "", []
        args = []
        try:
            c = config_path.as_posix()
            i = input_path.as_posix()
            o = output_path.as_posix()
            args = ["-c", c, "-i", i, "-o", o, "--minify"]

            result = pytailwindcss.run(
                args,
                auto_install=True,
                env=self._get_environment(),
                live_output=False,
            )

            log.info("Command output:\n%s", result)
        except Exception as e:
            return Exception(
                f"Failed to run tailwind command:\nCommand Output:{result}\nArgs:{args}\nCause:\n{e}"
            )

    def _run_for_content(
        self,
        parent: Path,
        content_path: str,
        tw_classes: Optional[List[str]] = None,
    ) -> Tuple[str, Optional[Exception]]:
        tw_classes = tw_classes or []

        input_path, err = self._set_input(parent)
        if err:
            return "", err

        config_path, err = self._set_configs(parent, content_path)
        if err:
            return "", err

        output_path, err = self._set_output(parent)
        if err:
            return "", err

        err = self._run_command(
            config_path=config_path,
            input_path=input_path,
            output_path=output_path,
        )
        if err:
            return "", err

        try:
            return output_path.read_text(), None
        except Exception as e:
            return "", Exception(f"Failed to read output file:\n{e}")

    def process_file_str(self, content: str) -> Tuple[str, Optional[Exception]]:
        """
        Process Tailwind str into CSS.

        Args:
            content - Contents of a HTML file

        Returns:
            Processed style file string, Potential Error
        """
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                parent = Path(temp_dir)
                parent.mkdir(parents=True, exist_ok=True)

                content_file = parent / "content.html"
                content_file.write_text(content)
                content_path = content_file.as_posix()

                result, err = self._run_for_content(
                    parent=parent,
                    content_path=content_path,
                )

                if err:
                    return "", err

                return result, None
        except Exception as e:
            return "", Exception(f"Failed process tailwind:\n{e}")

    def process(self, tailwind_classes: List[str]) -> Tuple[str, Optional[Exception]]:
        """
        Process Tailwind classes into CSS.

        Args:
            tailwind_classes - Classes to process

        Returns:
            Processed style file string, Potential Error
        """
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                parent = Path(temp_dir)
                parent.mkdir(parents=True, exist_ok=True)
                content_file = parent / "content.html"
                tw_classes = " ".join(tailwind_classes)
                content_file.write_text(f'<div class="{tw_classes}"></div>')
                content_path = content_file.as_posix()

                result, err = self._run_for_content(
                    parent=parent,
                    content_path=content_path,
                    tw_classes=tailwind_classes,
                )
                if err:
                    return "", err

                return result, None
        except Exception as e:
            return "", Exception(f"Failed to process tailwind classes:\n{e}")
