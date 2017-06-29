from itertools import zip_longest


# adapted from https://stackoverflow.com/a/434411
def chunk_bits(iterable, chunk_size, padding=True):
	args = [iter(iterable)] * chunk_size
	chunks = zip_longest(*args, fillvalue='0') if padding else zip(*args)
	return (int(''.join(chunk[::-1]), 2) for chunk in chunks)


def tobits(bs, per_byte=8):
	for b in bs:
		for i in range(per_byte):
			yield str((b & (1 << i)) >> i)
