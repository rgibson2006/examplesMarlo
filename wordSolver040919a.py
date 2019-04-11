# Author: Robert R Gibson
# Copyright (c) Robert R Gibson, 2019. All rights reserved.
# Developed with python 3.6.3

import copy


def findWordCandidates(moves, lastMoveI, lastMoveJ, lastWord, targetLen, grid, foundWords, debug=False):
    """Recursively identify all potential words in an N-by-N grid of letters. The list of candidates
    returned can be screened against any dictionary to identify matches. While optimizations are possible,
    we prefer readability and maintainability for this code. If speed is an issue (e.g., for larger
    grids), we could optimize by passing in the word dictionary as a trie and eliminating word
    candidates as soon as they are not represented in the dictionary.

    Another possible improvement is to store all of the current word candidates at a given iteration
    stage. Simply add them to the foundWords list if they are not in the list already. However, the
    puzzle we are solving specifies word length up front.

    ARGS:
        IN moves: 2D array of flags indicating whether a grid spot has already been visited
        IN (lastMoveI, lastMoveJ): the (x, y) coordinates of the last letter chosen from the grid
        IN lastWord: the word we are currently building in this invocation
        IN targetLen: when we reach this length, our candidate word is finished
        IN grid: N-by-N grid of letters
        OUT foundWords: list of word candidates that have been found
        IN debug=False: if True, will print formatted debug statements
    """
    # Prefix of whitespaces for logging messages to indicate recursion depth for readability
    prefix = ' ' * len(lastWord)
    if debug:
        print('{}moves: {}, lastMoveI: {}, lastMoveJ: {}, lastWord: {}'.format(prefix, moves, lastMoveI, lastMoveJ, lastWord))

    # Example of a sanity check: make sure the recorded history of "moves" matches the length
    # of the current word candidate we are processing. Sum up the moves 2D grid to get the
    # count of moves, since a "1" means the move was taken, "0" means not taken.
    sumMoves = sum(map(sum, moves))
    if sumMoves != len(lastWord):
        raise ValueError('{}Sanity check fail: moves does not match lastWord len'.format(prefix))

    # Check that grid is square. We could easily relax this constraint for non-square grids.
    gridSize = len(grid.keys())
    for k in grid.keys():
        if len(grid[k]) != gridSize:
            raise ValueError('Grid is not square: {}'.format(grid))

    # If our candidate word has reached the target length, we can record it and stop recursing
    if len(lastWord) == targetLen:
        if lastWord not in foundWords:
            foundWords.append(lastWord)
        return

    # Loop through all possible adjacent positions to the last position we considered. If that position
    # has already been checked, skip it. Otherwise, append the letter at that position and recurse.
    tryI = -1
    tryJ = -1
    for i in range(-1, 2):
        for j in range(-1, 2):
            # Create copies of key variables that we can pass to the next call so they can be
            # modified independently
            curLastMoveI = copy.deepcopy(lastMoveI)
            curLastMoveJ = copy.deepcopy(lastMoveJ)
            curMoves = copy.deepcopy(moves)
            curWord = copy.deepcopy(lastWord)

            # Calculate (tryI, tryJ), which is the next grid space to consider. If it is not valid
            # (e.g., off the grid or already tried), then skip that position.
            tryI = curLastMoveI + i
            tryJ = curLastMoveJ + j
            if tryI < 0 or tryI > (gridSize-1):
                continue
            if tryJ < 0 or tryJ > (gridSize-1):
                continue
            if debug:
                print('{}i: {}, j: {}, lastMoveI: {}, lastMoveJ: {}, tryI: {}, tryJ: {}, lastWord: {}, wouldbe: {}'.format(
                    prefix, i, j, lastMoveI, lastMoveJ, tryI, tryJ, lastWord, curWord+grid[tryI][tryJ]))
            if (curMoves[tryI][tryJ] == 1):
                # This spot has already been visited
                if debug:
                    print('{}spot is already visited, curMoves: {}'.format(prefix, curMoves))
                continue

            # Update the list of moves and the current candidate word to add in the letter
            # at (tryI, tryJ)
            if debug:
                print('{}tryI: {}, tryJ: {}, adding: {} to make {}'.format(prefix, tryI, tryJ, grid[tryI][tryJ], curWord))
            curWord += grid[tryI][tryJ]
            curMoves[tryI][tryJ] = 1
            # Call recursively with the updated word and list of moves
            findWordCandidates(curMoves, tryI, tryJ, curWord, targetLen, grid, foundWords, debug)
    if debug:
        print('{}returning with lastWord: {}, curWord: {}'.format(prefix, lastWord, curWord))


def findWords(grid, testDict, targetLen, debug=False):
    """Search a square grid of letters for candidate words. Match the words against a dictionary
    of known words and print out any matches. See comments to findWordCandidates for suggestions
    for optimization.

    IN grid: an N-by-N grid of letters to search for words
    IN testDict: a list of approved words; candidates from the grid will be matched against this
    IN targetLen: only consider words of this length
    IN debug=False: if True, log debugging info as we go
    """
    if grid is None or not isinstance(grid, dict):
        return []
    if testDict is None or len(testDict) < 1:
        return []
    if targetLen < 1:
        return []

    # Check that grid is square. We could easily relax this constraint for non-square grids.
    gridSize = len(grid.keys())
    for k in grid.keys():
        if len(grid[k]) != gridSize:
            raise ValueError('Grid is not square: {}'.format(grid))
    if gridSize < 1:
        return []

    # foundWords will accumulate all word candidates from successive invocations
    foundWords = []

    # Start a recursive search from each point on the grid, accumulating candidates as we go
    for i in range(gridSize):
        for j in range(gridSize):
            # Create a new copy of a 2D grid of zeroes to hold moves as they are taken
            moves = []
            for m in range(gridSize):
                moves.append([0 for n in range(gridSize)])
            # Mark the position and letter of the first move, then start recursing
            moves[i][j] = 1
            lastWord = grid[i][j]
            findWordCandidates(moves, i, j, lastWord, targetLen, grid, foundWords, debug)

    matches = []
    for foundWord in foundWords:
        if foundWord in testDict:
            print('Match: {}'.format(foundWord))
            matches.append(foundWord)
    if debug and len(matches) == 0:
        print('No matches found')
    return matches
