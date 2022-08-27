import pathlib
import zipfile
import io
from typing import Iterator


def compress(file_names : Iterator[pathlib.Path]) -> bytes:
    zip_buffer = io.BytesIO()

    # Select the compression mode ZIP_DEFLATED for compression
    # or zipfile.ZIP_STORED to just store the file
    compression = zipfile.ZIP_DEFLATED

    # create the zip file first parameter path/name, second mode
    zf = zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False)
    try:
        for file_name in file_names:
            if file_name.exists():
                assert isinstance(file_name, pathlib.Path)
                # Add file to the zip file
                # first parameter file to zip, second filename in zip
                zf.writestr(file_name.name, file_name.read_bytes())
                # zf.write(file_name.absolute(), file_name.name, compress_type=compression)

    except FileNotFoundError:
        print("An error occurred")
    finally:
        # Don't forget to close the file!
        zf.close()

    return zip_buffer.getvalue()

def blocks(files, size=65536):
    # https://stackoverflow.com/questions/9629179/python-counting-lines-in-a-huge-10gb-file-as-fast-as-possible
    while True:
        b = files.read(size)
        if not b: break
        yield b
