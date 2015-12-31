from SPARQLWrapper import SPARQLWrapper, JSON
import json
from sys import stdout
from basicStatistics import *
import pprint

def getDbpediaLinksForPoliticians():

    politicians = []

    sparql = SPARQLWrapper("http://linkedpolitics.ops.few.vu.nl/sparql/")
    sparql.setQuery("""
        PREFIX lpv: <http://purl.org/linkedpolitics/vocabulary/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX dbp: <http://dbpedia.org/property/>

        SELECT DISTINCT ?name ?speaker ?dbpedia
        WHERE {
            ?speech lpv:speaker ?speaker.
            ?speaker foaf:name ?name.
            ?speaker owl:sameAs ?dbpedia.
            filter( regex(str(?dbpedia), "http://dbpedia" ))
        }
    """)
    sparql.setReturnFormat(JSON)
    print("Fetching politicians and their dbpedia link")
    results1 = sparql.query().convert()
    # print(results1["results"]["bindings"])

    for result in results1["results"]["bindings"]:
        newdict = {"name":result["name"]["value"], "purl":result["speaker"]["value"], "dbpedia": result["dbpedia"]["value"]}
        politicians.append(newdict)

    return politicians

def fetch(politician, prefix, field):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
            SELECT ?field
            WHERE {
                <""" + politician["dbpedia"] + """> """+prefix+""":"""+field+""" ?field.
            }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    global stats
    stats[politician["name"]][field] = len(results["results"]["bindings"])

    if results["results"]["bindings"]:
        count=0
        while count < len(results["results"]["bindings"]):
            politician[field+str(count)] = results["results"]["bindings"][count]["field"]["value"]
            count += 1

    # print("return "+field)
    return politician


stats = {}

politicians = getDbpediaLinksForPoliticians()

print("Fetching dbpedia fields for each politician")
progress = 0.0
for politician in politicians:
    stdout.write("Download progress: %d%%  (%d/%d) \r" % ((100*progress)/len(politicians), progress, len(politicians)) )
    stdout.flush()

    stats[politician["name"]] = {}

    fetch(politician, "dbo", "abstract")
    fetch(politician, "dbp", "profession")
    fetch(politician, 'rdf', 'type')
    fetch(politician, "dbo", "almaMater")
    fetch(politician, "rdfs", "comment")

    progress = progress + 1

    # if(progress > 10):
        # break

# calculate statistics
stats = processStatistics(stats, "abstract", "profession", "type", "almaMater", "comment")
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(stats)

fo = open("kaw.json", "w+")
fo.write(json.dumps(politicians, separators=(',', ':')))
fo.close()
