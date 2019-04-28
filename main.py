import sklearn
import math
import sys
import re
from node import node

wordDict = {}

def loadsample(txtfile):
    data = ''
    with open(txtfile, "r") as sample:
        data = sample.read().replace('\n', '').lower()
    data = re.sub('[!?]', '.', data)
    data = re.sub('[^[\w\.\s]]', '', data)
    return data.split('.')

def appendWordTree(data): #takes a writing sample as a list of sentences and adds or increments the paths that those sentences describe to the word tree
    for sentence in data:
        wordList =  sentence.split()
        for index in range(len(wordList) -1):
            if index != len(wordList) -1:
                curWord = wordList[index]
                nextWord = wordList[index + 1]
                if curWord not in wordDict.keys():
                    wordDict[curWord] = node(curWord)
                if nextWord not in wordDict.keys():
                    wordDict[nextWord] = node(nextWord)
                wordDict[curWord].addEdge(wordDict[nextWord])

def identifyMiddleWord(start, end):
    startWord = wordDict[start]
    target = end
    possibleguesses = startWord.edgesToTarget(target)
    if len(possibleguesses) > 0:
        maxProb = 0
        currentGuess = ''
        for guess in possibleguesses:
            word = guess[1]
            nextProb = guess[0] * word.getPathProb(target)
            if maxProb < nextProb:
                maxProb = nextProb
                currentGuess = word.word
    return currentGuess


def main():
    sample1 = loadsample("./samples/sample1.txt")
    sample2 = loadsample("./samples/sample2.txt")
    sample3 = loadsample("./samples/sample3.txt")
    sample4 = loadsample("./samples/sample4.txt")
    sample5 = loadsample("./samples/sample5.txt")
    sample6 = loadsample("./samples/sample6.txt")
    sample7 = loadsample("./samples/sample7.txt")
    appendWordTree(sample1)
    appendWordTree(sample2)
    appendWordTree(sample3)
    appendWordTree(sample4)
    appendWordTree(sample5)
    appendWordTree(sample6)
    appendWordTree(sample7)
    print(identifyMiddleWord('which','of'))


if __name__ == "__main__":
    main()