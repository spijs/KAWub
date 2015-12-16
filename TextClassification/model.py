import json
import argparse
from pprint import pprint
from personClassifier import PersonClassifier
from textClassifier import TextClassifier

t = TextClassifier()

def main(params):
	with open('kaw.json') as data_file:    
	    data = json.load(data_file)

	p = PersonClassifier()
	med = 0
	eng = 0
	other = 0
	for politician in data:
		pclass =  p.classify_person(politician)
		if pclass == "med":
			med += 1
		elif pclass == "eng":
			eng += 1
		else :
			other +=1
		processPolitician(politician['purl'], pclass)

	print ("med:",med)
	print ("eng:",eng)
	print ("other",other)



def processPolitician(politician, pclass):
	speeches = getSpeeches(politician)
	p_med = 0
	p_eng = 0
	p_other = 0
	for speech in speeches:
		s_med, s_eng, s_other = t.classify_text(speech)
		p_med += s_med
		p_eng += s_eng
		p_other += s_other
	usePoliticianData(pclass, p_med, p_eng, p_other)

def usePoliticianData(pclass, p_med, p_eng, p_other):
	print ('politician: ',pclass)
	#print ('p_med:', p_med)
	#print ('p_eng:', p_eng)
	#print ('p_other:', p_other)


# TODO remove
def getSpeeches(politician):
	return ["this is an example speech with one medical word"]

''' Parses the given arguments'''
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    params = vars(args) # convert to ordinary dict
    main(params)