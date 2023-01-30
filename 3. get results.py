#%% 1. set working directory (revise)

import os
print(os.getcwd())

from base import *

#%%
feature_cols_ = ['BMI_Level', 'PCT', 'Quantile', 'Weight', 'Protein_Mass', 'Mineral_Mass',
       'Soft_Lean_Mass', 'Body_Fat_Mass', 'Skeletal_Muscle_Mass', 'BMR',
       'Months', 'Target_Months', 'Height', 'PW', 'MW', 'SW', 'BW', 'SMW',
       'SS', 'BS', 'Ages', 'Target_Ages']

# no_inbody_cols_ = ['BMI_Level', 'PCT', 'Quantile', 'Weight', 'Height', 'Months', 'Ages', 'Target_Ages', 'Target_Months']

def predicted_height_func(data0, prediction_model, month_end, pct = None, df_median = None):
    
    regressor = prediction_model[0][0]
    
    cols_ = feature_cols_
    
    unique_idx = data0['Months'].drop_duplicates().index
    data1 = data0.loc[unique_idx]
    #     month_end = data1['Months'].iloc[-1]
    
    fig = plt.figure(figsize = (8, 6))
    
    for i, data_temp in data1.iterrows():
    
        month_start = data_temp['Months']
    
        Target_Months_ = np.append(month_start, np.arange(month_start + (24-month_start%12.0), month_end+1, 12))
    
        if len(Target_Months_ > 0):
    
            X_hair = pd.DataFrame()
            X_hair = X_hair.append([data_temp]*len(Target_Months_), ignore_index = True)
            X_hair['Target_Months'] = Target_Months_
            X_hair['Target_Ages'] = Target_Months_//12
            X_hair = X_hair[cols_]
    
            predict = regressor.predict(X_hair)
            base_height = data_temp['Height']
    
            predicted_height = (predict + 1) * base_height
            predicted_height[0] = base_height
            
            plt.plot(Target_Months_/12, predicted_height, 'g*-')    
        
                    
            if df_median is not None:
                data_median = df_median[(df_median['Gender']==gender)&(df_median['Months']==month_start)]
                X_median = pd.DataFrame()
                X_median = X_median.append([data_median]*len(Target_Months_), ignore_index = True)
                X_median['Target_Months'] = Target_Months_
                X_median['Target_Ages'] = Target_Months_//12
                X_median = X_median[cols_]
                X_median[['Height', 'Quantile']] = X_hair[['Height', 'Quantile']]
                
                predict_m = regressor.predict(X_median)
        
                predicted_height_m = (predict_m + 1) * base_height
                predicted_height_m[0] = base_height  
                
                plt.plot(Target_Months_/12, predicted_height_m, 'r.-')
                plt.legend(['Predicted Height','Predicted Median Height'])
                
            plt.plot(data1['Months']/12, data1['Height'], 'k:o', label = '_nolegend_')
            
            plt.title(f'Student:{std_id} Height Prediction')
            plt.xlabel('Age')
            plt.ylabel('Height (cm)')          
                

    if pct is not None:
        month_init = data0['Months'].iloc[0]
        pct1 = pct[(pct['Months']>=month_init)&(pct['Months']<=month_end)]
        pct2 = pct1[pct1['Gender']==gender]
        plt.plot(pct2['Months']/12, pct2['P10'], 'k:', alpha = 0.5)
        plt.plot(pct2['Months']/12, pct2['P90'], 'k:', alpha = 0.5)
        
    for i, mth in enumerate(Target_Months_):
        if i == 0: print(f'현재 나이: {int(mth/12)}년 {int(mth%12)}개월, 현재 키: {predicted_height[i]:.1f}cm')
        else: print(f'예상 나이: {int(mth/12)}세, 예상 키: {predicted_height[i]:.1f}cm')
            
    predicted_height_output = pd.DataFrame({'Months': Target_Months_,
                                           'Heights': predicted_height})
    
    if df_median is not False:
        
        predicted_height_output = pd.DataFrame({'Months': Target_Months_,
                                               'Heights': predicted_height, 
                                               'Mean_Heights': predicted_height_m})
        
    return predicted_height_output
                

#%%
df = pd.read_csv(data_path+'df_sample_processing.csv')
unified_prediction_results = joblib.load(py_path + 'unified_prediction_results.pickle')

df_median = pd.read_csv(data_path + 'df_median.csv')
pct = pd.read_csv(data_path  + 'height_extended_10.csv')

#%%


#%% display

gender_label = ['male','female']

std_id = df['Student_ID'][0]
gender = df['Gender'][0]
gend = gender_label[gender-1]

model = 'lgbm'
age_end = 17

prediction_model = unified_prediction_results[gend][model]

predicted_height = predicted_height_func(df, prediction_model, age_end*12, pct = pct, df_median = df_median)

