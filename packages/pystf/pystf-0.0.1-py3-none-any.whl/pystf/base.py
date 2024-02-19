from typing import Any

try:
    import django
    from django.template import Template
except ImportError:
    django = None
    Template = None

from .exceptions import InvalidStreamType
from .types import Criteria, EmptyStream, ValueNotFound
from .renderers import REGISTERED_RENDERERS, GenericClassRenderer
from .utils import is_class, determine_stream_type

REGISTERED_TRANSFORMERS = {}


class BaseTransform:
    _stream = None
    _output = None
    _renderer = None

    def __init__(self, stream, output='dict', strict=False, delimiter="."):
        """Classes that implement BaseTransform must handle setting the the stream argument to
        self._stream
        """
        self.set_output(output=output, strict=strict)
        self._delimiter = delimiter

        assert self._stream is not None, 'Transform class must set self._stream'

    @classmethod
    def get_transformer_for_type(cls, stream, output='dict', strict=False, delimiter="."):
        from . import transformers  # noqa

        stream_type = determine_stream_type(stream)
        try:
            return REGISTERED_TRANSFORMERS[stream_type](stream, output, strict=strict, delimiter=delimiter)
        except KeyError:
            raise InvalidStreamType(f'No transformer found for type {stream_type}')

    def set_output(self, output, strict=False):
        # Try to determine if we got a class instance, if so, use the GenericClassRenderer, or a
        # specific renderer if one has been registered
        if django and isinstance(output, Template):
            self._output = 'django'
            self._renderer = REGISTERED_RENDERERS[self._output](output)
        if is_class(output):
            self._output = output.__class__.__name__
            if strict:
                try:
                    self._renderer = REGISTERED_RENDERERS[self._output](output)
                except KeyError as e:
                    raise ValueError('Invalid output format')
            else:
                self._renderer = REGISTERED_RENDERERS.get(self._output, GenericClassRenderer)(output)
        else:
            self._output = output
            try:
                self._renderer = REGISTERED_RENDERERS[self._output]()
            except KeyError as e:
                raise ValueError('Invalid output format')

    def _generate_output_stream(self, _stream, coerce_to_string=False):
        return self._renderer.render(_stream, coerce_to_string=coerce_to_string)

    def _parse_criteria(self, _criteria):
        key, operation, value = _criteria.split(' ')
        return Criteria(key=key, operation=operation, value=value.replace('"', '').replace("'", ""))  # FIXME

    def select(self, _filter, criteria, extract=None, _stream=EmptyStream, *, distinct=False, rendered=True, coerce_to_string=False):
        data = self.extract(_filter, _stream, rendered=False)
        if isinstance(data, str):
            data = [data]

        _criteria = self._parse_criteria(criteria)
        _res = []
        if data is None:
            return None

        for row in data:
            if isinstance(row, dict):
                value = row.get(_criteria.key, ValueNotFound())
                if _criteria.compare(value):
                    _res.append(row)
            elif hasattr(row, _criteria.key):
                value = getattr(row, _criteria.key)
                if _criteria.compare(value):
                    _res.append(row)

        if extract:
            _res = self.extract(extract, _stream=_res, distinct=distinct, rendered=False)

        if rendered:
            return self._generate_output_stream(_res, coerce_to_string=coerce_to_string)

        return _res

    def extract(self, _filter, _stream=EmptyStream, *, distinct=False, rendered=True, default_if_empty=None):
        fields = _filter.split(self._delimiter)

        if _stream is EmptyStream:
            s = self._stream
        else:
            s = _stream

        for i, field in enumerate(fields):
            if isinstance(s, dict):
                try:
                    _res = s[field]
                except KeyError:
                    s = None
                    break
            elif isinstance(s, list):
                _res = []
                for row in s:
                    _extracted_data = self.extract('.'.join(fields[i:]), row, rendered=rendered, default_if_empty=default_if_empty)
                    if not distinct or (distinct and _extracted_data not in _res):
                        _res.append(_extracted_data)
            elif is_class(s):
                value = getattr(s, field, ValueNotFound)
                if value is ValueNotFound:
                    break
                _res = value
            else:
                if isinstance(default_if_empty, Exception):
                    raise default_if_empty

                s = default_if_empty
                break

            s = _res

        if rendered:
            return self._generate_output_stream(s)
        return s

    def _map(self, key, func, *args, **kwargs):
        """A method for mapping keys from the specific function.  Currently, this is only called from
        `transform_multi`, and should be considered experimental.
        """
        return key, func(*args, **kwargs)

    def transform_multi(self, mapping: dict, output=None, strict=False, *, max_workers=5) -> Any:
        """A multi-threaded version of the transform function.  This is experimental, and
        things may change drastically.
        """
        import concurrent.futures

        # TODO - validate mapping
        if output:
            self.set_output(output, strict=strict)

        _data = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for key, _filter in mapping.items():
                func = getattr(self, _filter.pop('action'))
                transform_filter = _filter.pop('filter')
                futures.append(executor.submit(self._map, key, func, transform_filter, rendered=False, **_filter))

            for future in concurrent.futures.as_completed(futures):
                key, result = future.result()
                _data[key] = result

        return self._generate_output_stream(_data)

    def transform(self, mapping: dict, output=None, strict=False) -> Any:
        """Transforms a mapping using the requested actions."""
        # TODO - validate mapping
        if output:
            self.set_output(output, strict=strict)

        _data = {}
        for key, _filter in mapping.items():
            func = getattr(self, _filter.pop('action'))
            transform_filter = _filter.pop('filter')
            _data[key] = func(transform_filter, rendered=False, **_filter)

        return self._generate_output_stream(_data)
