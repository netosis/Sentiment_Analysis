#this file uses requests and beautiful soup to gather the data from the website and writes it into the 'test_file.txt' so that we are not constantly fetching data from the site and making the site mark us as spam or bots


import requests
from bs4 import BeautifulSoup as bs
from requests.api import head
from nltk.corpus import stopwords


site_url='https://insights.blackcoffer.com/rise-of-telemedicine-and-its-impact-on-livelihood-by-2040-3-2/'
headers=({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36','Accept-Language': 'en-US,en;q=0.9','Referer': 'https://www.example.com'})
req=requests.get(site_url,headers=headers)
contents=bs(req.content,'lxml')
contents.prettify()

#main_div= contents.find('div',class_='td_block_wrap tdb_single_content tdi_130 td-pb-border-top td_block_template_1 td-post-content tagdiv-type')
main_data= contents.findAll('p')

text_file=open('test_file.txt','w',encoding="utf8")

print(len(main_data))
soup=bs(str(main_data),'html.parser')
text=soup.get_text()
print('text=',len(text))

text_file.writelines(text)
