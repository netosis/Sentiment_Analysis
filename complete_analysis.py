from nltk.tokenize import word_tokenize
import syllables
import re
import pandas as pd


with open('test_file.txt','r',encoding="utf8") as scraped:
    text=scraped.readlines()

sentences=text[0].split('.')
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

pronoun_pattern = r'\b(I|we|my|ours|us)\b(?!S)'
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
    joined=' '.join(sentence)    
    personal_pronouns = re.findall(pronoun_pattern,joined, re.IGNORECASE)
    print(personal_pronouns)

avg_char=int(char_count/word_count)

percent_comp_words=int(comp_words/word_count)

fog_index=0.4*(avg_words+percent_comp_words)

print('POSITIVE SCORE',pos_score)
print('NEGATIVE SCORE',neg_score)
print('POLARITY SCORE',pol_score)
print('SUBJECTIVITY SCORE',sub_score)
print('AVG SENTENCE LENGTH',avg_words)
print('PERCENTAGE OF COMPLEX WORDS',percent_comp_words)
print('FOG INDEX',fog_index)
print('AVG NUMBER OF WORDS PER SENTENCE',avg_words)
print('COMPLEX WORD COUNT',comp_words)
print('WORD COUNT',word_count)
print('SYLLABLE PER WORD',syll_count)
print('PERSONAL PRONOUNS',pro_count)
print('AVG WORD LENGTH',avg_char)

# excel_file=pd.read_excel('C:\Internships\Test Assignment\Output Data Structure.xlsx')
# fill_data=(excel_file.iloc[0])
# fill_data['POSITIVE SCORE']=pos_score
# fill_data['NEGATIVE SCORE']=neg_score
# fill_data['POLARITY SCORE']=pol_score
# fill_data['SUBJECTIVITY SCORE']=sub_score
# fill_data['AVG SENTENCE LENGTH']=avg_words
# fill_data['PERCENTAGE OF COMPLEX WORDS']=percent_comp_words
# fill_data['FOG INDEX']=fog_index
# fill_data['AVG NUMBER OF WORDS PER SENTENCE']=avg_words
# fill_data['COMPLEX WORD COUNT']=comp_words
# fill_data['WORD COUNT']=word_count
# fill_data['SYLLABLE PER WORD']=syll_count
# fill_data['PERSONAL PRONOUNS']=pro_count
# fill_data['AVG WORD LENGTH']=avg_char