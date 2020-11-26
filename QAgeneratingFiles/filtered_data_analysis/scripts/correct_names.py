import bs4
import requests
from bs4 import BeautifulSoup
import re
import urllib2 
f=open('person_not_found.csv','r')
f2=open('../wiki_data_req_persons.csv','w')
#f2=open('../wiki_data_req_persons_actors.csv','w')
for line in f.readlines():
    line = line[:-1]
    page = requests.get("https://www.google.dz/search?q="+line+" wikipedia")
    print page
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
        print (url)
        print (urllib2.unquote(strtowrite).decode("UTF-8"))

        f2.write(urllib2.unquote(strtowrite).decode("UTF-8")+'\n')
        break



    

