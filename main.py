import sklearn
import math
import sys
import re
import os
from node import node
import random

wordDict = {}
testingData = []

def loadsample(txtfile):
    data = ''
    with open(txtfile, "r") as sample:
        data = sample.read().replace('\n', '').lower()
    data = re.sub('[!?]', '.', data)
    data = re.sub('[^\w\.\s]', '', data)
    return data.split('.')

def appendWordTree(data): #takes a writing sample as a list of sentences and adds or increments the paths that those sentences describe to the word tree
    epsilon = 0.02
    for sentence in data:
        wordList =  sentence.split()
        sentenceLength = (len(wordList) -1)
        for index in range(sentenceLength):
            if index < sentenceLength - 3:
                if random.random() < epsilon:
                    testpoint = [wordList[index], wordList[index + 2], wordList[index + 1]]
                    testingData.append(testpoint)
            if index != sentenceLength:
                curWord = wordList[index]
                nextWord = wordList[index + 1]
                if curWord not in wordDict.keys():
                    wordDict[curWord] = node(curWord, index == 0, False)
                if nextWord not in wordDict.keys():
                    wordDict[nextWord] = node(nextWord, False, index + 1 == sentenceLength)
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

def createTreeFromSamplesFolder():
    os.chdir('./samples')
    for sample in os.listdir('.'):
        if sample.endswith('.txt'):
            appendWordTree(loadsample(sample))

def getStartingPoint():
    wordKeys = list(wordDict.keys())
    index = random.randint(0,len(wordDict) -1)
    word = wordDict[wordKeys[index]]
    while not word.startnode:
        index = random.randint(0,len(wordDict) -1)
        word = wordDict[wordKeys[index]]
    return word

def generateRandomSentence():
    word = getStartingPoint()
    sentence = ''
    epsilon = 0.2
    while not word.finalnode:
        sentence += (word.word + ' ')
        if random.random() < epsilon:
            word = word.getRandomPath()
        else:
            word = word.getMostLikelyPath()
    print(sentence + word.word + '.')

def predictMissingWords():
    correct = 0
    for testpoint in testingData:
        prediction = identifyMiddleWord(testpoint[0], testpoint[1])
        print("Prediction: " + prediction + " | Actual: " + testpoint[2])
        if prediction == testpoint[2]:
            correct += 1
    print("Accuracy: ", correct/(len(testingData)))


def main():
    createTreeFromSamplesFolder()
    generateRandomSentence()
    print(len(wordDict))
    predictMissingWords()
    
if __name__ == "__main__":
    main()