from itertools import product, combinations
from collections import Counter


class Rack:

    def __init__(self, tiles, dd, t):
        self.tiles = tiles.upper()
        self.dd = dd
        self.t = t
        self.num_blanks = tiles.count('?')
        self.num_letters = len(tiles) - self.num_blanks

    def get_choices(self):

        order = "ABCDEFGHIJKLMNOPQRSTUVWXYZ?"
        tiles = ''.join(sorted(self.tiles.upper(), key=lambda item: order.index(item)))

        letters = tiles[:self.num_letters]
        options = list(product(order[:-1], repeat=self.num_blanks))

        res = set([])

        for opt in options:
            word = letters + ''.join(opt)
            res.add(''.join(sorted(word)))

        return res

    def get_subsets(self, choices):

        if not choices:
            return []

        res_set = set([])
        res_list = []

        for n in reversed(range(len(self.tiles))):
            for choice in choices:
                subsets = list(combinations(choice, n+1))
                for subset in subsets:
                    selection = ''.join(subset)
                    if selection not in res_set:
                        res_set.add(selection)
                        res_list.append(selection)

        return res_list

    def permute_solve(self):

        subsets = self.get_subsets(self.get_choices())
        res = []

        for subset in subsets:
            if subset in self.dd.word_map:
                plays = self.dd.word_map[subset]
                for play in plays:
                    res.append(play)
                    self.t -= 1
                    if self.t <= 0:
                        return res

        return res

    def frequency_solve(self):

        tile_freq = Counter(self.tiles)
        res = []

        def match(key_freq):
            mismatch = 0
            for letter in key_freq:
                if key_freq[letter] > tile_freq[letter]:
                    mismatch += key_freq[letter] - tile_freq[letter]
                    if tile_freq['?'] < mismatch:
                        return False
            return True

        for i in range(self.dd.start_index(len(self.tiles)), len(self.dd.counter_list)):
            if match(self.dd.counter_list[i][0]):
                for play in self.dd.word_map[self.dd.counter_list[i][1]]:
                    res.append(play)
                    self.t -= 1
                    if self.t <= 0:
                        return res
        return res
