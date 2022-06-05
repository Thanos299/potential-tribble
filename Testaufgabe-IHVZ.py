#!/usr/bin/env python3

# How to use:
# 1) Download website (with wget, curl, firefox …)
# 2) pass file name as arg1 to this script

import sys
import json


try:
    from bs4 import BeautifulSoup
except ImportError:
    print('Beautiful Soup 4 is not installed!')
    sys.exit(1)
    

if len(sys.argv) > 1:
    try:
        file = open(sys.argv[1])
    except FileNotFoundError:
        raise FileNotFoundError(f'File {sys.argv[1]} does not exist')
else:
    raise AttributeError('Please Specify A File')

# get the html into python
beauty = BeautifulSoup(file.read(), 'html.parser')
file.close()

release = str(beauty.select_one('.issue-title').string).strip()
release_tmp = release.split()[1]
release_no =  int(release_tmp.split('/')[0])
release_year =  int(release_tmp.split('/')[1])
del release_tmp

results = []

for element in beauty.select('.teaser'):
    entry = {}
    entry["Ausgabe"] = release_no

    datekategory = str(element.select_one('p').string).strip()
    entry["Datum"] = datekategory.split('|')[0].strip()

    entry["Jahr"] = release_year
    entry["Kategorie"] = datekategory.split('|')[1].strip()

    entry["Titel"] = str(element.select_one('h5').string).strip()

    authors = element.select_one('div')
    if authors:
        entry["Autoren"] = str(authors.string).strip()

    url = element.select_one('a')['href']
    entry["URL"]= 'https://www.springerprofessional.de' + url

    results.append(entry)
    
print(json.dumps(results, ensure_ascii=False, indent=4))
