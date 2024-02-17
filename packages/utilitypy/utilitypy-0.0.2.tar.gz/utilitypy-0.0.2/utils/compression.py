from io import BytesIO as _BytesIO
from zlib import (
    compressobj as _compressobj,
    decompressobj as _decompressobj
)
from gzip import (
    open as _gzipopen
)
from bz2 import (
    open as _bz2open,
    BZ2Compressor as _BZ2Compressor,
    BZ2Decompressor as _BZ2Decompressor,
)
from lzma import (
    open as _lzmaopen,
    LZMACompressor as _LZMACompressor,
    LZMADecompressor as _LZMADecompressor,
)


def gzip_file_generator(file_path, mode="rb", chunk_size=4096):
    '''The function `gzip_file_generator` reads a file in chunks and yields the decompressed data using the
    gzip compression algorithm.

    Parameters
    ----------
    file_path
        The file path is the path to the file that you want to gzip or decompress. It can be either a
    relative or absolute path.
    mode, optional
        The "mode" parameter specifies the mode in which the file should be opened. The default value is
    "rb", which means the file will be opened in binary read mode. This is suitable for reading binary
    files like gzip compressed files.
    chunk_size, optional
        The `chunk_size` parameter determines the size of each chunk of data that is read from the file. It
    is set to a default value of 4096 bytes, but you can change it to a different value if desired.

    '''
    c = _decompressobj()
    with _gzipopen(file_path, mode=mode) as fout:
        while True:
            data = fout.read(chunk_size)
            if not data:
                break
            yield c.decompress(data) # type: ignore


def bz2_file_generator(file_path, mode="rb", chunk_size=4096):
    '''The `bz2_file_generator` function is a generator that reads a file in chunks and yields the
    decompressed data using the BZ2 compression algorithm.

    Parameters
    ----------
    file_path
        The file_path parameter is the path to the BZ2 file that you want to read and decompress. It should
    be a string representing the file path, including the file name and extension.
    mode, optional
        The "mode" parameter specifies the mode in which the file should be opened. The default value is
    "rb", which means the file will be opened in binary mode for reading. However, you can also specify
    other modes like "r" for reading in text mode, "wb" for writing in
    chunk_size, optional
        The `chunk_size` parameter determines the size of each chunk of data that is read from the file. It
    is set to a default value of 4096 bytes, but you can change it to a different value if desired.

    '''
    c = _BZ2Decompressor()
    with _bz2open(file_path, mode=mode) as fout:
        while True:
            data = fout.read(chunk_size)
            if not data:
                break
            yield c.decompress(data) # type: ignore


def lzma_file_generator(file_path, mode="rb", chunk_size=4096):
    '''The `lzma_file_generator` function reads a file in chunks and yields the decompressed data using the
    LZMA compression algorithm.

    Parameters
    ----------
    file_path
        The file path is the path to the file that you want to decompress using the LZMA algorithm. It can
    be either a relative or an absolute path.
    mode, optional
        The "mode" parameter specifies the mode in which the file should be opened. The default value is
    "rb", which means the file will be opened in binary read mode. Other possible values for "mode"
    include "r" for text read mode, "w" for text write mode, "
    chunk_size, optional
        The `chunk_size` parameter determines the size of each chunk of data that is read from the file. It
    specifies the number of bytes to read at a time. In this case, the default value is set to 4096
    bytes.

    '''
    c = _LZMADecompressor()
    with _lzmaopen(file_path, mode=mode) as fout:
        while True:
            data = fout.read(chunk_size)
            if not data:
                break
            yield c.decompress(data) # type: ignore


def txt_file_generator(file_path, mode="rb", chunk_size=4096):
    '''The function `txt_file_generator` is a generator that reads a file in chunks and yields each chunk
    of data.

    Parameters
    ----------
    file_path
        The file path is the location of the file that you want to read or generate. It can be a relative
    or absolute path.
    mode, optional
        The "mode" parameter specifies the mode in which the file should be opened. The default value is
    "rb", which stands for "read binary". This mode is used for reading binary files, such as images or
    audio files.
    chunk_size, optional
        The chunk_size parameter determines the size of each chunk of data that is read from the file. In
    this case, it is set to 4096 bytes.

    '''
    with open(file=file_path, mode=mode) as fout:
        while True:
            data = fout.read(chunk_size)
            if not data:
                break
            yield data


_FILE_GENERATORS = {
    None: txt_file_generator,
    "gzip": gzip_file_generator,
    "bz2": bz2_file_generator,
    "lzma": lzma_file_generator,
}


def file_generator(file_path, mode="rb", chunk_size=4096, compression=None):
    '''The function `file_generator` is a generator that yields chunks of data from a file, with optional
    compression.

    Parameters
    ----------
    file_path
        The file path is the location of the file that you want to generate. It can be either a relative or
    an absolute path.
    mode, optional
        The `mode` parameter specifies the mode in which the file should be opened. It is optional and has
    a default value of "rb", which stands for "read binary". This mode is used for reading binary files.
    chunk_size, optional
        The chunk_size parameter determines the size of each chunk of data that is read from the file. It
    is measured in bytes. By default, it is set to 4096 bytes, but you can change it to a different
    value if desired.
    compression
        The `compression` parameter is used to specify the type of compression to be used when reading the
    file. It can be set to `None` if no compression is needed.

    '''
    yield from _FILE_GENERATORS[compression](file_path, mode=mode, chunk_size=chunk_size)


def gzip_compress_file(file_path, output=None, chunk_size=4096):
    '''The function `gzip_compress_file` compresses a file using the gzip algorithm and returns the
    compressed data.

    Parameters
    ----------
    file_path
        The file path is the path to the file that you want to compress using gzip.
    output
        The `output` parameter is an optional argument that specifies the output file or buffer where the
    compressed data will be written. If `output` is not provided or is set to `None`, a new `BytesIO`
    object will be created and used as the output buffer. If `output` is
    chunk_size, optional
        The `chunk_size` parameter specifies the size of each chunk of data that is read from the file and
    compressed. It determines how much data is processed at a time. In this case, the default value is
    set to 4096 bytes.

    Returns
    -------
        either a BytesIO object containing the compressed data, or True if an output parameter is provided.

    '''
    buf = output or _BytesIO()
    c = _compressobj()
    with _gzipopen(buf, "wb") as fout:
        for data in file_generator(file_path, mode="rb", chunk_size=chunk_size):
            fout.write(c.compress(data))
        fout.write(c.flush())
    if isinstance(buf, _BytesIO):
        buf.seek(0)
        return buf
    return True


def bz2_compress_file(file_path, output=None, chunk_size=4096):
    '''The function `bz2_compress_file` compresses a file using the BZ2 compression algorithm and returns
    the compressed data.

    Parameters
    ----------
    file_path
        The file path is the path to the file that you want to compress.
    output
        The `output` parameter is an optional argument that specifies the output file or buffer where the
    compressed data will be written. If no `output` is provided, a new `_BytesIO` object will be created
    and used as the output buffer.
    chunk_size, optional
        The `chunk_size` parameter specifies the size of each chunk of data that is read from the file and
    compressed. It is set to a default value of 4096 bytes.

    Returns
    -------
        either the compressed file as a BytesIO object or True if an output file path is not provided.

    '''
    buf = output or _BytesIO()
    c = _BZ2Compressor()
    with _bz2open(buf, "wb") as fout:
        for data in file_generator(file_path, mode="rb", chunk_size=chunk_size):
            fout.write(c.compress(data))
        fout.write(c.flush())
    if isinstance(buf, _BytesIO):
        buf.seek(0)
        return buf
    return True


def lzma_compress_file(file_path, output=None, chunk_size=4096):
    '''The function `lzma_compress_file` compresses a file using the LZMA algorithm and returns the
    compressed data.

    Parameters
    ----------
    file_path
        The file path is the path to the file that you want to compress.
    output
        The `output` parameter is an optional argument that specifies the output file or buffer where the
    compressed data will be written. If no output is provided, a `_BytesIO` object is created and used
    as the output buffer.
    chunk_size, optional
        The `chunk_size` parameter specifies the size of each chunk of data that is read from the file and
    compressed. It determines how much data is processed at a time during the compression process. In
    this case, the default value is set to 4096 bytes.

    Returns
    -------
        either the compressed file as a BytesIO object or True if an output file path is not provided.

    '''
    buf = output or _BytesIO()
    c = _LZMACompressor()
    with _lzmaopen(buf, "wb") as fout:
        for data in file_generator(file_path, mode="rb", chunk_size=chunk_size):
            fout.write(c.compress(data))
        fout.write(c.flush())
    if isinstance(buf, _BytesIO):
        buf.seek(0)
        return buf
    return True


def gzip_decompress_file(file_path, output=None, chunk_size=4096):
    '''The function `gzip_decompress_file` decompresses a gzip file and either writes the decompressed data
    to a file or returns it as a BytesIO object.

    Parameters
    ----------
    file_path
        The file path is the path to the gzip-compressed file that you want to decompress.
    output
        The `output` parameter is the file path where the decompressed data will be written. If `output` is
    `None`, the decompressed data will be returned as a BytesIO object.
    chunk_size, optional
        The `chunk_size` parameter specifies the size of each chunk of data that is read from the
    compressed file during decompression. It determines how much data is read and processed at a time.
    The default value is 4096 bytes, but you can adjust it based on your specific needs.

    Returns
    -------
        The function `gzip_decompress_file` returns either `True` if an `output` file path is provided and
    the decompressed data is successfully written to the output file, or it returns a `BytesIO` object
    containing the decompressed data if no `output` file path is provided.

    '''
    if output is not None:
        with open(output, "wb") as fout:
            for line in gzip_file_generator(file_path=file_path, mode="rb", chunk_size=chunk_size):
                fout.write(line)
        return True
    else:
        buf = _BytesIO()
        for line in gzip_file_generator(file_path=file_path, mode="rb", chunk_size=chunk_size):
            buf.write(line)
        buf.seek(0)
        return buf


def bz2_decompress_file(file_path, output=None, chunk_size=4096):
    '''The function `bz2_decompress_file` decompresses a file in the BZ2 format and either writes the
    decompressed data to a new file or returns it as a BytesIO object.

    Parameters
    ----------
    file_path
        The file path is the path to the compressed file that you want to decompress.
    output
        The `output` parameter is the file path where the decompressed data will be written. If `output` is
    `None`, the decompressed data will be returned as a BytesIO object instead of being written to a
    file.
    chunk_size, optional
        The `chunk_size` parameter specifies the size of each chunk of data that is read from the
    compressed file during decompression. It determines how much data is read at a time and can affect
    the performance and memory usage of the decompression process. A larger chunk size may result in
    faster decompression but

    Returns
    -------
        The function `bz2_decompress_file` returns either `True` if an output file is specified and the
    decompressed data is successfully written to the file, or it returns a `BytesIO` object containing
    the decompressed data if no output file is specified.

    '''
    if output is not None:
        with open(output, "wb") as fout:
            for line in bz2_file_generator(file_path=file_path, mode="rb", chunk_size=chunk_size):
                fout.write(line)
        return True
    else:
        buf = _BytesIO()
        for line in bz2_file_generator(file_path=file_path, mode="rb", chunk_size=chunk_size):
            buf.write(line)
        buf.seek(0)
        return buf


def lzma_decompress_file(file_path, output=None, chunk_size=4096):
    '''The function `lzma_decompress_file` decompresses an LZMA compressed file and either writes the
    decompressed data to a file or returns it as a BytesIO object.

    Parameters
    ----------
    file_path
        The file path is the path to the LZMA compressed file that you want to decompress.
    output
        The `output` parameter is the file path where the decompressed data will be written. If `output` is
    `None`, the decompressed data will be returned as a BytesIO object.
    chunk_size, optional
        The `chunk_size` parameter specifies the size of the chunks in which the file is read and written.
    It determines how much data is processed at a time. In this case, the default value is set to 4096
    bytes.

    Returns
    -------
        The function `lzma_decompress_file` returns either `True` if an output file is specified and the
    decompressed data is successfully written to the output file, or it returns a `BytesIO` object
    containing the decompressed data if no output file is specified.

    '''
    if output is not None:
        with open(output, "wb") as fout:
            for line in lzma_file_generator(file_path=file_path, mode="rb", chunk_size=chunk_size):
                fout.write(line)
        return True
    else:
        buf = _BytesIO()
        for line in lzma_file_generator(file_path=file_path, mode="rb", chunk_size=chunk_size):
            buf.write(line)
        buf.seek(0)
        return buf


_COMPRESSION_FN = {
    None: gzip_compress_file,
    "gzip": gzip_compress_file,
    "bz2": bz2_compress_file,
    "lzma": lzma_compress_file
}

_DECOMPRESSION_FN = {
    None: gzip_decompress_file,
    "gzip": gzip_decompress_file,
    "bz2": bz2_decompress_file,
    "lzma": lzma_decompress_file
}


def compress_file(file_path, output=None, compression="gzip", chunk_size=4096):
    '''The function compresses a file using a specified compression algorithm and saves the compressed file
    to a specified output location.

    Parameters
    ----------
    file_path
        The path to the file that you want to compress.
    output
        The `output` parameter is used to specify the path where the compressed file will be saved. If no
    value is provided for `output`, the compressed file will be saved in the same directory as the
    original file with the same name, but with the appropriate file extension for the chosen compression
    method.
    compression, optional
        The "compression" parameter specifies the type of compression to be used when compressing the file.
    The default value is "gzip", which stands for GNU zip compression. Other possible values for this
    parameter could be "zip", "bz2" (bzip2 compression), or "lzma" (
    chunk_size, optional
        The `chunk_size` parameter specifies the size of each chunk of data that is read from the input
    file and written to the output file during compression. It determines how much data is processed at
    a time. In this case, the default value is set to 4096 bytes.

    Returns
    -------
        the result of calling the compression function specified by the "compression" parameter on the file
    specified by "file_path". The result is then returned.

    '''
    fn = _COMPRESSION_FN.get(compression.lower(), _COMPRESSION_FN[None])
    return fn(file_path, output, chunk_size)


def decompress_file(file_path, output=None, compression="gzip", chunk_size=4096):
    '''The function decompresses a file using the specified compression algorithm and saves the output to a
    specified location.

    Parameters
    ----------
    file_path
        The file path is the location of the compressed file that you want to decompress. It should be a
    string that specifies the path to the file on your computer's file system.
    output
        The output parameter specifies the path where the decompressed file will be saved. If no output
    path is provided (i.e., output=None), the decompressed file will be saved in the same directory as
    the compressed file with the same name, but without the compression extension.
    compression, optional
        The "compression" parameter specifies the type of compression used for the file. It can be one of
    the following values:
    chunk_size, optional
        The chunk_size parameter determines the size of the chunks in which the compressed file will be
    read and decompressed. It specifies the number of bytes to be read at a time from the compressed
    file. This parameter is useful when dealing with large files, as it allows for efficient memory
    usage by decompressing

    Returns
    -------
        the result of calling the appropriate decompression function based on the specified compression
    type.

    '''
    fn = _DECOMPRESSION_FN.get(compression.lower(), _DECOMPRESSION_FN[None])
    return fn(file_path, output, chunk_size)