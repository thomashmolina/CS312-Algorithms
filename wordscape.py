import sys
import copy


class WordScape:
    def __init__(self, letters):
        word_path = '/usr/share/dict/words'
        with open(word_path, 'r') as readfile:
            self.dictionary = list(set([x.upper() for x in readfile.read().splitlines()]))
        self.letters = [x.upper() for x in letters]
        self.organized_words = {}

    def get_words(self, num_letters):
        words = list(filter(lambda x: (len(x) == num_letters), self.dictionary))
        new_words = [x.upper() for x in words if self.word_has_letters(x)]
        self.organized_words[num_letters] = sorted(new_words)
        return new_words

    def word_has_letters(self, word):
        letters = list(copy.deepcopy(self.letters))
        for char in word:
            if char not in letters:
                return False
            letters.remove(char)
        return True



if __name__ == "__main__":
    args = sys.argv[1:]
    min_chars = int(args[0])
    letters = [x.upper() for x in list(args[1])]
    w = WordScape(letters)
    words = []
    for lengths in range(min_chars, len(letters)+1):
        words += w.get_words(lengths)
    for key, value in w.organized_words.items():
        print(f"{key}: {', '.join(value)}")
    #print('\n'.join(sorted(w.dictionary)))
    #print(len(w.dictionary))

