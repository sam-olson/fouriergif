from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
from scipy.signal import find_peaks
import imageio
import os
import datetime
import time
import shutil

def pad_to_two(n):
    '''Pads a string of numbers to two digits by placing zeros in front'''
    n = str(n)
    while len(n) < 2:
        n = '0' + n
    return n

def make_time_stamp():
    ''' Creates time stamp with current time in format YYMMDDHHmmSS'''
    dt = datetime.datetime.now()
    dtstrng = str(dt.year)[2:] + pad_to_two(str(dt.month)) + pad_to_two(str(dt.day)) + '_' + pad_to_two(str(dt.hour)) + pad_to_two(str(dt.minute)) + pad_to_two(str(dt.second))
    return dtstrng

def fourier_gif(f, fps, saveimg = False):
    '''Function that takes a file and creates a .gif with
    Fourier transforms of the file through time.

    Parameters
    -----------
    f: file to analyze (in .wav format)
    fps: frames per second of the resulting .gif file
    saveimg: if True, keeps images used to create .gif
    '''
    start = time.time()

    fs, data = wavfile.read(f)

    # calculating length of data and period (t)
    n = len(data)
    t = 1 / fs

    # finding points at which to slice data based on frames per second
    # provided by user
    framlen = fs / fps
    nslice = n // framlen
    slicepts = n / nslice

    # residual (last) slice
    resslice = n%framlen / framlen

    # creating list of beginning/ending points for slicing
    slices = []
    for i in range(int(nslice)):
        begpt = int(i * slicepts)
        endpt = int(((i + 1) * slicepts) - 1)
        slices.append([begpt, endpt])

    # initializing data lists
    images = []
    drctry = 'Pics'+make_time_stamp()
    os.mkdir(drctry)

    # iterating through slice pts and calculating the FFT
    for j in range(len(slices)):
        y = data[slices[j][0]:slices[j][1]]
        N = len(y)
        xf = np.linspace(0.0, 1.0 / (2.0*t), N / 2)
        yf = scipy.fftpack.fft(y)
        scaled_yf = 2.0/N * np.abs(yf[:N // 2])
        time_stamp = j * (1/fps)

        # plotting/saving plots

        plt.plot(xf, scaled_yf)
        plt.xlim([0,20000])
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Intensity')
        plt.title(str(round(time_stamp, 3)) + 's')
        picname = drctry + '/IMG' + str(j) + '.png'
        plt.savefig(picname, dpi = 100)
        plt.close()
        images.append(imageio.imread(picname))

    # creating .gif
    imageio.mimsave(f.split('.')[0] + '.gif', images, duration = 1 / fps)

    # deleting images used to make .gif (unless the user wants to keep them)
    if saveimg == False:
        shutil.rmtree(drctry)
    end = time.time()
    print('That took {} seconds'.format(str(round(end-start,3))))

if __name__ == "__main__":
    fname = 'assets/freq_sweep.wav'
    fourier_gif(fname, 10)
