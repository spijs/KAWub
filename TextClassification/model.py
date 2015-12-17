import json
import unicodedata
import argparse
from pprint import pprint
from personClassifier import PersonClassifier
from textClassifier import TextClassifier
from SPARQLWrapper import SPARQLWrapper, JSON

t = TextClassifier()

def main(params):
	with open('kaw.json') as data_file:    
	    data = json.load(data_file)

	p = PersonClassifier()
	c_med = 0
	c_eng = 0
	c_other = 0
	c_law = 0
	results = {"med":[0,0,0], "eng":[0,0,0], "other":[0,0,0], "law":[0,0,0]}
	progress = 0

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
	print ("total meds:",c_med)
	print ("total eng:",c_eng)
	print ("total law:",c_law)
	print ("total other:",c_other)
	print ("med:",divide_array(results['med'],c_med))
	print ("eng:",divide_array(results['eng'],c_eng))
	print ("law:",divide_array(results['law'],c_law))
	print ("other",divide_array(results['other'],c_other))

def divide_array(a, nominator):
	for i in range(len(a)):
		a[i] = (1.0*a[i])/nominator
	return a

def add_values(result, new, pclass):
	ar = result[pclass]
	for i in range(3):
		ar[i] = ar[i] + new[i]
	result[pclass]= ar
	return result

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

def getSpeeches(politician):
    polSpeeches = []
    sparql = SPARQLWrapper("http://linkedpolitics.ops.few.vu.nl/sparql/")
    sparql.setQuery("""
        PREFIX lpv: <http://purl.org/linkedpolitics/vocabulary/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX dbp: <http://dbpedia.org/property/>

        SELECT DISTINCT ?text
        WHERE {
          ?speech lpv:text ?text.
          ?speech lpv:speaker ?speaker.

          FILTER(?speaker = <""" + politician + """>)
          FILTER(langMatches(lang(?text), "en"))
        }
    """)
    sparql.setReturnFormat(JSON)

    results = sparql.query().convert()


    for speech in results["results"]["bindings"]:
    	text = speech["text"]["value"]
    	text = text.encode("utf-8")
        polSpeeches.append(text)
    return polSpeeches
    

''' Parses the given arguments'''
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    params = vars(args) # convert to ordinary dict
    main(params)
