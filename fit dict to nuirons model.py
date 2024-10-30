import csv

dictionary = {} # Creates a new dictionary

# Opens the existing dictionary file
csv_filename = 'dictionary.csv'
with open(csv_filename) as f:
    reader = csv.reader(f)
    for row in reader:
        dictionary[str(row[0])] = (float(row[1][1:]), int(row[2][1:len(row[2]) - 1]))

# Converts the data to the format required by the neural network
with open('dictionary_1.csv', 'w') as output_file:
    for key in dictionary:
        k = [*key]
        str = ''
        for x in k:
            str = str + x + ','
        output_file.write("%s,%s,%s\n" % (str[:-1], dictionary[key][0], dictionary[key][1]))
output_file.close()

