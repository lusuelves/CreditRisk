
#First causal nex model

from causalnex.structure import StructureModel
from causalnex.plots import plot_structure
import pandas as pd

data = pd.read_csv('../data/hmeq_clean.csv', delimiter=';')

sm = StructureModel()
