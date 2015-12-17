from SPARQLWrapper import SPARQLWrapper, JSON


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
        polSpeeches.append(speech["text"]["value"])
    return polSpeeches
    

politicians = [{"name": "De Guy", "purl": "http://purl.org/linkedpolitics/EUmember_97058"}]
getSpeeches(politicians)

