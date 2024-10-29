import csv

import numpy as np

dictionary = {}
new_dict = {}

csv_filename = 'dictionary.csv'
with open(csv_filename) as f:
    reader = csv.reader(f)
    for row in reader:
        dictionary[str(row[0])] = (float(row[1][1:]), int(row[2][1:len(row[2]) - 1]))

len = dictionary.copy()
for i in len.items():
    string = ""
    arr = np.array(list(i[0]), dtype=int).reshape(4, 4)
    sub_array = arr
    string = string + ''.join(map(str, sub_array.flatten())) + ''.join(map(str, np.rot90(sub_array).flatten())) + ''.join(map(str, np.diagonal(sub_array).flatten())) + ''.join(map(str, np.diagonal(np.rot90(sub_array))))
    new_dict[string] = (float(i[1][0]), int(i[1][1]))

with open('dictionary_long.csv', 'w') as output_file:
    for key in new_dict:
        output_file.write("%s,%s\n" % (key, new_dict[key]))
output_file.close()
