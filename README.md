# Realtime-music-visualizer
Realtime visualizer built with python.

Wav file supported only.
To adjust the frequency sensitivity, modify `WINDOW_INTERVAL` in `realtime_play.py`.

**Usage: python realtime_play.py musicToPlay.wav**

Realtime visualize audio data received:

**Usage: python realtime_record.py**

If mp3 is to be played, here's also a script `toWav.sh` to convert mp3 to wav.

**Usage: ./toWav.sh outfile.wav inFile.mp3**

## Library required:
[pyqtgraph](http://www.pyqtgraph.org/)

[pyaudio](https://people.csail.mit.edu/hubert/pyaudio/docs/)

[numpy](http://www.numpy.org/)
