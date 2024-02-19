from .exceptions import InvalidStreamType


def is_class(obj):
    return hasattr(obj, '__dict__')  # FIXME - probably not a great way to determine this


def determine_stream_type(stream):  # FIXME - need way more sophisticated checks here
    if isinstance(stream, dict):
        return 'dict'
    elif isinstance(stream, str):
        cleaned_stream = stream.strip()[:100]
        if cleaned_stream.startswith(('[', '{')):
            return 'json'
        elif cleaned_stream.startswith('--'):
            return 'yaml'
        elif cleaned_stream.startswith('<'):
            return 'xml'
    elif hasattr(stream, '__dict__'):
        return 'class'
    raise InvalidStreamType('Unsupported stream type')