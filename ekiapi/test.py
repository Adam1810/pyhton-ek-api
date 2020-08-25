

import json


def getUrls ():
        
    with open('config.json', 'r') as f:
        config = json.load(f)

    baseUrl = config['DEFAULT']['baseUrl']
    sortingUrl = config['DEFAULT']['sortingUrl']
    legoUrl = config['DEFAULT']['legoUrl']
    siteUrl = config['DEFAULT']['siteUrl']
    appendUrl = config['DEFAULT']['appendUrl']


    setId = config['SETS']
    urls = []

    for l in setId:

        temp = str(l['setId'])

        new_url = baseUrl + sortingUrl + legoUrl + temp + appendUrl  
        urls.append(new_url)

        if l['site'] > 1:
            new_url = baseUrl + sortingUrl + siteUrl + legoUrl + temp + appendUrl  
            urls.append(new_url)

    return urls

print(getUrls())