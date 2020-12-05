# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import easyocr
import json
import numpy as np
import os
import sys


class NumpyEncoder(json.JSONEncoder):
    """ Custom encoder for numpy data types """

    def default(self, obj):
        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
                            np.int16, np.int32, np.int64, np.uint8,
                            np.uint16, np.uint32, np.uint64)):

            return int(obj)

        elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
            return float(obj)

        elif isinstance(obj, (np.complex_, np.complex64, np.complex128)):
            return {'real': obj.real, 'imag': obj.imag}

        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()

        elif isinstance(obj, np.bool_):
            return bool(obj)

        elif isinstance(obj, np.void):
            return None

        return json.JSONEncoder.default(self, obj)


def process_image(file_path):
    reader = easyocr.Reader(['en'])  # need to run only once to load model into memory
    result = reader.readtext(file_path)
    if result is None or len(result) == 0:
        print('No text detected')
        return
    else:
        result_json = []
        for text_data in result:
            result_json.append({'bound': text_data[0], 'text': text_data[1], 'confidence': text_data[2]})
        return result_json;
        # print(json.dumps(result_json, cls=NumpyEncoder))


def detect_text():
    i = 0
    log_path = sys.argv[2]
    result = []
    for file in os.listdir(sys.argv[1]):
        file_name, file_extension = os.path.splitext(file)
        if file_extension in ['.png', '.jpg']:
            i += 1
            if i % 3 == 0:
                image_file = sys.argv[1] + "/" + file
                detection_result = process_image(image_file)
                if detection_result is not None and len(detection_result) != 0:
                    result.append(detection_result)

    # convert into JSON:
    y = json.dumps(result, cls=NumpyEncoder)
    print(y)
    text_file = open(log_path, "w")
    text_file.write(y)
    text_file.close()
    return y


if __name__ == '__main__':
    # file_path = sys.argv[1]
    # if os.path.isfile(file_path):
    #     print("Submitted image to be processed by the model")
    #     process_image()
    # else:
    #     print('File does not exist in the given input file path')
    detect_text()
