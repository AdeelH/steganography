from itertools import chain, islice
import numpy as np
from PIL import Image
import sys
from math import ceil
from common import *


def unsteg(img, bits):
	mask = int(''.join(['0'] * (8 - bits) + ['1'] * bits), 2)
	chunks = np.nditer(img & mask)

	# extract the size in bytes of the hidden data
	dsize_bytes = chunks_to_bytes(islice(chunks, ceil(32 / bits)), bits)
	dsize = int.from_bytes(dsize_bytes, byteorder='little')

	# extract the data itself
	data_chunks = islice(chunks, ceil(8 * dsize / bits))
	data = list(chunks_to_bytes(data_chunks, bits))

	return np.array(data, dtype=np.uint8)


def chunks_to_bytes(chunks, chunk_size):
	bit_stream = chain.from_iterable(tobits(chunks, chunk_size))
	return chunk_bits(bit_stream, 8, False)


if __name__ == '__main__':
	if len(sys.argv[1:]) < 3:
		print('\nError: insufficient number of arguments.\n')
		print('Usage: python unsteg.py <image> <data-bits-per-byte> <output-file>\n')
		exit()
	img_in, bits, fout = sys.argv[1:]

	bits = int(bits)
	img = np.array(Image.open(img_in), dtype=np.uint8)

	assert 0 < bits <= 8
	assert 2 <= img.ndim <= 3

	print('Extracting hidden data from {} ... '.format(img_in))

	data = unsteg(img, bits)
	data.tofile(fout)

	print('Done.\nData saved to: {} '.format(fout))
