import pyaudio as pa
import pyqtgraph as pg
import numpy as np
import time

# CHUNK = 1024
WINDOW_INTERVAL = 0.1
FRAME_RATE = 44100
BUFFER = 4096
FORMAT = pa.paInt16
CHANNELS = 1


N = WINDOW_INTERVAL * FRAME_RATE # == len(t)

T = 1./FRAME_RATE
T_SCALE = 100
T_RANGE = 200
F_SCALE = N/2 * 10
F_RANGE = 200
print('*************************')
print('   realtime visualizer')
print('   Press Ctrl-C to exit')
print('*************************')


p = pa.PyAudio()

floatdata = np.array([])
# raw data
t = np.arange(0, WINDOW_INTERVAL, step=1./FRAME_RATE)
y = np.zeros(len(t), dtype=np.float32)



# f = np.linspace(0, 1/(1*T), int(N/2)) # [0:2*fs/N:fs]
f = np.arange(0, FRAME_RATE/2, step=float(FRAME_RATE)/N); # [0:fs/N:fs/2]
# f = np.fft.fftfreq(int(N), d=1./FRAME_RATE)[:int(N/2)]

win = pg.GraphicsWindow(title='realtime music visualizer')

plotItem_fft = win.addPlot(title='fft')
# plotItem_fft.plot(f[1:], 2./len(t) * amp[1:], clear=True)

plotItem_fft.setYRange(0, F_RANGE)
plotItem_fft.setXRange(50, 2000)
win.nextRow()
plotItem_time = win.addPlot(title='raw data')

plotItem_time.setYRange(-T_RANGE, T_RANGE)

# y = 10000*(np.sin(2*np.pi*300*t) + 0.4*np.sin(2*np.pi*100*t))
# amp = abs(np.fft.fft(y)[:int(N/2)])
# plotItem_fft.plot(f[1:], amp[1:]/F_SCALE, clear=True)
# plotItem_time.plot(t, y/T_SCALE, clear=True)

def callback(in_data, frame_count, time_info, flag):
	global y
	try:
		data = in_data
		# print len(data)
		if len(data) == 0:
			return(data, pa.paComplete)
		intdata = np.array([])
		intdata = np.frombuffer(data, dtype=np.int16)
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
try:
	while stream.is_active():
		# print(y)
		plotItem_time.plot(t, y/T_SCALE, clear=True)
		amp = abs(np.fft.fft(y))[:int(N/2)]
		# plotItem_fft.plot(f, 2./len(t) * amp, clear=True)
		plotItem_fft.plot(f[1:], amp[1:]/F_SCALE, clear=True)
		time.sleep(0.1)
		pg.QtGui.QApplication.processEvents()
except KeyboardInterrupt:
	cleanup()
	exit(-1)

cleanup()