# Stubs for gzip
from io import BufferedReader

# TODO: finish annotation
def open(filename: str,
	 mode: str = 'rb',
	 compresslevel: int = 9,
	 encoding: str = None) -> BufferedReader: ...
