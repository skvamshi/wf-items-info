import tesserocr


def detect_text_tess(path):
    print(tesserocr.tesseract_version())  # print tesseract-ocr version
    print(tesserocr.get_languages())  # prints tessdata path and list of available languages
    return tesserocr.file_to_text(path, lang='eng')
