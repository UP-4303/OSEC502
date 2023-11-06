import obspy

# FONCTIONNE PAS TOUT A FAIT
def sacToWav(st, path):
	for i in range(0, len(st.traces[0].data)):
		st.traces[0].data[i] *= 1000

	st.write(path, format='WAV', framerate=1000)