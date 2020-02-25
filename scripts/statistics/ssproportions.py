import numbers
helix = open("helix.txt", "r")
helix_counter = 0
for line in helix:
    splitted_line = line.rstrip().split(".")
    if splitted_line[1] != '':
        helix_counter += int(splitted_line[1]) - int(splitted_line[0])
print(helix_counter)

strand = open("strand.txt", "r")
strand_counter = 0
for line in strand:
    splitted_line = line.rstrip().split(".")
    if splitted_line[1] != '':
        strand_counter += int(splitted_line[1]) - int(splitted_line[0])
print(strand_counter)

turn = open("turn.txt", "r")
turn_counter = 0
for line in turn:
    splitted_line = line.rstrip().split(".")
    if splitted_line[1] != '':
        turn_counter += int(splitted_line[1]) - int(splitted_line[0])
print(turn_counter)