import sys

def dssp_from_pred(pred_file, original, dssp_pred_file):
    number_to_ss = {"1":"H", "2":"E", "3":"-"}
    pred = open(pred_file, "r")
    orig = open(original, "r")
    dssp_pred_file = open(dssp_pred_file, "a")

    overallposcounter = 0
    pred_list = pred.readlines()
    for line in orig.readlines():
        positioncounter = 0
        temp_list = []
        clean_line = line.rstrip()
        while positioncounter < len(clean_line):
            temp_list.append(number_to_ss[pred_list[overallposcounter + positioncounter].rstrip()])
            positioncounter += 1
        overallposcounter += len(clean_line)
        temp_list = "".join(temp_list)
        dssp_pred_file.write(temp_list + "\n")
        
    return()



if __name__ == "__main__":
    pred_file = sys.argv[1]
    original = sys.argv[2]
    dssp_pred_file = sys.argv[3]
    dssp_from_pred(pred_file, original, dssp_pred_file,)

