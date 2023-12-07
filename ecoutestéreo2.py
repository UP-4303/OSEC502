# -*- coding: utf-8 -*-
import soundfile as sf
import numpy as np

s, fe = sf.read('Diapason.mp3')
dt = 2  # décalage en secondes
fe = 48000
dts = round(dt * fe)  # décalage en nombre
# d'échantillons, en utilisant fe la
# fréquence d'échantiollonnage en Hz
a = s[0:-dts+1, 0]
b = s[dts:, 0]
S = np.concatenate((a, b)).reshape(-1, 1)
sf.write('ecoute stereo.mp4', S, fe)

# code avec pydub
 
from pydub import AudioSegment

# Charger le fichier audio
audio = AudioSegment.from_file('Diapason.mp3')

dt = 2  # décalage en secondes
dts = int(dt * 1000)  # décalage en millisecondes

# Appliquer le décalage
a = audio[:-(dts - 1)] if dts != 1 else audio
b = audio[dts - 1:]

# Concaténer les segments pour former le signal décalé
shifted_audio = a + b

# Enregistrer le signal décalé dans un nouveau fichier audio
shifted_audio.export('essai.mp4', format='mp4')


# code avec librosa

import soundfile as sf
import librosa

# Charger le fichier audio
s, fe = librosa.load('Diapason.mp3', sr=None, mono=True)

dt = 2  # décalage en secondes
dts = int(dt * fe)  # décalage en nombre d'échantillons

a = s[:-(dts - 1)] if dts != 1 else s  # Premier segment du signal
b = s[dts - 1:]  # Second segment du signal

# Concaténer les segments pour former le signal décalé
S = librosa.util.stack([a, b], axis=1)

# Enregistrer le signal décalé dans un nouveau fichier audio
sf.write('essai.mp4', S.T, fe)
