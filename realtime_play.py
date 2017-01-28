import pyaudio as pa
import pyqtgraph as pg
import numpy as np
import time
import sys
import wave

CHUNK = 1024
SLEEP_TIME = 0.1
WINDOW_INTERVAL = 0.5
BUFFER = 4096


if len(sys.argv) != 2:
	print 'Usage: python %s filename.wav' % sys.argv[0]
	exit(-1)
filename = sys.argv[1]



p = pa.PyAudio()
wf = wave.open(filename, 'rb')

floatdata = np.array([])
# raw data
t = np.arange(WINDOW_INTERVAL, step=1./wf.getframerate())
y = np.zeros(len(t))

# freq
N = WINDOW_INTERVAL * wf.getframerate()

T = 1./wf.getframerate()
f = np.linspace(0., 1./(1.*T), N/2)
amp = abs(np.fft.fft(y)[:N/2])
win = pg.GraphicsWindow(title='realtime music visualizer')
plotItem_fft = win.addPlot(title='fft')
plotItem_fft.plot(f[1:], 2./len(t) * amp[1:], clear=True)
plotItem_fft.setYRange(0, 5000)
plotItem_fft.setXRange(0, 2000)
win.nextRow()
plotItem_time = win.addPlot(title='raw data')
plotItem_time.plot(t, y, clear=True)
plotItem_time.setYRange(-50000, 50000)


def callback(in_data, frame_count, time_info, flag):
	global y, first, tmpdata
	try:
		data = wf.readframes(frame_count)
		# print len(data)
		if len(data) == 0:
			return(data, pa.paComplete)
		intdata = np.array([])
		if wf.getsampwidth() == 2:
			intdata = np.fromstring(data, dtype=np.int16)
		else:
			intdata = (np.fromstring(data, dtype=np.int8)).astype(np.int16)
			intdata <<= 6
		y = np.roll(y, -8192)
		y[-8192:] = intdata
		return (data, pa.paContinue)
	except KeyboardInterrupt:
		cleanup()
		exit(-1)
	# except ValueError:
	# 	cleanup()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
				rate=wf.getframerate(),
				channels=wf.getnchannels(),
				frames_per_buffer=BUFFER,
				output=True,
				stream_callback=callback)
def cleanup():
	stream.stop_stream()
	wf.close()
	p.terminate()



stream.start_stream()
while stream.is_active():
	try:
		plotItem_time.plot(t, y, clear=True)
		amp = abs(np.fft.fft(y)[:len(y)/2])
		plotItem_fft.plot(f, 2./len(t)*amp, clear=True)
		pg.QtGui.QApplication.processEvents()
	except KeyboardInterrupt:
		cleanup()
		exit(-1)

cleanup()