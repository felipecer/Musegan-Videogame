import mido
import os
from instr_tools import get_track_instrument
import matplotlib.pyplot as plt

tracksDict = {}
datasetPath = "./td-dataset/"

count = 0

# Recorremos el dataset.
for root, dirsArr, files in os.walk(datasetPath):
	for file in files:
		count += 1
		try:
			mid = mido.MidiFile(os.path.join(root, file))
		except:
			print("Posible archivo invalido en:", os.path.join(root, file))
		# Obtenemos el instrumento de cada track de la cancion.
		for track in mid.tracks:
			instr = get_track_instrument(track)
			# Aumentamos los contadores de cada instrumento.
			if instr in tracksDict:
				tracksDict[instr] += 1
			else:
				tracksDict[instr] = 0

		if count % 100 == 0:
			print("Canciones procesadas:", count)

# Para hacer el grafico de barras.
columns = []
freq = []
for col in tracksDict:
	if col == "None?":
		continue
	pltCol = col.replace(" ", "\n")
	columns.append(pltCol)
	freq.append(tracksDict[col])

zipped_lists = zip(freq, columns)
sorted_pairs = sorted(zipped_lists, reverse=True)
tuples = zip(*sorted_pairs)
freq, columns = [list(tup) for tup in  tuples]

plt.xlabel("Instrument family")
plt.ylabel("frequency")
plt.bar(columns, freq)
plt.show()