from helper_functions import transliterate, transcribe
from preprocessing import TigMorphPreprocess
import re


class TigrinyaStemmer:
    """
    The corpus is assumed to have gone through morphological preprocessing.
    """

    # REVIEW - dates should not get stemmed
    # NOTE - never use replace method to remove prefix and suffix of any kind!!

    vowels = ["ኧ", "ኡ", "ኢ", "ኣ", "ኤ", "እ", "ኦ"]

    def __init__(self, prefix_list, infix_map, suffix_list, corpus=""):
        self.prefix_list = sorted(prefix_list, key=len)
        self.infix_map = infix_map
        self.suffix_list = sorted(suffix_list, key=len)
        self.corpus = corpus

    def count_radicals(word):
        """Count the number of radicals in a word."""
        return sum([1 for char in word if char not in vowels])

    def extract_root(word):
        """Extract the root of a word."""
        # This is a placeholder. You'll need to implement based on Tigrinya morphology.
        return word

    def remove_prefix_suffix_pair(word, prefix_suffix_pairs):
        nw = count_radicals(word)
        if nw <= 3:
            return word

        for prefix, suffix in prefix_suffix_pairs:
            if word.startswith(prefix) and word.endswith(suffix):
                nps = count_radicals(prefix + suffix)
                if nw - nps >= 3:
                    pword = word[len(prefix) :]
                    sword = pword[: -len(suffix)]
                    return remove_prefix_suffix_pair(sword, prefix_suffix_pairs)

        return word

    def remove_double_reduplication(word):
        n = count_radicals(word)
        if n < 5:
            return word

        root = extract_root(word)
        for i in range(len(root) - 3):
            if root[i] == root[i + 2] and root[i + 1] == root[i + 3]:
                # Remove the reduplicated part. This is a simplified version.
                return word[:i] + word[i + 2 :]

        return word

    def remove_prefix(word, prefix_list):
        while True:
            n = count_radicals(word)
            if n <= 3:
                return word

            for prefix in prefix_list:
                if word.startswith(prefix):
                    np = count_radicals(prefix)
                    if n - np >= 3:
                        word = word[len(prefix) :]
                        break
            else:
                return word

    def remove_suffix(word, suffix_list):
        while True:
            n = count_radicals(word)
            if n <= 3:
                return word

            for suffix in suffix_list:
                if word.endswith(suffix):
                    ns = count_radicals(suffix)
                    if n - ns >= 3:
                        word = word[: -len(suffix)]
                        break
            else:
                return word

    def remove_single_reduplication(word):
        n = count_radicals(word)
        if n < 4:
            return word

        root = extract_root(word)
        for i in range(len(root) - 1):
            if root[i] == root[i + 1]:
                # Remove the reduplicated part. This is a simplified version.
                return word[:i] + word[i + 1 :]

        return word

    def stem_tigrinya(word, prefix_suffix_pairs, prefix_list, suffix_list):
        word = remove_prefix_suffix_pair(word, prefix_suffix_pairs)
        word = remove_double_reduplication(word)
        word = remove_prefix(word, prefix_list)
        word = remove_suffix(word, suffix_list)
        word = remove_single_reduplication(word)
        return word

    def stem(self, word):
        """
        For simplicity implementation is done assuming the method gets called passing a word.
        In practice, stem method should run on corpus.

        Converts to abugida form before handling prefixes.
        Converts back to original form before returning.
        """

        # word0 = self.handle_infixes(word)

        # word1 = segment_fidel(word0)

        # word2 = self.handle_suffixes(word1)
        # word3 = self.handle_prefixes(word2)

        # return fuse_segments(word3)
        pass


def load_files():
    # load prefix list
    with open("girma_prefix_list.txt", "r", encoding="utf-8") as file:
        prefix_list = file.read().splitlines()

    # load infix map
    infix_map = load_json_file("list_prep\infix_map0.json")

    # load prefix list
    with open("girma_suffix_list.txt", "r", encoding="utf-8") as file:
        suffix_list = file.read().splitlines()

    # load corpus
    # with open("processed_tig_corpus.txt", "r", encoding="utf-8") as file:
    #     corpus = file.read()

    return prefix_list, infix_map, suffix_list


def main():
    prefix_list, infix_map, suffix_list = load_files()

    stemmer = TigrinyaStemmer(prefix_list, infix_map, suffix_list)
    preprocessor = TigMorphPreprocess()

    word_list = ["ማእከላት", "ከተማታት", "ሰባቢሩ", "ተጻወቲ", "ዘይብሎም", "አይትግበር"]
    # word_list = ["አይትምጻእ", "አይተንብብ", "አይንግበር", "አይነበርኩን", "ብምግባርካ"]
    for word in word_list:
        preprocessed_word = preprocessor.normalize(word)
        if preprocessed_word == "":
            print(
                f"The word you provided ({word}) was removed during the preprocessing stage!"
            )
        else:
            stemmed_word = stemmer.stem(preprocessed_word)
            print(f"{word} --> {stemmed_word}")

    # word = "አይተንብብ"
    # preprocessed_word = preprocessor.normalize(word)
    # if preprocessed_word == "":
    #     print(
    #         f"The word you provided ({word}) was removed during the preprocessing stage!"
    #     )
    # else:
    #     stemmed_word = stemmer.stem(preprocessed_word)
    #     print(f"{word} --> {stemmed_word}")


if __name__ == "__main__":
    main()
