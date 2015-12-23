'''This class is used to classify the educational background of a person'''

class PersonClassifier:

    def __init__(self):
        self.medicalVoc = self.fillMedical()
        self.engineerVoc = self.fillEngineer()
        self.lawVoc = self.fillLawyer()

    ''' Fills the medical dataset'''
    def fillMedical(self):
        return ["health","medic","nurse","bio","healthcare","doctor ", "MD","hospital"]

    ''' Fills the engineering dataset'''
    def fillEngineer(self):
        return ["engineer","physic","scientist","technology" "chemi","material","energy","computer","mathematics"]

    ''' Fills the law dataset'''
    def fillLawyer(self):
        return ["law","lawyer","rights", "jugdge", "justice", "court", "prosecut", "attorney"]

    ''' Classifies and counts the words in the medical, engineer or law dataset'''
    def classify_text(self,text):
        med = 0
        eng = 0
        law = 0
        for medWord in self.medicalVoc:
            if medWord in text:
                med += 1
        for engWord in self.engineerVoc:
            if engWord in text:
                eng += 1
        for lawWord in self.lawVoc:
            if lawWord in text:
                law += 1
        return med, eng, law

    ''' Classifies a person in either medical, engineer, law or other'''
    def classify_person(self, person):
        med = 0
        eng = 0
        law = 0
        for item in person:
            med2, eng2, law2 = self.classify_text(person[item])
            med += med2
            eng += eng2
            law += law2
        if med > eng and med > law:
            return "med"
        elif law > eng and law > med:
            return "law"
        elif eng > law and eng > med:
            return "eng"
        else:return "other"


