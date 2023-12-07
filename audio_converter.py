from pydub import AudioSegment
import obspy
from distance import getDt

def sacToWav(st, path, filebasename, distance): # Distance is used for amplification
	# Amplification du signal (par exemple, multiplication par un facteur)
	amplificationBaseFactor = 10
	for trace in st:
			trace.data *= amplificationBaseFactor * (distance/1000)

	st.write(path + '/' + filebasename + '.wav', format='WAV', framerate=1000)

def wavToMp3(inputPath, outputPath, filebasename):
	# Charger le fichier WAV
	audio = AudioSegment.from_file(inputPath + '/' + filebasename + '.wav', format='wav')
    
	# Convertir en MP3 avec une qualité spécifiée (ici, 320 kbps)
	audio.export(outputPath + '/' + filebasename + '.mp3', format="mp3", bitrate="320k")

def mixMp3(inputPath, outputPath, filebasename, distance, samplingRate):
	# Charger le fichier audio
	audio = AudioSegment.from_file(inputPath + '/' + filebasename + '.mp3')
	distance /= 1000
	dt = getDt(distance)  # décalage en secondes
	print(distance)
	print(dt)
	dts = int(dt * (samplingRate/1000))  # décalage en millisecondes
	# Appliquer le décalage
	print(dts)
	if (dts != 1):
		a = audio[:-(dts - 1)]
		b = audio[(dts - 1):]
	else:
		a = audio
		b = audio

	# Concaténer les segments pour former le signal décalé
	shifted_audio = a + b
	shifted_audio.set_channels(2)

	# Enregistrer le signal décalé dans un nouveau fichier audio
	shifted_audio.export(outputPath + '/' + filebasename + '.mp3', format='mp3', bitrate="320k")