import obspy
from obspy import read

import numpy as np

import matplotlib
import matplotlib.pyplot as plt

from scipy.fft import fft, fftfreq

#importer les données du seisme
donnees_seisme= read(r"C:\Users\gatia\visual\IU.ANMO.00.BHZ.M.2010.058.063000.SAC")
print (donnees_seisme)

#informations sur les données
print ("Fréqence d'échantillonnage de la station (fs): " + str(donnees_seisme[0].stats.sampling_rate)+"Hz")

#afficher le contenu des données
donnees_seisme[0].plot()
plt.show()

#pré-traitement des donées + affichage
donnees_seisme_corr=donnees_seisme.copy()
donnees_seisme_corr.detrend(type='polynomial', order=3)
donnees_seisme_corr.detrend('demean')
donnees_seisme.taper(max_percentage=0.05, type='hann')
donnees_seisme_corr.filter('highpass',freq=0.05)

donnees_seisme_corr[0].plot()
plt.show() 

#calcul des spectres de fourier
fs=donnees_seisme[0].stats.sampling_rate
dt=1.0/fs

#nombre d'échantillons dans les sismogrammes
N_donnees_seisme= donnees_seisme_corr[0].stats.npts

# calcul de la transformée de fourier (fft)
FFT_donnees_seisme=fft(donnees_seisme_corr[0].data)

#on garde uniquement les fréquences positives
#valeurs en abscisses : Xf
xf_seisme= fftfreq(N_donnees_seisme,dt)[:N_donnees_seisme//2]

#on prend la valeur absolue de l'amplitude uniquement pour les fréquences positives et normalisation
#valeurs en ordonnées: yf
yf_seisme= np.abs(FFT_donnees_seisme[0:N_donnees_seisme//2])*2.0/N_donnees_seisme

#afficher les spectres de Fourier
plt.plot(xf_seisme,yf_seisme,linewidth=0.5, color='black')
plt.show()