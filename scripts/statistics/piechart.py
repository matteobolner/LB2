import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn
import plotly.express as px
import pandas as pd


kingdom_dict = {"Bacteria":639, "Eukaryota":455, "Archaea":93, "Viruses":63, "Other":3}
labels = list(kingdom_dict.keys())
sizes = list(kingdom_dict.values())
fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels = labels, autopct='%1.1f%%')
plt.tight_layout()
plt.savefig("kingdom_piechart.png")
plt.clf()

species_dict = {"H.sapiens":216, "E.coli":128, "T.thermophilus":38, "S.cerevisiae":32, "M.musculus":32, "B.subtilis":32, "T.maritima":31, "Other":736}
labels = list(species_dict.keys())
sizes = list(species_dict.values())
fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels = labels, autopct='%1.0f%%', rotatelabels = True)
plt.tight_layout()
plt.savefig("species_piechart.png")
plt.clf()
