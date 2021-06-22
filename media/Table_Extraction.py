import pandas as pd
import numpy as np
 
def countX(lst, x): 
    count = 0
    for ele in lst: 
        if (ele == x): 
            count = count + 1
    return count

def Table_Extraction(str_data,sheetname):
    
    column_with_occurance = []
    uniquee = []
    
    df = pd.read_excel("media/TempMapping.xlsx",encoding ='utf-8',sheet_name = sheetname)
    for i in df.columns:
        df[i].astype('str').apply(lambda x: uniquee.append(df[i].name) if x.startswith(str_data.lower().replace(" ","").strip()) else 'pass')

    #print(str_data.lower().replace(" ","").strip(),uniquee)
    temp_uinquee = np.unique(uniquee)
    #print(temp_uinquee)
    for t in temp_uinquee:
        tt = countX(uniquee,t)
        column_with_occurance.append([str_data,t,tt])
        #print(str_data)    
    return column_with_occurance