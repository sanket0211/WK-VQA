import urllib
f=open("../wiki_data_req_persons.csv", 'r')
f2=open("../wiki_data_req_persons_actual_names1.csv", 'w')
for line in f.readlines():
    line=line[:-1]
    f2.write(urllib.unquote(line)+'\n')


