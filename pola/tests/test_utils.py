from reportlab.graphics import renderPM

from pola.product.images import Barcode


def get_dummy_image(code="123", width=300):
    barcode = Barcode.get_barcode(code, width)
    data = renderPM.drawToString(barcode, fmt='PNG')
    return data
