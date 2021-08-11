import io
import json


class JsonRequestMixin:
    def json_request(self, url, data=None, **kwargs):
        body = json.dumps(data)
        return self.client.post(url, body, content_type="application/json", **kwargs)


def _create_image(width=100, height=None, color='blue', image_format='JPEG', image_palette='RGB'):
    # ImageField (both django's and factory_boy's) require PIL.
    # Try to import it along one of its known installation paths.
    from PIL import Image

    height = height or width

    thumb_io = io.BytesIO()
    with Image.new(image_palette, (width, height), color) as thumb:
        thumb.save(thumb_io, format=image_format)
    return thumb_io.getvalue()
