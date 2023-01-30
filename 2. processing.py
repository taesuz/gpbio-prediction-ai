#%% 1. set working directory (revise)

import os
print(os.getcwd())

from base import *

#%%
def get_bmi(h, w):
    return round(w/((h/100)**2),1)

# lag_cols = ['Height','Weight', 'Protein_Mass', 'Mineral_Mass', 'Soft_Lean_Mass', 'Body_Fat_Mass', 'Skeletal_Muscle_Mass', 
#                'BMR','PW','MW','SW','BW','SMW','SS','BS']
# lag_cols_ = [col+'_l' for col in lag_cols]

# def add_lagged_features(temp, lag = 6):
#     max_lag = max(len(temp)-1,6)
#     mths_first, mths_last = temp['Months'].iloc[0], temp['Months'].iloc[-1]
    
#     if mths_last - mths_first >= lag:
#         mths_ = np.arange(mths_first, mths_last+1)
#         temp1 = pd.DataFrame({'Student_ID':[std_id]*len(mths_), 'Months':mths_})    
#         temp2 = pd.merge(temp1, temp, on = ['Student_ID', 'Months'], how = 'left')
#         temp2.interpolate(inplace = True)
#         temp2[lag_cols_] = temp2.pct_change(lag)[lag_cols]
#         temp2.drop(columns = lag_cols, inplace = True)
#         temp3 = pd.merge(temp, temp2, on = ['Student_ID', 'Months'], how = 'left' )
        
#     else:
#         temp3 = deepcopy(temp)
#         temp3[lag_cols_] = np.nan
        
#     return temp3

#%%
mdf = pd.read_csv(data_path + 'df_sample.csv')
mdf.reset_index(drop=True, inplace=True)
# no_inbody = joblib.load(py_path + 'no_inbody.pickle')

#%%

bmi_section = pd.read_csv(data_path + "section_total_type.csv", sep=";")
bmi_section.columns=['index', 'Age', 'Months', 'Gender', 'H1', 'H2', 'bmi1', 'bmi2', 'bmi3', 'bmi4', 'bmi5']
bmi_section = bmi_section[['Gender', 'Months', 'bmi1', 'bmi2', 'bmi3', 'bmi4', 'bmi5']]
#성별 재구분
bmi_section['Gender'] = bmi_section['Gender'].replace({'M':1, "F":2})
#데이터 결합
mdf = pd.merge(mdf, bmi_section, left_on=['Gender', 'Months'], right_on=['Gender', 'Months'], how='left')
mdf['BMI'] = [get_bmi(a, b) for a, b in zip(mdf['Height'], mdf['Weight'])]
mdf.reset_index(drop=True, inplace=True)
#BMI 2단계로 구분
mdf['BMI_Level'] = 0
bmi1 = mdf[mdf['BMI']<=mdf['bmi2']]
bmi2 = mdf[mdf['BMI']>mdf['bmi2']]
bmi0 = mdf[mdf['bmi2'].isna()]

bmi1['BMI_Level'] = 1
bmi2['BMI_Level'] = 2
bmi0['BMI_Level'] = 1.5

mdf = pd.concat([bmi0, bmi1, bmi2], axis=0)
mdf.reset_index(drop=True, inplace=True)
mdf.drop(['bmi1', 'bmi2', 'bmi3', 'bmi4', 'bmi5'], axis=1, inplace=True)
mdf.reset_index(drop=True, inplace=True)
#신장 4단계로 구분
mdf['PCT'] = 0
mdf['PCT'] = (mdf['pct10'] + mdf['pct20']) + (mdf['pct30'] + mdf['pct40'] + mdf['pct50'])*2 + (mdf['pct60'] + mdf['pct70'] + mdf['pct80'])*3 + (mdf['pct90'] + mdf['pct100'])*4
mdf.drop(['pct10', 'pct20', 'pct30', 'pct40', 'pct50', 'pct60', 'pct70', 'pct80', 'pct90', 'pct100'], axis=1, inplace=True)

#필요 변수만 추출
feats = ['Protein_Mass','Mineral_Mass','Soft_Lean_Mass','Body_Fat_Mass','Skeletal_Muscle_Mass']
for f in feats:
    mdf = mdf[mdf[f]>0]
    mdf = mdf[mdf[f]<mdf['Weight']]
    
mdf.reset_index(drop=True, inplace=True)

#%%

# if not no_inbody:
mm_features = ['Weight', 'Protein_Mass', 'Mineral_Mass', 'Soft_Lean_Mass', 'Body_Fat_Mass', 'Skeletal_Muscle_Mass', 'BMR']
mdf_mms = mdf[mm_features]

mdf_ori = mdf[['PW','MW','SW','BW','SMW','SS','BS']]
# else:
#     mm_features = ['Weight']
#     mdf_mms, mdf_ori = mdf[mm_features], None

mdf_mm = mdf[['Student_ID','Age', 'Months', 'Height']].copy()


mdf_age = mdf[['Age']]
mdf_age.columns=['Ages']

gender = mdf[['Gender', 'BMI_Level', 'PCT', 'Quantile']]
df = pd.concat([gender, mdf_mms, mdf_mm, mdf_ori, mdf_age], axis=1)

#%%

# lag_cols = ['Height','Weight', 'Protein_Mass', 'Mineral_Mass', 'Soft_Lean_Mass', 'Body_Fat_Mass', 'Skeletal_Muscle_Mass', 
#                'BMR','PW','MW','SW','BW','SMW','SS','BS']

# mdf_unique = mdf[['Student_ID','Months']+lag_cols].drop_duplicates()

# std_id_ = mdf_unique['Student_ID'].unique()

# mdf_unique2 = []
# for std_id in std_id_:
#     temp = mdf_unique[mdf_unique['Student_ID']==std_id]
#     mdf_unique2.append(add_lagged_features(temp))
    
# mdf_unique2 = pd.concat(mdf_unique2)

# df = pd.merge(df, mdf_unique2.drop(columns = lag_cols), how = 'left', on = ['Student_ID','Months'])

#%%
df.to_csv(PATH+'df_sample_processing.csv', index=False)