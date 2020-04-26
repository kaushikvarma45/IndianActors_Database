# PROGRAM TO CREATE A LOCAL FOLDER OF IMAGES AND TEXT FILE OF EACH ACTOR : FURTHER Database.py USED TO CONVERT ALL THESE IMAGES AND TEXTS TO A DATABASE

from bs4 import BeautifulSoup
from urllib.request import urlopen,Request,urlretrieve
from googlesearch import search
import re
import pandas as pd


def create_csv(names):
    my_df = pd.DataFrame(names)
    my_df.to_csv('actorList.csv', index=False, header=False)


my_url = "https://www.imdb.com/list/ls002913270/" #IMDB list of 100 Indian actors
try:
    uclient = urlopen(my_url)
except Exception as e:
    print(str(e) + " No internet")
page_html = uclient.read()
uclient.close()
page_soup = BeautifulSoup(page_html,'html.parser')

names = [] # name of actor
biodata_links = [] #link of biodata of actor(not used for this database as we nees personality traits)
photo_links = [] #Online link of photo of actor
a_specific = page_soup.find_all('div',{'class':'lister-item-image'})
subname = [] #part of name first 4 letters(For testing later in sentence usefulness in txt file)

names.append('NAMES')
for i in a_specific:   #Running through the imdb site and specifically extracting names, photo links and bio-data links
    names.append(i.img['alt'])
    subname.append(i.img['alt'][0:4])
    photo_links.append(i.img['src'])
    link = 'imdb.com'+i.a['href']+'bio?ref_=nm_ov_bio_sm'
    biodata_links.append(link)
print(names)
create_csv(names) #Create csv file and save in current working directory

for member in range(1,len(names)): # Run segment wise as too many calls to a particular site may throw an error in the txt file
    #print(names[member])
    urlretrieve(photo_links[member], names[member] + '.jpg') #get image from link and store in jpg format
    query = names[member]+" personality traits of the actor" #Doing a Google search of celebrity personality Traits
    personality_links = []
    sentences_modified = []
    try:
        for j in search(query, tld="co.in", num=2, stop=2, pause=2): # using first 2 links here of google search can replace 2 with n for multiple sites(Will take more time as n increases)
            personality_links.append(j)
    except Exception as e:
        print('google site is not working(Internet connectivity lost)')
        continue
    for link_name in personality_links:
        my_url = link_name
        headers = {}
        headers['User-Agent']='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'
        #creating a fake header to prevent sites from tracking the search bot(works for many sites with blockers)

        req = Request(url=my_url,headers=headers)
        try:
            uclient = urlopen(req)
        except Exception as e:
            print(str(e)+" This website does not allow web crawler")
            continue
        page_html = uclient.read()
        uclient.close()
        print('ok site is read')
        page_soup = BeautifulSoup(page_html,'html.parser')
        data = page_soup.find_all(text=True)

        def visible(element):  #remove the obvious useless information from the html content
            if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
                return False
            elif re.match('<!--.*-->', str(element.encode('utf-8'))):
                return False
            return True


        result = filter(visible, data)
        sentences = list(set(result))

        count = 0 # Taking at max 15 sentences from each site(wikipedia has too much info)
        for i in sentences:
            if not subname[member] in i and not 'she' in i and not 'he' in i and not 'She' in i and not 'He' in i or '/' in i or 'American' in i:
                continue
            if len(i)>100 and count<15:
                sentences_modified.append(i)
                count+=1
    filename = names[member]+'.txt' # create a file using actor name as name of file
    fh = open(filename,'w')
    sentences_modified=list(set(sentences_modified))
    for i in sentences_modified:
        fh.write(i+'\n') # Write all sentences/paragraphs of list into this file
    fh.close()










