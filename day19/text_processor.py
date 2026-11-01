import re
from collections import Counter


def process_text(file_path):
    """
    Read a text file and generate text statistics.
    """

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Split content into lines
    lines = content.splitlines()

    # Find words
    words = re.findall(r"\b[\w']+\b", content.lower())

    # Calculate statistics
    line_count = len(lines)

    word_count = len(words)

    character_count = len(content)

    character_count_no_spaces = len(
        re.sub(r"\s", "", content)
    )

    if line_count > 0:
        average_words_per_line = word_count / line_count
    else:
        average_words_per_line = 0

    # Find most common words
    word_frequency = Counter(words)

    most_common_words = word_frequency.most_common(5)

    return {
        "line_count": line_count,
        "word_count": word_count,
        "character_count": character_count,
        "character_count_no_spaces": character_count_no_spaces,
        "average_words_per_line": average_words_per_line,
        "most_common_words": most_common_words
    }