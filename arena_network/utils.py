def normalize_text(text):
    replacements = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 'A': '4', 'E': '3', 'I': '1', 'O': '0'}
    for key, value in replacements.items():
        text = text.replace(key, value)
    return text


def contains_prohibited_words(value, prohibited_words):
    normalized_value = normalize_text(value)
    for word in prohibited_words:
        normalized_word = normalize_text(word)
        if normalized_word in normalized_value.lower():
            return True
    return False