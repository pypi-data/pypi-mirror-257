import json

import xmltodict
import yaml

from .base import BaseTransform, REGISTERED_TRANSFORMERS


class JSONTransform(BaseTransform):
    def __init__(self, stream, output='dict', strict=False, delimiter="."):
        self._stream = json.loads(stream)
        super().__init__(stream, output=output, strict=strict, delimiter=delimiter)


REGISTERED_TRANSFORMERS['json'] = JSONTransform


class DictTransform(BaseTransform):
    def __init__(self, stream, output='dict', strict=False, delimiter='.'):
        self._stream = stream
        super().__init__(stream, output=output, strict=strict, delimiter=delimiter)


REGISTERED_TRANSFORMERS['dict'] = DictTransform


class XMLTransform(BaseTransform):
    def __init__(self, stream, output='dict', strict=False, delimiter='.'):
        self._stream = xmltodict.parse(stream)
        super().__init__(stream, output=output, strict=strict, delimiter=delimiter)


REGISTERED_TRANSFORMERS['xml'] = XMLTransform


class YAMLTransform(BaseTransform):
    def __init__(self, stream, output='dict', strict=False, delimiter='.'):
        self._stream = yaml.load(stream)
        super().__init__(stream, output=output, strict=strict, delimiter=delimiter)


REGISTERED_TRANSFORMERS['yaml'] = YAMLTransform


class ClassTransform(BaseTransform):
    """
    There's really not any difference between this an DictTransform right now, but there may
    be in the future
    """
    def __init__(self, stream, output='dict', strict=False, **kwargs):
        self._stream = stream
        super().__init__(stream, output=output, strict=strict)


REGISTERED_TRANSFORMERS['class'] = ClassTransform


def get_transformer(stream, output='dict', strict=False, delimiter='.') -> type[BaseTransform]:
    return BaseTransform.get_transformer_for_type(stream, output=output, strict=strict, delimiter=delimiter)
