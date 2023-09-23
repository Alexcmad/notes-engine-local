"""
The main driver code of the app (solution) goes here
FASTAPI stuff
"""
import os

import wiki, openAI, file_reader, database


def upload_file(filename: str) -> dict:
    """

    :param filename: Name of tile to be uploaded
    :return: A Json object containing the content of the file
    """

    ext: str = filename.split(".")[1]

    extension_dict: dict = {
        "pdf": file_reader.read_pdf,
        "docx": file_reader.read_docx,
        "doc": file_reader.read_docx,
        "txt": file_reader.read_txt
    }
    response: dict = extension_dict.get(ext, file_reader.ocr_with_tesseract)(filename)
    database.insert_file_data(filename=response['filename'], content=response['content'], keywords=response['keywords'])


