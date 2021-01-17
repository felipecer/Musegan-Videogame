import pypianoroll as pypi
import mido
import pandas as pd
import numpy as np
from instr_tools import merge_tracks
import os

# CSV que contiene las canciones que cumplen con 4/4 y un time signature change. 
data = pd.read_csv("canciones_filtradas.csv")

# Directorios de los datos preprocesados y originales respectivamente.
pathPre = "./td_dataset_preprocesado"
pathData = "./td-dataset"

if not os.path.isdir(pathData):
	raise Exception("No existe el directorio del dataset:" + pathData)

if not os.path.isdir(pathPre):
	os.mkdir(pathPre)

# Itermaos por todos los datos que sirven.
for i in range(len(data.index)):

	if i % 100 == 0:
		print("EN", i, " DE ", len(data.index))

	try:
		mm = pypi.read("./td-dataset/" + data.loc[i][1] + "/" + data.loc[i][2])
	except:
		print("Posible error" + data.loc[i][1] + "/" + data.loc[i][2])
		continue

	# Combinamos los tracks de cada cancion cargada.
	mm = merge_tracks(mm)

	if not os.path.isdir(pathPre + "/" + data.loc[i][1]):
		try:
			os.mkdir(pathPre + "/" + data.loc[i][1])
		except:
			print("Posible nombre del directorio invalido:" + pathPre + "/" + data.loc[i][1])

	# Guardamos las canciones con tracks combinados.
	songName = data.loc[i][2][:-3] + "npz"
	mm.save(pathPre + "/" + data.loc[i][1] + "/" + songName)