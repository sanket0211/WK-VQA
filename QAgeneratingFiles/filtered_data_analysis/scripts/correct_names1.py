import bs4
import requests
import requests
from bs4 import BeautifulSoup
import re
import urlparse
import urllib2 
f=open('../person_data_missing.csv','r')
#f2=open('wiki_data_req_persons.csv','w')
f2=open('../wiki_data_req_persons_sportsperson.csv','w')
for line in f.readlines():
    line = line[:-1]
    print line
    page = requests.get("https://www.google.dz/search?q="+line+" sportsperson wikipedia")
    soup = BeautifulSoup(page.content)
    links = soup.findAll("a")
    for link in  soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
        url = re.split(":(?=http)",link["href"].replace("/url?q=",""))
        #url = urlparse.parse_qsl(url)
        #print url[0].encode("utf-8")
        url=url[0].split('&')
        url = url[0].split('/')
        #print url[len(url)-1]
        #print type(url[len(url)-1])
        strtowrite=url[len(url)-1]
        #print urllib2.unquote(strtowrite).decode("UTF-8")
        f2.write(urllib2.unquote(strtowrite).decode("UTF-8")+'\n')
        break



    

