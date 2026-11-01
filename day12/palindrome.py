def check_palindrome(text):
    # Convert text to lowercase
    # Remove spaces
    normalized_text = text.lower().replace(" ", "")

    # Reverse the normalized text
    reversed_text = normalized_text[::-1]

    # Check whether it is a palindrome
    if normalized_text == reversed_text:
        return True, normalized_text, reversed_text
    else:
        return False, normalized_text, reversed_text