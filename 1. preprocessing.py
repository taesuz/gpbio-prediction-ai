#%% 1. set working directory (revise)

import os
print(os.getcwd())

from base import *

#%%

def month_age(bdate,mdate):
    months = (mdate.year - bdate.year)*12 + (mdate.month - bdate.month) + ((mdate.day - bdate.day) / 30.4)
    return np.round(months,0)

def str_date(x):
    return datetime.strptime(x, '%Y-%m-%d').date()

def get_sample():

    data = pd.read_csv(PATH + 'data_sample.csv')        
    data['Birthdate'] = data['Birthdate'].apply(str_date)
    data['Measure_Date'] = data['Measure_Date'].apply(str_date)

    return data

def preprocessing(data):
    
    #성별 표기 수정
    data = data[data['Gender'] != '']
    data.reset_index(drop=True, inplace=True)
    data = data.replace({'m':'M', 'f':'F'})        
    
    #측정항목 소수점 한자리로 수정
    
    feats = ['Height', 'Weight', 'Protein_Mass', 'Mineral_Mass', 'Body_Fat_Mass', 'Soft_Lean_Mass', 'Skeletal_Muscle_Mass']
    
    for feat in feats:    
        data[feat] = data[feat].astype(float).apply(lambda x: round(x, 1))
        # add_db[feat] = add_db[feat].astype(float).apply(lambda x: round(x, 1))

    data['BMR'] = data['BMR'].astype(int)
    # add_db['BMR'] = add_db['BMR'].astype(int)

    data['Months'] = [int(month_age(x, y)) for x, y in zip(data['Birthdate'], data['Measure_Date'])]
    data['Age'] = (data['Months']/12).astype(int)
    data = data.drop(['Birthdate', 'Measure_Date'], axis=1)

    features = ['Student_ID', 'Gender', 'Age', 'Months', 'Height', 'Weight', 'Protein_Mass', 'Mineral_Mass', 'Soft_Lean_Mass', 'Body_Fat_Mass', 'Skeletal_Muscle_Mass', 'BMR']
    # final_db = pd.concat([data[features], add_db[features]], axis=0)
    data1 = data[features]
    data1.reset_index(drop=True, inplace=True)
    # print(len(np.unique(final_db['Student_ID'])))
    
    st_list = np.unique(data1['Student_ID'])
    
    one_point_feat = ['Height', 'Weight', 'Protein_Mass', 'Mineral_Mass', 'Soft_Lean_Mass', 'Body_Fat_Mass', 'Skeletal_Muscle_Mass']
    zero_point_feat = ['BMR']

    for i in one_point_feat:
        data1[i] = [np.round(x,1) for x in data1[i]]
    for i in zero_point_feat:
        data1[i] = [np.round(x,0) for x in data1[i]]

    mdf = deepcopy(data1)
    

    mdf['PW'] = mdf['Protein_Mass']/mdf['Weight']
    mdf['MW'] = mdf['Mineral_Mass']/mdf['Weight']
    mdf['SW'] = mdf['Soft_Lean_Mass']/mdf['Weight']
    mdf['BW'] = mdf['Body_Fat_Mass']/mdf['Weight']
    mdf['SMW'] = mdf['Skeletal_Muscle_Mass']/mdf['Weight']
    mdf['SS'] = mdf['Skeletal_Muscle_Mass']/mdf['Soft_Lean_Mass']
    mdf['BS'] = mdf['Body_Fat_Mass']/mdf['Soft_Lean_Mass']       
      
        
    height = pd.read_csv(PATH + 'height_extended_10.csv')
    mdf['Gender'] = mdf['Gender'].replace({'M':1, 'F':2})
    mdf = pd.merge(mdf, height, left_on=['Gender', 'Months'], right_on=['Gender', 'Months'], how='left')

    for i in range(10, 110, 10):
        mdf['pct'+str(i)] = 0   
        
    for i in range(10, 110, 10):
        if i == 10:
            mdf.loc[mdf[mdf['Height']<=mdf['P'+str(i)]].index, 'pct'+str(i)] = 1
        elif i == 100:
            mdf.loc[mdf[mdf['Height']>mdf['P'+str(i-10)]].index, 'pct'+str(i)] = 1
        else:
            mdf.loc[mdf[(mdf['Height']<=mdf['P'+str(i)])&(mdf['Height']>mdf['P'+str(i-10)])].index, 'pct'+str(i)] = 1
        
    for i in range(10, 100, 10):
        mdf.drop('P'+str(i), axis=1, inplace=True)
        
    # add quantile
        
    height_std_table = pd.read_csv(PATH + 'height_pct_LMS.csv')

    hstd = pd.merge(mdf, height_std_table, how = 'left', on = ['Gender','Months'])
    hstd['zscore'] = (((hstd['Height']/hstd['M'])**hstd['L'])-1)/(hstd['L']*hstd['S'])

    mdf['Quantile'] = norm.cdf(hstd['zscore'])
    

    return st_list, mdf

#%% main code

data = get_sample()
st_list, df  = preprocessing(data)
df.reset_index(drop=True, inplace=True)
df.to_csv(PATH + 'df_sample.csv', index=False)
