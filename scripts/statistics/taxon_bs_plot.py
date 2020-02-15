import matplotlib.pyplot as plt
labels = 'H.sapiens', 'M.musculus', 'P.aeruginosa', 'S.pombe', 'E.coli', 'S.cerevisiae', 'D.melanogaster', 'Other'
sizes = [35,8,5,4,4,4,3,89]
fig, ax = plt.subplots()
plt.pie(sizes, labels=labels, autopct='%1.0f%%',pctdistance=0.85, rotatelabels=1, startangle=140)
fig.tight_layout()
fig.subplots_adjust(bottom=0.2)
plt.axis('equal')
plt.savefig("organism.png")