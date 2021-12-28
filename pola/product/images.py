from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.graphics.shapes import Drawing
from reportlab.lib import units


class Barcode:
    @staticmethod
    def get_barcode(value, width, barWidth=0.05 * units.inch, fontSize=30, humanReadable=True):

        barcode = createBarcodeDrawing(
            'Code128', value=value, barWidth=barWidth, fontSize=fontSize, humanReadable=humanReadable
        )

        drawing_width = width
        barcode_scale = drawing_width / barcode.width
        drawing_height = barcode.height * barcode_scale

        drawing = Drawing(drawing_width, drawing_height)
        drawing.scale(barcode_scale, barcode_scale)
        drawing.add(barcode, name='barcode')

        return drawing
