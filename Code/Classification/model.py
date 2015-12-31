
import argparse
from pprint import pprint
from personClassifier import PersonClassifier
from textClassifier import TextClassifier
import json
import unicodedata
from SPARQLWrapper import SPARQLWrapper, JSON
import sys
sys.path.append("../GetData")
from getSpeeches import getSpeeches

''' This class is the model we use to retrieve the topic distributions per educational background category'''

t = TextClassifier()
''' First determines the educational background of a politician then process the speeches of each politician and aggregates these results.
    Finally the results are aggregated for each category of educational background'''
def main(params):
	# Open politician data
	with open('kaw.json') as data_file:    
	    data = json.load(data_file)

	p = PersonClassifier()
	c_med, c_eng, c_other, c_law, progress = 0,0,0,0,0
	results = {"med":[0,0,0], "eng":[0,0,0], "other":[0,0,0], "law":[0,0,0]}
	for politician in data:
		pclass =  p.classify_person(politician)
		if pclass == "med":
			c_med += 1
		elif pclass == "eng":
			c_eng += 1
		elif pclass == "law":
			c_law += 1		
		else :
			c_other +=1
		p_med,p_eng,p_other = processPolitician(politician['purl'])
		results = add_values(results, [p_med, p_eng, p_other], pclass)
		print ("progress:",1.0*progress/len(data))
		progress += 1
	printResults(c_med,c_eng,c_law,c_other,results)

''' Prints the results of the model'''
def printResults(c_med,c_eng,c_law,c_other,results):
	print ("total meds:",c_med)
	print ("total eng:",c_eng)
	print ("total law:",c_law)
	print ("total other:",c_other)
	print ("med:",divide_array(results['med'],c_med))
	print ("eng:",divide_array(results['eng'],c_eng))
	print ("law:",divide_array(results['law'],c_law))
	print ("other",divide_array(results['other'],c_other))

''' Divides an array by a nominal denominator '''
def divide_array(a, nominator):
	for i in range(len(a)):
		a[i] = (1.0*a[i])/nominator
	return a

''' Adds a 'new' array to the array corresponding to 'pclass' in 'result' '''
def add_values(result, new, pclass):
	ar = result[pclass]
	for i in range(3):
		ar[i] = ar[i] + new[i]
	result[pclass]= ar
	return result

''' Processes the speeches of a single politician '''
def processPolitician(politician):
	speeches = getSpeeches(politician)
	p_med = 0
	p_eng = 0
	p_other = 0
	for speech in speeches:
		s_med, s_eng, s_other = t.classify_text(speech)
		p_med += s_med
		p_eng += s_eng
		p_other += s_other
	total = len(speeches)
	print total
	if total==0:
		return 0,0,0
	else:
		return p_med/total, p_eng/total, p_other/total
    

''' Parses the given arguments'''
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    params = vars(args) # convert to ordinary dict
    main(params)
