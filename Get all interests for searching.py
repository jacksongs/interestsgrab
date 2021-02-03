#!/usr/bin/env python
# coding: utf-8

# In[1]:


# downloads all MPs and Senators' disclosures for the current parliament
# counts how many pages and how many words
# based on that, makes call on whether they are searchable.
# puts all that in a spreadsheet
# provides a searchable pdf

import datetime
today = datetime.datetime.now().strftime("%Y-%m-%d")
get_ipython().system('mkdir $today')
get_ipython().system('mkdir $today/house')
get_ipython().system('mkdir $today/senate')


# In[43]:


# mps

import requests
from bs4 import BeautifulSoup
page = requests.get("https://www.aph.gov.au/Senators_and_Members/Members/Register")
soup = BeautifulSoup(page.content)
links = soup.find_all('a')
pdflinks = []
for l in links:
    try:
        if "pdf" in l.get("href"):
            if "46P" in l.get("href"):
                pdflinks.append(l.get("href"))
    except Exception as e:
        pass
        #print(e,l)
for p in pdflinks:
    name = p.split("/")[-1].split("?")[0]
    print(name)
    r = requests.get("http://aph.gov.au"+p, stream=True)
    with open(today+'/house/'+name, 'wb') as fd:
        for chunk in r.iter_content(2000):
            fd.write(chunk)


# In[44]:


# senators

import requests
from bs4 import BeautifulSoup
page = requests.get("https://www.aph.gov.au/Parliamentary_Business/Committees/Senate/Senators_Interests/Register46thparl")
soup = BeautifulSoup(page.content)
links = soup.find_all('a')
pdflinks = []
for l in links:
    try:
        if "pdf" in l.get("href"):
            if "46th_Parl" in l.get("href"):
                pdflinks.append(l.get("href"))
    except Exception as e:
        pass
        #print(e,l)
for p in pdflinks:
    name = p.split("/")[-1].split("?")[0]
    print(name)
    r = requests.get("http://aph.gov.au"+p, stream=True)
    with open(today+'/senate/'+name, 'wb') as fd:
        for chunk in r.iter_content(2000):
            fd.write(chunk)


# In[45]:


import os
from PyPDF2 import PdfFileReader
import pandas as pd
import PyPDF2 
import textract, re
df = pd.DataFrame(columns=['file', 'chamber', 'pages', 'words'])
for root, dirs, files in os.walk(os.getcwd()):
    for f in files:
        if f.lower().endswith(".pdf"):
            pdf=PdfFileReader(open(os.path.join(root, f),'rb'))
            if "senate" in root:
                chamber = "senate"
            else:
                chamber = "house"
            text = textract.process(os.path.join(root, f),method='pdfminer')
            words = len(str(text).split(" "))
            df2 = pd.DataFrame([[f, chamber,pdf.getNumPages(),words]], columns=['file', 'chamber','pages','words'])
            df = df.append(df2, ignore_index=True)
df.to_csv(today+"/table.csv")


# In[49]:


from PyPDF2 import PdfFileMerger

for chamber in ["house","senate"]:
    pdfs = os.listdir(today+"/"+chamber)

    merger = PdfFileMerger()

    for pdf in pdfs:
        #filename = today+"/"+chamber+"/"+pdf
        #print(filename)
        merger.append(filename,import_bookmarks=False )

    merger.write(today+"/"+chamber+".pdf")
    merger.close()


# In[ ]:





# In[ ]:




