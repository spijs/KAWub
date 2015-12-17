from SPARQLWrapper import SPARQLWrapper, JSON


def getSpeeches(politicians):
    polSpeeches = []
    polCount = 0

    for politician in politicians:
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

              FILTER(?speaker = <""" + politician["purl"] + """>)
              FILTER(langMatches(lang(?text), "en"))
            }
        """)
        sparql.setReturnFormat(JSON)

        results = sparql.query().convert()
        count = 0

        newdict = {"name": politician["name"], "purl": politician["purl"]}
        polSpeeches.append(newdict)

        for speech in results["results"]["bindings"]:
            polSpeeches[polCount]["speech" + str(count)] = speech["text"]["value"]
            count += 1

        polCount += 1

    print(polSpeeches)


politicians = [{"name": "De Guy", "purl": "http://purl.org/linkedpolitics/EUmember_97058"}]
getSpeeches(politicians)

