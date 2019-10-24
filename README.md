# fouriergif

Some fun Python code for creating .gif files of Fourier transforms over the duration of an audio file. The audio file should be a .wav file containing audible sound (i.e. below 20 kHz for young people). To use this code, you must have the following external packages: [numpy](https://numpy.org/), [matplotlib](https://matplotlib.org/), [scipy](https://www.scipy.org/), and [imageio](http://imageio.github.io/). 

To create a .gif, simply run the `fourier_gif` function with a file name and a value for frames per second (note that large .wav files will result in unruly sizes for .gif files at high framerates):

```python
fname = 'assets/freq_sweep.wav'	# file name
fps = 10			# frames per second
fourier_gif(fname, fps)		# creates a .gif file with the same name as the .wav
```