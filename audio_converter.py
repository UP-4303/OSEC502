from pydub import AudioSegment
import obspy

def sacToWav(st, path, filebasename, distance): # Distance is used for amplification
	# Amplification du signal (par exemple, multiplication par un facteur)
	amplificationBaseFactor = 10
	print(st[0].data)
	for trace in st:
			trace.data *= amplificationBaseFactor * (distance/1000)
	print(st[0].data)

	st.write(path + '/' + filebasename + '.wav', format='WAV', framerate=1000)

def wavToMp3(inputPath, outputPath, filebasename):
	# Charger le fichier WAV
	audio = AudioSegment.from_file(inputPath + '/' + filebasename + '.wav', format='wav')
    
	# Convertir en MP3 avec une qualité spécifiée (ici, 320 kbps)
	audio.export(outputPath + '/' + filebasename + '.mp3', format="mp3", bitrate="320k")