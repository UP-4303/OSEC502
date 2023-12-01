#amplification du signal .sac puis conversion en fichier .wav
#import obspy


# FONCTIONNE PAS TOUT A FAIT

#def sacToWav(st, path):
#	tableau= st.traces[0].data
#	amplified_data=[]
#	for i in range(0, len(tableau)):
#		tableau[i] *= 450
#		amplified_data.append(tableau[i].astype(np.float64) * 450)
#import obspy

# Charger le fichier SAC
#st = obspy.read("chemin/vers/le/fichier.sac")

# Amplification du signal (par exemple, multiplication par un facteur)
#amplification_factor = 2.0
#for trace in st:
 #   trace.data *= amplification_factor

# Enregistrer le fichier amplifié
#st.write("chemin/vers/le/fichier_amplifie.sac", format="SAC")
		# Normaliser pour s'assurer que les valeurs restent dans la plage autorisée
#		max_val = np.max(np.abs(amplified_data))
#		normalized_data = (450 / max_val) * 32767

		# Convertir en np.int16 après la normalisation
#		amplified_data = normalized_data.astype(np.int16)

#	amplified_data.write(path, format='WAV', framerate=1000)
#donnees_seisme= obspy.read(r"C:\Users\gatia\visual\IU.ANMO.00.BHZ.M.2010.058.063000.SAC")
#sacToWav(donnees_seisme,r"C:\Users\gatia\visual\audio3.wav")




import obspy

# Charger le fichier SAC
st = obspy.read(r"C:\Users\gatia\visual\IU.ANMO.00.BHZ.M.2010.058.063000.SAC")

print("ouvert")
# Amplification du signal (par exemple, multiplication par un facteur)
amplification_factor = 500 
for trace in st:
    trace.data *= amplification_factor
    
print("amplifié")

# Enregistrer le fichier amplifié
# st.write(r"C:\Users\gatia\visual\audio1.sac", format="SAC")

# print("fermé")
# st1= obspy.read(r"C:\Users\gatia\visual\audio1.sac")
# print("reouvert")

st.write(r"C:\Users\gatia\visual\audio2.wav", format='WAV', framerate=1000)
print("refermé")

from pydub import AudioSegment

def wav_to_mp3(input_wav, output_mp3):
    # Charger le fichier WAV
    audio = AudioSegment.from_file(input_wav, format='wav')
    
    # Convertir en MP3 avec une qualité spécifiée (ici, 320 kbps)
    audio.export(output_mp3, format="mp3", bitrate="320k")

# Spécifier le chemin du fichier WAV en entrée et du fichier MP3 en sortie
input_wav_file = r"C:\Users\gatia\visual\audio2.wav"
output_mp3_file = r"C:\Users\gatia\visual\audio3.mp3"

# Convertir le fichier WAV en MP3
wav_to_mp3(input_wav_file, output_mp3_file)