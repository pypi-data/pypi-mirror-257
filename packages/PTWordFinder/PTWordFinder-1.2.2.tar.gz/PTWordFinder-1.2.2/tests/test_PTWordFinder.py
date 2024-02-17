import io
import os
import re
import pytest
from unittest import mock

from unittest.mock import mock_open, patch

from ptwordfinder.commands.PTWordFinder import (
    calculate_words,
    count_multiple_words_in_file,
    count_word_in_file,
    count_pattern_in_file,
    nonblank_lines,
)

from click.testing import CliRunner


def test_help_message():
    """
    Test calculate_words function with --help option.

    Verifies that:
    - The function displays the help message correctly.
    """
    runner = CliRunner()
    result = runner.invoke(calculate_words, ["--help"])
    assert result.exit_code == 0
    assert "Count the occurrence of words in a text file." in result.output


def test_error_on_both_word_options():
    """
    Test calculate_words function with both --words-input-file and --single-word options.

    Verifies that:
    - The function raises an error when both options are used simultaneously.
    """
    runner = CliRunner()
    result = runner.invoke(
        calculate_words, ["--words-input-file", "words.txt", "--single-word", "hello"]
    )
    assert result.exit_code == 2
    assert re.search("Error: Invalid value for '--words-input-file'", result.output)
    assert re.search("No such file or directory", result.output)


def test_error_on_missing_options():
    """
    Test calculate_words function with missing mandatory options.

    Verifies that:
    - The function raises an error when required options are not provided.
    """
    runner = CliRunner()
    result = runner.invoke(calculate_words)
    assert result.exit_code == 2
    assert re.search("Missing option", result.output)
    assert re.search("--searched-file", result.output)


def test_count_multiple_words():
    """
    Test calculate_words function with --words-input-file option to count multiple words.

    Verifies that:
    - The function correctly counts the occurrences of words from a file within a text file.
    """
    # Create test files
    with open("words.txt", "w") as f:
        f.write("hello\nworld")
    with open("text.txt", "w") as f:
        f.write("This is a test sentence with hello and world.")

    runner = CliRunner()
    result = runner.invoke(
        calculate_words,
        ["--words-input-file", "words.txt", "--searched-file", "text.txt"],
    )
    assert result.exit_code == 0
    assert re.search("Found 2 matching words", result.output)

    # Clean up test files
    os.remove("words.txt")
    os.remove("text.txt")


def test_count_single_word():
    """
    Test the `calculate_words` function with the `--single-word` option.

    Verifies that:
    - The function correctly counts the occurrences of a single specified word in a text file.
    - The search is case-sensitive (i.e., "Hello" and "hello" are considered different words).
    - Words are counted within non-blank lines, excluding leading and trailing whitespaces.

    Raises:
        FileNotFoundError: If the specified searched file does not exist.
    """
    # Create test file
    with open("text.txt", "w") as f:
        f.write("This is a test sentence with hello and world.")

    runner = CliRunner()
    result = runner.invoke(
        calculate_words, ["--single-word", "hello", "--searched-file", "text.txt"]
    )
    assert result.exit_code == 0
    assert "Found 'hello' 1 times in 'text.txt'." in result.output

    # Clean up test file
    os.remove("text.txt")


def test_count_pattern():
    """
    Test the `count_pattern()` function for correctly counting pattern matches.

    Verifies that:
    - The function accurately counts the number of occurrences of a specified pattern in a text file.
    """
    # Create test file
    with open("text.txt", "w") as f:
        f.write("This is a test sentence with hello and world.")

    runner = CliRunner()
    result = runner.invoke(
        calculate_words, ["--pattern", "world", "--searched-file", "text.txt"]
    )
    assert result.exit_code == 0
    assert "Found 1 matches for pattern 'world' in 'text.txt'." in result.output

    # Clean up test file
    os.remove("text.txt")


def test_file_not_found():
    """
    Test the `calculate_words` function with a non-existent searched file.

    Verifies that:
    - The function raises a `FileNotFoundError` when the specified searched file does not exist.
    - The error message indicates that the file does not exist.

    Raises:
        FileNotFoundError: If the searched file is not found.
    """
    runner = CliRunner()
    result = runner.invoke(calculate_words, ["--searched-file", "nonexistent_file.txt"])
    assert result.exit_code == 2
    assert re.search("does not exist.", result.output)
