import sys
import matplotlib.pyplot as plt

def get_kingdom(inputfile):
    kingdom_dict = {"Archaea":0, "Bacteria":0, "Eukaryota":0, "Viruses":0, "TOT":0}
    open_file = open(inputfile, "r")
    for line in open_file:
        kingdom = line.rstrip()
        kingdom_dict[kingdom] += 1
        kingdom_dict["TOT"] += 1  

    kingdom_dict = {k: v / kingdom_dict["TOT"]  for k, v in kingdom_dict.items()} 
    kingdom_dict.pop("TOT")
    
    kingdom_piechart(kingdom_dict)
    return()


def kingdom_piechart(kingdom_dict):
    labels = list(kingdom_dict.keys())
    sizes = list(kingdom_dict.values())
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels = labels, autopct='%1.1f%%')
    plt.tight_layout()
    plt.savefig("taxonomy.png")
    plt.clf()
    return()

if __name__ == "__main__":
    inputfile = sys.argv[1]
    get_kingdom(inputfile)
