from .base import BaseFileHandler

try:
    from PIL import Image
except ImportError:
    Image = None

class PILHandler(BaseFileHandler):
    str_like = False

    def load_from_fileobj(self, file, **kwargs):
        return Image.open(file, **kwargs)

    def dump_to_fileobj(self, obj, file, **kwargs):
        obj.save(file, **kwargs)

    def dump_to_str(self, obj, **kwargs):
        raise NotImplementedError