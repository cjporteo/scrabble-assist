# Scrabble Assist Tool
## About
This tool takes a tileset as input and returns valid words sorted by word length in descending order. Blank tiles are represented with ``?``. There no limit to the number of tiles or blanks inputted to the solver, the script will dynamically switch between two solving algorithms to ensure minimal runtime.

## Installation and Usage:
To install:
<br>

``$ git clone https://github.com/cjporteo/scrabble-assist``

<br>

Included are two dictionaries, the Collins 2015 Scrabble Dictionary and a Master Word List, containing all the words from *a* to *zwitterionic*.

<br>

To boot the script:
``$ python Scrabble/scrabble.py``

<br>

There 3 optional command line arguments:

 - dictionary to be used, either ``collins15`` or ``master`` - **Default**: ``collins15``
 - number of total results to output - **Default**: ``45``
 - number of rows displayed  - **Default**: ``15``

Upon seeing a dictionary for the first time, the script will configure some useful data structures to use for anagram searching. This will take a few seconds to complete, and the objects will be serialized and written to local storage as *pickles*. When this dictionary is called again in the future, the *pickles* will be imported for use.

The program will then prompt you to enter a tileset. Enter letters only (upper case and lower case are both valid) and use ``?`` to denote blank tiles. The program will choose the algorithm that leads to optimal runtime and find the best words you can make.

Results are displayed to the terminal, along with runtime statistics.

Word prompting will continue until ``0`` is inputted to exit the utility.

![](https://scontent.fybz2-2.fna.fbcdn.net/v/t1.15752-9/69898963_1193142634206359_5133116402739183616_n.png?_nc_cat=104&_nc_oc=AQkIFHIAhh4y-SiqEQJ1XcUVOm71cOu10iNo_4qoMUZWq8sJFMHk0hC7SwEnssMjCt0&_nc_ht=scontent.fybz2-2.fna&oh=9f74d25d1922e928bfe84dab262ba85b&oe=5E0D7A7A)

## Algorithms

First, let's talk about the aforementioned data structures that were created when initializing the dictionary. 

We start by sorting the dictionary by word length, descending.

We then iterate through the dictionary, creating a word hashmap.
This hashmap uses lexicographically sorted tilesets (A to Z) as keys, and a list of all valid word with that tileset as values.

**Example:**
```"AER" : ["are", "ear", "era"]```

The next data structure needed is a counter list, a list of ``Counter`` objects storing the letter frequency for each key in the word hashmap.

The last data structure is we need is the most simple one, a length to index hashmap. The key here will be wordmap key length, and the value will be the first index in the wordlist where this word length is seen.

With these 3 data structures, we have all the dictionary information necessary to be speedy with our anagrams.

### P-Solve (Permutation Solve):

This method is quicker for short tilesets containing ~2 or less blank tiles. Blank tiles will complicate things factorially.

First, we process any blank tiles by making a hashset holding all possible realizations of the tileset.

``"ABC?"`` becomes ``["ABCA", "ABCB", "ABCC", "ABCD", ... ,"ABCZ"]``
<br>
For each element in the hashset, we sort the tiles lexicographically and consider all combinations we could make.

For each combination, we simply check if the entry exists as a key in the wordmap. If it exists, each word in ``wordmap[key]`` can be played.

### F-Solve (Frequency Solve):

This algorithm uses a **way** simpler approach. We just run through the wordmap looking at ``Counter`` objects for each key, and if the count of each letter in our tileset is greater than or equal to the count of each letter in the key ``Counter``, we can make all words at ``wordmap[key]``. Each blank tile in our tileset contributes one degree of lenience for matching the ``Counter``.

We use the length to index hashmap to reduce our search. If our tileset is length 8, for example, there is no point considering word keys that have 9 more letters, we know we **cannot** make any of them. Don't bother searching them.

### Choosing Between Them
Edge case testing was conducted to find the cutoff points between algorithms. Number of blanks and number of standard letters in the tileset were the parameters. It turns out that any more than 2 blanks and **F-Solve** starts beating **P-Solve** fairly convincingly. The exact cutoffs are more particular than that, but that's the general idea. For in-game scenarios, P-Solve will almost always be used since the game of Scrabble only has 2 blank tiles. Implementing F-solve was a pretty academic exercise, but interesting nonetheless.
