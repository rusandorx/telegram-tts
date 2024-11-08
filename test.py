
import re


def parse_text(text):
    # Updated pattern to allow hyphens in the key
    pattern = r"\[([\w-]+)\]\s*([^[]+)"
    matches = re.findall(pattern, text)

    result = []

    for key, value in matches:
        result.append([key, value.strip()])
    return [[key, value.strip()] for key, value in matches]


print(parse_text('[saul-goodman] im saul goodman [rusandor] im rusandor'))
