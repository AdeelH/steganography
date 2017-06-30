from itertools import chain
from struct import pack
import numpy as np
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
	if len(sys.argv[1:]) < 4:
		print('\nError: insufficient number of arguments.\n')
		print('Usage: python steg.py <input-file> <input-image> <data-bits-per-byte> <output-image>\n')
		exit()
	# read in command line args
	filename, img_in, bits, img_out = sys.argv[1:]

	# # of bits per byte of the image that will be overwritten
	bits = int(bits)
	# load image into a numpy array
	img = np.array(Image.open(img_in), dtype=np.uint8)
	# read binary data from file into a numpy array
	fdata = np.fromfile(filename, dtype=np.uint8)
	fsize = fdata.size

	# sanity checks
	assert 0 < bits <= 8
	assert 2 <= img.ndim <= 3
	assert ceil(8 * (fsize) / bits) + ceil(32 / bits) <= img.size

	print('Hiding contents of {} ({} bytes) in {} ...'.format(filename, fsize, img_in))

	# break into bit-chunks; also include the data size
	data = prepare_data(fdata, fsize, bits)

	# apply steganography
	stegged = steg(img, data, bits)

	# save modified image
	Image.fromarray(stegged).save(img_out)

	print('Done.\nNew image: {}'.format(img_out))
