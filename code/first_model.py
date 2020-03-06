
#First causal nex model

from causalnex.structure import StructureModel
from causalnex.plots import plot_structure
import pandas as pd
from causalnex.structure.notears import from_pandas
from causalnex.network import BayesianNetwork
from sklearn.model_selection import train_test_split

data = pd.read_csv('../data/hmeq_clean.csv', delimiter=',')
data = data.apply(pd.to_numeric,errors='coerce')
data.drop(columns=['Unnamed: 0'], inplace=True)

sm = from_pandas(data)
def determine_structure():

    _, _, _ = plot_structure(sm)
    
    sm.remove_edges_below_threshold(0.8)
    _, _, _ = plot_structure(sm)
    
    """
    Now I have to determine what relationships are right.
    I can see that BAD determines VALUE and MORTDUE when it should be the other way
    round. SO I am going to change the arrows. 
    """
    sm.remove_edge("BAD", "VALUE")
    sm.remove_edge("BAD", "MORTDUE")
    sm.remove_edge("BAD", "LOAN")
    sm.add_edge("MORTDUE", "BAD")
    sm.add_edge("VALUE", "BAD")
    
    
    """
    DEBTINC is debt-to-income ratio so mortgage and salary affects this variable,
    not the other way round.
    
    """
    sm.remove_edge("DEBTINC", "CLAGE")
    sm.remove_edge("DEBTINC", "VALUE")
    sm.remove_edge("DEBTINC", "MORTDUE")
    sm.remove_edge("DEBTINC", "LOAN")
    
    sm.add_edge("MORTDUE", "DEBTINC")
    sm.add_edge("VALUE", "DEBTINC")
    sm.add_edge("CLAGE", "DEBTINC")
    sm.add_edge("LOAN", "DEBTINC")
    
    """
    NINQ is number of inquires, so variables are the other way round
    not the other way round.
    
    """
    
    sm.remove_edge("NINQ", "VALUE")
    sm.remove_edge("NINQ", "MORTDUE")
    sm.remove_edge("NINQ", "LOAN")
    
    sm.add_edge("MORTDUE", "NINQ")
    sm.add_edge("VALUE", "NINQ")
    sm.add_edge("LOAN", "NINQ")

#_, _, _ = plot_structure(sm)

#determine_structure()
sm.remove_edges_below_threshold(0.8)
sm.remove_edge("BAD", "VALUE")
sm.remove_edge("BAD", "MORTDUE")
sm.remove_edge("BAD", "LOAN")
sm = sm.get_largest_subgraph()
bn = BayesianNetwork(sm)


discretised_data = data.copy()

"""
1: very small loan
2: small loan
3: large loan
4: very large loan
"""
def categorize(col):
    mini = int(data[col].min())
    maxi = int(data[col].max())
    rangi = (maxi-mini)//1
    print(col)
    print(rangi)
    reference = range(mini,maxi,rangi)
    hey_jude = []
    for loan in data[col]:
        i = 0
        while loan >= reference[i] and i < len(reference) - 1:
            i += 1
        hey_jude.append(i)
    return hey_jude

categorized_data = data.copy()
cats = ['LOAN','MORTDUE','VALUE','YOJ','CLAGE','CLNO','DEBTINC','DEROG','DELINQ','NINQ']
for col in cats:
    categorized_data[col] = categorize(col) 

data_vals = {col: data[col].unique() for col in data.columns}


#bn = bn.fit_node_states(categorized_data)

train,test = train_test_split(categorized_data, train_size=0.9, test_size=0.1, random_state=7)

#bn = bn.fit_cpds(train, method="BayesianEstimator", bayes_prior="K2")

#bn.predict(categorized_data,'BAD')
#print(bn.predict(categorized_data,'BAD'))




