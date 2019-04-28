class node:
    def addEdge(self, wordNode):
        self.frequency += 1
        if wordNode.word in self.paths.keys():
            self.paths[wordNode.word][1] += 1
        else:
            self.paths[wordNode.word] = [wordNode, 1]

    def print(self):
        print(self.word)

    def canReach(self, target):
        if target in self.paths.keys():
            return True
        else:
            return False
    
    def getPathProb(self, target):
        if target in self.paths.keys():
            return self.paths[target][1] / self.frequency
        else:
            return 0

    def edgesToTarget(self, target):
        edges = list(self.paths.values())
        edges.sort(key=lambda x: x[1]) #sort the edges that the word can take based on frequence lowest to largest
        edges.reverse()
        returnedges = []
        for edge in edges:
            if edge[0].canReach(target):
                returnedges.append((edge[1] / self.frequency, edge[0]))
        return returnedges



    def __init__(self, word):
        self.frequency = 0
        self.word = word
        self.paths = {}
