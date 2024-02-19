import abc
import json

from dicttoxml import dicttoxml
import yaml

try:
    import django
except ImportError:
    django = None


class BaseRenderer(abc.ABC):
    @abc.abstractmethod
    def render(self, _stream, coerce_to_string=False):
        pass


class DictRenderer(BaseRenderer):
    def render(self, _stream, coerce_to_string=False):
        if coerce_to_string and isinstance(_stream, list) and len(_stream) == 1:
            return _stream[0]

        return _stream


class JSONRenderer(BaseRenderer):
    def render(self, _stream, coerce_to_string=False):
        return json.dumps(_stream)


class XMLRenderer(BaseRenderer):
    def render(self, _stream, coerce_to_string=False):
        return dicttoxml(_stream)


class YAMLRenderer(BaseRenderer):
    def render(self, _stream, coerce_to_string=False):
        return yaml.dump(_stream)


class GenericClassRenderer(BaseRenderer):
    def __init__(self, instance):
        self._instance = instance

    def render(self, _stream, coerce_to_string=False):
        for key, value in _stream.items():
            setattr(self._instance, key, value)


REGISTERED_RENDERERS = {'json': JSONRenderer, 'xml': XMLRenderer, 'yaml': YAMLRenderer, 'dict': DictRenderer, 'class': GenericClassRenderer}


if django:
    from django.template import Template

    class DjangoTemplateRenderer(BaseRenderer):
        def __init__(self, template: str):
            self._template = template

        def render(self, _stream, coerce_to_string=False):
            template = Template(self._template)
            return template.render(context=_stream)

    REGISTERED_RENDERERS['django'] = DjangoTemplateRenderer
