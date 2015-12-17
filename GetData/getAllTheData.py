from SPARQLWrapper import SPARQLWrapper, JSON
import json

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
print(results1["results"]["bindings"])

for result in results1["results"]["bindings"]:
    newdict = {"name":result["name"]["value"], "purl":result["speaker"]["value"], "dbpedia": result["dbpedia"]["value"]}
    politicians.append(newdict)

print("Fetching abstracts for each politician")
for politician in politicians:
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
            SELECT ?abstract
            WHERE {
                <""" + politician["dbpedia"] + """> dbo:abstract ?abstract.
            }
    """)
    # FILTER(langMatches(lang(?abstract), "en"))
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    if results["results"]["bindings"]:
        count = 0
        while count < len(results["results"]["bindings"]):
            if results["results"]["bindings"][count]["abstract"]["xml:lang"] == 'en':
                politician["abstract"] = results["results"]["bindings"][count]["abstract"]["value"]
                print(politician["abstract"])
            count += 1

print("Fetching dbp:profession for each politician")
for politician in politicians:
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
            SELECT ?profession
            WHERE {
                <""" + politician["dbpedia"] + """> dbp:profession ?profession.
            }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    if results["results"]["bindings"]:
        count=0
        while count < len(results["results"]["bindings"]):
            politician["profession"+str(count)] = results["results"]["bindings"][count]["profession"]["value"]
            count += 1

print("Fetching rdf:type for each politician")
for politician in politicians:
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
            SELECT ?type
            WHERE {
                <""" + politician["dbpedia"] + """> rdf:type ?type.
            }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    if results["results"]["bindings"]:
        count = 0
        while count < len(results["results"]["bindings"]):
            politician["type"+str(count)] = results["results"]["bindings"][count]["type"]["value"]
            count += 1

print("Fetching dbo:almaMater for each politician")
for politician in politicians:
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
            SELECT ?dboAlmaMater        
            WHERE {
                <""" + politician["dbpedia"] + """> dbo:almaMater ?dboAlmaMater.
            }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    if results["results"]["bindings"]:
        count=0
        while count < len(results["results"]["bindings"]):
            politician["dboAlmaMater"+str(count)] = results["results"]["bindings"][count]["dboAlmaMater"]["value"]
            count += 1

print("Fetching rdfs:comment for each politician")
for politician in politicians:
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
            SELECT ?comment
            WHERE {
                <""" + politician["dbpedia"] + """> rdfs:comment ?comment.
            }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    if results["results"]["bindings"]:
        count = 0
        while count < len(results["results"]["bindings"]):
            if results["results"]["bindings"][count]["comment"]["xml:lang"] == 'en':
                politician["comment"+str(count)] = results["results"]["bindings"][count]["comment"]["value"]
            count += 1

fo = open("kaw_data.json", "w+")
fo.write(json.dumps(politicians, separators=(',', ':')))
fo.close()
