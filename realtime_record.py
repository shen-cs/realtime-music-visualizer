import pyaudio as pa
import pyqtgraph as pg
import numpy as np
import time

# CHUNK = 1024
WINDOW_INTERVAL = 0.5
FRAME_RATE = 44100
BUFFER = 4096
FORMAT = pa.paInt16
CHANNELS = 2
print '*************************'
print '   realtime visualizer'
print '   Press Ctrl-C to exit'
print '*************************'


p = pa.PyAudio()

floatdata = np.array([])
# raw data
t = np.arange(WINDOW_INTERVAL, step=1./FRAME_RATE)
y = np.zeros(len(t))

# freq
N = WINDOW_INTERVAL * FRAME_RATE

T = 1./FRAME_RATE
f = np.linspace(0., 1./(1.*T), N/2)
amp = abs(np.fft.fft(y)[:N/2])
win = pg.GraphicsWindow(title='realtime music visualizer')
plotItem_fft = win.addPlot(title='fft')
plotItem_fft.plot(f[1:], 2./len(t) * amp[1:], clear=True)
plotItem_fft.setYRange(0, 1200)
plotItem_fft.setXRange(50, 2000)
win.nextRow()
plotItem_time = win.addPlot(title='raw data')
plotItem_time.plot(t, y, clear=True)
plotItem_time.setYRange(-20000, 20000)


def callback(in_data, frame_count, time_info, flag):
	global y
	try:
		data = in_data
		# print len(data)
		if len(data) == 0:
			return(data, pa.paComplete)
		intdata = np.array([])
		intdata = np.fromstring(data, dtype=np.int16)
		y = np.roll(y, -len(intdata))
		y[-len(intdata):] = intdata
		return (data, pa.paContinue)
	except KeyboardInterrupt:
		cleanup()
		exit(-1)
	# except ValueError:
	# 	cleanup()

stream = p.open(format=FORMAT,
				rate=FRAME_RATE,
				channels=CHANNELS,
				frames_per_buffer=BUFFER,
				input=True,
				stream_callback=callback)
def cleanup():
	stream.stop_stream()
	p.terminate()



stream.start_stream()
while stream.is_active():
	try:
		plotItem_time.plot(t, y, clear=True)
		amp = abs(np.fft.fft(y)[:len(y)/2])
		plotItem_fft.plot(f, 2./len(t) * amp, clear=True)
		pg.QtGui.QApplication.processEvents()
	except KeyboardInterrupt:
		cleanup()
		exit(-1)

cleanup()