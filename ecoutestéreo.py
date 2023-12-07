# -*- coding: utf-8 -*-
import soundfile as sf
import numpy as np

s, fe = sf.read('fichier son mp3')
dt = 2  # décalage en secondes
fe = 48000
dts = round(dt * fe)  # décalage en nombre
# d'échantillons, en utilisant fe la
# fréquence d'échantiollonnage en Hz
a = s[0:-dts+1, 0]
b = s[dts:, 0]
S = np.concatenate((a, b)).reshape(-1, 1)
sf.write('ecoute stereo.mp4', S, fe)
