from urllib.request import urlopen, urlretrieve, quote
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import os

# Se puede cambiar a otros enlaces, para descargar de otras consolas.
url = 'https://www.vgmusic.com/music/console/nintendo/snes/'
u = urlopen(url)
try:
	html = u.read().decode('utf-8')
finally:
	u.close()

soup = BeautifulSoup(html)

# Hacemos el csv con pares juego,cancion.
with open("dataDesc.csv", "w") as csvFile:
	currName = ""
	csvFile.write("Game,Song\n")
	for midi in soup.find_all("a"):
		if midi.text == "Comments":
			continue
		href = midi.get('href')
		if href and href.endswith(".mid"):
			csvFile.write("\"" + currName + "\"," + "\"" +  href + "\"\n")
		elif "name" in str(midi):
			currName = midi.text
			currName = currName.replace(":", " ")
			currName = currName.replace("\"", " ")

# Descargamos las canciones.
path = "./data"
try:
	os.mkdir(path)
except OSError:
	print ("Creation of the directory %s failed" % path)

for midi in soup.find_all("a"):
	if midi.text == "Comments":
		continue
	href = midi.get('href')
	if href and href.endswith(".mid"):
		print(href)
		dl = urljoin(url, href)
		try:
			urlretrieve(dl, path+"/"+href)
		except:
			print('failed to download' + str(href))
	elif "name" in str(midi):
		currName = midi.text
		currName = currName.replace(":", " ")
		currName = currName.replace("\"", " ")
		path = "./data/" + currName
		try:
			os.mkdir(path)
		except OSError:
			print ("Creation of the directory %s failed" % path)

