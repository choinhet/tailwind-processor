import textwrap
from pathlib import Path

import pytest

from tailwind_processor.tailwind_processor import TailwindProcessor


@pytest.fixture
def tailwind_processor() -> TailwindProcessor:
    return TailwindProcessor()


def test_text_processor(tailwind_processor: TailwindProcessor):
    tailwind_classes = [
        "text-red-500",
        "h-dvh",
    ]
    processed, err = tailwind_processor.process(tailwind_classes)
    print(err)

    assert err is None
    assert r".h-dvh{height:100dvh}.text-red-500" in processed


def test_file_processor(tailwind_processor: TailwindProcessor):
    file_content = textwrap.dedent("""
    <div class="text-red-500 h-dvh">
        Hey!
    </div>
    """)
    processed, err = tailwind_processor.process_file_str(file_content)

    assert err is None
    assert r".h-dvh{height:100dvh}.text-red-500" in processed


def test_command_error(
    tailwind_processor: TailwindProcessor,
    monkeypatch,
):
    def mock_error(*args, **kwargs):
        raise Exception("Tailwind command failed")

    monkeypatch.setattr("pytailwindcss.run", mock_error)

    _, err = tailwind_processor.process(["text-red-500"])
    assert err is not None

    _, err = tailwind_processor.process_file_str("text-red-500")
    assert err is not None


def test_set_input_inner_error(
    tailwind_processor: TailwindProcessor,
    mocker,
):
    def mock_error(*args, **kwargs):
        raise Exception("Failure")

    mock = mocker.MagicMock(spec=Path)
    mock.__truediv__.side_effect = mock_error
    _, err = tailwind_processor._set_input(mock)

    assert err is not None


def test_set_input_error(
    tailwind_processor: TailwindProcessor,
    mocker,
):
    def mock_error(*args, **kwargs):
        return "", Exception("Failure")

    mocker.patch.object(
        tailwind_processor,
        "_set_input",
        mock_error,
    )

    _, err = tailwind_processor.process(["text-red-500"])
    assert err is not None

    _, err = tailwind_processor.process_file_str("text-red-500")
    assert err is not None


def test_set_config_inner_error(
    tailwind_processor: TailwindProcessor,
    mocker,
):
    def mock_error(*args, **kwargs):
        raise Exception("Failure")

    mock = mocker.MagicMock(spec=Path)
    mock.__truediv__.side_effect = mock_error

    _, err = tailwind_processor._set_configs(mock, content_file="")
    assert err is not None


def test_set_config_error(
    tailwind_processor: TailwindProcessor,
    mocker,
):
    def mock_error(*args, **kwargs):
        return "", Exception("Failure")

    mocker.patch.object(
        tailwind_processor,
        "_set_configs",
        mock_error,
    )
    _, err = tailwind_processor.process(["text-red-500"])
    assert err is not None

    _, err = tailwind_processor.process_file_str("text-red-500")
    assert err is not None


def test_set_output_inner_error(
    tailwind_processor: TailwindProcessor,
    mocker,
):
    def mock_error(*args, **kwargs):
        raise Exception("Failure")

    mock = mocker.MagicMock(spec=Path)
    mock.__truediv__.side_effect = mock_error

    _, err = tailwind_processor._set_output(mock)
    assert err is not None


def test_set_output_error(
    tailwind_processor: TailwindProcessor,
    mocker,
):
    def mock_error(*args, **kwargs):
        return "", Exception("Failure")

    mocker.patch.object(
        tailwind_processor,
        "_set_output",
        mock_error,
    )
    _, err = tailwind_processor.process(["text-red-500"])
    assert err is not None

    _, err = tailwind_processor.process_file_str("text-red-500")
    assert err is not None


def test_process_inner_exception(
    tailwind_processor: TailwindProcessor,
    mocker,
):
    def mock_error(*args, **kwargs):
        raise Exception("Failure")

    mocker.patch.object(
        tailwind_processor,
        "_set_input",
        mock_error,
    )
    _, err = tailwind_processor.process(["text-red-500"])
    assert err is not None

    _, err = tailwind_processor.process_file_str("text-red-500")
    assert err is not None


def test_corrupted_output(
    tailwind_processor: TailwindProcessor,
    mocker,
):
    def mock_error(*args, **kwargs):
        raise Exception("Failure")

    corrupted_output = mocker.MagicMock(Path)
    corrupted_output.read_text.side_effect = mock_error

    mocker.patch.object(
        tailwind_processor,
        "_set_output",
        lambda *args, **kwargs: (corrupted_output, None),
    )
    _, err = tailwind_processor.process(["text-red-500"])
    assert err is not None

    _, err = tailwind_processor.process_file_str("text-red-500")
    assert err is not None


if __name__ == "__main__":
    pytest.main([__file__])
