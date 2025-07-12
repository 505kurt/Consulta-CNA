import warnings
from io import BytesIO

import easyocr
import numpy
import requests
from PIL import Image

warnings.filterwarnings('ignore', category=UserWarning)

reader = easyocr.Reader(['pt'])


def ocr_check_status(image_url):
    response = requests.get(image_url)
    response.raise_for_status()

    img = numpy.array(Image.open(BytesIO(response.content)))

    results = reader.readtext(img)

    texts = [text.upper() for (_, text, _) in results]

    for keyword in ['REGULAR', 'LICENCIADO', 'CANCELADO']:
        if any(keyword in t for t in texts):
            return keyword

    return 'STATUS NÃO IDENTIFICADO'
