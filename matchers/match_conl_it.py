import pandas as pd
import os 
import re

cut_matches=[]
files=['it_postwita-ud-dev.CONLLU','it_postwita-ud-train.CONLLU','it_postwita-ud-test.CONLLU']
for file in files:
    with open(os.getcwd()[:-9]+'/langs/it/'+file) as file:
        temp_list=[]
        temp_token_list=[]
        tokenized_strings=[]
        temp_string=''
        flag=0
        flag2=0
        skip=0
        for line in file:
            if skip!=0:
                skip=skip-1
                continue
            line=line.strip()

            if line!='':
                if line[0]=='#' and line[2:5]=='tex':
                    text=line[9:]
                    temp_list.append(text)
                    flag=1
                    continue
                elif flag==1 and line[0]!='#':
                        split=line.split('\t')
                        if len(split[0])!=1 and '-' in split[0]:
                            temp_token_list.append(split[1])
                            temp_string=temp_string+split[1]+'omega_ts'
                            skip=int(split[0].split('-')[1])-int(split[0].split('-')[0])+1
                        else:
                            temp_token_list.append(split[1])
                            temp_string=temp_string+split[1]+'omega_ts'
            else:
                temp_list.append(temp_token_list)
                temp_list.append(temp_string)
                tokenized_strings.append(temp_string)
                if temp_list not in cut_matches:
                    cut_matches.append(temp_list)
                temp_list=[]
                temp_token_list=[]
                temp_string=''
col1=[]
col2=[]
for i in cut_matches:
    col1.append(i[0])
    col2.append(i[2])
matched_df=pd.DataFrame([col1,col2])
matched_df=matched_df.T
matched_df.columns=['Original','Tokenized']

matched_df.to_csv(os.getcwd()[:-9]+'/matched/matched_it.csv',index=False)
print(matched_df)   