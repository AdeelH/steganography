from itertools import chain
from struct import pack
import numpy as np
from os import stat
from PIL import Image
import sys
from math import ceil
from common import *


def steg(img, data, bits):
	mask = int(''.join(['1'] * (8 - bits) + ['0'] * bits), 2)
	data = np.array(list(data), dtype=np.uint8)
	data = np.pad(data, (0, img.size - data.size), 'constant').reshape(img.shape)
	return (img & mask) | data


def prepare_data(data, fsize, bits):
	fsize_chunks = chunk_bits(tobits(pack('i', fsize)), bits)
	data_chunks = chunk_bits(tobits(data), bits)
	return chain(fsize_chunks, data_chunks)


if __name__ == '__main__':
	if len(sys.argv[1:]) < 3:
		print('\nError: insufficient number of arguments.\n')
		print('Usage: python steg.py <input-file> <image> <data-bits-per-byte>\n')
		exit()
	fname, img_in, bits, img_out = sys.argv[1:]

	bits = int(bits)
	img = np.array(Image.open(img_in), dtype=np.uint8)
	fsize = stat(fname).st_size
	fdata = np.fromfile(fname, dtype=np.uint8)

	assert 0 < bits <= 8
	assert 2 <= img.ndim <= 3
	assert len(fdata) == fsize
	assert ceil(8 * (fsize) / bits) + ceil(32 / bits) <= img.size

	print('Hiding contents of {} ({} bytes) in {} ...'.format(fname, fsize, img_in))

	stegged = steg(img, prepare_data(fdata, fsize, bits), bits)
	Image.fromarray(stegged).save(img_out)

	print('Done.\nNew image: {}'.format(img_out))
