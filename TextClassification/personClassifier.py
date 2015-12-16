class PersonClassifier:

    def __init__(self):
        self.medicalVoc = self.fillMedical()
        self.engineerVoc = self.fillEngineer()

    def fillMedical(self):
        return ["health","medic","nurse","bio","healthcare","doctor ", "MD"]

    def fillEngineer(self):
        return ["engineer","physic","scientist","technology" "chemic","material","energy","computer","mathematics"]

    def classify_text(self,text):
        med = 0
        eng = 0
        for medWord in self.medicalVoc:
            if medWord in text:
                med += 1
        for engWord in self.engineerVoc:
            if engWord in text:
                eng += 1
        return med, eng

    def classify_person(self, person):
        med = 0
        eng = 0
        for item in person:
            med2, eng2 = self.classify_text(person[item])
            med += med2
            eng += eng2
        if med > eng:
            return "med"
        elif med < eng:
            return "eng"
        elif eng > 0:
            return "eng"
        else:return "other"


