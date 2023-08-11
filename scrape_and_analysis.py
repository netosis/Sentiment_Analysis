import requests
from bs4 import BeautifulSoup as bs
from requests.api import head
from nltk.corpus import stopwords
import pandas as pd
from nltk.tokenize import word_tokenize
import syllables
import re


link_file=pd.read_excel('C:\Internships\Test Assignment\Output Data Structure-1.xlsx')
links=link_file['URL']
headers=({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36','Accept-Language': 'en-US,en;q=0.9','Referer': 'https://www.example.com'})
link_counter=0
link_id=list(link_file['URL_ID'])
excel_file=pd.read_excel('C:\Internships\Test Assignment\Output Data Structure.xlsx')
mainframe=pd.DataFrame()

for url in links:
    print(url)
    print(link_counter)
    site_url=str(url)
    
    req=requests.get(site_url,headers=headers)
    contents=bs(req.content,'lxml')
    contents.prettify()
    print(len(contents))

    main_data= contents.findAll('p')

    text_file=open('test_file.txt','w',encoding="utf8")

    print(len(main_data))
    soup=bs(str(main_data),'html.parser')
    text=soup.get_text()
    print('text=',len(text))

    text_file.writelines(text)
    print(type(text))
    print(len(text))

    #now the cleaning and analysis part


    sentences=text.split('.')
    print(sentences[0])
    sentences[0].replace('[','')
    sentences[-1].replace(']','')
    print('sentences=',len(sentences))

    stop_word_list=set()
    file_list=['StopWords_Auditor','StopWords_Currencies','StopWords_DatesandNumbers','StopWords_Generic','StopWords_GenericLong','StopWords_Geographic','StopWords_Names']
    for file_name in file_list:
        with open('C:\\Internships\Test Assignment\StopWords\{}.txt'.format(file_name),'r') as f_open:
            words=f_open.readlines()
        for word in words:
            word_1=word.split()
            stop_word_list.add(word_1[0])
            if len(word_1)>1:
                stop_word_list.add(word_1[-1])

    clean_sentences=[]
    for i in range(len(sentences)):
        clean_sentences.append([j for j in word_tokenize(sentences[i]) if j.lower() not in stop_word_list])
        

    word_count=0
    for i in clean_sentences:
        word_count+=len([word for word in i if word.isalpha()])
    print('words=',word_count)

    with open('C:\Internships\Test Assignment\MasterDictionary\positive-words.txt','r') as pos:
        pos_list=(pos.readlines())
        pos_list=[words.replace('\n','') for words in pos_list]
        pos_list=set(pos_list)

    pos_score=0

    with open("C:\Internships\Test Assignment\MasterDictionary\{}-words.txt".format('negative'),'r') as neg:
        neg_list=(neg.readlines())
        neg_list=[words.replace('\n','') for words in neg_list]
        neg_list=set(neg_list)

    neg_score=0

    for sentence in clean_sentences:
        for word in sentence:
            if word.lower() in pos_list:
                pos_score+=1

            elif word.lower() in neg_list:
                neg_score+=1

    print('pos=',pos_score)
    print('neg=',neg_score)

    pol_score=(pos_score+neg_score)/(pos_score+neg_score+0.000001)
    print(pol_score)

    sub_score=(pos_score+neg_score)/(word_count+0.000001)
    print(sub_score)


    avg_words=int((word_count/len(clean_sentences)))
    print('avg words=',avg_words)

    pattern = re.compile(r'\b(I|we|my|ours|(?-i:us))\b',re.I)
    pro_count=0

    char_count=0

    comp_words=0

    syll_count=0

    for sentence in clean_sentences:
        for word in sentence:
            sylls=(syllables.estimate(word))
            if sylls>2:
                comp_words+=1
                
            syll_count+=sylls

            if word.isalpha():
                char_count+=len(word)
        pron=' '.join(sentence)
        personal_pronouns = re.findall(pattern,pron)
        pro_count+=len(personal_pronouns)

    avg_char=(char_count/word_count)

    percent_comp_words=int((comp_words/word_count)*100)

    fog_index=0.4*(avg_words+percent_comp_words)


    complete_analysis_data={'URL_ID':list(),'URL':[],'POSITIVE SCORE':list(),'NEGATIVE SCORE':[],'POLARITY SCORE':[],'SUBJECTIVITY SCORE':[],'AVG SENTENCE LENGTH':[],"PERCENTAGE OF COMPLEX WORDS":[],'FOG INDEX':[],'AVG NUMBER OF WORDS PER SENTENCE':[],'COMPLEX WORD COUNT':[],'WORD COUNT':[],'SYLLABLE PER WORD':[],'PERSONAL PRONOUNS':[],'AVG WORD LENGTH':[]}
    complete_analysis_data['URL_ID'].append(link_id[link_counter])
    complete_analysis_data['URL'].append(url)
    complete_analysis_data['POSITIVE SCORE'].append(pos_score)
    complete_analysis_data['NEGATIVE SCORE'].append(neg_score)
    complete_analysis_data['POLARITY SCORE'].append(pol_score)
    complete_analysis_data['SUBJECTIVITY SCORE'].append(sub_score)
    complete_analysis_data['AVG SENTENCE LENGTH'].append(avg_words)
    complete_analysis_data['PERCENTAGE OF COMPLEX WORDS'].append(percent_comp_words)
    complete_analysis_data['FOG INDEX'].append(fog_index)
    complete_analysis_data['AVG NUMBER OF WORDS PER SENTENCE'].append(avg_words)
    complete_analysis_data['COMPLEX WORD COUNT'].append(comp_words)
    complete_analysis_data['WORD COUNT'].append(word_count)
    complete_analysis_data['SYLLABLE PER WORD'].append(syll_count)
    complete_analysis_data['PERSONAL PRONOUNS'].append(pro_count)
    complete_analysis_data['AVG WORD LENGTH'].append(avg_char)


    data_frame=pd.DataFrame(complete_analysis_data)
    mainframe=pd.concat([mainframe,data_frame],ignore_index=True)
    
    link_counter+=1
    if link_counter==5:
        break

mainframe.to_excel('new.xlsx',index=False)

