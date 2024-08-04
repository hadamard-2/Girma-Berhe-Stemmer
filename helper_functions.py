import re
import json


def filter_text(word: str) -> str:
    # remove punctuation marks (english & ethiopic)
    english_punctuation = "".join(
        [
            "\u002E",  # Period.
            "\u002C",  # Comma.
            "\u0021",  # Exclamation Mark.
            "\u003F",  # Question Mark.
            "\u003A",  # Colon.
            "\u003B",  # Semicolon.
            "\u0027",  # Apostrophe.
            "\u0022",  # Double Quotation Mark.
            "\u201C",  # Left Double Quotation Mark.
            "\u201D",  # Right Double Quotation Mark.
            "\u2018",  # Left Single Quotation Mark.
            "\u2019",  # Right Single Quotation Mark.
            "\u2010",  # Hyphen.
            "\u2013",  # En Dash.
            "\u2014",  # Em Dash.
            "\u0028",  # Left Parenthesis.
            "\u0029",  # Right Parenthesis.
            "\u005B",  # Left Square Bracket.
            "\u005D",  # Right Square Bracket.
            "\u007B",  # Left Curly Bracket.
            "\u007D",  # Right Curly Bracket.
            "\u2026",  # Ellipsis.
            "\u002F",  # Slash
            "\u005C",  # Backslash
            "\u0026",  # Ampersand
            "\u002A",  # Asterisk
        ]
    )
    # pattern for english punctuation marks
    eng_pattern = f"[{re.escape(english_punctuation)}]"
    filtered_text0 = re.sub(eng_pattern, "", word)

    # pattern for ethiopic punctuation marks
    eth_pattern = r"[\u1361-\u1368]+"
    filtered_text1 = re.sub(eth_pattern, "", filtered_text0)

    # replace newlines with spaces
    filtered_text2 = filtered_text1.replace("\n", " ")

    # remove any item containing non-Ethiopic letters
    ethiopic_letters = load_json_file("SERA_transliteration.json")

    filtered_list = []
    for word in filtered_text2.split():
        if all(char in ethiopic_letters.keys() for char in word):
            filtered_list.append(word)

    # join using newline char and return
    return "\n".join(filtered_list)


def load_txt_file(filepath, separator=" "):
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read().splitlines()


def load_json_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        collection_map = json.load(file)
    return collection_map


transliteration_table = load_json_file("SERA_transliteration.json")
transcription_table = {value: key for key, value in transliteration_table.items()}
vowels = ["e", "u", "i", "a", "E", "", "o"]


def transliterate(word: str) -> str:
    """
    Transliteration of word written in Ethiopic script using Latin alphabet.
    """
    transliteration = ""
    for letter in word:
        if 4608 <= ord(letter) <= 4954:
            transliteration += transliteration_table[letter]
        else:
            transliteration += letter

    return transliteration


def transcribe(word: str) -> str:
    """
    Converts transliterated word back to its original form.
    """
    transcription = ""
    unit = ""
    i = 0
    while i < len(word):
        unit += word[i]
        # if it's a vowel
        if unit[-1] in vowels:
            transcription += transcription_table[unit]
            unit = ""
        # if it's a consonant
        elif unit[-1] not in {"'", "W"}:
            # if it's the last letter in the word or the next letter is a consonant or a single quote
            if i == len(word) - 1 or word[i + 1] not in set(vowels).union({"W"}):
                transcription += transcription_table[unit]
                unit = ""
        i += 1

    return transcription


def main():
    # text = """ሰላም! Today's date is 2024-07-30.
    # The event is scheduled for 30 ሓምለ 2024.
    # Please note that the deadline is 07/15/2024.
    # The fiscal year starts on 2024211.፥ ፣ ፤ ፡
    # """
    # text = "yellow ."

    # print(filter_text(text))
    # filter_text(text)

    # transliterate("ኢትዮጵያ")
    # transliterate("መንግሥት")
    # transliterate("ቸርቻሪዎች")
    # transliterate("ተፈርቷል")
    # transliterate("ጭማሪ")
    # transliterate("ከፍተኛ")

    # transcribe("he")
    # transcribe("He")
    # transcribe("'se")
    # transcribe("i")
    # transcribe("lWa")
    # transcribe("hWi")
    # transcribe("KWE")
    # transcribe("gWa")

    # transcribe(transliterate("ኢትዮጵያ"))
    # transcribe(transliterate("መንግሥት"))
    # transcribe(transliterate("ቸርቻሪዎች"))
    # transcribe(transliterate("ተፈርቷል"))
    # transcribe(transliterate("ጭማሪ"))
    # transcribe(transliterate("ከፍተኛ"))

    print(transcribe(transliterate("ጓደኛ")))
    pass


if __name__ == "__main__":
    main()
