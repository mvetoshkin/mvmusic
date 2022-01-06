import importlib


def import_object(path):
    module_name, object_name = path.rsplit('.', 1)
    mod = importlib.import_module(module_name)
    if not hasattr(mod, object_name):
        raise ImportError

    return getattr(mod, object_name)


def to_camel_case(text):
    text = text.replace('-', ' ').replace('_', ' ').lower()
    if not text:
        return text

    chunks = text.split()
    return chunks[0] + ''.join(i.capitalize() for i in chunks[1:])
