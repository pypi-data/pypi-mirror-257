import sys
import time
import click
import re


@click.command()
@click.option(
    "--words-input-file",
    "-w",
    type=click.File("r"),
    help="File containing words to search for",
)
@click.option(
    "--searched-file",
    "-s",
    type=click.Path(exists=True),
    required=True,
    help="Text file to search in",
)
@click.option(
    "--single-word",
    "-w",
    type=click.STRING,
    help="Specific word to count (exclusive to --words-input-file)",
)
@click.option("--pattern", "-p", help="Regular expression pattern to match")
def calculate_words(words_input_file, searched_file, single_word, pattern):
    """Count the occurrence of words in a text file.

    Args:
        words_input_file (file, optional): File containing words to search for. Defaults to None.
        searched_file (str): Path to the text file to search in. Required.
        single_word (str, optional): Specific word to count. Defaults to None.
        pattern (str, optional): Regular expression pattern to match. Defaults to None.

    Note:
        --words-input-file and --single-word are mutually exclusive.
        At least one of --words-input-file, --single-word, or --pattern must be provided.
    """

    if words_input_file and single_word:
        click.echo(
            "Error: --words-input-file and --single-word are mutually exclusive.",
            err=True,
        )
        sys.exit(1)

    if not (words_input_file or single_word or pattern):
        click.echo(
            "Error: At least one of --words-input-file, --single-word, or --pattern must be provided.",
            err=True,
        )
        sys.exit(1)

    start_time = time.time()

    if words_input_file:
        # Process list of words
        word_list = [elt.strip() for elt in words_input_file.readlines()]
        word_set = set(word_list)
        counter = count_multiple_words_in_file(word_set, searched_file)
        print(
            f"Found {counter} matching words from '{words_input_file}' in '{searched_file}'."
        )

    elif single_word:
        # Count specific word
        counter = count_word_in_file(single_word, searched_file)
        print(f"Found '{single_word}' {counter} times in '{searched_file}'.")

    else:
        # Match regular expression pattern
        counter = count_pattern_in_file(pattern, searched_file)
        print(f"Found {counter} matches for pattern '{pattern}' in '{searched_file}'.")

    stop_time = time.time()
    print(f"Time elapsed: %.1f seconds" % (stop_time - start_time))


def count_multiple_words_in_file(word_set, searched_file):
    """
    Count the occurrences of words from a given word set in a text file.

    Args:
        word_set (set): A set containing the words to search for.
        searched_file (str): The path to the text file to search in.

    Returns:
        int: The total count of occurrences of words from the word set in the text file.

    Note:
        This function reads the content of the text file specified by 'searched_file'
        and counts the occurrences of words from 'word_set' in each non-blank line of the file.
        It utilizes the 'nonblank_lines' generator to yield non-blank lines from the file.
        The function returns the total count of occurrences of words from 'word_set' in the file.
    """

    counter = 0
    with open(searched_file, "r") as file:
        for line in nonblank_lines(file):
            for word in line:
                if word in word_set:
                    counter += 1
    return counter


def count_word_in_file(word, searched_file):
    """Count how many times a word appears in a file.

    Args:
        word (str): The word to search for.
        searched_file (str): The path to the file to search in.
    """
    try:
        # Initialize a counter to keep track of occurrences
        count = 0

        # Open the file in read mode
        with open(searched_file, "r") as file:
            # Read the content of the file
            file_content = file.read()

            # Split the content into words
            words_in_file = file_content.split()

            # Iterate through the words in the file
            for w in words_in_file:
                # Check if the word is in the file
                for match in re.findall(word, w):
                    count += 1

        # Print the count of occurrences
        return count

    except FileNotFoundError:
        # If the file is not found, print an error message and return a non-zero exit code
        click.echo(f"Error: Path '{searched_file}' does not exist.", err=True)
        raise

def count_pattern_in_file(pattern, searched_file):
    """Counts occurrences of a pattern in a file, considering non-blank lines.

    Args:
        pattern (str): The pattern to search for.
        searched_file (str): The path to the file to search.

    Returns:
        int: The number of occurrences of the pattern in the file.
    """

    counter = 0
    with open(searched_file, "r") as file:
        for line in file:
            for match in re.findall(pattern, line):
                print(match)
                counter += 1
    return counter


def nonblank_lines(text_file):
    """Generate non-blank lines from a text file.
    
    - erased blank lines from begin and end of string
    - it also remove all nonalphanumerical characters
    - exclude space character

    Input: any string text from opened file

    Args:
        text_file (file): The input text file.

    Yields:
        list: Non-blank lines of the text file.
        example : ['word','','word']
    """
    for line in text_file:
        line = line.strip()
        if line:
            text = re.split(r"\s{1,}", line)
            stripped_line = []
            for item in text:
                stripped = "".join(ch for ch in item if ch.isalnum())
                stripped_line.append(stripped)
            yield stripped_line

