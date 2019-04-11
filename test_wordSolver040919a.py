# Author: Robert R Gibson
# Copyright (c) Robert R Gibson, 2019. All rights reserved.
# Developed with python 3.6.3

import wordSolver040919a


def createTestGrid():
    """Create a sample grid for testing. This one has a lot
    of x's on the edges to create strange boundary conditions
    """
    grid = {}
    grid[0] = {0: 's', 1: 'a', 2: 'l', 3: 'x', 4: 'x'}
    grid[1] = {0: 'i', 1: 's', 2: 'e', 3: 'x', 4: 'x'}
    grid[2] = {0: 'g', 1: 'o', 2: 'u', 3: 'x', 4: 'x'}
    grid[3] = {0: 'x', 1: 'x', 2: 'x', 3: 'x', 4: 'x'}
    grid[4] = {0: 'x', 1: 'x', 2: 'x', 3: 'x', 4: 'x'}

    words5 = ['salse', 'sales', 'sials', 'sisal', 'sisel', 'sioux',
              'aleus', 'aisle', 'lasse', 'lasso', 'lassu', 'laise',
              'issue', 'ioxus', 'elais', 'essig', 'gisla', 'gisel',
              'goias', 'ossal', 'ossia', 'osela', 'ousia', 'ousel']
    return grid, words5


def test_noneGrid():
    """grid is None"""
    grid = None
    words = []
    wordLen = 1
    matches = wordSolver040919a.findWords(grid, words, wordLen, False)
    assert(matches is not None)
    assert(len(matches) == 0)


def test_invalidGridType():
    """grid is not a dict"""
    grid = []
    words = []
    wordLen = 1
    matches = wordSolver040919a.findWords(grid, words, wordLen, False)
    assert(matches is not None)
    assert(len(matches) == 0)


def test_emptyGrid():
    """grid is empty dict"""
    grid = {}
    words = []
    wordLen = 1
    matches = wordSolver040919a.findWords(grid, words, wordLen, False)
    assert(matches is not None)
    assert(len(matches) == 0)


def test_noneTestDict():
    """testDict is None"""
    grid, _ = createTestGrid()
    wordLen = 1
    matches = wordSolver040919a.findWords(grid, None, wordLen, False)
    assert(matches is not None)
    assert(len(matches) == 0)


def test_emptyTestDict():
    """testDict is empty"""
    grid, _ = createTestGrid()
    wordLen = 1
    matches = wordSolver040919a.findWords(grid, [], wordLen, False)
    assert(matches is not None)
    assert(len(matches) == 0)


def test_zeroWordLen():
    """Requesting words of zero length"""
    grid, words5 = createTestGrid()
    wordLen = 0
    matches = wordSolver040919a.findWords(grid, words5, wordLen, False)
    assert(matches is not None)
    assert(len(matches) == 0)


def test_findOneLetterWords():
    """Find a list of five-letter words"""
    wordLen = 1
    grid, _ = createTestGrid()
    words1 = ['i', 'o']
    matches = wordSolver040919a.findWords(grid, words1, wordLen, False)
    assert(matches is not None)
    for word in words1:
        assert(word in matches)
    for word in matches:
        assert(word in words1)


def test_findFiveLetterWords():
    """Find a list of five-letter words"""
    wordLen = 5
    grid, words5 = createTestGrid()
    matches = wordSolver040919a.findWords(grid, words5, wordLen, False)
    assert(matches is not None)
    for word in words5:
        assert(word in matches)
    for word in matches:
        assert(word in words5)


# Could add many other edge cases

# Randomized testing would also be good to have; we could create
# a grid on the fly with known words in it and make sure those
# words are all found
