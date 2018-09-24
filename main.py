import os
import pickle
import sys

"""configurations"""
cardsResourcesPath = "E:\\Art\\MTG"
cardFileNamePosfix = ".xlhq.jpg"
deckInputFileName = "deck.txt"
deckOutputFileName = "deck.html"
deckGenerationWorkingDirectory = "."
cardWidth = 375
cardHeight = 525

"""constants"""
cardIndexFileName = "index.cards"
overallTopLevelDirectories = len(os.listdir(cardsResourcesPath))

"""globals"""
processedTopLevelDirectories = 0



class Card:
    "Class for storing card data"
    def __init__(self, cardName, cardSetsList):
        self.cardName = cardName
        self.cardSetsList = cardSetsList

    def getCardName(self):
        return self.cardName

    def getCardSets(self):
        return self.cardSetsList

    def addSetToCard(self, newSet):
        isReallyNewSet = True
        for cardSet in self.cardSetsList:
            if cardSet == newSet:
                isReallyNewSet = False
                break
        
        if isReallyNewSet:
            self.cardSetsList.append(newSet)

class CardIndex:
    cards = []

    def addCard(self, newCard):
        isReallyNewCard = True
        for card in self.cards:
            if card.getCardName() == newCard.getCardName():
                """Newly found cards will always have only one set"""
                newCardSet = newCard.getCardSets()
                card.addSetToCard(newCardSet[0])
                isReallyNewCard = False
                break
        
        if isReallyNewCard:
            self.cards.append(newCard)

    def findCard(self, cardName):
        for card in self.cards:
            if card.getCardName().lower() == (cardName + cardFileNamePosfix).lower():
                return card
        return None

    def dumpCardIndex(self):
        for card in self.cards:
            print("card name: " + card.getCardName())
            print("  Sets:")
            for cardSet in card.getCardSets():
                print("  " + cardSet)



def IndexCards(rootDirectory, cardIndexObject):
    listOfFiles = os.listdir(rootDirectory)
    for foundFile in listOfFiles:
        if os.path.isdir(rootDirectory + "\\" + foundFile):
            IndexCards(rootDirectory + "\\" + foundFile, cardIndexObject)
        else:
            newFoundCard = Card(foundFile, [rootDirectory])
            cardIndexObject.addCard(newFoundCard)
    sys.stdout.write('\r')
    globals()["processedTopLevelDirectories"] += 1
    percentage = globals()["processedTopLevelDirectories"] / globals()["overallTopLevelDirectories"] * 100
    sys.stdout.write(" Processing directories: %d%%" % percentage)

# Format for deck file is number + card name:
# 1 Black Cat
# 4 Zombie
def ComposeDeckPage(deckInputFileName, deckOutputFileName, cardsIndex):
    deckInputFile = open(deckInputFileName, 'r')
    deckOutputFile = open(deckOutputFileName, 'w')

    deckOutputFile.write("<!DOCTYPE html>\n  <html><head>\n    <style> img{float: left} </style>\n  </head>\n    <body>\n")
    
    for line in deckInputFile:
        line = line.rstrip()
        words = line.split(" ")
        amountOfCards = int(words[0])
        words.pop(0)
        cardName = " ".join(words)
        card = cardsIndex.findCard(cardName)
        imageTag = ""
        if card is None:
            imageTag = "Unable to find " + cardName
        else:
            imageTag = "<img src=\"" + card.getCardSets()[0] + "\\" + card.getCardName() + "\" style=\"width:" + str(cardWidth) + "px;height:" + str(cardHeight) + "px;\">"
        
        for i in range(amountOfCards):
            deckOutputFile.write(imageTag + "\n")
    
    deckOutputFile.write("     \n</body>\n</html>")
    deckInputFile.close()
    deckOutputFile.close()



cardsCache = CardIndex()
if os.path.exists(cardIndexFileName):
    readCardsIndexFile = open(cardIndexFileName, 'rb')
    cardsCache.cards = pickle.load(readCardsIndexFile)
    readCardsIndexFile.close()
else:
    processedTopLevelDirectories = 0
    IndexCards(cardsResourcesPath, cardsCache)
    writtenCardIndexFile = open(cardIndexFileName, 'wb')
    pickle.dump(cardsCache.cards, writtenCardIndexFile)
    writtenCardIndexFile.close()

# cardsCache.dumpCardIndex()

ComposeDeckPage(deckGenerationWorkingDirectory + "\\" + deckInputFileName, deckGenerationWorkingDirectory + "\\" + deckOutputFileName, cardsCache)