from PIL import Image
import os

def crop(cnt,img_id, img_path, x,y,h,w):
    print img_path
    print x
    print y
    print h
    print w
    img = Image.open("/scratche/home/sanket/kvqa/datasets/"+img_path)
    img2 = img.crop((x,y,h,w))
    basewidth = 160
    wpercent = (basewidth/float(img2.size[0]))
    hsize = int((float(img2.size[1])*float(wpercent)))
    img2 = img2.resize((basewidth,hsize), Image.ANTIALIAS)
    img2.save("cropped_images2/"+str(img_id)+"/"+str(cnt)+'.jpg')



#crop(1,1,'wikiVQA/politicians/Albert_Goldman/2.jpeg',563, 173, 34,)
f3=open('/scratche/home/sanket/kvqa/QAgeneratingFiles/master_analysis/total_images.csv', 'r')
total_images=[]
for line in f3:
    line=line.split('\t')
    total_images.append(line[0])
f2=open('cropped_images2/uncropped_images.csv','w')
f=open("../trisha/master_file.csv", "r")
for line in f.readlines():
    line=line.split("\t")
    complete_cords=[]
    if line[0] not in total_images:
        print "ignore"
        continue
    directory='cropped_images2/'+line[0]
    if not os.path.exists(directory):
        os.makedirs(directory)
    flag=0
    cords=""
    cnt=0
    for ch in line[2]:
        if ch=="]":
            flag=0
            cnt=cnt+1
            cords=cords.split(', ')
            complete_cords.append(cords)
            cords=""
        if flag==1:
            cords+=ch
        if ch=='[':
            flag=1
    complete_cords.sort()
    for i in range(0,len(complete_cords)):
        try:
            crop(i+1, line[0], line[1], float(complete_cords[i][0]), float(complete_cords[i][1]), float(float(complete_cords[i][0])+float(complete_cords[i][2])), float(float(complete_cords[i][1])+float(complete_cords[i][3])))
        except:
            f2.write(line[0]+'\t'+str(cnt))
