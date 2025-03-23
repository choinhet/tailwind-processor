import textwrap
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
    processed, err = tailwind_processor.process(tailwind_classes)

    assert err is None
    assert r".h-dvh{height:100dvh}.text-red-500" in processed


def test_file_processor(tailwind_processor):
    file_content = textwrap.dedent("""
    <div class="text-red-500 h-dvh">
        Hey!
    </div>
    """)
    processed, err = tailwind_processor.process_file_str(file_content)

    assert err is None
    assert r".h-dvh{height:100dvh}.text-red-500" in processed


def test_process_exception_handling(monkeypatch):
    def mock_error(*args, **kwargs):
        raise Exception("Tailwind command failed")

    monkeypatch.setattr("pytailwindcss.run", mock_error)

    _, err = TailwindProcessor().process(["text-red-500"])
    assert err is not None

    _, err = TailwindProcessor().process_file_str("text-red-500")
    assert err is not None

if __name__ == "__main__":
    pytest.main([__file__])
