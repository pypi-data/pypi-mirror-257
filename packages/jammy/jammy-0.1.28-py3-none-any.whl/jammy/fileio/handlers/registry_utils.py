# Copyright (c) OpenMMLab. All rights reserved.
from jammy.utils.py_types import is_list_of

from .base import BaseFileHandler
from .json_handler import JsonHandler
from .pickle_handler import PickleHandler
from .pil_handler import PILHandler
from .tarfile_handler import TarHandler
from .torch_handler import TorchHandler
from .yaml_handler import YamlHandler

file_handlers = {
    "json": JsonHandler(),
    "yaml": YamlHandler(),
    "yml": YamlHandler(),
    "pickle": PickleHandler(),
    "pkl": PickleHandler(),
    "pt": TorchHandler(),
    "pth": TorchHandler(),
    "ckpt": TorchHandler(),
    "tar": TarHandler(),
    "jpg": PILHandler(),
    "jpeg": PILHandler(),
    "png": PILHandler(),
    "bmp": PILHandler(),
    "gif": PILHandler(),
}


def _register_handler(handler, file_formats):
    """Register a handler for some file extensions.

    Args:
        handler (:obj:`BaseFileHandler`): Handler to be registered.
        file_formats (str or list[str]): File formats to be handled by this
            handler.
    """
    if not isinstance(handler, BaseFileHandler):
        raise TypeError(
            f"handler must be a child of BaseFileHandler, not {type(handler)}"
        )
    if isinstance(file_formats, str):
        file_formats = [file_formats]
    if not is_list_of(file_formats, str):
        raise TypeError("file_formats must be a str or a list of str")
    for ext in file_formats:
        file_handlers[ext] = handler


def register_handler(file_formats, **kwargs):
    def wrap(cls):
        _register_handler(cls(**kwargs), file_formats)
        return cls

    return wrap
