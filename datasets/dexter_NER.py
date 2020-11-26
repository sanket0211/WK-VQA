import requests
import json
from pymongo import MongoClient
import wptools
import inspect
import os
import sys
import argparse
import csv
from tqdm import tqdm 
import pdb
parser = argparse.ArgumentParser()

parser.add_argument('--datasetName', type=str, default='wikiVQA', help='the datasetname, eg, wikiVQA-mini, wikiVQA')
parser.add_argument('--whichCap', type=str, default='wikiCap', help='captioning method, eg, msCap, wikiCap')
parser.add_argument('--st', type=int, default=1, help='start image id (counting begins with 1)')
parser.add_argument('--en', type=int, default=50000, help='end image id (included)')
parser.add_argument('--cuda', action='store_true', help='enables cuda')


opt = parser.parse_args()


csvFile = '../phase1AnnCloseList.csv'
outFile = 'ms_cap2_entities_dexter_%s_%s_st%d_en%d.csv' % (opt.datasetName,opt.whichCap,opt.st,opt.en)
print("USAGE EXAMPLE: python3 dexter_NER.py --datasetName wikiVQA --whichCap wikiCap --st 1 --en 71928")


file = open(outFile,"ab")
i=0


#currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# replace current_dir with image caption file directory name instead of code directory name
currentdir = '/scratche/home/sanket/kvqa'

def replace_by_current_directory_name_if_necessary(text):
    
    current_dir = os.path.basename(currentdir) 
    
    if current_dir.replace('_',' ') not in text:
        list_of_words = current_dir.split("_")
        for word in list_of_words:
            if word in text:
                text = text.replace(word, current_dir.replace('_',' '), 1)
                break
    return text

def get_infobox(entity):
    
    page = wptools.page(entity, verbose = False)
    page.get_parse()
    infobox = page.data['infobox']
    #try:
    #   dpURL=page.data['image'][0]['url']
    #except:
    #   dpURL=" "
    return infobox#, dpURL

def get_named_entity_wiki_list(text): 
    
    text = replace_by_current_directory_name_if_necessary(text)
    json0_url = "http://momo.cds.iisc.ac.in:31991/dexter-webapp/api/rest/annotate"
    payload = {'text':text,'wn':False,'debug':False,'format':'text'}

    try:
        resp = requests.post(json0_url, data=payload)
        data = json.loads(resp.text)
        candidates = {}
        id_list = []
        id2title = {}

        c_momo = MongoClient('mongodb://10.24.28.103:27017/')
        wiki_map = c_momo['wikiPageDB']['wikiPageTitle']

        for ele in data['spots']:
            mention, wiki_id = ele['mention'], ele['entity']
            if mention not in candidates:
                candidates[mention] = wiki_id
                id_list.append(wiki_id)

        resp = wiki_map.find({"pageId" : {"$in": id_list}})
        for ele in resp:
            id2title[ele['pageId']] = ele['title']

        entity_list = []
        corresponding_wiki_link_list = []
        #dpURL=[]
        for wiki_id in id_list:
            try:
                info = get_infobox(id2title[wiki_id])
                if "birth_date" in info.keys():
                    entity = id2title[wiki_id]
                    entity_list.append(entity.replace('_',' '))
                    corresponding_wiki_link_list.append("https://en.wikipedia.org/wiki/" + entity)
                    #dpURL.append(dp)
            except:
                continue
        return entity_list, corresponding_wiki_link_list#, dpURL
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        #print(exc_type, fname, exc_tb.tb_lineno)
        return [], []


#text = "Modi with other BRICS leaders in 2016. Left to right: Temer, Modi, Xi, Putin and Zuma."
#list1, list2 = get_named_entity_wiki_list(text)
#print(list1)
#print(list2)
with open(csvFile, 'r') as csvfile:
     spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
     if(opt.whichCap=='wikiCap'):
        included_cols=[3]
     if(opt.whichCap=='msCap'):
       included_cols=[4]
     
     for row in tqdm(spamreader):
        imgPath=row[0]
        #print(imgPath)
        cap = list(row[i] for i in included_cols)
        i=i+1
        if(i < opt.st or i > opt.en):
           continue
        #print(cap)
        cap=', '.join(cap)
        try:

           c='/'
           #print(cap)
           ind=[pos for pos, char in enumerate(imgPath) if char == c]
           wikiName=imgPath[ind[1]+1:ind[2]];
           peopleList,peopleWikiLinks=get_named_entity_wiki_list(cap) #.encode('utf-8'))
           #print(peopleList)
           #peopleList.append(wikiName.replace('_',' '))
           wikiLink="https://en.wikipedia.org/wiki/"+wikiName
           peopleWikiLinks.append(wikiLink)
           peopleList=list(set(peopleList))
           peopleWikiLinks=list(set(peopleWikiLinks))
           peopleList.sort()
           peopleWikiLinks.sort()
           str2write=""
           for item in peopleList:
               str2write=str2write+";"+item
           str2write=str2write+"\t"
           for item in peopleWikiLinks:
               str2write=str2write+";"+item
           str2write=str2write+"\n"
           #for item in dpURL:
           #    str2write=str2write+";"+item
           str2write=str2write+"\n"
           file.write(str2write.encode('utf-8'))
        except:
           #print("in except block")
           nerList="Nothing detected\n"
           file.write(nerList.encode('utf-8'))
file.close()



