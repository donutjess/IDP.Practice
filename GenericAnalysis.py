import json
import matplotlib.pyplot as plt
import numpy as np
import statistics

# TODO - ADD MORE COMMENTS;
# SPLIT FUNCTIONS INTO... WELL... FUNCTIONS;
# MAKE IT LESS HARD CODED (EX. TITLE GRAPHS WITH ORGANISM NAME FROM FILE)
# GET ERROR BARS WORKING?

file = open('C:\\Users\\koprekj\\github\\IDP.Practice\\data\\eColiDisorderedProteome.json', encoding='utf8')
file2 = open('C:\\Users\\koprekj\\github\\IDP.Practice\\eColiProteome.fasta',)

data = json.load(file)

IDs = {}
ScrollingSeq = ""
for i in data['data']:
    for j in i['regions']:
        start = j['start']
        end = j['end']
        IDs.update({i['disprot_id']: i['sequence'][start: end]})
        ScrollingSeq += i['sequence'][start: end]

totalAA = 0
AADict = dict.fromkeys(['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V'])

for j in ScrollingSeq:
    totalAA += 1

print("\n\nTotal aa's = \t" + str(totalAA))

Aminos = {}
for key in AADict:
    counts = 0
    stringed = str(key)
    for j in ScrollingSeq:
        if j == stringed:
            counts += 1
    AADict[key] = counts
    fraction = round(int(AADict[key])/totalAA, 3)
    Aminos.update({key: fraction})
    print("Total " + stringed + " =\t" + str(counts) + "\tFraction of aa's that are " + stringed + " = \t\t" + str(fraction))
print(Aminos)
basics = int(AADict['R']) + int(AADict['H']) + int(AADict['K'])
print("\nBasic aa's = \t" + str(basics) + "\tFraction of aa's that are basic = \t" + str(round(basics/totalAA, 3)))
acidics = int(AADict['D']) + int(AADict['E'])
print("Acidic aa's = \t" + str(acidics) + "\tFraction of aa's that are acidic = \t" + str(round(acidics/totalAA, 3)))

proteome = {}
bigstring = ""
z = 0
while(True):
    line = file2.readline()
    if not line:
        break
    if ">" not in line:
        bigstring += str(line.strip())
        z += len(line.strip())

for keys in AADict:
    r = 0
    for j in bigstring:
        if j == str(keys):
            r += 1
    proteome.update({keys: (r/z)})
print(proteome)

# # counts how often each aa shows up in each protein - makes list of the proteins (as dictionaries) and dictionaries for each protein containing each aa and occurances of them
# colorList = ['brown','peru','darkorange','gold','lawngreen','forestgreen','turquoise','deepskyblue','b','mediumslateblue','blueviolet','violet','magenta','crimson']
# labels = AADict.keys()
# x = np.arange(len(labels))
Proteins = []
#go through each protein
for protein in IDs:
    dict = {}
    #go through each aa
    for keys in AADict:
        r = 0
        for j in str(IDs[protein]):
            if j == str(keys):
                r += 1
        dict.update({keys: (r/len(IDs[protein]))})
        plt.scatter(dict.keys(), dict.values())
    Proteins.append(dict)
    # TODO - CHANGE GRAPH TYPE TO MAKE MORE SENSE!

Ranges = []
for keys in AADict:
    list = [sub[keys] for sub in Proteins]
    Ranges.append([max(list), min(list)])

plt.xlabel("Amino acid")
plt.ylabel("Fraction of Occcurances")
plt.show()

# figure out yerr
plt.bar(Aminos.keys(), Aminos.values(), 0.33, color='b', align='edge', label = 'Disordered')
plt.bar(proteome.keys(), proteome.values(), -0.33, color='g', align='edge', label = 'Proteome')
plt.title("Disordered sections AA distribution vs Codon Use")
plt.xlabel("Amino acid")
plt.ylabel("Fraction of Occcurances")
plt.legend()
plt.show()
print("\nProteins list of dictionaries is")
print(Proteins)

file.close()
file2.close()
