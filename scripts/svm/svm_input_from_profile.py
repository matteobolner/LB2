
import sys
import os

def get_profile_from_file(profile_file):
    profile_list = []
    profile_opened = open(profile_file, "r")
    for line in profile_opened:
        #print(line)
        line = line.rstrip().split()
        profile_list.append(line)
    
    return profile_list

 
def add_padding():
    a = get_profile_from_file(profile_file)
    #print(a)
    window = 17                         #window size
    pad = (int(window)//2)
    padding_matrix = [["0.0" for x in range(20) for y in range(pad)]]
    padded_profile = padding_matrix + a + padding_matrix
    #print(padded_profile)
    return padded_profile


    
def obtain_input(dssp_file):
    b = add_padding()
    #print(b)
    ss = {"H" : "1", "E" : "2", "-" : 3}    #secondary structure elements as classes
    window = 17
    #print(dssp_file)
    output_filename = (dssp_file.split("/")[-1]).replace(".dssp", "") + ".svm"
    #print(output_filename)
    dssp_opened = open(dssp_file, "r")
    filepath = os.path.join(output_path, output_filename)
    #print(filepath)
    final_output = open(filepath, "w")
    for line in dssp_opened:
        if line[0] == ">":
            continue
        else:
            dssp_seq = line.rstrip()
    for i,j in zip(dssp_seq, range(len(dssp_seq))):
        #print(i,j)
        v,f = [],0
        for k in b[j:j+int(window)]:
            for r in k:
                r = float(r)/100
                f +=1
                if r == 0:
                    continue
                else:
                    v.append(str(f) + ":" + str(r))   
        #print(v)
        final_output.write(str(ss[i]) + " " + " ".join(v)+"\n")
        #print(str(ss[i]) + " " + " ".join(v)+"\n")
    return()



if __name__ == "__main__":
    
    jpred_list = sys.argv[1]
    profile_folder = sys.argv[2]
    output_path = sys.argv[3]
    
    jpred_list_open = open(jpred_list , "r")

    for file in jpred_list_open:
        if (file.rstrip() + ".profile") in os.listdir(profile_folder):
            profile_file = os.path.join(profile_folder, (file.rstrip() + ".profile"))
            dssp_file = os.path.join(profile_folder, (file.rstrip() + ".dssp"))
            obtain_input(dssp_file)
        else:
            continue

        