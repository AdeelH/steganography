Allows hiding binary data in an image, the data is broken into bit-chunks of the specified size and each chunk is stored in the least significant bits of each byte of the image.

The reverse operation extracts the data from the image and restores it to a file.

## Usage
```shell
# hide data
$ python steg.py <input-data-file> <input-image> <data-bits-per-byte> <output-image>

# unhide data
$ python unsteg.py <image> <data-bits-per-byte> <output-file>
```

## Dependencies
- Numpy
- Pillow
