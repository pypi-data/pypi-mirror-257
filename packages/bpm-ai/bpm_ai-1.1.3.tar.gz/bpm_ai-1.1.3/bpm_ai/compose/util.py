import html

from bpm_ai.compose.stopwords import stopwords


def remove_stop_words(sentence, separator=' ', max_n_result_words: int = 6):
    # Split the sentence into individual words
    words = sentence.split()
    # Use a list comprehension to remove stop words
    filtered_words = [word for word in words if word not in stopwords]
    # Join the filtered words back into a sentence
    return separator.join(filtered_words[:max_n_result_words])


def type_to_prompt_type_str(type: str) -> str:
    match type:
        case "letter":
            return "emails and letters"
        case "chat":
            return "chat messages"
        case "social":
            return "social media posts"
        case "text":
            return "texts"


def decode_if_needed(text):
    """fix for encoding errors in new OpenAI models API"""
    text = html.unescape(text)
    if '\\u' in text:
        return text.encode().decode('unicode-escape')
    else:
        return text
