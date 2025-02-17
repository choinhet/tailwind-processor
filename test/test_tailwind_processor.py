import pytest

from tailwind_processor.tailwind_processor import TailwindProcessor


@pytest.fixture
def tailwind_processor():
    return TailwindProcessor()


def test_text_processor(tailwind_processor):
    tailwind_classes = [
        "text-red-500",
        "h-dvh",
    ]
    processed = tailwind_processor.process(tailwind_classes)
    assert r".h-dvh{height:100dvh}.text-red-500" in processed


def test_process_exception_handling(monkeypatch):
    def mock_run(*args, **kwargs):
        raise Exception("Tailwind command failed")

    monkeypatch.setattr("pytailwindcss.run", mock_run)

    with pytest.raises(Exception, match="Tailwind command failed"):
        TailwindProcessor().process(["text-red-500"])


def test_output_file_not_created(monkeypatch):
    def mock_run(*args, **kwargs):
        return "Mocked successful run"

    monkeypatch.setattr("pytailwindcss.run", mock_run)
    monkeypatch.setattr("pathlib.Path.exists", lambda self: False)

    with pytest.raises(FileNotFoundError, match="Output CSS file not created"):
        TailwindProcessor().process(["text-red-500"])
