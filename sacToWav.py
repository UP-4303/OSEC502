from pydub import AudioSegment
import obspy

def sacToWav(st, path):

	# Amplification du signal (par exemple, multiplication par un facteur)
	amplification_factor = 10000
	for trace in st:
		trace.data *= amplification_factor
    
print("amplifié")

# Enregistrer le fichier amplifié
# st.write(r"C:\Users\gatia\visual\audio1.sac", format="SAC")

# print("fermé")
# st1= obspy.read(r"C:\Users\gatia\visual\audio1.sac")
# print("reouvert")

st.write(baselink + r"\audio2.wav", format='WAV', framerate=1000)
print("refermé")

def wav_to_mp3(input_wav, output_mp3):
    # Charger le fichier WAV
    audio = AudioSegment.from_file(input_wav, format='wav')
    
    # Convertir en MP3 avec une qualité spécifiée (ici, 320 kbps)
    audio.export(output_mp3, format="mp3", bitrate="320k")

# Spécifier le chemin du fichier WAV en entrée et du fichier MP3 en sortie
input_wav_file = baselink + r"\audio2.wav"
output_mp3_file = baselink + r"\audio3.mp3"

# Convertir le fichier WAV en MP3
wav_to_mp3(input_wav_file, output_mp3_file)