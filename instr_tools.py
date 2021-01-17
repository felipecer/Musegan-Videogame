import matplotlib.pyplot as plt
import pandas as pd
from mido import MidiFile
import pypianoroll as pypi

# Recibe un track (de Mido) y retorna la familia de instrumentos de este.
def get_track_instrument(track):
	instr = "None?"
	for msg in track:

		if msg.is_meta: continue
		msgInfo = vars(msg)

		# Si el channel es 9 es percucion.
		if "channel" in msgInfo and msgInfo["channel"] == 9:
			instr = "drums"
			break

		# Si no lo clasificamos en su tipo.
		elif "type" in msgInfo and msgInfo["type"] == "program_change":

			if msgInfo["program"] < 8:
				instr = "piano"

			elif msgInfo["program"] < 16:
				instr = "chromatic percussion"

			elif msgInfo["program"] < 24:
				instr = "organ"

			elif msgInfo["program"] < 32:
				instr = "guitar"

			elif msgInfo["program"] < 40:
				instr = "bass"

			elif msgInfo["program"] < 48:
				instr = "strings"

			elif msgInfo["program"] < 56:
				instr = "ensemble"

			elif msgInfo["program"] < 64:
				instr = "brass"

			elif msgInfo["program"] < 72:
				instr = "reed"

			elif msgInfo["program"] < 80:
				instr = "pipe"

			elif msgInfo["program"] < 88:
				instr = "synth lead"

			elif msgInfo["program"] < 96:
				instr = "synth pad"

			elif msgInfo["program"] < 104:
				instr = "synth effects"

			elif msgInfo["program"] < 112:
				instr = "ethnic"

			elif msgInfo["program"] < 120:
				instr = "percussive"

			elif msgInfo["program"] < 128:
				instr = "sound effects"

			break

	return instr

# Obtiene los tracks validos (ya no se usa mucho).
def get_num_valid_instr(mid):
	validInstr = ["drums", "bass", "ensemble", "brass", "strings"]
	
	numValid = 0
	numUnique = 0
	instrList = []

	for track in mid.tracks:
		instr = get_track_instrument(track)
		if instr in validInstr:
			numValid += 1
			if instr not in instrList:
				instrList.append(instr)
				numUnique += 1

	return numValid, numUnique

# Combina los tracks de un multitrack (pypianoroll) para generar un nuevo multitrack
# conformado de 5 tracks de las 5 familias de instrumentos escogidas.
def merge_tracks(multitrack):
	# Familia de instrumentos escogidas.
	trackInfo = (("Drums", 0), ("Bass", 33), ("Brass", 56), ("Piano", 0), ("Ensemble", 48),)
	tracksToMerge = [[], [], [], [], []]
	# Observamos a que familia de instrumentos pertenece cada track de la cancion
	# original.
	for i, track in enumerate(multitrack.tracks):
		if track.is_drum:
			tracksToMerge[0].append(i)
		elif 32 <= track.program < 40:
			tracksToMerge[1].append(i)
		elif 56 <= track.program < 64:
			tracksToMerge[2].append(i)
		elif 0 <= track.program < 8:
			tracksToMerge[3].append(i)
		elif track.program < 96 or 104 <= track.program < 112:
			tracksToMerge[4].append(i) 

	tracks = []

	# Una vez que asignamos los tracks a mezclarse, los recorremos, mezclandolos.
	for i, trackList in enumerate(tracksToMerge):
		# Si hay tracks que se pueden mezclar.
		if trackList:
			newTracks = []
			for trackIndex in trackList:
				newTracks.append(multitrack.tracks[trackIndex])
			auxM = pypi.Multitrack(tracks=newTracks, tempo=multitrack.tempo, downbeat=multitrack.downbeat, resolution=multitrack.resolution)
			merged = auxM.blend("max")
			tracks.append(pypi.Track(pianoroll=merged, program=trackInfo[i][1], is_drum=(i == 0), name=trackInfo[i][0]).standardize().binarize())
		# Si no hay tracks, se genera un track vacio.
		else:
			tracks.append(pypi.Track(pianoroll=None, program=trackInfo[i][1], is_drum=(i == 0), name=trackInfo[i][0]).standardize().binarize())
	# Multitrack con los 5 tracks a utilizar.
	m = pypi.Multitrack(tracks=tracks, tempo=multitrack.tempo[0], downbeat=multitrack.downbeat, resolution=multitrack.resolution, name=multitrack.name)
	return m


