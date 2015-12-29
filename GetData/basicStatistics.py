from SPARQLWrapper import SPARQLWrapper, JSON
import json
import collections
import pprint

def prefixes():
    return """
        PREFIX lpv: <http://purl.org/linkedpolitics/vocabulary/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX dbp: <http://dbpedia.org/property/>
        PREFIX lp: <http://purl.org/linkedpolitics/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX type: <http://dbpedia.org/class/yago/>
        """

def printCount(name, results):
    print(name)
    print(results["results"]["bindings"][0]["count"]["value"])

def numberOfSpeakers():

    sparql = SPARQLWrapper("http://linkedpolitics.ops.few.vu.nl/sparql/")
    sparql.setQuery(prefixes()+
        """
        SELECT (count(DISTINCT ?speaker) as ?count)
        WHERE {
            ?speech lpv:speaker ?speaker.
        }
        """
    )
    sparql.setReturnFormat(JSON)

    results = sparql.query().convert()
    printCount("Speakers in ToE", results)
#
# def numberOfSpeechlessMeps():
#
#     sparql = SPARQLWrapper("http://linkedpolitics.ops.few.vu.nl/sparql/")
#     sparql.setQuery(prefixes()+
#         """
#         SELECT (count(?member) as ?count)
#         WHERE {
#             SELECT ?member (count(?speech) as ?speechCount)
#             WHERE {
#                 ?member rdf:type ?type.
#                 ?speech lpv:speaker ?member.
#                 filter(?type = "MemberOfParliament")
#             } Group by ?member
#         }
#         """
#     )
#     sparql.setReturnFormat(JSON)
#     results = sparql.query().convert()
#     printCount("Speechless MEPS", results)

def numberOfMepsWithDbpediaPage():

    sparql = SPARQLWrapper("http://linkedpolitics.ops.few.vu.nl/sparql/")
    sparql.setQuery(prefixes()+
        """
        SELECT (count(DISTINCT ?speaker) as ?count)
        WHERE {
            ?speech lpv:speaker ?speaker.
            ?speaker foaf:name ?name.
            ?speaker owl:sameAs ?dbpedia.
            filter( regex(str(?dbpedia), "http://dbpedia" ))
        }
        """
    )
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    printCount("ToE Speakers with DBPedia page", results)

def averageNumberOfSpeechesPerDBpediaMep():

    sparql = SPARQLWrapper("http://linkedpolitics.ops.few.vu.nl/sparql/")
    sparql.setQuery(prefixes()+
    """
        SELECT (avg(?count) as ?average)
        WHERE{
            SELECT ?speaker (count(?speech) as ?count)
            WHERE {
                ?speech lpv:speaker ?speaker.
                ?speaker foaf:name ?name.
                ?speaker owl:sameAs ?dbpedia.
                filter( regex(str(?dbpedia), "http://dbpedia" ))
            }
            GROUP BY ?speaker
        }
    """)
    sparql.setReturnFormat(JSON)
    print("Average speeches per MEP")
    results = sparql.query().convert()
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(results["results"]["bindings"])
    print(results["results"]["bindings"][0]["average"]["value"])


def averageNumberOfSpeechesPerMep():

    sparql = SPARQLWrapper("http://linkedpolitics.ops.few.vu.nl/sparql/")
    sparql.setQuery(prefixes()+
    """
        SELECT (avg(?count) as ?average)
        WHERE{
            SELECT ?speaker (count(?speech) as ?count)
            WHERE {
                ?speech lpv:speaker ?speaker.
            }
            GROUP BY ?speaker
        }
    """)
    sparql.setReturnFormat(JSON)
    print("Average speeches per MEP")
    results = sparql.query().convert()
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(results["results"]["bindings"])
    print(results["results"]["bindings"][0]["average"]["value"])

'''process dbpedia fields for statistics'''
def processStatistics(stats, *args):

    results = {}
    for arg in args:
        numbersonly = flatten(stats, arg)
        results[arg] = processStat(numbersonly)
    return results

def flatten(stats, arg):
    r = []
    for politicianName in stats:
        r.append(stats[politicianName][arg])
    return r

def processStat(l):
    Stat = collections.namedtuple('Stat', ['minimum', 'average', 'maximum', 'empties'])
    return Stat(min(l), round(sum(l)/float(len(l)),4), max(l), l.count(0))

if __name__ == "__main__" :
    numberOfSpeakers()
    # numberOfSpeechlessMeps()
    averageNumberOfSpeechesPerMep()
    numberOfMepsWithDbpediaPage()
    averageNumberOfSpeechesPerDBpediaMep()
