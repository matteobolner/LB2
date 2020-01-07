import sys
import collections

def get_aa_ss(merged_file):
    f = open(merged_file, "r")
    line_list = f.read().split("\n")
    counter_value = collections.Counter({})
    for line in line_list:
        if line == "":
            break
        if line[0] == ">":
            aa_index = (line_list.index(line) + 1)
            ss_index = (line_list.index(line) + 2)
            counter_value += (collections.Counter(list((zip(line_list[aa_index],line_list[ss_index])))))
        else:
            continue
    sorted_counter_values = (sorted(counter_value.items()))
    residue_dict = {"A":0, "C":0, "D":0, "E":0, "F":0, "G":0, "H":0, "I":0, "K":0, "L":0, "M":0, "N":0, "P":0, "Q":0, "R":0, "S":0, "T":0, "V":0, "W":0, "Y":0, "X":0}
    for element in sorted_counter_values:
        residue_dict[element[0][0]] += int(element[1])
    print(residue_dict)
    #print(sorted_counter_values)
    total_ss_values = open(total_ss_file, "r")
    ss_dict = {"H":0, "E":0, "-":0}
    for line in total_ss_values:
        s = line.split(" = ")
        ss_dict[s[0]] += int(s[1])

    for couple in sorted_counter_values:
        formatted_aa_ss_number_and_frequence = (str(sorted_counter_values[sorted_counter_values.index(couple)]) + " ; " + str(couple[0]) + " : " + str(float(couple[1]/float(ss_dict[couple[0][1]]))))
        print(formatted_aa_ss_number_and_frequence)
    #print(counter_value)
    


if __name__ == "__main__":
    merged_file = sys.argv[1]
    total_ss_file = sys.argv[2]
    get_aa_ss(merged_file)