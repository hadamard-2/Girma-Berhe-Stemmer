from helper_functions import *


class TigMorphPreprocess:
    """
    Class for doing Tigrinya specific morphological preprocessing.
    Works for both large text corpus and single words.
    """

    def __init__(self, corpus=""):
        if corpus != "":
            self.corpus = corpus.replace("\n", " ")

    def filter_text(self):
        return [
            word
            for word in self.corpus.split(" ")
            if all(4608 <= ord(char) <= 4954 for char in word)
        ]

    def tokenize(self, word="") -> str:
        """
        Removes words containing non-alphabet characters from corpus.
        Keeping dates is not worth the added complexity.
        """
        if word != "":
            return self.filter_text(word)

        self.corpus = self.filter_text()

    def normalize_helper(self, list1: list, list2: list, word=""):
        if word != "":
            for i in range(len(list1)):
                word = word.replace(list1[i], list2[i])
            return word

        for i in range(len(list1)):
            self.corpus = self.corpus.replace(list1[i], list2[i])

    def normalize(self, word="") -> str:
        """
        Does tigrinya language specific normalization.
        Converges similar sounding characters.
        """
        h1 = ["ሐ", "ሑ", "ሒ", "ሓ", "ሔ", "ሕ", "ሖ", "ሗ", "ሗ"]
        h2 = ["ሀ", "ሁ", "ሂ", "ሃ", "ሄ", "ህ", "ሆ", "ሗ", "ሗ"]
        h3 = ["ኀ", "ኁ", "ኂ", "ኃ", "ኄ", "ኅ", "ኆ", "ኇ", "ኋ"]

        s1 = ["ሰ", "ሱ", "ሲ", "ሳ", "ሴ", "ስ", "ሶ", "ሷ"]
        s2 = ["ሠ", "ሡ", "ሢ", "ሣ", "ሤ", "ሥ", "ሦ", "ሧ"]

        q1 = ["ቀ", "ቁ", "ቂ", "ቃ", "ቄ", "ቅ", "ቆ", "ቈ", "ቊ", "ቋ", "ቌ", "ቍ"]
        q2 = ["ቐ", "ቑ", "ቒ", "ቓ", "ቔ", "ቕ", "ቖ", "ቘ", "ቚ", "ቛ", "ቜ", "ቝ"]

        a1 = ["አ", "ኡ", "ኢ", "ኣ", "ኤ", "እ", "ኦ"]
        a2 = ["ዐ", "ዑ", "ዒ", "ዓ", "ዔ", "ዕ", "ዖ"]

        ts1 = ["ጸ", "ጹ", "ጺ", "ጻ", "ጼ", "ጽ", "ጾ", "ጿ"]
        ts2 = ["ፀ", "ፁ", "ፂ", "ፃ", "ፄ", "ፅ", "ፆ", "ጿ"]

        if word != "":
            word = self.normalize_helper(h2, h1, word)
            word = self.normalize_helper(h3, h1, word)
            word = self.normalize_helper(s2, s1, word)
            word = self.normalize_helper(q2, q1, word)
            word = self.normalize_helper(a2, a1, word)
            word = self.normalize_helper(ts2, ts1, word)
            return word

        self.normalize_helper(h2, h1)
        self.normalize_helper(h3, h1)
        self.normalize_helper(s2, s1)
        self.normalize_helper(q2, q1)
        self.normalize_helper(a2, a1)
        self.normalize_helper(ts2, ts1)

    def remove_stopwords(self, word=""):
        """
        Removes a predefined stopwords from the corpus.
        """
        stopwords = load_txt_file("stopword_list0.txt")

        if word != "":
            for stopword in stopwords:
                word = word.replace(stopword, "")
            return word

        for stopword in stopwords:
            self.corpus = self.corpus.replace(stopword, "")


# def main():
#     with open("tig_corpus.txt", "r", encoding="utf-8") as file:
#         raw_corpus = file.read()

#     preprocessor = TigMorphPreprocess(raw_corpus)
#     preprocessor.normalize()
#     preprocessor.tokenize()
#     preprocessor.remove_stopwords()

#     with open("processed_tig_corpus.txt", "w", encoding="utf-8") as file:
#         file.write(preprocessor.corpus)


# if __name__ == "__main__":
#     main()
