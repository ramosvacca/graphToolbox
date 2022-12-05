import json
import requests

response = requests.get('https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=json&titles=Non-steroidal_anti-inflammatory_drug&rvsection=0&rvparse')

toparse = response.json()

page_one = next(iter(toparse['query']['pages'].values()))
revisions = page_one.get('revisions', [])
html = next(iter(revisions[0].values()))

#print(html)

from bs4 import BeautifulSoup

filetoread = '/media/newbuntu/rdfal/rx-dron/wikisearch.json'

folderToSave = "/media/newbuntu/rdfal/rx-dron/"
fileName = folderToSave + 'wikiSearch.ttl'
fileToSave = open(fileName, 'w+')

# Opening JSON file
f = open(filetoread)

# returns JSON object as
# a dictionary
data = json.load(f)
n = 0
# Iterating through the json
# list. For each value will execute the search in wikipedia
m=0
for i in data['results']['bindings']:
    uri_value = i["s"]["value"]
    search_value = i['wikiSearch']['value']

    response = requests.get(
        'https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=json&titles={}&rvsection=0&rvparse'.format(search_value))

    toparse = response.json()

    try:
        page_one = next(iter(toparse['query']['pages'].values()))
        revisions = page_one.get('revisions', [])
        html = next(iter(revisions[0].values()))

        parsed_html = BeautifulSoup(html, features="html.parser")
        table = parsed_html.find('table', attrs={'class':'infobox'}).find('tbody')

        # The first tr contains the field names.

        datasets = []
        for row in table.find_all("tr")[1:]:
            #print(row)
            headings = [th.get_text().strip() for th in row.find_all("th")]
            dataset = dict(zip(headings, (td.get_text() for td in row.find_all("td"))))
            datasets.append(dataset)
        #print(datasets)

        for dataset in datasets:
            #print(dataset)
            for field in dataset:
                fileToSave.write('<{}> <urn:stardog:drugs:{}> """{}""" . '.format(uri_value, field.replace(" ","_"), dataset[field]))
            print(m,n)
            n+=1
        m += 1
        #print(datasets)
    except:
        print('No salió')
