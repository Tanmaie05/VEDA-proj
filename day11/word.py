import re


def analyze_text(text):
    # Count characters including spaces
    character_count = len(text)

    # Count words
    word_count = len(text.split())

    # Count spaces
    space_count = text.count(" ")

    # Count sentences using ., !, or ?
    sentence_count = len(re.findall(r'[.!?]+', text))

    return character_count, word_count, sentence_count, space_count


def main():
    print("=" * 45)
    print("       WORD AND CHARACTER COUNTER")
    print("=" * 45)

    text = input("\nEnter a paragraph: ").strip()

    # Handle empty input
    if not text:
        print("\nError: Please enter some text.")
        return

    character_count, word_count, sentence_count, space_count = analyze_text(text)

    print("\n" + "-" * 45)
    print("           TEXT STATISTICS")
    print("-" * 45)

    print(f"Characters : {character_count}")
    print(f"Words      : {word_count}")
    print(f"Sentences  : {sentence_count}")
    print(f"Spaces     : {space_count}")

    print("-" * 45)


if __name__ == "__main__":
    main()