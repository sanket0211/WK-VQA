import urllib
import requests
from os import listdir
from os.path import isfile, join

list_images=[]
for f in listdir('../data/entity_images'):
    f=f.split('.')
    f=f[0]
    #print f
    list_images.append(f)

cnt=1
f=open('new_entity_list.csv', 'r')
for line in f.readlines():
    line=line[:-1]
    print(cnt)
    line=line.replace(" ", "_")
    cnt=cnt+1
    try:
        f2=open('../../wikiAttributesExtr/'+ line+'.csv')
    except:
        continue
    for l in f2.readlines():
        l=l[:-1]
        l=l.split('\t')
        if l[0]=='Img':
            try:
                #urllib.urlretrieve(l[1], line+'.jpg')
                #print l[1]
                if l[1]=='NOT-AVAILABLE':
                    continue
                with open('../data/entity_images/'+urllib.unquote(line)+'.jpg', 'wb') as handle:
                    #print(l[1])
                    response = requests.get(l[1], stream=True)

                    if not response.ok:
                        print(response)
                    for block in response.iter_content(1024):
                        if not block:
                            break

                        handle.write(block)

            except:
                continue

