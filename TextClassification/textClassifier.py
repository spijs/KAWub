__author__ = 'thijs'

''' This class is used to derive a topic distribution from a given speech '''
class TextClassifier:

    def __init__(self):
        self.medicalVoc = self.fillVocabulary("medical.txt")
        self.energyVoc = self.fillVocabulary("energy.txt")
        self.stopwords = self.fillVocabulary("stopwords.txt")

    ''' returns a topic distribution for a given string of text'''
    def classify_text(self,text):
        words = self.remove_common_words(str.split(text))
        total = len(words)
        numberOfMedical = self.getNumberOfOccurences(words,self.medicalVoc)
        numberOfEnergy = self.getNumberOfOccurences(words,self.energyVoc)
        #print("total words", total)
        #print("total medical", numberOfMedical)
        #print("total energy", numberOfEnergy)
        return self.classify(numberOfMedical, numberOfEnergy, total)

    ''' Returns a list corresponding to a lexicon file '''
    def fillVocabulary(self,file):
        result = []
        with open(file) as f:
            for line in f:
                result.append(line.rstrip())
        return result

    ''' Counts the number of times a word from 'voc' occurs in 'text' '''
    def getNumberOfOccurences(self, text, voc):
        result = 0
        for word in text:
            if word in voc:
                result += 1
        return result

    ''' Returns a distribution given counts for medical, energy and total'''
    def classify(self, numberOfMedical, numberOfEnergy, total):
        return 1.0*numberOfMedical/total, 1.0*numberOfEnergy/total, 1.0*(total-numberOfMedical-numberOfEnergy)/total
       
    ''' Removes the stop words from a sentence '''
    def remove_common_words(self,sentence):
        result = []
        for word in sentence:
            if not word.lower() in self.stopwords:
                result.append(word.lower())
        return result
