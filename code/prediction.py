from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform

data = pd.read_csv('../data/hmeq_clean_cat.csv')
model_rf = RandomForestClassifier(n_estimators=200)
X = data.drop(columns=['BAD','Unnamed: 0'])
y = data['BAD']
model_rf.fit(X,y)

def tonumeric(X_test):
    jobs = ['Mgr', 'Office', 'Other', 'ProfExe', 'Sales', 'Self']
    reasons = ['DebtCon','HomeImp']
    X_test[3] = reasons.index(X_test[3])
    X_test[4] = jobs.index(X_test[4])
    return X_test

def predict(X_test):
    X_test = tonumeric(X_test)
    df = pd.DataFrame(np.array([X_test]),columns=X.columns)
    answer = model_rf.predict(df)
    return answer[0]


def recommendation(X_test):
    X_test = tonumeric(X_test)
    data_pos = data.loc[data['BAD']==0]
    data_pos.drop(columns=['BAD','Unnamed: 0'],inplace=True)
    data_pos = data_pos.T
    data_pos['TOM'] = X_test
    distances = pd.DataFrame(1/(1 + squareform(pdist(data_pos.T, 'euclidean'))), 
                             index=data_pos.columns, columns=data_pos.columns)
    similarities = distances['TOM'].sort_values(ascending=False)[1:]
    
    ## Este es el vector de similiaridad de TOM con el resto de usuarios respecto a sus
    ## visualizaciones comunes
    
    similars = pd.DataFrame(similarities)
    return pd.DataFrame(similars).head()