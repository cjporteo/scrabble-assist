from collections import Counter, defaultdict
import pickle


class DictData:

    def __init__(self, filename):
        name = filename.split('.')[0]

        try:
            self.word_map = pickle.load(open(name + "wm.pickle", "rb"))
            self.counter_list = pickle.load(open(name + "cl.pickle", "rb"))
            self.len_ind_map = pickle.load(open(name + "lim.pickle", "rb"))
        except FileNotFoundError:
            self.configure_dict(name)

    def configure_dict(self, name):
        words = [line.rstrip('\n') for line in open(name + ".txt")]
        if name == "collins2015":
            words = words[2:]
        words = sorted(words, key=lambda x: -len(x))

        word_map = defaultdict(list)  # word key : list of valid words (ex. "AER" : ["are", "ear", "era"])
        counter_list = []  # letter frequency counters for every word key - word key is also stored in the item
        len_ind_map = {}  # length : starting index
        ind = 0
        prev_len = 0

        for word in words:
            word = word.upper()
            key = ''.join(sorted(word))
            if not word_map[key]:
                counter_list.append([Counter(key), key])
                if ind == 0:
                    len_ind_map[len(key)] = 0
                elif len(key) < prev_len:
                    len_ind_map[len(key)] = ind
                prev_len = len(key)
                ind += 1
            word_map[key].append(word)

        self.word_map = word_map
        self.counter_list = counter_list
        self.len_ind_map = len_ind_map

        def dump(dat, filename):
            _out = open(filename, "wb")
            pickle.dump(dat, _out)
            _out.close()

        dump(word_map, name + "wm.pickle")
        dump(counter_list, name + "cl.pickle")
        dump(len_ind_map, name + "lim.pickle")

    def start_index(self, length):
        while length not in self.len_ind_map:
            length -= 1
            if length <= 0:
                return len(self.counter_list)
        return self.len_ind_map[length]
